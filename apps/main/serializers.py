from rest_framework import serializers

from .models import FaceswapImage
from .faceswap import convert_image
from .tasks import generate_new_image


class FaceswapImageSerializer(serializers.Serializer):
    image_from = serializers.ImageField()
    image_to = serializers.ImageField()

    def validate(self, data):
        self.image_from = convert_image(data['image_from'])
        self.image_to = convert_image(data['image_to'])
        return data

    def save(self):
        new_image = FaceswapImage.objects.create()
        self.additional_data = {"name": new_image.name}
        generate_new_image.apply_async(
            (new_image.name, self.image_from, self.image_to),
            serializer='pickle',
        )


class FaceswapImageStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaceswapImage
        fields = ('name', 'status', 'status_message', 'image')
