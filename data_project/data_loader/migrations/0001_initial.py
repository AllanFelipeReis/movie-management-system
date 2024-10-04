# Generated by Django 5.1.1 on 2024-10-03 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_the_movie', models.IntegerField()),
                ('title', models.CharField(max_length=255)),
                ('release_date', models.DateField()),
                ('overview', models.TextField()),
                ('popularity', models.FloatField()),
                ('vote_average', models.FloatField()),
                ('vote_count', models.IntegerField()),
                ('poster_path', models.CharField(max_length=255)),
            ],
        ),
    ]
