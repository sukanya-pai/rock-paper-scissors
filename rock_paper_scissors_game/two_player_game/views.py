# Django Import
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from two_player_game.models import *
from django.db.models import F

# Python Import
import random
import logging
log = logging.getLogger(__name__)

def home(request):
    '''
    homepage and redirect to start game logic
    '''
    if request.method=='POST':
        details = {
            'player1name':request.POST.get('player1name'),
            'mode':request.POST.get('mode'),
            'player2name':request.POST.get('player2name','Computer')
        }
        # Get latest game ID
        game_id = Game.objects.order_by('-game_id').values_list('game_id',flat=True)
        game_id = 1 if not game_id else (game_id[0]+1)
        details['game_id'] = game_id

        # create players
        player1,pl1created = Player.objects.get_or_create(name=details['player1name']) 
        player2,pl2created = Player.objects.get_or_create(name=details['player2name'])

        # Create game object
        pl1 = Game(game_id = game_id,
                player=player1, score=0)
        pl1.save()
        pl2 = Game(game_id = game_id,
                player=player2, score=0)
        pl2.save()

        return render(request,'game.html',details)

    return render(request, 'home_page.html')

def about(request):
    '''
    about page
    '''
    return render(request, 'about.html')

def contact(request):
    '''
    contact page
    '''
    return render(request, 'contact.html')


def game(request):
    if request.method == 'POST':
        details = {
            'player1name':request.POST.get('player1name'),
            'mode':request.POST.get('mode'),
            'player2name':request.POST.get('player2name','Computer'),
            'game_id' : request.POST.get('game_id')
        }

        player1option = request.POST.get('player1option')
        # Play with player mode
        if details['mode'] == 'player':
            player2option = request.POST.get('player2option')
            messages.info(request, f"You selected {player1option}, {details['player2name']} selected {player2option}" )
        else:
            player2option = get_computer_option()
            messages.info(request, f"You selected {player1option}, computer selected {player2option}")
        
        # Save move details
        pl1_move = GameMove(game = Game.objects.get(game_id = details['game_id'], player=Player.objects.get(name=details['player1name'])),
                        player = Player.objects.get(name=details['player1name']),
                        move = player1option)
        pl1_move.save()
        pl2_move = GameMove(game =  Game.objects.get(game_id = details['game_id'], player=Player.objects.get(name=details['player2name'])),
                        player = Player.objects.get(name=details['player2name']),
                        move = player2option)
        pl2_move.save()


        # process the game
        result = process_game(request, 
                            {'name':details['player1name'],'option':player1option}, 
                            {'name':details['player2name'],'option':player2option})

        # Save score
        if result is not 'tie':
            Game.objects.filter(game_id=details['game_id'], player__name=result).update(score=F("score") + 1)
        
        details['player1score'] = list(Game.objects.filter(game_id=details['game_id'], player__name=details['player1name']).values_list('score', flat=True))[0]
        details['player2score'] = list(Game.objects.filter(game_id=details['game_id'], player__name=details['player2name']).values_list('score', flat=True))[0]

        return render(request,'game.html',details)



def get_computer_option():
    """
    Function to get computer's option
    """
    gamelist = ['rock', 'paper', 'scissors']
    computer_option = random.choice(gamelist)
    return computer_option

def process_game(request, player_one, player_two):
    result = None
    player_one_option = player_one['option']
    player_two_option = player_two['option']

    if player_one_option == player_two_option:
        messages.info(request, f"Nobody wins! Its a tie!")
        result = 'tie'
    elif player_one_option == "rock":
        if player_two_option == "scissors":
            result = player_one['name']
            messages.success(request, "You win! :)")
        else:
            result = player_two['name']
            messages.info(request, "You lose! :(")
    elif player_one_option == "paper":
        if player_two_option == "rock":
            result = player_one['name']
            messages.success(request, "You win! :)")
        else:
            result = player_two['name']
            messages.info(request, "You lose! :(")
    elif player_one_option == "scissors":
        if player_two_option == "paper":
            result = player_one['name']
            messages.success(request, "You win! :)")
        else:
            result = player_two['name']
            messages.info(request, "You lose! :(")
    return result    


