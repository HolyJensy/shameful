from django.db import models
from django.urls import reverse
from django.contrib.auth.admin import User


def get_path_image(uname, iname):
    ''' формируем имя файла картинки. К имени спереди
    -добавляем путь - папку, с именем пользователя, где будет хранится картинка.
    Если этого не делать, то все фотографии будут в одной папке'''
    path = str(uname).lower() + '/' + str(iname)
    return path


class Gallery(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Описание', max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['title']

    def get_detailUrl(self):
        return reverse('gallery_update', kwargs={'pk': self.pk})

    def get_deleteUrl(self):
        return reverse('gallery_delete', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class Advert(
    models.Model):  # Описание окон для записи CharField - небольшой текст до 200 символов, TextField-текс с большим количеством символов, EmailField - для Эмейлов, DateTimeField-модель для дат
    # , их названия verbose_name(которые будут высвечиватся),  max_length - максимальное количество символов, blank=True - охначает что поле необязательно для зполнения,
    # False-поле обязательно для заполнения (стоит по умолчанию можно не указывать, null=True - для БД, при отсутсвии укажет значение Null в таблице, акутально со значение blank-True
    # auto_now_add=True автоматически указывает настоящее время
    title = models.CharField(verbose_name='Заглавие', max_length=20)
    text = models.TextField(verbose_name='Текст', null=True, blank=True)
    phone = models.CharField(verbose_name='Тел. номер', max_length=20, null=True, blank=True)
    email = models.EmailField(verbose_name='Email', max_length=30, null=True)
    date = models.DateTimeField(auto_now_add=True)
    gallery = models.ForeignKey(Gallery, verbose_name='Галерея', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:  # Для админки, будет написано для объявлений Объявления, для одного просто Объявление
        verbose_name = 'Объявление'
        verbose_name_plural = "Объявления"
        ordering = ['date']  # сортировка по дате добавления записи

    def get_detailUrl(self):  # reverse позволяет по имени вьюхи получить её url.
        return reverse('adv_detail', kwargs={
            'pk': self.pk})  # 'adv_detail' - имя из urls.py kwargs={'pk':self.pk} - динамиические изменяемые данные статьи будет иметь int значение

    def get_absolute_url(self):
        return reverse('adv_list')

    def get_UpdateUrl(self):
        return reverse('adv_update', kwargs={'pk': self.pk})

    def get_DeleteUrl(self):
        return reverse('adv_delete', kwargs={'pk': self.pk})


class Photo(models.Model):  # класс модели фото в панеле администратора
    title = models.CharField(verbose_name='Описание', max_length=30, blank=True,
                             null=True)  # Описание картинки для удобног опоиска
    image = models.ImageField(verbose_name='Фото',
                              upload_to='gallery/')  # добавляем фото и добавляем фото в папку gallery
    # advert=models.ForeignKey(Advert, verbose_name='Объявление', on_delete=models.CASCADE) #выбор к какому объявлению прикрепить и при удалении удалить все фотографии
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    gallery = models.ForeignKey(Gallery, verbose_name='Галлерея', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
        ordering = ['user', 'gallery', 'title']

    def save(self, *args, **kwargs):
        ''' Переопределяем метод save чтобы изменить значените image.name'''
        self.image.name = get_path_image(self.user, self.image.name)
        super().save(*args, **kwargs)

    def get_PhotodeleteUrl(self):
        return reverse('photodelete', kwargs={'pk':self.pk})

    def __str__(self):
        return self.title
