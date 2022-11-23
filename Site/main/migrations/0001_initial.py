# Generated by Django 4.0.4 on 2022-04-26 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Advert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, verbose_name='Заглавие')),
                ('text', models.TextField(blank=True, null=True, verbose_name='Текст')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Тел. номер')),
                ('email', models.EmailField(max_length=30, null=True, verbose_name='Email')),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]