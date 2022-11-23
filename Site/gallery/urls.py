from django.urls import path
from .views import GalleryListView, GalleryCreateView, GalleryUpdateView, GalleryDeleteView
from main.views import PhotoGalleryCreate, PhotoGalleryList, PhotoDelete


urlpatterns = [
    path('list/', GalleryListView.as_view(), name='gallery_list'),
    path('create/', GalleryCreateView.as_view(), name='gallery_create'),
    path('update/<int:pk>', GalleryUpdateView.as_view(), name='gallery_update'),
    path('delete/<int:pk>', GalleryDeleteView.as_view(), name='gallery_delete'),
    path('photocreate', PhotoGalleryCreate.as_view(), name='photo_create'),
    path('photolist/<int:pk>', PhotoGalleryList.as_view(), name='photo_gallery_list'),
    path('photodelete/<int:pk>',PhotoDelete.as_view(), name='photo_delete'),
]