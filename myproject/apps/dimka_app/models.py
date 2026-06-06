from django.db import models

class Author(models.Model):
    """Модель автора"""
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Genre(models.Model):
    """Каф"""
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Article(models.Model):
    """Статьи"""
    title = models.CharField(max_length=100)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE
    )
    genres = models.ManyToManyField(Genre)  # geners -> genres

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

















# Create your models here.
