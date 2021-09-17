from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Search(models.Model):
    search = models.CharField(max_length=50)
    date_searched = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

class Article(models.Model):
    title = models.CharField(max_length=250)
    abstract = models.TextField()
    pubmedlink = models.URLField()
    search_folder = models.ForeignKey(Search, on_delete=models.CASCADE)
    
class Link(models.Model):
    link = models.URLField()
    free = models.BooleanField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
