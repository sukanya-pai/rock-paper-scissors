# Generated by Django 3.2.13 on 2022-04-19 20:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('two_player_game', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gamemove',
            old_name='game_id',
            new_name='game',
        ),
    ]