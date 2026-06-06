from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="articles"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articles"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    views_count = models.PositiveIntegerField(default=0)

    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]


class Comment(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    text = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.author} → {self.article.title[:30]}"


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ("user", "article")