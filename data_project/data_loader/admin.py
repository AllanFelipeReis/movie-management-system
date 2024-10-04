from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.utils.html import mark_safe
from .models import Movie, Genre
import logging

# Cria o logger
logger = logging.getLogger('myapp')

class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at') 
    search_fields = ('name',)

    def get_queryset(self, request):
        return super().get_queryset(request)

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_year', 'get_genres', 'show_poster', 'created_at', 'updated_at')
    search_fields = ('title',)
    list_filter = ('release_date', 'genre__name')

    def get_year(self, obj):
        return obj.release_date.year if obj.release_date else 'N/A'
    get_year.short_description = 'Ano'

    def get_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genre.all()])
    get_genres.short_description = 'Gêneros'

    def show_poster(self, obj):
        if obj.poster_path:
            return mark_safe(f'<img src="https://image.tmdb.org/t/p/original/{obj.poster_path}" style="width: 100px; height: auto;" />')
        return "Sem Pôster"
    show_poster.short_description = 'Pôster'


class CustomAdminSite(admin.AdminSite):
    site_header = 'Admin do Sistema de Filmes'
    site_title = 'Admin do Sistema de Filmes'
    index_title = 'Bem-vindo ao Painel de Administração'

custom_admin_site = CustomAdminSite(name='custom_admin')

custom_admin_site.register(Genre, GenreAdmin)
custom_admin_site.register(Movie, MovieAdmin)

