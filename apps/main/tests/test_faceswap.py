import random

import numpy as np

import pytest

from ..faceswap import swap_faces, FaceswapError
from ..models import FaceswapImage, generate_filename


def test_the_correct_output(image_with_many_faces, image_with_one_face,
                            correct_output_image_array):
    output_image = swap_faces(image_with_one_face, image_with_many_faces)
    assert np.array_equal(output_image, correct_output_image_array)


def test_too_many_from_faces(image_with_many_faces, image_with_one_face):
    with pytest.raises(FaceswapError) as e:
        swap_faces(image_with_many_faces, image_with_one_face)
    assert str(e.value) == "Too many faces detected in the first image"


def test_no_faces_from(image_with_no_faces, image_with_one_face):
    with pytest.raises(FaceswapError) as e:
        swap_faces(image_with_no_faces, image_with_one_face)
    assert str(e.value) == "No faces detected in the first image"


def test_no_faces_to(image_with_one_face, image_with_no_faces):
    with pytest.raises(FaceswapError) as e:
        swap_faces(image_with_one_face, image_with_no_faces)
    assert str(e.value) == "No faces detected in the second image"


@pytest.mark.django_db
def test_filename_generation():
    random.seed(1)
    assert generate_filename() == "ExcitedlyScaryBombay.jpg"
    assert generate_filename() == "KnavishlyCruelTermite.jpg"
    assert generate_filename() == "WronglyLudicrousSomali.jpg"


@pytest.mark.django_db
def test_no_duplicate_filenames():
    random.seed(1)
    img1 = FaceswapImage.objects.create()
    random.seed(1)
    img2 = FaceswapImage.objects.create()
    assert img1.name != img2.name
