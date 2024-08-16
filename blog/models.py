from django.db import models

NULLABLE = {"blank": True, "null": True}


class Blog(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name="Заголовок блога",
        help_text="Введите заголовок блога",
    )
    content = models.TextField(
        **NULLABLE,
        verbose_name="Содержание блога",
        help_text="Введите содержание блога",
    )
    preview = models.ImageField(
        upload_to="blog/blog_preview",
        **NULLABLE,
        verbose_name="Изображение",
        help_text="Загрузите изображение",
    )
    created_at = models.DateTimeField(
        **NULLABLE,
        verbose_name="Дата создания блога",
        help_text="Введите дату создания блога",
    )
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    is_published = models.BooleanField(default=True, verbose_name="Опубликован")
    views_count = models.PositiveIntegerField(default=0, verbose_name="просмотры")

    class Meta:
        verbose_name = "Блог"
        verbose_name_plural = "Блоги"

    def __str__(self):
        return self.title
