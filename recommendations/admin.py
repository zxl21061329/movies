from django.contrib import admin
from .models import Rating, UserSimilarity, ItemSimilarity

admin.site.register(Rating)
admin.site.register(UserSimilarity)
admin.site.register(ItemSimilarity)
