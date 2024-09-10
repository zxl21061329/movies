from django.db import models

class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    release_year = models.IntegerField()
    genre = models.CharField(max_length=100)
    rating = models.FloatField()
    director = models.CharField(max_length=100)
    actors = models.TextField()  # 存储演员列表，可以用JSON格式存储
    language = models.CharField(max_length=50)
    reviews = models.TextField()  # 存储影评，可以用JSON或其他结构化格式
    img = models.ImageField(upload_to='movie_images/', null=True, blank=True)

    def __str__(self):
        return self.title
