from board.move import move
from pieces.nullpiece import nullpiece
from pieces.queen import queen
import random

class AI:

    global tp
    tp=[]


    def __init__(self):
        pass


    def evaluate(self,gametiles):
        min=100000
        count=0
        count2=0
        chuk=[]
        movex=move()
        tp.clear()
        xp=self.minimax(gametiles,3,-1000000000,1000000000,False)

        for zoom in tp:
            if zoom[4]<min:
                chuk.clear()
                chuk.append(zoom)
                min=zoom[4]
            if zoom[4]==min:
                chuk.append(zoom)
        fx=random.randrange(len(chuk))
        print(tp)
        return chuk[fx][0],chuk[fx][1],chuk[fx][2],chuk[fx][3]


    def reset(self,gametiles):
        for x in range(8):
            for y in range(8):
                if gametiles[x][y].pieceonTile.tostring()=='k' or gametiles[x][y].pieceonTile.tostring()=='r':
                    gametiles[x][y].pieceonTile.moved=False


    def updateposition(self,x,y):
        a=x*8
        b=a+y
        return b

    def checkmate(self,gametiles):
        movex=move()
        if movex.checkw(gametiles)[0]=='checked':
            array=movex.movesifcheckedw(gametiles)
            if len(array)==0:
                return True

        if movex.checkb(gametiles)[0]=='checked' :
            array=movex.movesifcheckedb(gametiles)
            if len(array)==0:
                return True

    def stalemate(self,gametiles,player):
        movex=move()
        if player==False:
            if movex.checkb(gametiles)[0]=='notchecked':
                check=False
                for x in range(8):
                    for y in range(8):
                        if gametiles[y][x].pieceonTile.alliance=='Black':
                            moves1=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                            lx1=movex.pinnedb(gametiles,moves1,y,x)
                            if len(lx1)==0:
                                continue
                            else:
                                check=True
                            if check==True:
                                break
                    if check==True:
                        break

                if check==False:
                    return True

        if player==True:
                if movex.checkw(gametiles)[0]=='notchecked':
                    check=False
                    for x in range(8):
                        for y in range(8):
                            if gametiles[y][x].pieceonTile.alliance=='White':
                                moves1=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                                lx1=movex.pinnedw(gametiles,moves1,y,x)
                                if len(lx1)==0:
                                    continue
                                else:
                                    check=True
                                if check==True:
                                    break
                        if check==True:
                            break

                    if check==False:
                        return True






    def minimax(self,gametiles, depth,alpha , beta ,player):
        if depth==0 or self.checkmate(gametiles)==True or self.stalemate(gametiles,player)==True:
            return self.calculateb(gametiles)
        if not player:
            minEval=100000000
            kp,ks=self.eva(gametiles,player)
            for lk in kp:
                for move in lk:
                    mts=gametiles[move[2]][move[3]].pieceonTile
                    gametiles=self.move(gametiles,move[0],move[1],move[2],move[3])
                    evalk=self.minimax(gametiles,depth-1,alpha,beta,True)
                    if evalk<minEval and depth==3:
                        tp.clear()
                        tp.append(move)
                    if evalk==minEval and depth==3:
                        tp.append(move)
                    minEval=min(minEval,evalk)
                    beta=min(beta,evalk)
                    gametiles=self.revmove(gametiles,move[2],move[3],move[0],move[1],mts)
                    if beta<=alpha:
                        break

                if beta<=alpha:
                    break
            return minEval

        else:
            maxEval=-100000000
            kp,ks=self.eva(gametiles,player)
            for lk in ks:
                for move in lk:
                    mts=gametiles[move[2]][move[3]].pieceonTile
                    gametiles=self.movew(gametiles,move[0],move[1],move[2],move[3])
                    evalk=self.minimax(gametiles,depth-1,alpha,beta,False)
                    maxEval=max(maxEval,evalk)
                    alpha=max(alpha,evalk)
                    gametiles=self.revmove(gametiles,move[2],move[3],move[0],move[1],mts)
                    if beta<=alpha:
                        break
                if beta<=alpha:
                    break

            return maxEval



    def printboard(self,gametilles):
        count = 0
        for rows in range(8):
            for column in range(8):
                print('|', end=gametilles[rows][column].pieceonTile.tostring())
            print("|",end='\n')


    def checkeva(self,gametiles,moves):
        arr=[]
        for move in moves:
            lk=[[move[2],move[3]]]
            arr.append(self.calci(gametiles,move[0],move[1],lk))

        return arr



    def eva(self,gametiles,player):
        lx=[]
        moves=[]
        kp=[]
        ks=[]
        movex=move()
        for x in range(8):
            for y in range(8):
                    if gametiles[y][x].pieceonTile.alliance=='Black' and player==False:
                        if movex.checkb(gametiles)[0]=='checked':
                            moves=movex.movesifcheckedb(gametiles)
                            arr=self.checkeva(gametiles,moves)
                            kp=arr
                            return kp,ks
                        moves=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                        if len(moves)==0:
                            continue
                        else:
                            if(gametiles[y][x].pieceonTile.tostring()=='K'):
                                ax=movex.castlingb(gametiles)
                                if not len(ax)==0:
                                    for l in ax:
                                        if l=='ks':
                                            moves.append([0,6])
                                        if l=='qs':
                                            moves.append([0,2])
                        if gametiles[y][x].pieceonTile.alliance=='Black':
                            lx=movex.pinnedb(gametiles,moves,y,x)
                        moves=lx
                        if len(moves)==0:
                            continue
                        kp.append(self.calci(gametiles,y,x,moves))


                    if gametiles[y][x].pieceonTile.alliance=='White' and player==True:
                        if movex.checkw(gametiles)[0]=='checked':
                            moves=movex.movesifcheckedw(gametiles)
                            arr=self.checkeva(gametiles,moves)
                            ks=arr
                            return kp,ks
                        moves=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                        if moves==None:
                            print(y)
                            print(x)
                            print(gametiles[y][x].pieceonTile.position)
                        if len(moves)==0:
                            continue
                        else:
                            if(gametiles[y][x].pieceonTile.tostring()=='k'):
                                ax=movex.castlingw(gametiles)
                                if not len(ax)==0:
                                    for l in ax:
                                        if l=='ks':
                                            moves.append([7,6])
                                        if l=='qs':
                                            moves.append([7,2])
                        if gametiles[y][x].pieceonTile.alliance=='White':
                            lx=movex.pinnedw(gametiles,moves,y,x)
                        moves=lx
                        if len(moves)==0:
                            continue
                        ks.append(self.calci(gametiles,y,x,moves))

        return kp,ks



    def calci(self,gametiles,y,x,moves):
        arr=[]
        jk=object
        for move in moves:
            jk=gametiles[move[0]][move[1]].pieceonTile
            gametiles[move[0]][move[1]].pieceonTile=gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile=nullpiece()
            mk=self.calculateb(gametiles)
            gametiles[y][x].pieceonTile=gametiles[move[0]][move[1]].pieceonTile
            gametiles[move[0]][move[1]].pieceonTile=jk
            arr.append([y,x,move[0],move[1],mk])
        return arr

    """
    From this point on will be code the group added
    No modifications were made to functions other 
    than the evaluation function, and these additions
    are only used within themselves or in the evaluation function
    """

    #Using Stockfish values, source: https://chess.stackexchange.com/a/27391
    #use same dict for both white and black
    #reminder: black is capitals
    piece_value_midgame = {
        'p' : 126,
        'n' : 781,
        'b' : 825,
        'r' : 1276,
        'q' : 2538,
        'k' : 100000,
        'P' : -126,
        'N' : -781,
        'B' : -825,
        'R' : -1276,
        'Q' : -2538,
        'K' : -100000,
        '-' : 0
    }
    piece_value_endgame = {
        'p' : 208,
        'n' : 854,
        'b' : 915,
        'r' : 1380,
        'q' : 2682,
        'k' : 100000,
        'P' : -208,
        'N' : -854,
        'B' : -915,
        'R' : -1380,
        'Q' : -2682,
        'K' : -100000,
        '-' : 0
    }

    """
    Search over board and sum mats
    """
    def material_sum(self, gametiles, piece_value):
        mat_sum = 0
        for x in range(8):
            for y in range(8):
                mat_sum += piece_value[gametiles[y][x].pieceonTile.tostring()]
        return mat_sum


    """
    it's possible and common to use opening vs midgame vs endgame
    but it's also pretty common to treat opening and midgame as the same
    since we're not doing anything special in openings because 
    that would overcomplicate this even more,
    we're just going to treat opening and midgame the same material-wise
    """
    """
    How we're calculating endgame vs not:
    pretty much just count how many non-trivial pieces there are
    """
    def is_endgame(self, gametiles):
        major_minor_count = 0
        for x in range(8):
            for y in range(8):
                if gametiles[y][x].pieceonTile.tostring() == 'b' or gametiles[y][x].pieceonTile.tostring() == 'B':
                    major_minor_count = major_minor_count + 1
                if gametiles[y][x].pieceonTile.tostring() == 'n' or gametiles[y][x].pieceonTile.tostring() == 'N':
                    major_minor_count = major_minor_count + 1
                if gametiles[y][x].pieceonTile.tostring() == 'r' or gametiles[y][x].pieceonTile.tostring() == 'R':
                    major_minor_count = major_minor_count + 1
                if gametiles[y][x].pieceonTile.tostring() == 'q' or gametiles[y][x].pieceonTile.tostring() == 'Q':
                    major_minor_count = major_minor_count + 1
        if major_minor_count <= 7:
            return True
        return False


    """
    eval idea from https://hxim.github.io/Stockfish-Evaluation-Guide/ 
    there are some shortcuts to not make this take 100 years to run
    and or things that would require refactoring that we're not allowed to do
    """
    def bishop_pair(self, gametiles):
        #return count of bishop pairs
        white_count = sum(x.count('b') for x in gametiles)
        black_count = sum(x.count('B') for x in gametiles)
        return white_count - black_count
    
    def get_column(self, matrix, col):
        return [row[col] for row in matrix]


    def isolated_pawns(self, gametiles):
        #NTS: gametiles is rows by columns
        #isolated pawn is one that has no friendly pawn in the adjacent cols
        white_iso_pawn_count = 0
        black_iso_pawn_count = 0
        for x in range(8):
            for y in range(8):
                if gametiles[y][x].pieceonTile.tostring() == 'p':
                    #if we get a p, we need to check adjacent columns
                    if x == 0:
                        if self.get_column(gametiles, x + 1).count('p') == 0:
                            white_iso_pawn_count = white_iso_pawn_count + 1
                    elif x == 7:
                        if self.get_column(gametiles, x - 1).count('p') == 0:
                            white_iso_pawn_count = white_iso_pawn_count + 1
                    else:
                        if self.get_column(gametiles, x - 1).count('p') == 0 and self.get_column(gametiles, x + 1).count('p') == 0:
                            white_iso_pawn_count = white_iso_pawn_count + 1
                if gametiles[y][x].pieceonTile.tostring() == 'P':
                    if x == 0:
                        if self.get_column(gametiles, x + 1).count('P') == 0:
                            black_iso_pawn_count = black_iso_pawn_count + 1
                    elif x == 7:
                        if self.get_column(gametiles, x - 1).count('P') == 0:
                            black_iso_pawn_count = black_iso_pawn_count + 1
                    else:
                        if self.get_column(gametiles, x - 1).count('P') == 0 and self.get_column(gametiles, x + 1).count('P') == 0:
                            black_iso_pawn_count = black_iso_pawn_count + 1

        return white_iso_pawn_count - black_iso_pawn_count

    def supported_pawns(self, gametiles):
        #number of pawns behind each piece,
        #double counting if has 2 behind it
        #
        white_supp_pawn_count = 0
        black_supp_pawn_count = 0
        #can abuse fact no pawn can be in rows 0 and 7
        for x in range(1,7):
            for y in range(8): 
                if gametiles[y][x].pieceonTile.tostring() == 'p':
                    if y == 0:
                        white_supp_pawn_count += (1 if gametiles[y+1][x+1].pieceonTile.tostring() == 'p' else 0)
                    elif y == 7:
                        white_supp_pawn_count += (1 if gametiles[y-1][x+1].pieceonTile.tostring() == 'p' else 0)
                    else:
                        white_supp_pawn_count += (1 if gametiles[y+1][x+1].pieceonTile.tostring() == 'p' else 0)
                        white_supp_pawn_count += (1 if gametiles[y-1][x+1].pieceonTile.tostring() == 'p' else 0)
                if gametiles[y][x].pieceonTile.tostring() == 'P':
                    if y == 0:
                        black_supp_pawn_count += (1 if gametiles[y+1][x-1].pieceonTile.tostring() == 'P' else 0)
                    elif y == 7:
                        black_supp_pawn_count += (1 if gametiles[y-1][x-1].pieceonTile.tostring() == 'P' else 0)
                    else:
                        black_supp_pawn_count += (1 if gametiles[y+1][x-1].pieceonTile.tostring() == 'P' else 0)
                        black_supp_pawn_count += (1 if gametiles[y-1][x-1].pieceonTile.tostring() == 'P' else 0)
        return white_supp_pawn_count - black_supp_pawn_count

    def mobility(self, gamestate):
        white_legal = 0
        black_legal = 0
        for x in range(8):
            for y in range(8):
                if gamestate[y][x].pieceonTile.alliance and gamestate[y][x].pieceonTile.legalmoveb(gamestate):
                    if gamestate[y][x].pieceonTile.alliance == 'White':
                        white_legal += len(gamestate[y][x].pieceonTile.legalmoveb(gamestate))
                    if gamestate[y][x].pieceonTile.alliance == 'Black':
                        black_legal += len(gamestate[y][x].pieceonTile.legalmoveb(gamestate))
        return white_legal - black_legal     

    def center_check(self, gametiles):
        pos_bonus = 0
        for x in range(8):
            for y in range(8):
                if gametiles[y][x] in ["P", "R", "N", "B", "Q"]:
                    if x in [3,4] and y in [3,4]:
                        pos_bonus -= 100
                    if x in [2,5] and y in [2,5]:
                        pos_bonus -= 40
                if gametiles[y][x] in ["p", "r", "n", "b", "q"]:
                    if x in [3,4] and y in [3,4]:
                        pos_bonus += 100
                    if x in [2,5] and y in [2,5]:
                        pos_bonus += 40
        return pos_bonus

    def king_safety(self, gametiles):
        safe_bonus = 0
        for x in range(8):
            for y in range(8):
                safety = min(x,y,7-x,7-y)
                if gametiles[y][x].pieceonTile.tostring() == 'k':
                    safe_bonus += 200 * safety
                if gametiles[y][x].pieceonTile.tostring() == 'K':
                    safe_bonus -= 200 * safety
        return safe_bonus

    
    def calculateb(self,gametiles):
        """
        General framework of evaluation criteria:
        Eval(s) = material + mobility + king-safety + center-control
        Source: Page 56/57 of https://web.stanford.edu/class/archive/cs/cs221/cs221.1186/lectures/games1.pdf
        """
        value=0
        if self.is_endgame(gametiles):
            material_sum = self.material_sum(gametiles, self.piece_value_endgame)
        else:
            material_sum = self.material_sum(gametiles, self.piece_value_midgame)

        #imbalance, using estimate of (material_sum + bishop_pair) / 16
        bishop_pair = self.bishop_pair(gametiles)
        imbalance = (material_sum + bishop_pair) / 16
        #pawns check
        iso_val = self.isolated_pawns(gametiles)
        supp_val = self.supported_pawns(gametiles)
        pawns_val = (-5 * iso_val) + (8 * supp_val)
        #mobility: number of legal moves, usually uses a table but this is 
        #relatively rudimentary, using arbitrary scaling
        mobility_val = 20 * self.mobility(gametiles)
        #center checking
        center_val = self.center_check(gametiles)
        #king safety
        safe_val = self.king_safety(gametiles)
        value = material_sum + imbalance + pawns_val + mobility_val + center_val + safe_val
    
        return value

    """
    End of group modifications
    """

    def move(self,gametiles,y,x,n,m):
        promotion=False
        if gametiles[y][x].pieceonTile.tostring()=='K' or gametiles[y][x].pieceonTile.tostring()=='R':
            gametiles[y][x].pieceonTile.moved=True

        if gametiles[y][x].pieceonTile.tostring()=='K' and m==x+2:
            gametiles[y][x+1].pieceonTile=gametiles[y][x+3].pieceonTile
            s=self.updateposition(y,x+1)
            gametiles[y][x+1].pieceonTile.position=s
            gametiles[y][x+3].pieceonTile=nullpiece()
        if gametiles[y][x].pieceonTile.tostring()=='K' and m==x-2:
            gametiles[y][x-1].pieceonTile=gametiles[y][0].pieceonTile
            s=self.updateposition(y,x-1)
            gametiles[y][x-1].pieceonTile.position=s
            gametiles[y][0].pieceonTile=nullpiece()



        if gametiles[y][x].pieceonTile.tostring()=='P' and y+1==n and y==6:
            promotion=True


        if promotion==False:

            gametiles[n][m].pieceonTile=gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile=nullpiece()
            s=self.updateposition(n,m)
            gametiles[n][m].pieceonTile.position=s

        if promotion==True:

            if gametiles[y][x].pieceonTile.tostring()=='P':
                gametiles[y][x].pieceonTile=nullpiece()
                gametiles[n][m].pieceonTile=queen('Black',self.updateposition(n,m))
                promotion=False

        return gametiles



    def revmove(self,gametiles,x,y,n,m,mts):
        if gametiles[x][y].pieceonTile.tostring()=='K':
            if m==y-2:
                gametiles[x][y].pieceonTile.moved=False
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][7].pieceonTile=gametiles[x][y-1].pieceonTile
                s=self.updateposition(n,7)
                gametiles[n][7].pieceonTile.position=s
                gametiles[n][7].pieceonTile.moved=False

                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()

            elif m==y+2:
                gametiles[x][y].pieceonTile.moved=False
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][0].pieceonTile=gametiles[x][y+1].pieceonTile
                s=self.updateposition(m,0)
                gametiles[n][0].pieceonTile.position=s
                gametiles[n][0].pieceonTile.moved=False
                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()

            else:
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[x][y].pieceonTile=mts

            return gametiles

        if gametiles[x][y].pieceonTile.tostring()=='k':
            if m==y-2:

                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][7].pieceonTile=gametiles[x][y-1].pieceonTile
                s=self.updateposition(n,7)
                gametiles[n][7].pieceonTile.position=s
                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()


            elif m==y+2:

                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][0].pieceonTile=gametiles[x][y+1].pieceonTile
                s=self.updateposition(n,0)
                gametiles[n][0].pieceonTile.position=s
                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()


            else:
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[x][y].pieceonTile=mts


            return gametiles

        gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
        s=self.updateposition(n,m)
        gametiles[n][m].pieceonTile.position=s
        gametiles[x][y].pieceonTile=mts

        return gametiles



    def movew(self,gametiles,y,x,n,m):
        promotion=False
        if gametiles[y][x].pieceonTile.tostring()=='k' or gametiles[y][x].pieceonTile.tostring()=='r':
            pass

        if gametiles[y][x].pieceonTile.tostring()=='k' and m==x+2:
            gametiles[y][x+1].pieceonTile=gametiles[y][x+3].pieceonTile
            s=self.updateposition(y,x+1)
            gametiles[y][x+1].pieceonTile.position=s
            gametiles[y][x+3].pieceonTile=nullpiece()
        if gametiles[y][x].pieceonTile.tostring()=='k' and m==x-2:
            gametiles[y][x-1].pieceonTile=gametiles[y][0].pieceonTile
            s=self.updateposition(y,x-1)
            gametiles[y][x-1].pieceonTile.position=s
            gametiles[y][0].pieceonTile=nullpiece()



        if gametiles[y][x].pieceonTile.tostring()=='p' and y-1==n and y==1:
            promotion=True


        if promotion==False:

            gametiles[n][m].pieceonTile=gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile=nullpiece()
            s=self.updateposition(n,m)
            gametiles[n][m].pieceonTile.position=s

        if promotion==True:

            if gametiles[y][x].pieceonTile.tostring()=='p':
                gametiles[y][x].pieceonTile=nullpiece()
                gametiles[n][m].pieceonTile=queen('White',self.updateposition(n,m))
                promotion=False

        return gametiles
























                        
