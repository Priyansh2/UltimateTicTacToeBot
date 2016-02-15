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

INF = 100000000

with open('currentstate') as f:
    initial = [[int(x) for x in line.split()] for line in f]

def block_win(player,game,base1,base2):
    base1*=3
    base2*=3
    if game[base1+0][base2+0]==player and game[base1+1][base2+1]==player and game[base1+2][base2+2]==player:
        return 1
    if game[base1+0][base2+2]==player and game[base1+1][base2+1]==player and game[base1+2][base2+0]==player:
        return 1
    for i in range(0,3):
        if game[base1+i][base2+0]==player and game[base1+i][base2+1]==player and game[base1+i][base2+2]==player:
            return 1
        if game[base1+0][base2+i]==player and game[base1+1][base2+i]==player and game[base1+2][base2+i]==player:
            return 1
    return 0

def board_win(player,game):
    blocks = [[0,0,0],[0,0,0],[0,0,0]]
    for i in range(0,3):
        for j in range(0,3):
            blocks[i][j]=block_win(player,game,i,j)
    if blocks[0][0]==player and blocks[1][1]==player and blocks[2][2]==player:
        return 1
    if blocks[0][2]==player and blocks[1][1]==player and blocks[2][0]==player:
        return 1
    for i in range(0,3):
        if blocks[i][0]==player and blocks[i][1]==player and blocks[i][2]==player:
            return 1
        if blocks[0][i]==player and blocks[1][i]==player and blocks[2][i]==player:
            return 1
    return 0

def completed_board(game):
    for i in range(0,9):
        for j in range(0,9):
            if game[i][j]==0:
                return 0
    return 1

def completed_block(game,a,b):
    for i in range(0,3):
        for j in range(0,3):
            if game[i+a*3][j+b*3]==0:
                return 0
    return 1

#HEURISTIC
def assumedScore(game,depth,player):
    captured=0
    for i in range(0,9):
        for j in range(0,9):
            if game[i][j]==player:
                captured+=1
    if player==1:
        return captured
    else:
        return -captured


def minimax(player,game,firstcall,depth,alpha,beta,selected_block):

    if alpha>beta:
        if player==1:
            #Parent is minimizer
            return INF
        else:
            #Parent is maximizer
            return -INF
    #The game is complete (All blocks filled) or if there is a winner of the game, then return the heruistic based cost function values
    if board_win(1,game) or board_win(2,game) or completed_board(game) or depth>=3:    
        return assumedScore(game,depth,player)

    scores = []
    moves = []
    copy = deepcopy(game)

    available=[[0,0,0],[0,0,0],[0,0,0]]
    if selected_block==0:
        if completed_block(copy,0,1) and completed_block(copy,1,0):
            selected_block=-1
        else:
            available[0][1]=1
            available[1][0]=1
    if selected_block==1:
        if completed_block(copy,0,2) and completed_block(copy,0,0):
            selected_block=-1
        else:
            available[0][2]=1
            available[0][0]=1
    if selected_block==2:
        if completed_block(copy,0,1) and completed_block(copy,1,2):
            selected_block=-1
        else:
            available[0][1]=1
            available[1][2]=1
    if selected_block==3:
        if completed_block(copy,0,0) and completed_block(copy,2,0):
            selected_block=-1
        else:
            available[0][0]=1
            available[2][0]=1
    if selected_block==4:
        if completed_block(copy,1,1):
            selected_block=-1
        else:
            available[1][1]=1
    if selected_block==5:
        if completed_block(copy,0,2) and completed_block(copy,2,2):
            selected_block=-1
        else:
            available[0][2]=1
            available[2][2]=1
    if selected_block==6:
        if completed_block(copy,1,0) and completed_block(copy,2,1):
            selected_block=-1
        else:
            available[1][0]=1
            available[2][1]=1
    if selected_block==7:
        if completed_block(copy,2,0) and completed_block(copy,2,2):
            selected_block=-1
        else:
            available[2][0]=1
            available[2][2]=1
    if selected_block==8:
        if completed_block(copy,1,2) and completed_block(copy,2,1):
            selected_block=-1
        else:
            available[1][2]=1
            available[2][1]=1
    if selected_block==-1: #Any move allowed
        for i in range(0,3):
            for j in range(0,3):
                available[i][j]=1
    
    for i in range(0,9):
        for j in range(0,9):
            if copy[i][j]==0 and available[i/3][j/3]==1:
                copy[i][j]=player
                if player==1:
                    cur_score = minimax(2,copy,1,depth+1,alpha,beta,(i%3)*3+j%3)
                    scores.append(cur_score)
                    alpha = max(alpha, cur_score)
                else:
                    cur_score = minimax(1,copy,1,depth+1,alpha,beta,(i%3)*3+j%3)
                    scores.append(cur_score)
                    beta = min(beta, cur_score)
                copy[i][j]=0
                moves.append((i)*10+(j))
    
    #If we are playing
    if player==1:
        max_score = scores.index(max(scores))
        j=(moves[max_score])%10
        i=(moves[max_score]/10)%10
        if firstcall==0:
            print i,j
        return scores[max_score]
    else:
        min_score = scores.index(min(scores))
        j=(moves[min_score])%10
        i=(moves[min_score]/10)%10
        if firstcall==0:
            print i,j
        return scores[min_score]

previous_move_x,previous_move_y = map(int,raw_input().split()) #Input where the last move was made (0,9) in x and (0,9) in y
if previous_move_x==-1 and previous_move_y==-1:
    selected_block=-1
else:
    selected_block = ((previous_move_x)%3+((previous_move_y)%3)*3) #x is the column y is the row
minimax(1,initial,0,0,-INF,INF,selected_block)
