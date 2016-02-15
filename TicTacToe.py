#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 vishalapr <vishalapr@vishalapr-Lenovo-G50-70>
#
# Distributed under terms of the MIT license.

"""

"""
from copy import deepcopy

with open('currentstate') as f:
    initial = [[int(x) for x in line.split()] for line in f]


def win(player,game):
    if game[0][0]==player and game[1][1]==player and game[2][2]==player:
        return 1
    if game[0][2]==player and game[1][1]==player and game[2][0]==player:
        return 1
    for i in range(0,3):
        if game[i][0]==player and game[i][1]==player and game[i][2]==player:
            return 1
        if game[0][i]==player and game[1][i]==player and game[2][i]==player:
            return 1
    return 0

def score(game,depth):
    if win(1,game):
        return 15-depth
    elif win(2,game):
        return depth-15
    else:
        return 0

def completed(game):
    for i in range(0,3):
        for j in range(0,3):
            if game[i][j]==0:
                return 0
    return 1


#HEURISTIC
def assumedScore(game,depth,player):
    captured=0
    for i in range(0,3):
        for j in range(0,3):
            if game[i][j]==player:
                captured+=1
    if player==1:
        return captured
    else:
        return -captured


def minimax(player,game,firstcall,depth):
    #The game is complete (All blocks filled) or if there is a winner of the game, then return the actual cost function values
    if win(1,game) or win(2,game) or completed(game):    
        return score(game,depth)

    #The game is not complete or no one has won yet, we use our heuristic to compute the estimated cost function values
    if depth>=4:
        return assumedScore(game,depth,player)

    scores = []
    moves = []
    copy = deepcopy(game)

    for i in range(0,3):
        for j in range(0,3):
            if copy[i][j]==0:
                copy[i][j]=player
                if player==1:
                    scores.append(minimax(2,copy,1,depth+1))
                else:
                    scores.append(minimax(1,copy,1,depth+1))
                copy[i][j]=0
                moves.append((i+1)*10+(j+1))
    
    #If we are playing
    if player==1:
        max_score = scores.index(max(scores))
        j=(moves[max_score])%10-1
        i=(moves[max_score]/10)%10-1
        if firstcall==0:
            print i,j
        return scores[max_score]
    else:
        min_score = scores.index(min(scores))
        j=(moves[min_score])%10-1
        i=(moves[min_score]/10)%10-1
        if firstcall==0:
            print i,j
        return scores[min_score]

minimax(1,initial,0,0)
