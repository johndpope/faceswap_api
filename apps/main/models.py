import random
import os

from django.db import models


def generate_filename():
    data_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "data",
    )
    filename_generation_files = [
        os.path.join(data_dir, "adverbs.txt"),
        os.path.join(data_dir, "adjectives.txt"),
        os.path.join(data_dir, "animal_names.txt"),
    ]
    filename = ""
    for data_file in filename_generation_files:
        with open(data_file, "r") as f:
            words = f.read().splitlines()
            random_word = random.choice(words)
            filename += random_word.capitalize()
    filename = f"{filename}.jpg"
    try:
        FaceswapImage.objects.get(name=filename)
        filename = generate_filename()
    except FaceswapImage.DoesNotExist:
        pass
    return filename


class FaceswapImage(models.Model):
    STATUS_CHOICES = (
        ('queued', 'Queued'),
        ('success', 'Success'),
        ('error', 'Error'),
    )

    image = models.ImageField(upload_to='./', blank=True)
    name = models.TextField(default=generate_filename, unique=True)
    status = models.TextField(choices=STATUS_CHOICES, default="queued")
    status_message = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def change_status(self, new_status, new_status_message=""):
        self.status = new_status
        self.status_message = new_status_message
        self.save()

    def __str__(self):
        return f"{self.pk} - {self.name}"
