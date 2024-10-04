import logging
import os
import pandas as pd
from django.core.management.base import BaseCommand
from data_loader.models import Movie, Genre
import aiohttp
import asyncio
from asgiref.sync import sync_to_async
from django.conf import settings

# Cria o logger
logger = logging.getLogger('myapp')

API_KEY = settings.TMDB_API_KEY

class Command(BaseCommand):
    help = 'Load data from a CSV, clean it, enrich it using an external API, and save the data to the database.'

    def handle(self, *args, **kwargs):
        # 1. Carregar o CSV e realizar a limpeza de dados
        df = self.load_and_clean_data()

        # 2. Enriquecer os dados com informações da API externa
        asyncio.run(self.enrich_data(df))
    
    def load_and_clean_data(self):
        csv_file_path = os.path.join(os.path.dirname(__file__), 'movie.csv')
        df = pd.read_csv(csv_file_path)
        
        # 1. Remover a coluna 'Unnamed: 0'
        df_cleaned = df.drop(columns=['Unnamed: 0'])

        # 2. Remover duplicatas
        df_cleaned.drop_duplicates(inplace=True)

        # 3. Converter a coluna 'release_date' para o formato de data
        df_cleaned['release_date'] = pd.to_datetime(df_cleaned['release_date'], errors='coerce')

        # 4. Remover valores nulos (caso alguma data tenha falhado na conversão)
        df_cleaned = df_cleaned.dropna()

        logger.info(f"Dados limpos. Total de registros: {len(df_cleaned)}")
        return df_cleaned

    async def enrich_data(self, df):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for _, row in df.iterrows():
                tasks.append(self.fetch_data(session, row['id']))

            enriched_data = await asyncio.gather(*tasks)

            # Criar ou atualizar os registros no banco de dados
            for index, movie_details in enumerate(enriched_data):
                await self.create_or_update_movie(df.iloc[index], movie_details)

    async def fetch_data(self, session, movie_id):
        api_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
        logger.info(f"Buscando dados para o filme ID {movie_id}")
        async with session.get(api_url) as response:
            return await response.json()

    @sync_to_async
    def create_or_update_movie(self, row, movie_details):
        movie, created = Movie.objects.get_or_create(
            id_the_movie=row['id'],
            defaults={
                'title': row['title'],
                'release_date': row['release_date'],
                'overview': row['overview'],
                'popularity': row['popularity'],
                'vote_average': row['vote_average'],
                'vote_count': row['vote_count'],
                'poster_path': movie_details.get('poster_path', '/sample.jpg')
            }
        )

        # Processar e salvar os gêneros
        self.save_genres(movie, movie_details.get('genres', []))

        movie.save()

    def save_genres(self, movie, genres):
        for genre_data in genres:
            genre, _ = Genre.objects.get_or_create(name=genre_data['name'])
            movie.genre.add(genre)
        logger.info(f"Gêneros salvos para o filme {movie.title}")
