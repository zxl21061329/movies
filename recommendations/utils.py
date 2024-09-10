from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from recommendations.models import Movie, ItemSimilarity, Rating
import numpy as np

# 计算电影之间的相似度，基于电影的类型、导演和演员等特征
def compute_movie_similarity():
    # 获取所有电影数据
    movies = Movie.objects.all()
    features = [f"{movie.genre} {movie.director} {movie.actors}" for movie in movies]

    # 使用TF-IDF向量化电影特征
    vectorizer = TfidfVectorizer()
    feature_matrix = vectorizer.fit_transform(features)

    # 计算电影之间的余弦相似度
    similarity_matrix = cosine_similarity(feature_matrix)

    # 存储相似度数据
    for i in range(len(movies)):
        for j in range(i + 1, len(movies)):
            similarity_score = similarity_matrix[i][j]
            # 将相似度保存到数据库中
            ItemSimilarity.objects.create(
                movie_id_1=movies[i],
                movie_id_2=movies[j],
                similarity_score=similarity_score
            )

# 计算基于用户评分的电影相似度
def compute_item_similarity_from_ratings():
    # 获取所有电影
    movies = Movie.objects.all()
    movie_ids = [movie.id for movie in movies]
    ratings_matrix = np.zeros((len(movies), len(movies)))

    # 为每对电影计算相似度
    for i, movie_1 in enumerate(movies):
        for j, movie_2 in enumerate(movies):
            if i != j:
                # 获取每个电影的评分
                ratings_1 = Rating.objects.filter(movie=movie_1).values_list('rating', flat=True)
                ratings_2 = Rating.objects.filter(movie=movie_2).values_list('rating', flat=True)

                # 确保两个电影的评分数据都有
                if ratings_1 and ratings_2:
                    # 使用余弦相似度计算评分之间的相似度
                    # 将评分转换为适当的格式
                    ratings_1 = np.array(ratings_1).reshape(1, -1)
                    ratings_2 = np.array(ratings_2).reshape(1, -1)

                    # 计算余弦相似度
                    similarity_score = cosine_similarity(ratings_1, ratings_2)[0][0]

                    # 存储相似度数据
                    ItemSimilarity.objects.create(
                        movie_id_1=movie_1,
                        movie_id_2=movie_2,
                        similarity_score=similarity_score
                    )


# 为用户生成基于物品的推荐电影
def recommend_movies_based_on_items(user_id, num_recommendations=5):
    # 获取用户的评分
    user_ratings = Rating.objects.filter(user_id=user_id)
    movie_scores = {}

    # 遍历用户已评分的电影，并基于相似电影的评分计算推荐分数
    for rating in user_ratings:
        similar_movies = ItemSimilarity.objects.filter(movie_id_1=rating.movie)
        for sim_movie in similar_movies:
            if sim_movie.movie_id_2 not in movie_scores:
                movie_scores[sim_movie.movie_id_2] = 0
            # 将相似度和用户评分相乘，累积得分
            movie_scores[sim_movie.movie_id_2] += sim_movie.similarity_score * rating.rating

    # 按分数从高到低排序，并推荐前n部电影
    recommended_movies = sorted(movie_scores.items(), key=lambda x: x[1], reverse=True)[:num_recommendations]
    return [movie[0] for movie in recommended_movies]
