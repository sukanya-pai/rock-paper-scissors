from django.db import models
from django.contrib.auth.models import User


class Player(models.Model):
    '''
    Player model 
    '''
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Game(models.Model):
    '''
     model in which all players result will be stored
    '''
    id = models.BigAutoField(primary_key=True)
    player1 = models.ForeignKey("Player", on_delete=models.CASCADE, related_name='player1')
    player2 = models.ForeignKey("Player", on_delete=models.CASCADE, related_name='player2')
    player1_move = models.CharField(max_length=50)
    player2_move = models.CharField(max_length=50)
    winner = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.player.name

class GameResult(models.Model):
    game = models.ForeignKey("Game",on_delete=models.CASCADE, related_name = "game")
    player = models.ForeignKey("Player", on_delete=models.CASCADE, related_name='player')
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.player__name