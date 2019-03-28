from django.contrib import admin

from .models import FaceswapImage


class FaceswapImageAdmin(admin.ModelAdmin):
    model = FaceswapImage


admin.site.register(FaceswapImage, FaceswapImageAdmin)
