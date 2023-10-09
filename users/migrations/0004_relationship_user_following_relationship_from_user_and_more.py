# Generated by Django 4.1 on 2023-10-09 07:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_like_posts'),
    ]

    operations = [
        migrations.CreateModel(
            name='Relationship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='following',
            field=models.ManyToManyField(related_name='followers', through='users.Relationship', to=settings.AUTH_USER_MODEL, verbose_name='팔로우 중인 사용자들'),
        ),
        migrations.AddField(
            model_name='relationship',
            name='from_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following_relationships', to=settings.AUTH_USER_MODEL, verbose_name='팔로우를 요청한 사용자'),
        ),
        migrations.AddField(
            model_name='relationship',
            name='to_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower_relationships', to=settings.AUTH_USER_MODEL, verbose_name='팔로우 요청의 대상'),
        ),
    ]
