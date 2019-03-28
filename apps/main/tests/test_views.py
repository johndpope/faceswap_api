import pytest

from django.urls import reverse


pytestmark = pytest.mark.django_db


def test_home_page(client, admin_user):
    url = "/"
    response = client.get(url)
    assert response.status_code == 404


def test_upload_page(client, admin_user):
    url = reverse("image_upload")
    response = client.get(url)
    assert response.status_code == 405
