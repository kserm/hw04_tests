from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200,
                             verbose_name='Группа',
                             help_text='Группа, к которой будет относиться '
                             'пост'
                             )
    slug = models.SlugField(unique=True,
                            verbose_name='URL',
                            help_text='Название группы для URL'
                            )
    description = models.TextField(verbose_name='Описание группы',
                                   help_text='Подробное описание группы'
                                   )

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(verbose_name='Текст поста',
                            help_text='Текст нового поста')
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата публикации',
                                    help_text='Дата публикации поста'
                                    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор',
        help_text='Автор поста'
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Группа',
        help_text='Группа, к которой относится пост'
    )

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
