from django.shortcuts import render
from django.db.models import Count, Avg
from django.db.models.functions import ExtractYear
from .models import Movie, Genre

def dashboard_view(request):
    # Total de filmes e gêneros
    total_movies = Movie.objects.count()
    total_genres = Genre.objects.count()

    # Dados para gráficos de Gêneros
    genres_data = Genre.objects.annotate(count=Count('movie'))
    genres_names = [genre.name for genre in genres_data]
    genres_counts = [genre.count for genre in genres_data]

    # Dados para os Top 10 Filmes por Popularidade
    top_movies = Movie.objects.order_by('-popularity')[:10]
    top_movies_titles = [movie.title for movie in top_movies]
    top_movies_popularity = [movie.popularity for movie in top_movies]

    # Agrupamento por ano e cálculo da popularidade média
    movies_by_year = Movie.objects.annotate(year=ExtractYear('release_date')) \
                                  .values('year') \
                                  .annotate(avg_popularity=Avg('popularity')) \
                                  .order_by('year')

    release_years = [entry['year'] for entry in movies_by_year]
    avg_popularity = [entry['avg_popularity'] for entry in movies_by_year]

    movies = Movie.objects.order_by('-release_date')[:20]

    context = {
        'total_movies': total_movies,
        'total_genres': total_genres,
        'genres_names': genres_names,
        'genres_counts': genres_counts,
        'top_movies_titles': top_movies_titles,
        'top_movies_popularity': top_movies_popularity,
        'movies': movies,
        'release_years': release_years,  
        'avg_popularity': avg_popularity
    }

    return render(request, 'dashboard.html', context)