from django.db import models
from django.utils import timezone

class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class SoftDeleteModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        """Implementação de soft delete"""
        self.is_deleted = True
        self.save()

    def restore(self, *args, **kwargs):
        """Restaura um registro que foi marcado como deletado"""
        self.is_deleted = False
        self.save()

class Genre(SoftDeleteModel):
    name = models.CharField(max_length=100)
    
    objects = SoftDeleteManager()

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Gênero"
        verbose_name_plural = "Gêneros"

class Movie(SoftDeleteModel):
    id_the_movie = models.IntegerField()
    title = models.CharField(max_length=255)
    release_date = models.DateField() 
    overview = models.TextField() 
    popularity = models.FloatField()
    vote_average = models.FloatField()
    vote_count = models.IntegerField()
    poster_path = models.CharField(max_length=255)
    genre = models.ManyToManyField(Genre)
    
    objects = SoftDeleteManager()

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Filme"
        verbose_name_plural = "Filmes"