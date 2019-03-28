import os

import cv2
import numpy as np
import pytest

from ..serializers import FaceswapImageSerializer


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
FIXTURES_DIR = os.path.join(CURRENT_DIR, "fixtures")


@pytest.fixture
def image_with_no_faces():
    filename = os.path.join(FIXTURES_DIR, "no_faces.jpg")
    return cv2.imread(filename, cv2.IMREAD_UNCHANGED)


@pytest.fixture
def image_with_many_faces():
    filename = os.path.join(FIXTURES_DIR, "many_faces.jpg")
    return cv2.imread(filename, cv2.IMREAD_UNCHANGED)


@pytest.fixture
def image_with_one_face():
    filename = os.path.join(FIXTURES_DIR, "one_face.jpg")
    return cv2.imread(filename, cv2.IMREAD_UNCHANGED)


@pytest.fixture
def correct_output_image_array():
    return np.load(os.path.join(FIXTURES_DIR, "output_image.npy"))


@pytest.fixture
def image_serializer():
    return FaceswapImageSerializer()
