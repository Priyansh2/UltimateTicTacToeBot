#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

from copy import deepcopy

INF = 1000000000

class Player76:

	def block_win(self,player,game,base1,base2):
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

	def board_win(self,player,game):
	    blocks = [[0,0,0],[0,0,0],[0,0,0]]
	    for i in range(0,3):
	        for j in range(0,3):
	            blocks[i][j]=self.block_win(player,game,i,j)
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

	def completed_board(self,game):
	    for i in range(0,9):
	        for j in range(0,9):
	            if game[i][j]=='-':
	                return 0
	    return 1

	def completed_block(self,game,a,b):
	    for i in range(0,3):
	        for j in range(0,3):
	            if game[i+a*3][j+b*3]=='-':
	                return 0
	    return 1

	#HEURISTIC
	def assumedScore(self,game,depth,player,flag):
	    captured=0
	    for i in range(0,9):
	        for j in range(0,9):
	            if game[i][j]==player:
	                captured+=1
	    if player==flag:
	        return captured
	    else:
	        return -captured

	def minimax(self,player,game,firstcall,depth,alpha,beta,selected_block,flag):

	    if alpha>beta:
	        if player==flag:
	            #Parent is minimizer
	            return INF
	        else:
	            #Parent is maximizer
	            return -INF
	    #The game is complete (All blocks filled) or if there is a winner of the game, then return the heruistic based cost function values
	    if self.board_win(1,game) or self.board_win(2,game) or self.completed_board(game) or depth>=3:    
	        return self.assumedScore(game,depth,player,flag)

	    scores = []
	    moves = []
	    copy = deepcopy(game)

	    available=[[0,0,0],[0,0,0],[0,0,0]]
	    if selected_block==0:
	        if self.completed_block(copy,0,1) and self.completed_block(copy,1,0):
	            selected_block=-1
	        else:
	            available[0][1]=1
	            available[1][0]=1
	    if selected_block==1:
	        if self.completed_block(copy,0,2) and self.completed_block(copy,0,0):
	            selected_block=-1
	        else:
	            available[0][2]=1
	            available[0][0]=1
	    if selected_block==2:
	        if self.completed_block(copy,0,1) and self.completed_block(copy,1,2):
	            selected_block=-1
	        else:
	            available[0][1]=1
	            available[1][2]=1
	    if selected_block==3:
	        if self.completed_block(copy,0,0) and self.completed_block(copy,2,0):
	            selected_block=-1
	        else:
	            available[0][0]=1
	            available[2][0]=1
	    if selected_block==4:
	        if self.completed_block(copy,1,1):
	            selected_block=-1
	        else:
	            available[1][1]=1
	    if selected_block==5:
	        if self.completed_block(copy,0,2) and self.completed_block(copy,2,2):
	            selected_block=-1
	        else:
	            available[0][2]=1
	            available[2][2]=1
	    if selected_block==6:
	        if self.completed_block(copy,1,0) and self.completed_block(copy,2,1):
	            selected_block=-1
	        else:
	            available[1][0]=1
	            available[2][1]=1
	    if selected_block==7:
	        if self.completed_block(copy,2,0) and self.completed_block(copy,2,2):
	            selected_block=-1
	        else:
	            available[2][0]=1
	            available[2][2]=1
	    if selected_block==8:
	        if self.completed_block(copy,1,2) and self.completed_block(copy,2,1):
	            selected_block=-1
	        else:
	            available[1][2]=1
	            available[2][1]=1
	    if selected_block==-1: #Any move allowed
	        for i in range(0,3):
	            for j in range(0,3):
	                available[i][j]=1
	    
	    #if firstcall==0:
	    #	print available
	    alphatemp = deepcopy(alpha)
	    betatemp = deepcopy(beta)

	    for i in range(0,9):
	        for j in range(0,9):
	            if copy[i][j]=='-' and available[i/3][j/3]==1:
	                copy[i][j]=player
	                if player==flag:
	                    cur_score = self.minimax(2,copy,1,depth+1,alphatemp,betatemp,(i%3)*3+j%3,flag)
	                    scores.append(cur_score)
	                    alphatemp = max(alphatemp, cur_score)
	                else:
	                    cur_score = self.minimax(1,copy,1,depth+1,alphatemp,betatemp,(i%3)*3+j%3,flag)
	                    scores.append(cur_score)
	                    betatemp = min(betatemp, cur_score)
	                copy[i][j]=0
	                moves.append((i)*10+(j))
	    
	    #If we are playing
	    if player==flag:
	        max_score = scores.index(max(scores))
	        j=(moves[max_score])%10
	        i=(moves[max_score]/10)%10
	        if firstcall==0:
	            return (int(i+1),int(j+1))
	        return scores[max_score]
	    else:
	        min_score = scores.index(min(scores))
	        j=(moves[min_score])%10
	        i=(moves[min_score]/10)%10
	        if firstcall==0:
	            return (int(i+1),int(j+1))
	        return scores[min_score]

	def move(self, temp_board, temp_block, old_move, flag):
		previous_move_r, previous_move_c = old_move[0], old_move[1]
		if previous_move_c==-1 and previous_move_r==-1:
		    selected_block=-1
		else:
		    selected_block = ((previous_move_c-1)%3+((previous_move_r-1)%3)*3) #x is the column y is the row
		return self.minimax(flag,temp_board,0,0,-INF,INF,selected_block,flag)
