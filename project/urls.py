from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from apps.main.views import FaceswapImageView, FaceswapImageStatusView


urlpatterns = [
    path('upload/', FaceswapImageView.as_view(), name="image_upload"),
    path('upload/status/<str:name>', FaceswapImageStatusView.as_view(),
         name="image_status"),
    path('adminpage/', admin.site.urls),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.conf.urls import url
    import debug_toolbar

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]
