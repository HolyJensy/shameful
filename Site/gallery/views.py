from django.contrib.auth.mixins import LoginRequiredMixin #Доступ для зарегестрированным пользователям
from django.http import HttpResponseRedirect
from django.views import generic    # Общие представления(generic views) Django были разработаны, чтобы избавить нас от этой скуки. В их основе лежит набор идиом и шаблонов, базирующийся на практическом опыте
                                    # создания представлений, который дает нам абстрактный каркас для быстрого создания собственных представлений, без необходимости писать лишний, повторяющийся код.
from main.models import Gallery
from .forms import GalleryForm


class GalleryCreateView(generic.CreateView):
    template_name = 'gallery/gallery_create.html' # Добавить !!!!!!
    form_class = GalleryForm # Форма

    def post(self, request, *args, **kwargs): # Привязка пользователя к галлереи
        bindform = GalleryForm(request.POST)
        post = bindform.save(commit=False) # Промежуточное сохранение (не в базу данных)
        post.user = request.user
        post.save()
        return HttpResponseRedirect('/gallery/list/') # Возвращение по адресу gallery/list

class GalleryListView(LoginRequiredMixin, generic.ListView):
    context_object_name = 'gallery'
    template_name = 'gallery/gallery_list.html'
    paginate_by = 1

    def get_queryset(self): # функция которая показывает галлерею которая принадлежит только пользователю
        queryset = Gallery.objects.filter(user=self.request.user)
        return queryset

class GalleryUpdateView(generic.UpdateView):
    template_name = 'gallery/gallery_update.html'
    form_class = GalleryForm
    context_object_name = 'gallery'
    success_url = '/gallery/list/'

    def get_queryset(self):
        queryset = Gallery.objects.filter(pk=self.kwargs['pk'])
        return queryset

class GalleryDeleteView(generic.DeleteView):
    model = Gallery
    context_object_name = 'gallery'
    template_name = 'gallery/gallery_delete.html'
    success_url = '/gallery/list'