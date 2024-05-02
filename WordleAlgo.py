import random
import pygame

WORDS=[]
with open("allenglish.txt") as file:
    for line in file:
        WORDS.append((line.strip().upper()))
#GATOR
#RAZOR
def PLAY(NEWINFO):#SOARE
    if len(WORDS)>1:
        LETTERS_IN_WORD=set()
        for position in range(5):
            WORDS_TO_REMOVE=set()
            # letter=input(f"letter in position{position}")
            letter=NEWINFO[position]
            color=det_color(NEWINFO.upper(),position)
            # print(f"{letter},{color[1]}")
            for word in WORDS:
                if color[1] == 'g':
                    if word[position]!=letter:
                        WORDS_TO_REMOVE.add(word)
                    LETTERS_IN_WORD.add(letter)
                    
                elif color[1] == 'y':
                    if letter not in word:
                        WORDS_TO_REMOVE.add(word)
                    elif word[position]==letter:
                        WORDS_TO_REMOVE.add(word)
                  ##SLIM SKILL
                    LETTERS_IN_WORD.add(letter)
                elif color[1] == 'b':
                    for x in range(position+1,5):
                        result=det_color(NEWINFO,x)
                        if letter==NEWINFO[x]:
                            if result[1]=='g' or result[1]=='y':
                                LETTERS_IN_WORD.add(letter)
                        # if letter==NEWINFO[x] and (det_color(NEWINFO,x)=='g' or det_color(NEWINFO,x)=='y'):
                        #     LETTERS_IN_WORD.add(letter)
                                break

                    if letter in word:
                        # if letter in ANSWER:
                        #     LETTERS_IN_WORD.append(letter)
                        if letter not in LETTERS_IN_WORD:
                            WORDS_TO_REMOVE.add(word)
                        if word[position]==letter:
                            WORDS_TO_REMOVE.add(word)

            # print(LETTERS_IN_WORD)
            for word in WORDS_TO_REMOVE:
                WORDS.remove(word)
        print(ANSWER)
        print(INPUT)
        print((WORDS))
        # return random.choice(WORDS)
    return WORDS[0]
    
     
        # TRY=if len(WORDS)>1:random.choice(WORDS)
        # return TRY
    
def load_dict(file_name):
    file=open(file_name)
    words=file.readlines()
    file.close()
    return [word[:5].upper() for word in words]  # so we print first 5 letter w/o n line

DICT_GUESSING=load_dict("allenglish.txt")
ANSWER=random.choice(DICT_GUESSING)
# ANSWER="SKILL"
### Dimensions
WIDTH = 600
HEIGHT=650
MARGIN=10 #between squares
T_B_L_R_MARGIN=100
T_MARGIN=100
B_MARGIN=100
LR_MARGIN=100

GREY= (70,70,80)
GREEN=(6,214,160)
YELLOW=(255,209,102)

ALPHAPET="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
GUESSES=[]
UNGUESSES=ALPHAPET #initially
GAME_OVER= False

pygame.init()
pygame.font.init()
pygame.display.set_caption("Wordle")

SQ_SIZE=(WIDTH-4*MARGIN-2*LR_MARGIN)//5
FONT=pygame.font.SysFont("free sans bold", SQ_SIZE)
FONT_SMALL=pygame.font.SysFont("free sans bold", SQ_SIZE//2)#####################

def det_unguessed(guesses): #guesses is list of words
    guessed_letters="".join(guesses)
    #####print(guesses)
    unguessed_letters=""
    for letter in ALPHAPET:
        if letter not in guessed_letters:
            unguessed_letters+=letter
    return unguessed_letters

def det_color(guess,j): #jth letter being checked
    letter=guess[j]
    if letter == ANSWER[j]:
        GREEN_RESULT=[GREEN,'g']
        return GREEN_RESULT
    elif letter in ANSWER:
        n_target=ANSWER.count(letter)
        n_correct= 0 #already green
        n_occurrence=0
        YELLOW_RESULT=[YELLOW,'y']
        for i in range(5):
            if guess[i]==letter:
                if i<=j:
                    n_occurrence+=1
                if letter==ANSWER[i]:
                    n_correct+=1
        if n_target-n_correct-n_occurrence>=0:
            return YELLOW_RESULT
    GREY_RESULT=[GREY,'b']    
    return GREY_RESULT


#create screen
screen = pygame.display.set_mode((WIDTH,HEIGHT))

INPUT="SOARE"
animating = True
while animating:
    #bg
    screen.fill("white")
    #det_unguessed(GUESSES)  ## to check it prints all guessed words
    # draw unguessed letters
    letters=FONT_SMALL.render(UNGUESSES,False,GREY)
    surface=letters.get_rect(center=(WIDTH//2,T_MARGIN//2))
    screen.blit(letters,surface)
    #draw guesses
    y=T_MARGIN
    for i in range(6):
        x=LR_MARGIN
        GREEN_COUNT=0
        for j in range(5):
            #square
            square=pygame.Rect(x,y,SQ_SIZE,SQ_SIZE)
            pygame.draw.rect(screen,GREY,square,width=2, border_radius=3)

            #guesses letters
            if i <len(GUESSES):
                color=det_color(GUESSES[i],j)
                pygame.draw.rect(screen,color[0],square,border_radius=3)
                if color[1]=='g':GREEN_COUNT+=1
                letter=FONT.render(GUESSES[i][j],False,(255,255,255))
                surface=letter.get_rect(center=(x+SQ_SIZE//2,y+SQ_SIZE//2))#in center
                screen.blit(letter,surface)
                
            # user text input, next guess ## to print letter by letter while typing
            if i == len(GUESSES) and j<len(INPUT):
                letter=FONT.render(INPUT[j],False,GREY)
                surface=letter.get_rect(center=(x+SQ_SIZE//2,y+SQ_SIZE//2))
                screen.blit(letter,surface)

            x+=SQ_SIZE+MARGIN
        if GREEN_COUNT==5:INPUT=""
        y+=SQ_SIZE+MARGIN
    # print(GREEN_COUNT)

    #show correct answer if game is over
    if len(GUESSES)==6 and GUESSES[5]!=ANSWER:
        GAME_OVER=True
        letters=FONT.render(ANSWER,False,GREY)
        surface=letters.get_rect(center=(WIDTH//2,HEIGHT-B_MARGIN//2+MARGIN))
        screen.blit(letters,surface)

#update screen
    pygame.display.flip()
#track user interaction
    for event in pygame.event.get():
        #close
        if event.type == pygame.QUIT:#############################################
            animating = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                animating = False
            #backspace to delete letter
            if event.key==pygame.K_BACKSPACE:
                if len(INPUT)>0:
                    INPUT=INPUT[:len(INPUT)-1]
            #return key to submit guess
            elif event.key == pygame.K_RETURN:
                if len(INPUT)==5:
                    GUESSES.append(INPUT)
                    INPUT=PLAY(INPUT)
                    UNGUESSES=det_unguessed(GUESSES)    #to modify the unguessed list of letters up there
                    GAME_OVER=True if INPUT == ANSWER else False
                    # INPUT="" #reset input
            #restart
            elif event.key==pygame.K_SPACE:
                GAME_OVER=False
                ANSWER=random.choice(DICT_GUESSING)
                GUESSES=[]
                UNGUESSES=ALPHAPET
                INPUT="SOARE"
                WORDS=[]
                with open("allenglish.txt") as file:
                    for line in file:
                        WORDS.append((line.strip().upper())[:5])
        
            
            elif len(INPUT) <5 and not GAME_OVER:
                INPUT=INPUT+event.unicode.upper()
                # print(INPUT)
            # elif GAME_OVER:
            #     INPUT=""
                # print(INPUT)

