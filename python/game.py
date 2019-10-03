import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import copy

#these should be passed in as start params
player = "white"

#records the selected square
selected = None

#holds the state of the board
board = None

#flag that indicates whether the board should be redrawn
#currently not used
redraw = True

#turn counter even will be whites turn and odd will be blacks turn
turnCounter = 0

#special move flags
doubleMove = False
enPassantCapture = False
castling = False

def initBoard():
    global board
    board = [[{"piece":"blank"} for x in range(8)] for y in range(8)] 
    board[0][1] = {"piece":"pawn"  , "color":"white", "moved": False, "lastMoved": -1}
    board[1][1] = {"piece":"pawn"  , "color":"white", "moved": False, "lastMoved": -1}
    board[2][1] = {"piece":"pawn"  , "color":"white", "moved": False, "lastMoved": -1}
    board[3][1] = {"piece":"pawn"  , "color":"white", "moved": False, "lastMoved": -1}
    board[4][1] = {"piece":"pawn"  , "color":"white", "moved": False, "lastMoved": -1}
    board[5][1] = {"piece":"pawn"  , "color":"white", "moved": False, "lastMoved": -1}
    board[6][1] = {"piece":"pawn"  , "color":"white", "moved": False, "lastMoved": -1}
    board[7][1] = {"piece":"pawn"  , "color":"white", "moved": False, "lastMoved": -1}
    board[0][0] = {"piece":"rook"  , "color":"white", "moved": False, "lastMoved": -1}
    board[7][0] = {"piece":"rook"  , "color":"white", "moved": False, "lastMoved": -1}
    board[1][0] = {"piece":"knight", "color":"white", "moved": False, "lastMoved": -1}
    board[6][0] = {"piece":"knight", "color":"white", "moved": False, "lastMoved": -1}
    board[2][0] = {"piece":"bishop", "color":"white", "moved": False, "lastMoved": -1}        
    board[5][0] = {"piece":"bishop", "color":"white", "moved": False, "lastMoved": -1}        
    board[3][0] = {"piece":"queen" , "color":"white", "moved": False, "lastMoved": -1}
    board[4][0] = {"piece":"king"  , "color":"white", "moved": False, "lastMoved": -1}

    board[0][6] = {"piece":"pawn"  , "color":"black", "moved": False, "lastMoved": -1}
    board[1][6] = {"piece":"pawn"  , "color":"black", "moved": False, "lastMoved": -1}
    board[2][6] = {"piece":"pawn"  , "color":"black", "moved": False, "lastMoved": -1}
    board[3][6] = {"piece":"pawn"  , "color":"black", "moved": False, "lastMoved": -1}
    board[4][6] = {"piece":"pawn"  , "color":"black", "moved": False, "lastMoved": -1}
    board[5][6] = {"piece":"pawn"  , "color":"black", "moved": False, "lastMoved": -1}
    board[6][6] = {"piece":"pawn"  , "color":"black", "moved": False, "lastMoved": -1}
    board[7][6] = {"piece":"pawn"  , "color":"black", "moved": False, "lastMoved": -1}
    board[0][7] = {"piece":"rook"  , "color":"black", "moved": False, "lastMoved": -1}
    board[7][7] = {"piece":"rook"  , "color":"black", "moved": False, "lastMoved": -1}
    board[1][7] = {"piece":"knight", "color":"black", "moved": False, "lastMoved": -1}
    board[6][7] = {"piece":"knight", "color":"black", "moved": False, "lastMoved": -1}
    board[2][7] = {"piece":"bishop", "color":"black", "moved": False, "lastMoved": -1}
    board[5][7] = {"piece":"bishop", "color":"black", "moved": False, "lastMoved": -1} 
    board[3][7] = {"piece":"queen" , "color":"black", "moved": False, "lastMoved": -1}
    board[4][7] = {"piece":"king"  , "color":"black", "moved": False, "lastMoved": -1}

def translate(val):
    return val/4.0-1

#functions to draw the pieces
def pawn(x, y):
    glVertex2f(x+.10, y+.10)
    glVertex2f(x+.15, y+.10)
    glVertex2f(x+.15, y+.15)
    glVertex2f(x+.10, y+.15)
def rook(x, y):
    glVertex2f(x+.10, y+.075)
    glVertex2f(x+.15, y+.075)
    glVertex2f(x+.15, y+.175)
    glVertex2f(x+.10, y+.175)
def knight(x, y):
    glVertex2f(x+.10,  y+.075)
    glVertex2f(x+.10,  y+.175)
    glVertex2f(x+.175, y+.175)
    glVertex2f(x+.175, y+.125)
    glVertex2f(x+.15,  y+.125)
    glVertex2f(x+.15,  y+.075)
def bishop(x, y):
    glVertex2f(x+.10, y+.075)
    glVertex2f(x+.15, y+.075)
    glVertex2f(x+.15, y+.175)
    glVertex2f(x+.10, y+.125)
def queen(x, y):
    glVertex2f(x+.10, y+.05)
    glVertex2f(x+.15, y+.05)
    glVertex2f(x+.15, y+.15)
    glVertex2f(x+.125, y+.2)
    glVertex2f(x+.10, y+.15)
def king(x, y):
    glVertex2f(x+.10, y+.05)
    glVertex2f(x+.15, y+.05)
    glVertex2f(x+.15, y+.2)
    glVertex2f(x+.125, y+.15)
    glVertex2f(x+.10, y+.2)

def drawPieces():
    for x in range(8):
        for y in range(8):
            if board[x][y]["piece"] == "blank":
                continue
            glBegin(GL_POLYGON)
            if board[x][y]["color"] == "white":
                #draw white
                glColor3f(0.5,0.5,0.5)
            else:
                #draw black
                glColor3f(0.0,0.0,0.0)
            tx = translate(x)
            ty = translate(y)
            if board[x][y]["piece"] == "pawn":
                pawn(tx, ty)
            elif board[x][y]["piece"] == "rook":
                rook(tx, ty)
            elif board[x][y]["piece"] == "knight":
                knight(tx, ty)
            elif board[x][y]["piece"] == "bishop":
                bishop(tx, ty)
            elif board[x][y]["piece"] == "queen":
                queen(tx, ty)
            elif board[x][y]["piece"] == "king":
                king(tx, ty)
            glEnd()

        


#function to draw a board square
def square(whiteOrBlack, x, y):
    tx = translate(x)
    ty = translate(y)
    glBegin(GL_POLYGON)
    if whiteOrBlack:
        #draw white
        glColor3f(1.0,1.0,1.0)
    else:
        #draw black
        glColor3f(0.54,0.27,0.07)

    glVertex2f(tx, ty)
    glVertex2f(tx+.25, ty)
    glVertex2f(tx+.25, ty+.25)
    glVertex2f(tx, ty+.25)
    glEnd()

#highlights the selected square
def selectedSquare(x,y):
    tx = translate(x)
    ty = translate(y)
    glBegin(GL_LINES)
    #draw green
    glColor3f(0,0.7,0)
    glVertex2f(tx, ty)
    glVertex2f(tx+.25, ty)

    glVertex2f(tx+.25, ty)
    glVertex2f(tx+.25, ty+.25)

    glVertex2f(tx+.25, ty+.25)
    glVertex2f(tx, ty+.25)

    glVertex2f(tx, ty+.25)
    glVertex2f(tx, ty)
    glEnd()


#todo
#display whose turn it is 
#display captured pieces
#checkmate
#castling

#function to draw the board
def drawBoard():
    for x in range(0,8):
        for y in range(0,8):
            square(x%2!=y%2, x, y)
    if selected:
        selectedSquare(selected[0], selected[1])
    #now print all the pieces
    drawPieces()

def inCheck(source, dest, color):
    otherColor = "black" if color=="white" else "white"

#cant take your own piece, returns true if you're trying to take your own piece
def checkOwnPiece(board, source, dest):
    if board[dest[0]][dest[1]]["piece"] != "blank":
        return board[source[0]][source[1]]["color"] == board[dest[0]][dest[1]]["color"]
    return False

#cant move through pieces (excepting knight)
#returns true if you would move through a piece
def checkCollision(board, source, dest):
    xDelta = 0 
    if (dest[0]-source[0]) > 0:
        xDelta = 1
    elif (dest[0]-source[0]) < 0:
        xDelta = -1
    yDelta = 0 
    if (dest[1]-source[1]) > 0:
        yDelta = 1
    elif (dest[1]-source[1]) < 0:
        yDelta = -1
    loc = (source[0] + xDelta, source[1] + yDelta)
    while loc != dest:
        if board[loc[0]][loc[1]]["piece"] != "blank":
            return True #found a piece collision
        loc = (loc[0] + xDelta, loc[1] + yDelta)
    return False

def validKnightMove(source, dest):
    diff0 = abs(source[0] - dest[0])
    diff1 = abs(source[1] - dest[1])
    if (diff0==2 and diff1==1) or (diff0==1 and diff1==2):
        return True
    return False 

def validPawnMove(board, source, dest, color):
    global doubleMove, enPassantCapture
    if color == "white":
        forward = 1
    else:
        forward=-1
    #no horizontal movement
    if source[0] == dest[0]:
        #move forward 1
        if source[1]+forward == dest[1]:
            return board[dest[0]][dest[1]]["piece"] == "blank"
        #move forward 2
        if not board[source[0]][source[1]]["moved"]:
            if source[1]+2*forward == dest[1]:
                doubleMove=True
                return True
    elif (source[0] == dest[0]+1 or source[0] == dest[0]-1) and source[1]+forward == dest[1]:
        #take diagonally
        if board[dest[0]][dest[1]]["piece"] != "blank" and color != board[dest[0]][dest[1]]["color"]:
            return True 
        #en-passant
        if board[dest[0]][dest[1]]["piece"] == "blank" and board[dest[0]][dest[1]-forward]["lastMoved"]==turnCounter-1:
            enPassantCapture = (dest[0],dest[1]-forward)
            return True
    return False      
    
def validRookMove(source, dest):
    if source[0] == dest[0] or source[1] == dest[1]:
        return True
    return False

def validBishopMove(source, dest):
    diff0 = abs(source[0] - dest[0])
    diff1 = abs(source[1] - dest[1])
    if diff0 == diff1:
        return True
    return False

def validQueenMove(source, dest):
    return validRookMove(source, dest) or validBishopMove(source, dest)

def validKingMove(board, source, dest, color):
    global castling
    if abs(dest[0]-source[0]) <= 1 and abs(dest[1]-source[1]) <= 1:
        return True
    elif board[source[0]][source[1]]["moved"] == False:
        if dest == (6,source[1]): #kingside
            #rook is there and hasn't been moved
            if board[7][source[1]]["piece"] == "rook" and not board[7][source[1]]["moved"]:
                #spots in between are not in check
                testBoard = copy.deepcopy(board)
                testBoard[5][source[1]] = testBoard[4][source[1]]
                testBoard[4][source[1]] = {"piece":"blank"}
                if not inCheck(testBoard, color):
                    print "approved the castling!"
                    castling = True
                    return True
        elif dest == (2,source[1]): #queenside
            #rook is there and hasn't been moved
            if board[0][source[1]]["piece"] == "rook" and not board[0][source[1]]["moved"]:
                #spots in between are not in check
                testBoard = copy.deepcopy(board)
                testBoard[3][source[1]] = testBoard[4][source[1]]
                testBoard[4][source[1]] = {"piece":"blank"}
                if not inCheck(testBoard, color):
                    castling = True
                    return True
    return False

def findKing(board, color):
    for x in range(8):
        for y in range(8):
            if board[x][y]["piece"] == "king" and board[x][y]["color"] == color:
                return (x, y)

def inCheck(board, color):
    kingLoc = findKing(board, color)
    otherColor = "black" if color == "white" else "white"
    for x in range(8):
        for y in range(8):
            if board[x][y]["piece"] != "blank" and board[x][y]["color"] == otherColor:
                if legalMove(board, (x,y), kingLoc, False):
                    return True
    return False

def calculateProposedBoard(source, dest):
    global doubleMove, enPassantCapture, castling
    proposedBoard = copy.deepcopy(board)
    if doubleMove:
        print "double move handler"
        proposedBoard[source[0]][source[1]]["lastMoved"] = turnCounter #update this for a pawn so it can be taken in en passant
        doubleMove = False
    elif enPassantCapture:
        print "en passant handler"
        proposedBoard[enPassantCapture[0]][enPassantCapture[1]] = {"piece": "blank"}
        enPassantCapture = False
    elif castling:
        print "handling castling special case"

        #queenside
        if dest[0]<source[0]:
            proposedBoard[dest[0]+1][dest[1]] = proposedBoard[0][dest[1]]
            proposedBoard[0][dest[1]] = {"piece": "blank"}
        #kingside
        else:
            print "kingside"
            print (dest[1]-1, dest[1])
            proposedBoard[dest[0]-1][dest[1]] = proposedBoard[7][dest[1]]
            proposedBoard[7][dest[1]] = {"piece": "blank"}
        castling = False

        

        
    proposedBoard[dest[0]][dest[1]] = proposedBoard[source[0]][source[1]]
    proposedBoard[dest[0]][dest[1]]["moved"] = True
    proposedBoard[source[0]][source[1]] = {"piece": "blank"}
    return proposedBoard

#TODO implement rules for piece movement
def legalMove(board, source, dest, realMove):
    if checkOwnPiece(board, source, dest):
        return False
    pieceType = board[source[0]][source[1]]["piece"]
    color = board[source[0]][source[1]]["color"]
    if pieceType == "knight":
        if not validKnightMove(source, dest):
            return False
    else:
        if pieceType == "pawn":
            if not validPawnMove(board, source, dest, color):
                return False
        elif pieceType == "rook":
            if not validRookMove(source, dest):
                return False
        elif pieceType == "bishop":
            if not validBishopMove(source, dest):
                return False
        elif pieceType == "queen":
            if not validQueenMove(source, dest):
                return False
        elif pieceType == "king":
            if not validKingMove(board, source, dest, color):
                return False
        if checkCollision(board, source, dest):
            return False
    proposedBoard = calculateProposedBoard(source, dest)
    if realMove and inCheck(proposedBoard, color):
        return False
    return proposedBoard



#check if a piece should be moved based on a click
def movePiece(source, dest):
    global selected, turnCounter, board
    if board[source[0]][source[1]]["piece"] == "blank":
        selected = dest
    elif board[source[0]][source[1]]["color"] == "white" and turnCounter%2==1 or board[source[0]][source[1]]["color"] == "black" and turnCounter%2==0:
        return
    else:
        ret = legalMove(board, source, dest, True)
        if ret:
            board = ret
            selected = None
            turnCounter += 1
    doubleMove = False
    enPassantCapture = False

    return

#translates pixel in mouse event to board coordinate
def translatePixel(pos):
    x = (pos[0]-207) / 48
    y = 7 - (pos[1]-207) / 48
    return (x,y)


# def output(x, y, message):
#     font = GLUT_BITMAP_HELVETICA_10
#     glBegin()
#     glColor3f(1, 1, 1)
#     glRasterPos2f(x, y)
#     len = strlen(string)
#     for character in message:
#         glutBitmapCharacter(font, character)
#     glEnd()

def getPiece(pos):
    return board[pos[0]][pos[1]]

def setPiece(pos, piece):
    board[pos[0]][pos[1]] = piece

def updateSelected(newPos):
    global player
    if tmp[0] > 7 or tmp[1] > 7:
        pass #outside of the board
    elif selected == tmp:
        selected = None
    elif selected == None:
        if getPiece(pos)["color"] == player:
            selected = tmp
    else:
        movePiece(selected, tmp)

if __name__ == "__main__":
    initBoard()
    pygame.init()
    display = (800,800)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0,0.0, -5)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                tmp = translatePixel(pos)
                updateSelected(tmp)

                
        glClear(GL_COLOR_BUFFER_BIT)
        drawBoard()
        pygame.display.flip()
        pygame.time.wait(10)