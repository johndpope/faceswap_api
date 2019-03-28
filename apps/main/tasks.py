from celery import shared_task

from django.core.files.images import ImageFile

from .models import FaceswapImage
from .faceswap import swap_faces, FaceswapError, get_image_as_file_object


@shared_task
def generate_new_image(name, image_from, image_to):
    new_image_object = FaceswapImage.objects.get(name=name)
    try:
        new_image = swap_faces(image_from, image_to)
        image_file_object = get_image_as_file_object(new_image)
        new_image_object.image.save(name, ImageFile(image_file_object))
        new_image_object.change_status('success')
    except FaceswapError as e:
        error_message = str(e)
        new_image_object.change_status('error', error_message)
