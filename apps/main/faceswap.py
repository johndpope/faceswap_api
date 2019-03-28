import cv2
import dlib
import numpy as np
import os
from io import BytesIO


PREDICTOR_FILENAME = "shape_predictor_face_landmarks.dat"
PREDICTOR_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "data",
    PREDICTOR_FILENAME,
)

FACE_POINTS = list(range(17, 68))
MOUTH_POINTS = list(range(48, 61))
RIGHT_BROW_POINTS = list(range(17, 22))
LEFT_BROW_POINTS = list(range(22, 27))
RIGHT_EYE_POINTS = list(range(36, 42))
LEFT_EYE_POINTS = list(range(42, 48))
NOSE_POINTS = list(range(27, 35))
JAW_POINTS = list(range(0, 17))

# Points used to line up the images.
ALIGN_POINTS = (LEFT_BROW_POINTS + RIGHT_EYE_POINTS + LEFT_EYE_POINTS +
                RIGHT_BROW_POINTS + NOSE_POINTS + MOUTH_POINTS)

# Points from the second image to overlay on the first. The convex hull of each
# element will be overlaid.
OVERLAY_POINTS = [
    LEFT_EYE_POINTS + RIGHT_EYE_POINTS + LEFT_BROW_POINTS + RIGHT_BROW_POINTS,
    NOSE_POINTS + MOUTH_POINTS,
]

# Amount of blur to use during colour correction, as a fraction of the
# pupillary distance.
COLOUR_CORRECT_BLUR_FRAC = 0.6

FEATHER_AMOUNT = 11

IMAGE_MAX_RESOLUTION = 800


detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(PREDICTOR_PATH)


class FaceswapError(Exception):
    pass


def resize_image(image):
    height = image.shape[0]
    width = image.shape[1]
    if height > IMAGE_MAX_RESOLUTION or width > IMAGE_MAX_RESOLUTION:
        scale_factor = IMAGE_MAX_RESOLUTION / max(height, width)
        image = cv2.resize(image, (int(width * scale_factor),
                                   int(height * scale_factor)))
    return image


def convert_image(image):
    image.seek(0)
    image = np.asarray(bytearray(image.read()), dtype=np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    image = resize_image(image)
    return image


def get_image_as_file_object(image):
    image = cv2.imencode('.jpg', image)[1]
    file_buffer = BytesIO()
    file_buffer.write(image)
    return file_buffer


def get_landmarks(im):
    faces = detector(im, 1)
    landmarks = []
    for face in faces:
        landmarks.append(
            np.array([[p.x, p.y] for p in predictor(im, face).parts()])
        )
    return landmarks


def draw_convex_hull(im, points, color):
    points = cv2.convexHull(points)
    cv2.fillConvexPoly(im, points, color=color)


def get_face_mask(im, landmarks):
    im = np.zeros(im.shape[:2], dtype=np.float64)

    for group in OVERLAY_POINTS:
        draw_convex_hull(im,
                         landmarks[group],
                         color=1)

    im = np.array([im, im, im]).transpose((1, 2, 0))

    im = (cv2.GaussianBlur(im, (FEATHER_AMOUNT, FEATHER_AMOUNT), 0) > 0) * 1.0
    im = cv2.GaussianBlur(im, (FEATHER_AMOUNT, FEATHER_AMOUNT), 0)

    return im


def transformation_from_points(points1, points2):
    """
    Return an affine transformation [s * R | T] such that:
        sum ||s*R*p1,i + T - p2,i||^2
    is minimized.
    """
    # Solve the procrustes problem by subtracting centroids, scaling by the
    # standard deviation, and then using the SVD to calculate the rotation. See
    # the following for more details:
    #   https://en.wikipedia.org/wiki/Orthogonal_Procrustes_problem

    points1 = points1.astype(np.float64)
    points2 = points2.astype(np.float64)

    c1 = np.mean(points1, axis=0)
    c2 = np.mean(points2, axis=0)
    points1 -= c1
    points2 -= c2

    s1 = np.std(points1)
    s2 = np.std(points2)
    points1 /= s1
    points2 /= s2

    U, S, Vt = np.linalg.svd(points1.T @ points2)

    # The R we seek is in fact the transpose of the one given by U * Vt. This
    # is because the above formulation assumes the matrix goes on the right
    # (with row vectors) where as our solution requires the matrix to be on the
    # left (with column vectors).
    R = (U @ Vt).T

    a1 = (s2 / s1) * R
    a2 = np.array([c2]).T - (s2 / s1) * R @ np.array([c1]).T
    return np.vstack([np.hstack((a1, a2)), np.array([0., 0., 1.])])


def warp_im(im, M, dshape):
    output_im = np.zeros(dshape, dtype=im.dtype)
    cv2.warpAffine(im,
                   M[:2],
                   (dshape[1], dshape[0]),
                   dst=output_im,
                   borderMode=cv2.BORDER_TRANSPARENT,
                   flags=cv2.WARP_INVERSE_MAP)
    return output_im


def correct_colours(im1, im2, landmarks):
    landmarks_norm = np.linalg.norm(
        np.mean(landmarks[LEFT_EYE_POINTS], axis=0) -
        np.mean(landmarks[RIGHT_EYE_POINTS], axis=0)
    )
    blur_amount = COLOUR_CORRECT_BLUR_FRAC * landmarks_norm
    blur_amount = int(blur_amount)
    if blur_amount % 2 == 0:
        blur_amount += 1
    im1_blur = cv2.GaussianBlur(im1, (blur_amount, blur_amount), 0)
    im2_blur = cv2.GaussianBlur(im2, (blur_amount, blur_amount), 0)

    # Avoid divide-by-zero errors.
    im2_blur += (128 * (im2_blur <= 1.0)).astype(im2_blur.dtype)

    return (im2.astype(np.float64) *
            im1_blur.astype(np.float64) /
            im2_blur.astype(np.float64))


def apply_face(image_from, landmarks_from, image_to, landmarks_to):
    M = transformation_from_points(landmarks_to[ALIGN_POINTS],
                                   landmarks_from[ALIGN_POINTS])

    mask = get_face_mask(image_from, landmarks_from)
    warped_mask = warp_im(mask, M, image_to.shape)
    combined_mask = np.max(
        [get_face_mask(image_to, landmarks_to), warped_mask], axis=0
    )

    warped_image_from = warp_im(image_from, M, image_to.shape)
    warped_corrected_image_from = correct_colours(
        image_to, warped_image_from, landmarks_to
    )

    output_im = (image_to * (1.0 - combined_mask) +
                 warped_corrected_image_from * combined_mask)
    return output_im


def swap_faces(image_from, image_to):
    landmarks_from_list = get_landmarks(image_from)
    landmarks_to_list = get_landmarks(image_to)

    if len(landmarks_from_list) > 1:
        raise FaceswapError("Too many faces detected in the first image")
    elif len(landmarks_from_list) == 0:
        raise FaceswapError("No faces detected in the first image")
    else:
        landmarks_from = landmarks_from_list[0]

    if len(landmarks_to_list) == 0:
        raise FaceswapError("No faces detected in the second image")

    for landmarks_to in landmarks_to_list:
        processed_image = apply_face(image_from, landmarks_from,
                                     image_to, landmarks_to)
        image_to = processed_image

    final_image = image_to
    return final_image
