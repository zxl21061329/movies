from django.shortcuts import render, redirect
from .utils import recommend_movies_based_on_items

def recommendations_view(request):
    if request.user.is_authenticated:
        user_id = 2
        recommended_movies = recommend_movies_based_on_items(user_id)
        print("Recommended Movies:", recommended_movies)  # 调试信息
        return render(request, 'recommendation/movies.html', {'recommended_movies': recommended_movies})
    else:
        return redirect('login')  # Redirect to login page if not authenticated
