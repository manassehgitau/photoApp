from django.urls import path
from .views import index, profile_view, profile_update, change_password, photo_detail, like_photo, upload_photo, my_photos

urlpatterns = [
    path('', index, name='index'),
    path('profile/', profile_view, name='profile'),
    path('profile/update/', profile_update, name='profile_update'),
    path('profile/change-password/', change_password, name='change_password'),
    path('photo/<int:photo_id>/', photo_detail, name='photo_detail'),
    path('photo/<int:photo_id>/like/', like_photo, name='like_photo'),
    path('photo/upload/', upload_photo, name='upload_photo'),
    path('my-photos/', my_photos, name='my_photos'),
]