from django.db import models
from users.models import User
from movies_recommend.models import Movie

class Rating(models.Model):
    rating_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_ratings')
    rating = models.FloatField()
    rated_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username} - {self.movie.title} - {self.rating}"


class UserSimilarity(models.Model):
    user_id_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_similarity_1')
    user_id_2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_similarity_2')
    similarity_score = models.FloatField()

    def __str__(self):
        return f"Similarity between {self.user_id_1.username} and {self.user_id_2.username}"


class ItemSimilarity(models.Model):
    movie_id_1 = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='item_similarity_1')
    movie_id_2 = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='item_similarity_2')
    similarity_score = models.FloatField()

    def __str__(self):
        return f"Similarity between {self.movie_id_1.title} and {self.movie_id_2.title}"
