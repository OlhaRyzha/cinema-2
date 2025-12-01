from django.db import models
from main.validators import mark_validator
from django.urls import reverse

class Genre(models.Model):
    name = models.CharField(max_length=255, verbose_name="Назва")
    image = models.ImageField(upload_to="ganre/", null=True, blank=True, verbose_name="Зображення")

    def __str__(self):
        return f'{self.name} (id: {self.id})'
    @property
    def img(self):
        if self.image:
            return self.image.url
        else:
            return "/static/main/images/null_img.png"

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанри"

    def get_absolute_url(self):
        return reverse("genre_view", args=[str(self.id)])

class Movie(models.Model):
    TYPES = [
        (1, 'Movie'),
        (2, 'Series'),
        (3, 'Cartoon'),
        (4, 'Anime'),
    ]

    name = models.CharField(max_length=255, verbose_name="Назва")
    release_date = models.DateField(verbose_name="Дата випуску")
    duration = models.FloatField(verbose_name="Тривалість")
    description = models.TextField(verbose_name="Опис")
    is_top_five = models.BooleanField(default=False, verbose_name="Топ 5")
    tag = models.CharField(max_length=20, null=True, blank=True, verbose_name="Тег")
    rating = models.FloatField(default=0, verbose_name="Рейтинг")
    type = models.IntegerField(choices=TYPES, default=1, verbose_name="Тип")
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name="movies", verbose_name="Жанр")

    class Meta:
        verbose_name = "Фільм"
        verbose_name_plural = "Фільми"
        
class SiteReview(models.Model):
    name = models.CharField(max_length=255, verbose_name="Ім'я користувача")
    text = models.TextField(verbose_name="Текст відгуку")
    mark = models.IntegerField(verbose_name="Оцінка")
    created_time = models.DateTimeField(auto_created=True, auto_now_add=True, verbose_name="Час створення")

    class Meta:
        verbose_name = "Відгук"
        verbose_name_plural = "Відгуки"