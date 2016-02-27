#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

from copy import deepcopy
import time
from random import shuffle

INF = 1000000000
t0 = 0
complete = False

visited = {}

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
        if blocks[0][0]==1 and blocks[1][1]==1 and blocks[2][2]==1:
            return 1
        if blocks[0][2]==1 and blocks[1][1]==1 and blocks[2][0]==1:
            return 1
        for i in range(0,3):
            if blocks[i][0]==1 and blocks[i][1]==1 and blocks[i][2]==1:
                return 1
            if blocks[0][i]==1 and blocks[1][i]==1 and blocks[2][i]==1:
                return 1
        return 0

    def completed_board(self,game):
        for i in range(0,9):
            for j in range(0,9):
                if game[i][j]=='-' and self.block_win('x',game,i/3,j/3)==0 and self.block_win('o',game,i/3,j/3)==0:
                    return 0
        return 1

    def completed_block(self,game,a,b):
        if self.block_win('x',game,a,b) or self.block_win('o',game,a,b):
            return 1
        for i in range(0,3):
            for j in range(0,3):
                if game[i+a*3][j+b*3]=='-':
                    return 0
        return 1

    #HEURISTIC
    def assumedScore(self,game,depth,player,flag):
        block = [[0,0,0],[0,0,0],[0,0,0]]
        for i in range(0,3):
            for j in range(0,3):
                captured=0
                baser = i * 3
                basec = j * 3
                pdp = 0
                sdp = 0
                pdo = 0
                sdo = 0
                for p in range(0,3):
                    cr = 0
                    cc = 0
                    opr = 0
                    opc = 0
                    for q in range(0,3):
                        if game[baser + p][basec + q] == player:
                            cr+=1
                        if game[baser + p][basec + q] == ('x' if player == 'o' else 'o'):
                            opr+=1
                        if game[baser + q][basec + p] == player:
                            cc+=1
                        if game[baser + q][basec + p] == ('x' if player == 'o' else 'o'):
                            opc+=1
                    if cr == 3:
                        captured += 100
                    if cr == 2:
                        captured += 10
                    if cr == 1:
                        captured += 1
                    if cc == 3:
                        captured += 100
                    if cc == 2:
                        captured += 10
                    if cc == 1:
                        captured += 1
                    if opr == 3:
                        captured -= 100
                    if opr == 2:
                        captured -= 10
                    if opr == 1:
                        captured -= 1
                    if opc == 3:
                        captured -= 100
                    if opc == 2:
                        captured -= 10
                    if opc == 1:
                        captured -= 1
                    if game[baser + p][basec + p] == player:
                        pdp += 1
                    if game[baser + p][basec + 2 - p] == player:
                        sdp += 1
                    if game[baser + p][basec + p] == ('x' if player == 'o' else 'o'):
                        pdo += 1
                    if game[baser + p][basec + 2 - p] == ('x' if player == 'o' else 'o'):
                        sdo += 1
                if pdp == 3:
                    captured += 100
                if pdp == 2:
                    captured += 10
                if pdp == 1:
                    captured += 1
                if sdp == 3:
                    captured += 100
                if sdp == 2:
                    captured += 10
                if sdp == 1:
                    captured += 1
                if pdo == 3:
                    captured -= 100
                if pdo == 2:
                    captured -= 10
                if pdo == 1:
                    captured -= 1
                if sdo == 3:
                    captured -= 100
                if sdo == 2:
                    captured -= 10
                if sdo == 1:
                    captured -= 1
                block[i][j] = captured

        final_score = 0
        for i in range(0,3):
            row = 1
            col = 1
            if block[i][0]>0:
                row *= block[i][0]
            if block[i][1]>0:
                row *= block[i][1]
            if block[i][2]>0:
                row *= block[i][2]
            if block[0][i]>0:
                col *= block[0][i]
            if block[1][i]>0:
                col *= block[1][i]
            if block[2][i]>0:
                col *= block[2][i]

            final_score += row + col

            row = 1
            col = 1
            if block[i][0]<0:
                row *= abs(block[i][0])
            if block[i][1]<0:
                row *= abs(block[i][1])
            if block[i][2]<0:
                row *= abs(block[i][2])
            if block[0][i]<0:
                col *= abs(block[0][i])
            if block[1][i]<0:
                col *= abs(block[1][i])
            if block[2][i]<0:
                col *= abs(block[2][i])

            final_score -= row + col

        diag11 = 1
        diag12 = 1
        diag21 = 1
        diag22 = 1
        for p in range(0,3):
            if block[p][p]>0:
                diag11 *= block[p][p]
            if block[p][p]<0:
                diag12 *= abs(block[p][p])
            if block[p][2-p]>0:
                diag21 *= block[p][2-p]
            if block[p][2-p]<0:
                diag22 *= abs(block[p][2-p])

        final_score += diag11 + diag21 - diag12 - diag22

        if player==flag:
            return final_score
        else:
            return -final_score

    def minimax(self,player,game,firstcall,depth,alpha,beta,selected_block,flag,maxdepth):

    	global visited

    	state_string = self.getStateString(game)
    	if state_string in visited and firstcall != 0:
    		return visited[state_string]

        global t0
        global complete
        if time.clock() - t0 >=9:
            complete = False
            return self.assumedScore(game,depth,player,flag)
        if alpha>beta:
            if player==flag:
                #Parent is minimizer
                return INF
            else:
                #Parent is maximizer
                return -INF
        #The game is complete (All blocks filled) or if there is a winner of the game, then return the heruistic based cost function values
        if self.board_win('o',game) or self.board_win('x',game) or self.completed_board(game) or depth>=maxdepth: 
            return self.assumedScore(game,depth,player,flag)

        scores = []
        moves = []
        copy = deepcopy(game)

        available=[[0,0,0],[0,0,0],[0,0,0]]
        if selected_block==0:
            if self.completed_block(copy,0,1) and self.completed_block(copy,1,0):
                selected_block=-1
            if not self.completed_block(copy,0,1):
                available[0][1]=1
            if not self.completed_block(copy,1,0):
                available[1][0]=1
        if selected_block==1:
            if self.completed_block(copy,0,2) and self.completed_block(copy,0,0):
                selected_block=-1
            if not self.completed_block(copy,0,2):
                available[0][2]=1
            if not self.completed_block(copy,0,0):
                available[0][0]=1
        if selected_block==2:
            if self.completed_block(copy,0,1) and self.completed_block(copy,1,2):
                selected_block=-1
            if not self.completed_block(copy,0,1):
                available[0][1]=1
            if not self.completed_block(copy,1,2):
                available[1][2]=1
        if selected_block==3:
            if self.completed_block(copy,0,0) and self.completed_block(copy,2,0):
                selected_block=-1
            if not self.completed_block(copy,0,0):
                available[0][0]=1
            if not self.completed_block(copy,2,0):
                available[2][0]=1
        if selected_block==4:
            if self.completed_block(copy,1,1):
                selected_block=-1
            if not self.completed_block(copy,1,1):
                available[1][1]=1
        if selected_block==5:
            if self.completed_block(copy,0,2) and self.completed_block(copy,2,2):
                selected_block=-1
            if not self.completed_block(copy,0,2):
                available[0][2]=1
            if not self.completed_block(copy,2,2):
                available[2][2]=1
        if selected_block==6:
            if self.completed_block(copy,1,0) and self.completed_block(copy,2,1):
                selected_block=-1
            if not self.completed_block(copy,1,0):
                available[1][0]=1
            if not self.completed_block(copy,2,1):
                available[2][1]=1
        if selected_block==7:
            if self.completed_block(copy,2,0) and self.completed_block(copy,2,2):
                selected_block=-1
            if not self.completed_block(copy,2,0):
                available[2][0]=1
            if not self.completed_block(copy,2,2):
                available[2][2]=1
        if selected_block==8:
            if self.completed_block(copy,1,2) and self.completed_block(copy,2,1):
                selected_block=-1
            if not self.completed_block(copy,1,2):
                available[1][2]=1
            if not self.completed_block(copy,2,1):
                available[2][1]=1
        if selected_block==-1: #Any move allowed
            for i in range(0,3):
                for j in range(0,3):
                    if not self.completed_block(copy,i,j):
                        available[i][j]=1
      
        alphatemp = deepcopy(alpha)
        betatemp = deepcopy(beta)

        for i in range(0,9):
            for j in range(0,9):
                if copy[i][j]=='-' and available[i/3][j/3]==1:
                    moves.append((i)*10+(j))

        shuffle(moves)

        for t in range(len(moves)):
            i = moves[t]/10
            j = moves[t]%10
            copy[i][j]=player
            if player==flag:
                cur_score = self.minimax(('x' if player == 'o' else 'o'),copy,1,depth+1,alphatemp,betatemp,(i%3)*3+j%3,flag,maxdepth)
                scores.append(cur_score)
                alphatemp = max(alphatemp, cur_score)
            else:
                cur_score = self.minimax(('x' if player == 'o' else 'o'),copy,1,depth+1,alphatemp,betatemp,(i%3)*3+j%3,flag,maxdepth)
                scores.append(cur_score)
                betatemp = min(betatemp, cur_score)
            copy[i][j]='-'
       
        #If we are playing
        if player==flag:
            max_score_index = scores.index(max(scores))
            j=(moves[max_score_index])%10
            i=(moves[max_score_index]/10)%10
            copy[i][j] = player
            state_string = self.getStateString(copy)
            visited[state_string] = scores[max_score_index]
            copy[i][j] = '-'
            if firstcall==0:
                return (int(i),int(j))
            return scores[max_score_index]
        else:
            min_score_index = scores.index(min(scores))
            j=(moves[min_score_index])%10
            i=(moves[min_score_index]/10)%10
            copy[i][j] = player
            state_string = self.getStateString(copy)
            visited[state_string] = scores[min_score_index]
            copy[i][j] = '-'
            if firstcall==0:
                return (int(i),int(j))
            return scores[min_score_index]

    def getStateString(self, temp_board):
    	ret_string = ''
    	for i in range(0,9):
    		for j in range(0,9):
    			if temp_board[i][j] == 'o':
    				ret_string += '1'
    			elif temp_board[i][j] == 'x':
    				ret_string += '2'
    			elif temp_board[i][j] == '-':
    				ret_string += '0'
    	return ret_string

    def move(self, temp_board, temp_block, old_move, flag):
        global t0
        global complete
        t0 = time.clock()
        previous_move_r, previous_move_c = old_move[0], old_move[1]
    	if previous_move_c==-1 and previous_move_r==-1:
    	    selected_block=-1
    	else:
    	    selected_block = ((previous_move_c)%3+((previous_move_r)%3)*3) #x is the column y is the row
        complete = True
        answer = self.minimax(flag,temp_board,0,0,-INF,INF,selected_block,flag,4)
        t1 = time.clock()
        max_depth = 5
        while t1-t0 <= 8:
            complete = True
            answer1 = self.minimax(flag,temp_board,0,0,-INF,INF,selected_block,flag,max_depth)
            if complete == True:
                answer = answer1
                max_depth += 1
                t1 = time.clock()
            else:
                break
        return answer

