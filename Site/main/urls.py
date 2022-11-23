from django.urls import path #path - любая не пустая строка т.е. ссылаемся на нее
from django.http import HttpResponse # позволяет вывести текст в функции
from .views import AdvertListView, AdvertDetailView, AdvertCreate, AdvertUpdate, AdvertDelete # Наследует из данной директории из папки views классы...

def testView(request):
    return HttpResponse('<div align="center"><h1 style="color:red">Это тестовая страница</h1><div>')    #Тестовая страница

urlpatterns=[
    path('', AdvertListView.as_view(), name='adv_list'), # '' переходя на такую ссылку, открывается из views.py класс AdvertListView.as_view(), можем обращатся к нему по имени 'adv_list'
    path('detail/<int:pk>', AdvertDetailView.as_view(), name='adv_detail'), # 'detail/<int:pk>', ссылка с динамическим ключом с целым числом int 1,2,3..
    path('create/', AdvertCreate.as_view(), name='adv_create'),
    path('update/<int:pk>', AdvertUpdate.as_view(), name='adv_update'),
    path('delete/<int:pk>', AdvertDelete.as_view(), name='adv_delete'),
]