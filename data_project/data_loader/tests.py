from django.test import TestCase
from data_loader.models import Movie, Genre
from datetime import date

class MovieGenreTestCase(TestCase):
    
    def setUp(self):
        self.genre1 = Genre.objects.create(name="Action")
        self.genre2 = Genre.objects.create(name="Thriller")
        
        self.movie = Movie.objects.create(
            id_the_movie=12345,
            title="Test Movie",
            release_date=date.today(),
            overview="This is a test movie.",
            popularity=7.8,
            vote_average=8.5,
            vote_count=1500,
            poster_path="/path/to/poster.jpg"
        )
        self.movie.genre.add(self.genre1, self.genre2)

    def test_movie_creation(self):
        self.assertEqual(self.movie.title, "Test Movie")
        self.assertEqual(self.movie.genre.count(), 2)

    def test_soft_delete(self):
        self.movie.delete()
        self.assertTrue(self.movie.is_deleted)

        active_movies = Movie.objects.all()
        self.assertEqual(active_movies.count(), 0)

        # Restaurar o filme
        self.movie.restore()
        self.assertFalse(self.movie.is_deleted)
        self.assertEqual(Movie.objects.count(), 1)

    def test_genre_creation(self):
        self.assertEqual(Genre.objects.count(), 2)
        self.assertEqual(self.genre1.name, "Action")
        self.assertEqual(self.genre2.name, "Thriller")

    def test_timestamp(self):
        self.assertIsNotNone(self.movie.created_at)
        self.assertIsNotNone(self.movie.updated_at)