# recommendations/urls.py

from django.urls import path
from recommendations.views import recommendations_view

urlpatterns = [
    path('recommend/', recommendations_view, name='recommend_movies_view'),
]
