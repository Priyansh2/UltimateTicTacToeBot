#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 varshit <varshit@varshit-Lenovo>
#
# Distributed under terms of the MIT license.


"""

"""

import random,datetime
#import sys

class Player36:

    def __init__(self):

        #Valid moves
        self.goTo={
                (0,0):[(1,0),(0,1)],
                (0,1):[(0,0),(0,2)],
                (0,2):[(0,1),(1,2)],
                (1,0):[(0,0),(2,0)],
                (1,1):[(1,1)],
                (1,2):[(0,2),(2,2)],
                (2,0):[(1,0),(2,1)],
                (2,1):[(2,0),(2,2)],
                (2,2):[(1,2),(2,1)]
                }

        #Offset for block to cell mapping
        self.base={
                (0,0):[0,0],
                (0,1):[0,3],
                (0,2):[0,6],
                (1,0):[3,0],
                (1,1):[3,3],
                (1,2):[3,6],
                (2,0):[6,0],
                (2,1):[6,3],
                (2,2):[6,6],
                }

        self.rows=((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))
        self.directreturn=0

    def heuristic(self,board,block,flag):
        blocks=((0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2))
        temp = [[0 for aa in range(3)] for bb in range(3)]
        for i in range(len(block)):
            ans=0
            base_tuple=self.base[blocks[i]]
            for j in range(8):
                os=0
                xs=0
                prerow = self.rows[j]
                for k in range(3):
                    if board[prerow[k]/3+base_tuple[0]][prerow[k]%3+base_tuple[1]]=='x':
                        xs+=1
                    if board[prerow[k]/3+base_tuple[0]][prerow[k]%3+base_tuple[1]]=='o':
                        os+=1
                if(flag=='x'):
                    if xs==3:
                        ans+=100
                    elif xs==2 and os==0:
                        ans+=10
                    elif xs==1:
                        ans+=1

                    if os==3:
                        ans-=100
                    elif os==2 and xs==0:
                        ans-=10
                if(flag=='o'):
                    if os==3:
                        ans+=100
                    elif os==2 and xs==0:
                        ans+=10
                    elif os==1:
                        ans+=1

                    if xs==3:
                        ans-=100
                    elif xs==2 and os==0:
                        ans-=10
            temp[i/3][i%3]=ans
        ans=0
        for i in range(8):
            prerow=self.rows[i]
            tempans=0
            os=0
            xs=0
            for j in range(3):
                tempans+=temp[prerow[j]/3][prerow[j]%3]/100.0
                if block[prerow[j]]=='x':
                    xs+=1
                if block[prerow[j]]=='o':
                    os+=1
            if flag=='o' and xs==3:
                ans-=100
            if flag=='x' and os==3:
                ans-=100
            if flag=='x' and xs==3:
                ans+=100
            if flag=='o' and os==3:
                ans+=100
            if (tempans>1 and tempans<10):
                ans+=1+((tempans-1)*9)
            elif (tempans>10 and tempans<100):
                ans+=10+(tempans-10)*90
            elif (tempans<-1 and tempans>-10):
                ans+=-1+(tempans+1)*9
            elif (tempans<-10 and tempans>-100):
                ans+=-10+(tempans+10)*90

        return ans




    def makeMove(self,board,block,enemyPos,depth,flag,parentvalues):

        # childvalues = (float("-inf"),float("inf"))
        childvalues = parentvalues
        if((depth%2)==1):
            temp = (parentvalues[0],parentvalues[1],float("inf"))
            childvalues = temp
        else:
            temp = (parentvalues[0],parentvalues[1],float("-inf"))
            childvalues = temp
        #First move
        miniMaxDict={}
        if enemyPos[0]==-1:
            pos=(4,(2,2))
            return pos

        # glaf var to determine draw of a block
        glaf=0
        #Assigning signs
        if(flag=='x' and depth!=0):
          board[enemyPos[0]][enemyPos[1]]='x'
        if(flag=='o' and depth!=0):
          board[enemyPos[0]][enemyPos[1]]='o'
        # if flag=='x':
        #     flag='o'
        # else:
        #     flag='x'
        base_tuple=self.base[(enemyPos[0]/3,enemyPos[1]/3)]
        glaf1=0
        for i in range(8):
            os=0
            xs=0
            prerow=self.rows[i]
            for j in range(3):
                if board[prerow[j]/3+base_tuple[0]][prerow[j]%3+base_tuple[1]]=='x':
                    xs+=1
                if board[prerow[j]/3+base_tuple[0]][prerow[j]%3+base_tuple[1]]=='o':
                    os+=1
            if os==3:
                block[(enemyPos[0]/3)*3+(enemyPos[1]/3)]='o'
                glaf1=1
                break
            if xs==3:
                block[(enemyPos[0]/3)*3+(enemyPos[1]/3)]='x'
                glaf1=1
                break

        # if depth==1:
        #     for i in range(8):
        #         prerow=self.rows[i]
        #         os=0
        #         xs=0
        #         for j in range(3):
        #             if block[prerow[j]]=='x':
        #                 xs+=1
        #             if block[prerow[j]]=='o':
        #                 os+=1
        #         if self.flag5=='x' and xs==3:
        #             self.directreturn=1
        #             return ((1000,1000,1000),enemyPos)
        #         if self.flag5=='o' and os==3:
        #             self.directreturn=1
        #             return ((1000,1000,1000),enemyPos)


                
        for j in range(3):
            for k in range(3):
                if board[j+base_tuple[0]][k+base_tuple[1]]=='-':
                    glaf=1
                    break
        if (glaf==0 and glaf1==0):
            block[(enemyPos[0]/3)*3+(enemyPos[1]/3)]='D'

        ourBlocks=self.goTo[(enemyPos[0]%3,enemyPos[1]%3)]
        
        #Checking for moves
        templist=[]
        for iters in range(len(ourBlocks)):
            if(block[ourBlocks[iters][0]*3+ourBlocks[iters][1]]=='-'):
                templist.append(ourBlocks[iters])

        #Block empty or not to get a free move
        ourBlocks = templist
        if(len(ourBlocks)==0):
            templist=[]
            for position in range(9):
                if(block[position]=='-'):
                    templist.append((position/3,position%3))
        ourBlocks = templist

        #leaf node
        if(len(ourBlocks)==0):
            p=self.heuristic(board,block,self.flag5)
            # p = random.randint(-100,100)
            return ((p,p,p),0)

        #Final return of heuristic
        if depth==5:
            p=self.heuristic(board,block,self.flag5)
            # print p
            # p=random.randint(-100,100)
            return ((p,p,p),0)
        else:
            for i in range(len(ourBlocks)):
                cells=ourBlocks[i]
                base_tuple=self.base[cells]
                bflag=0 
                for j in range(3):
                    for k in range(3):
                        if self.directreturn==1:
                            break
                        if board[j+base_tuple[0]][k+base_tuple[1]]=='-':
                            temp = [['-' for aa in range(9)] for bb in range(9)]
                            for l in range(9):
                                for m in range(9):
                                    temp[l][m]=board[l][m]
                            # print "childvalues:::",childvalues,enemyPos," ",(j+base_tuple[0],k+base_tuple[1])
                            #Calling minimax recursively
                            # fl = 'x'
                            # if flag=='x':
                            #     fl='o'
                            rtuple=self.makeMove(temp,block,(j+base_tuple[0],k+base_tuple[1]),depth+1,flag,childvalues)[0]
                            if depth%2==0:
                                temp1=(max(rtuple[2],childvalues[2]),childvalues[1],max(rtuple[2],childvalues[2]))
                                # childvalues[0]=max(rtuple[0],childvalues[0])
                                childvalues = temp1
                            if depth%2==1:
                                temp1 = (childvalues[0],min(rtuple[2],childvalues[2]),min(rtuple[2],childvalues[2]))
                                # childvalues[1]=min(rtuple[1],childvalues[1])
                                childvalues = temp1
                            # print
                            # print "Before pruning:::",rtuple," ",childvalues," ",depth," ",enemyPos," ",(j+base_tuple[0],k+base_tuple[1])
                            utility=rtuple
                            miniMaxDict[utility]=(j+base_tuple[0],k+base_tuple[1])
                            if childvalues[0]>=childvalues[1]:
                                # print
                                # print childvalues," 45678"," ",depth," ",enemyPos," ",(j+base_tuple[0],k+base_tuple[1])
                                bflag=1
                                break
                    if bflag==1:
                        break

        # print "miniMax len %s" %len(miniMaxDict)
        # print
        # print miniMaxDict
        # print

        #Return the max or min values based on level 
        if depth%2==0 and len(miniMaxDict)!=0 and depth==0:
            return sorted(miniMaxDict.items())[len(miniMaxDict)-1]
        else:
            return (childvalues,enemyPos)
        # if depth%2==1 and len(miniMaxDict)!=0:
        #     return sorted(miniMaxDict.items())[len(miniMaxDict)-1]

    def move(self,board,block,enemyPos,flag):
        #calling minimax funtion
        print datetime.datetime.now()
        # if flag=='x':
        #     flag='o'
        # else:
        #     flag='x'
        self.flag5=flag
        temp=[]
        for i in range(9):
            temp.append(block[i])
        final=self.makeMove(board,temp,enemyPos,0,flag,(float("-inf"),float("inf"),float("inf")))
        print 'Player sign and move',flag,final[1]
        print datetime.datetime.now()
        return final[1]
