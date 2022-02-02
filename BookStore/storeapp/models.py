from django.db import models

# Create your models here.
class Post(models.Model):
    id = models.IntegerField(primary_key=True)
    book_name=models.CharField(max_length=70)
    book_desc=models.TextField()

