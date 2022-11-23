from django.contrib.auth.mixins import LoginRequiredMixin #Доступ для зарегестрированным пользователям
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic    # Общие представления(generic views) Django были разработаны, чтобы избавить нас от этой скуки. В их основе лежит набор идиом и шаблонов, базирующийся на практическом опыте
                                    # создания представлений, который дает нам абстрактный каркас для быстрого создания собственных представлений, без необходимости писать лишний, повторяющийся код.
from .forms import AdvertForm
from .models import Advert, Photo, Gallery
from .permissions import UserIsOwnerOrAdminMixin
from gallery.forms import PhotoCreateForm


class AdvertListView(generic.ListView): #ListView подходит так как отображаются списки статьи
    # queryset = Advert.objects.all() # Все записи(объекты) из метода Advert
    template_name = 'main/advertlist.html' # Ссылка на исполняемый файл, он должен быть отдельно в папке templates внутри должна быть папка с приоложением где находится html файл
    context_object_name = 'adv' # Это просто понятное человеку имя переменной для доступа к шаблонам
    paginate_by = 10 #Разбиение на записи в одной странице (цифрой можно указат ьсколько страниц будет)

    def get_queryset(self):
        if self.request.GET.get('val'):
            value = self.request.GET.get('val')
            queryset = Advert.objects.filter(Q(text__contains=value) | Q(title__contains=value))
        else:
            queryset = Advert.objects.all()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        val = self.request.GET.get('val')
        context['search'] = val
        return context

class AdvertDetailView(LoginRequiredMixin, generic.DetailView): # сама запись и ее отображение
    model = Advert
    template_name = 'main/advertdetail.html'
    context_object_name = 'adv'

    def get_context_data(self, **kwargs): # Добавляем фото в объявление
        context = super().get_context_data(**kwargs)
        #context['photo'] = Photo.objects.filter(advert=self.kwargs['pk'])
        pk = self.kwargs['pk']
        qsetAdvert = Advert.objects.values('gallery_id').filter(pk=pk)
        gallery =qsetAdvert.get().get('gallery_id')
        context['photo'] = Photo.objects.filter(gallery=gallery)  # По нему находим какие фотки в галлерее в файле advertdetail.html
        context['permit'] = UserIsOwnerOrAdminMixin.has_permission(self) #проверяет является ли пользователь хозяином объявления и если что не показывает кнопки редактирования и удаления
        return context

class AdvertCreate(LoginRequiredMixin, generic.CreateView): #создание записи
    # form_class = AdvertForm
    template_name = 'main/advertcrete.html'

    def get_form(self, form_class=AdvertForm):
        form = AdvertForm(user = self.request.user)
        return form


    def post(self, request, *args, **kwargs):
        bindform = AdvertForm(request.user, request.POST)
        post = bindform.save(commit=False)
        post.user = request.user
        post.save()
        return HttpResponseRedirect('/')


class AdvertUpdate(UserIsOwnerOrAdminMixin, generic.UpdateView): # изменение данных в записи
    ''' Редактирование обьявления '''
    permission_required = 'firstproject.nge_advert'
    template_name = 'main/advertupdate.html'
    form_class = AdvertForm

    def get_queryset(self):
        queryset = Advert.objects.filter(pk=self.kwargs['pk'])
        return queryset

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.user = self.request.user
        return form


class AdvertDelete(UserIsOwnerOrAdminMixin, generic.DeleteView): # удаление записи
    model = Advert
    template_name = 'main/advertdelete.html'
    context_object_name = 'adv'
    success_url = '/' # куда вернутся после удаления записи

class PhotoGalleryCreate(generic.CreateView):
    template_name = 'gallery/photo_create.html' #Темплейт добавления фоток

    def get_form(self, form_class=PhotoCreateForm):
        form = PhotoCreateForm(user=self.request.user) # Передаем юзера
        return form

    def post(self, request, *args, **kwargs):
        bindform = PhotoCreateForm(request.user, request.POST, files=request.FILES)
        print('=========>', bindform.data)
        gallery = bindform.data['gallery']
        if bindform.is_valid(): #Если все ок то добавляем пользователя
            post = bindform.save(commit=False)
            post.user = request.user
            post.save()
        else:
            print('Errors ======>', bindform.errors)
        return HttpResponseRedirect('/gallery/photolist/{}'.format(gallery))

class PhotoGalleryList(generic.ListView):
        template_name = 'gallery/photo_list.html'
        context_object_name = 'photolist'
        paginate_by = 1
        def get_queryset(self):
            queryset = Photo.objects.filter(gallery=self.kwargs['pk'])
            return queryset

class PhotoDelete(generic.DeleteView):
    ''' Удаление фотографий из галереи '''
    model = Photo
    template_name = 'gallery/photo_delete.html'
    success_url = '/gallery/list/'
