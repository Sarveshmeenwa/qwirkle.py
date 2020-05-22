#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import termcolor
from termcolor import colored
import pprint
import random

scores=[0,0,0]

FORMES = {
    "croix": "X",
    "losange": "♦",
    "cercle": "●",
    "carré": "■",
    "étoile": "☼",
    "trèfle": "♣"
}

COULEURS = {
    "rouge": "red",
    "violet": "magenta",
    "bleu": "blue",
    "gris": "white",  # pas d'orange en console
    "vert": "green",
    "jaune": "yellow",
}
"""
dico_example_2 = {(0, 0): ('losange', 'violet'),
                      (1, 0): ('croix', 'violet'),
                      (2, 0): ('cercle', 'violet'),
                      (-1, 0): ('étoile', 'violet'),
                      (2, -1): ('cercle', 'gris'),
                      (0, 1): ('losange', 'vert'),
                      (-1, 1): ('étoile', 'vert'),
                      (0, -1): ('losange', 'bleu'),
                      (0, 2): ('losange', 'jaune'),
                      (-1, 2): ('étoile', 'jaune'),
                      (-2, -2): ('croix', 'bleu')}
"""                   
dico_example_2 = {(0, 0): ('losange', 'violet')
               }
NOMBRE_DE_JOUEURS = 3
NOMBRE_DE_CARTE_PAR_MAIN = 6

NOMBRE_DE_TUILES_IDENTIQUES = 3

COULEUR = "couleur"
FORME = "forme"


def render_hand(hand, sep="\t"):
    output = []
    for carte in hand:
        try:
            forme = FORMES[carte[0]]
            couleur = COULEURS[carte[1]]
            output.append(termcolor.colored(forme, couleur))
        except TypeError:
            output.append(termcolor.colored(" ", None))
    return sep.join(output)


def extract_bigger_categories(categories):
    maximum = categories[0]
    for i in range(len(categories)):
        if categories[i][1] > maximum[1]:
            maximum = categories[i]
    return maximum


def get_bigger_set_of_cards(hand):
    color_sets = {color: set() for color in COULEURS}
    formes_sets = {forme: set() for forme in FORMES}

    for forme, couleur in hand:
        color_sets[couleur].add((forme, couleur))
        formes_sets[forme].add((forme, couleur))

    # à partir du dictionnaire color_sets -> une liste de tuples [(couleur, nombre de cartes de cette couleur), ...]
    colors_count = []
    for color in color_sets:
        tuple_temp = (color, len(color_sets[color]))
        colors_count.append(tuple_temp)
    formes_count = []
    for forme in formes_sets:
        tuple_temp = (forme, len(formes_sets[forme]))
        formes_count.append(tuple_temp)
    most_found_color = extract_bigger_categories(colors_count)
    most_found_forme = extract_bigger_categories(formes_count)

    if most_found_color[1] >= most_found_forme[1]:
        return COULEUR, most_found_color
    else:
        return FORME, most_found_forme



def get_first_player(joueurs: dict):
    # for joueur in joueurs:
    #     print(joueur, "\t", render_hand(joueurs[joueur]))
    #     print(get_bigger_set_of_cards(joueurs[joueur]))
    joueurs_sets = {}
    for joueur in joueurs:
        joueurs_sets[joueur] = get_bigger_set_of_cards(joueurs[joueur])
    #print(joueurs_sets)----> to see everybody maximum set
    #print(joueurs_sets)
    maximum = (list(joueurs_sets.keys())[0], joueurs_sets[list(joueurs_sets.keys())[0]])
    for joueur in joueurs_sets:
        number = joueurs_sets[joueur][1][1]
        if number > maximum[1][1][1]:
            maximum = (joueur, joueurs_sets[joueur])
    
    return maximum

#To check horizontal/vertical line is not interupted
def adjacent_checks(position,dico_example_2,attribute):
    scale_x_n=(0,-1)
    scale_y_p=(-1,0)
    scale_x_p=(0,1)
    scale_y_n=(1,0)
    result_1=tuple(p+q for p, q in zip(position,scale_x_n ))
    result_2=tuple(p+q for p, q in zip(position,scale_y_p ))
    result_3=tuple(p+q for p, q in zip(position,scale_x_p ))
    result_4=tuple(p+q for p, q in zip(position,scale_y_n ))
    check_adj=False
    for key in dico_example_2:
        if (key==result_1) or (key==result_2) or (key==result_3) or (key==result_4):
            check_adj=True
            break
        else:
            check_adj=False
    
    return check_adj
  

#function to check whether each row/column has same shapes or colours, validation check
#Check forward in x direction
def is_shape_col_valid_x(x,y,attribute,max_adj_col,max_adj_line):
    valid=True
    shape=attribute[0]
    colour=attribute[1]
    while matrix_output[y][x+1]!= None:
        temp_att=matrix_output[y][x+1]
        temp_form=temp_att[0]
        temp_colour=temp_att[1] 
        if (shape==temp_form) or (colour==temp_colour):
            valid=True
        else:
            valid=False
            break

        x=x+1
        if x==max_adj_col:
            break
                
    return valid

#check backwards in x direction
def is_x_shape_colour_valid(x,y,attribute):
    valid=True
    shape=attribute[0]
    colour=attribute[1]   
    while matrix_output[y][x-1] != None:
        temp_att=matrix_output[y][x-1]
        temp_form=temp_att[0]
        temp_colour=temp_att[1] 
        if (shape==temp_form) or (colour==temp_colour):
            valid=True
        else:
            valid=False
            break
        x=x-1
        if x==0:
            break

    return valid

#check in upwards direction
def is_shape_col_valid_y(x,y,attribute):
    
    valid=True
    shape=attribute[0]
    colour=attribute[1]

    while matrix_output[y-1][x] != None:
        temp_att=matrix_output[y-1][x]
        temp_form=temp_att[0]
        temp_colour=temp_att[1] 
        if (shape==temp_form) or (colour==temp_colour):
            valid=True
        else:
            valid=False
            break
        y=y-1
        if y== 0:
            break
            
    return valid

#check in downwards direction
def y_is_shape_col_valid(x,y,attribute,max_adj_line):
    valid=True
    shape=attribute[0]
    colour=attribute[1]
    while matrix_output[y+1][x]!= None:
        temp_att=matrix_output[y+1][x]
        temp_form=temp_att[0]
        temp_colour=temp_att[1]
        if (shape==temp_form) or (colour==temp_colour):
            valid=True
        else:
            valid=False
            break
        
        y+=1
        if y==max_adj_line:
            break  
     
    return valid    

#Validation whether in forward direction, there is no "doubles"
            
def for_x(x,y,attribute,max_adj_col,max_adj_line):
    check_for=True    
    while matrix_output[y][x+1]!= None:
        if matrix_output[y][x+1]==attribute:
            check_for=False
            break
        else:
            check_for=True

        x=x+1
        if x==max_adj_col:
            break
                
    return check_for

#Validation check whether there is no doubles in backwards direction
def back_x(x,y,attribute,max_adj_line):
    check_back=True       
    while matrix_output[y][x-1] != None:

        if matrix_output[y][x-1]== attribute:
            check_back= False
            break
        else:
            check_back=True
        x=x-1
        if x==0:
            break

    return check_back

#Validation check whether there is no doubles in upwards direction
def up_y(x,y,attribute, max_adj_col):
    check_up=True
    while matrix_output[y-1][x] != None:
        if matrix_output[y-1][x]== attribute:
            check_up= False
            break
        else:
            check_up=True
        y=y-1
        if y== 0:
            break
            
    return check_up


#Validation check whether there is no doubles in downwards direction
def down_y(x,y,attribute,max_adj_line,max_adj_col):
    check_down=True
    while matrix_output[y+1][x]!= None:
        if matrix_output[y+1][x]==attribute:
            check_down=False
            break
        else:
            check_down=True
        y+=1
        if y==max_adj_line:
            break  
            
    return check_down


def score_fx(x,y,attribute,max_adj_col,max_adj_line):
    
    if matrix_output[y][x+1] != None:
        score=1
    else:
        score=0
        
    qwirkle_c=0   
    while matrix_output[y][x+1]!= None:
        if matrix_output[y][x+1] != None:
            score+=1
        if score==6:
            score+=6
        x=x+1
        if x==max_adj_col:
            break
            
    score=score+(qwirkle_c*6)
    return score


def score_bx(x,y,attribute,max_adj_line):
    qwirkle_c=0
    if matrix_output[y][x-1] != None:
        score=1
    else:
        score=0
          
    while matrix_output[y][x-1] != None:

        if matrix_output[y][x-1] != None:
            score+=1
        x=x-1
        if score==6:
            qwirkle_c +=1

        if x==0:
            break  
                    
    score=score+(qwirkle_c*6)                
    return score

def score_u_y(x,y,attribute, max_adj_col):
    
    qwirkle_c=0
    if matrix_output[y-1][x] != None:
        score=1
    else:
        score=0

    while matrix_output[y-1][x] != None:
        if matrix_output[y-1][x]!= None:
            score+=1
        if score==6:
            qwirkle_c+=1
        y=y-1
        if y== 0:
            break

    score =score+ (qwirkle_c*6)
    return score


def score_d_y(x,y,attribute,max_adj_line,max_adj_col):
    qc=0
    if matrix_output[y+1][x] != None:
        score=1
    else:
        score=0

    while matrix_output[y+1][x]!= None:
        if matrix_output[y+1][x] !=None:
            score+=1
        if score==6:
            qc+=1
        y+=1
        if y==max_adj_line:
            break
                    
    score=score+(qc*6)         
    return score



def score(dico_example_2,position,attribute):
    list_of_numline = []
    list_of_numcol = []
    for key in dico_example_2:
        list_of_numline.append(key[0])
        list_of_numcol.append(key[1])

    min_line = min(list_of_numline)
    max_line = max(list_of_numline)
    min_col = min(list_of_numcol)
    max_col = max(list_of_numcol)
    y_min=abs(min_line)
    x_min=abs(min_col)
    max_adj_col=x_min+max_col
    min_adj_col=0
    max_adj_line=y_min+max_line
    min_adj_line=0
    
    position_temp=[]
    position_temp.append(y_min+position[0])
    position_temp.append(x_min+position[1])
    pos_tuple=(position_temp[0],position_temp[1])

    x=pos_tuple[1]
    y=pos_tuple[0]
    s1=0
    s2=0
    s3=0
    s4=0
     
    
    if x<0 and y==0:
        s1=score_fx(x,y,attribute,max_adj_col,max_adj_line)
    if y<0 and x==0:
        s4= score_d_y(x,y,attribute,max_adj_line,max_adj_col)

    if x>max_adj_col and y==0:
        s2=score_bx(x,y,attribute,max_adj_line)
    
   
    if y<0 and x==max_adj_col:
        s4=score_d_y(x,y,attribute,max_adj_line,max_adj_col)
        
    if x<0 and y==max_adj_line:
        s1=score_fx(x,y,attribute,max_adj_col,max_adj_line)
        
    
    if y>max_adj_line and x==0:
        s3=score_u_y(x,y,attribute, max_adj_col)
       
        
    if y>max_adj_line and x==max_adj_col:
        s3=score_u_y(x,y,attribute, max_adj_col)
        
    if x>max_adj_col and y==max_adj_line:
        s2=score_bx(x,y,attribute,max_adj_line)
        
    if x<0 and (y > 0 and y <max_adj_line) :
        s1=score_fx(x,y,attribute,max_adj_col,max_adj_line)
        
    if y<0 and (x>0 and x<max_adj_col ):
        s4=score_d_y(x,y,attribute,max_adj_line,max_adj_col)
        
    if x>max_adj_col and (y> 0 and y < max_adj_line ):
        s2=score_bx(x,y,attribute,max_adj_line)
        
    if y>max_adj_line and (x >0 and x <max_adj_col ):
        s3=score_u_y(x,y,attribute, max_adj_col)
        
        
    if x==0 and y==0:
        s1=score_fx(x,y,attribute,max_adj_col,max_adj_line)
        s4=score_d_y(x,y,attribute,max_adj_line,max_adj_col)
        
    if x==max_adj_col and y==0:
        s2=score_bx(x,y,attribute,max_adj_line)
        s4=score_d_y(x,y,attribute,max_adj_line,max_adj_col)
        
    if y==max_adj_line and x==0:
        s1=score_fx(x,y,attribute,max_adj_col,max_adj_line)
        s3=score_u_y(x,y,attribute, max_adj_col)
        
    
    if x==max_adj_col and y==max_adj_line:
        s2=score_bx(x,y,attribute,max_adj_line)
        s3=score_u_y(x,y,attribute, max_adj_col)

    if y==0 and (x > 0 and x < max_adj_col ):
        s2=score_bx(x,y,attribute,max_adj_line)
        s1=score_fx(x,y,attribute,max_adj_col,max_adj_line)
        s4=score_d_y(x,y,attribute,max_adj_line,max_adj_col)
        if s2 !=0 and s1 !=0 and s4 !=0:
            s2=s2-1
        
    if x==0 and (y >0 and y <max_adj_line):
        s1=score_fx(x,y,attribute,max_adj_col,max_adj_line)
        s3=score_u_y(x,y,attribute, max_adj_col)
        s4=score_d_y(x,y,attribute,max_adj_line,max_adj_col)
        if s3 !=0 and s1 !=0 and s4 !=0:
            s3=s3-1
    if y== max_adj_line and (x >0 and x < max_adj_col):
        s2=score_bx(x,y,attribute,max_adj_line)
        s1=score_fx(x,y,attribute,max_adj_col,max_adj_line)
        s3=score_u_y(x,y,attribute, max_adj_col)
        if s3 !=0 and s1 !=0 and s2 !=0:
            s3=s3-1
        
       
        
    if x== max_adj_col and (y >0 and y < max_adj_line):
        s2=score_bx(x,y,attribute,max_adj_line)
        s3=score_u_y(x,y,attribute, max_adj_col)
        s4=score_d_y(x,y,attribute,max_adj_line,max_adj_col)
        if s3 !=0 and s2 !=0 and s4 !=0:
            s3=s3-1
       
    if (x>=1 and x<= max_adj_col-1) and (y>=1 and y<=max_adj_line-1)  :
        s2=score_bx(x,y,attribute,max_adj_line)
        s1=score_fx(x,y,attribute,max_adj_col,max_adj_line)
        s3=score_u_y(x,y,attribute, max_adj_col)
        s4=score_d_y(x,y,attribute,max_adj_line,max_adj_col)
   
    scores=s1+s2+s3+s4
    return scores

def get_key(val): 
    for key, value in dico_example_2.items(): 
        if val == value: 
            return key

#Check whether there is no doubles in col/row
def is_row_col_valid(dico_example_2,position,attribute):
    list_of_numline = []
    list_of_numcol = []
    for key in dico_example_2:
        list_of_numline.append(key[0])
        list_of_numcol.append(key[1])

    min_line = min(list_of_numline)
    max_line = max(list_of_numline)
    min_col = min(list_of_numcol)
    max_col = max(list_of_numcol)
    y_min=abs(min_line)
    x_min=abs(min_col)
    max_adj_col=x_min+max_col
    min_adj_col=0
    max_adj_line=y_min+max_line
    min_adj_line=0
    
    position_temp=[]
    position_temp.append(y_min+position[0])
    position_temp.append(x_min+position[1])
    pos_tuple=(position_temp[0],position_temp[1])

    x=pos_tuple[1]
    y=pos_tuple[0]

    
    c1=True
    c2=True
    c3=True
    c4=True
    sc1=True
    sc2=True
    sc3=True
    sc4=True
    
    
    
    if x<0 and y==0:
        c1=for_x(x,y,attribute,max_adj_col,max_adj_line)
        sc1=is_shape_col_valid_x(x,y,attribute,max_adj_col,max_adj_line)

    if y<0 and x==0:
        c4=down_y(x,y,attribute,max_adj_line,max_adj_col)
        sc4=y_is_shape_col_valid(x,y,attribute,max_adj_line)

    if x>max_adj_col and y==0:
        c2=back_x(x,y,attribute,max_adj_line)
        sc2=is_x_shape_colour_valid(x,y,attribute)
   
    if y<0 and x==max_adj_col:
        c4=down_y(x,y,attribute,max_adj_line,max_adj_col)
        sc4=y_is_shape_col_valid(x,y,attribute,max_adj_line)

        
    if x<0 and y==max_adj_line:
        c1=for_x(x,y,attribute,max_adj_col,max_adj_line)
        sc1=is_shape_col_valid_x(x,y,attribute,max_adj_col,max_adj_line)
    
    if y>max_adj_line and x==0:
        c3=up_y(x,y,attribute, max_adj_col)
        sc3=is_shape_col_valid_y(x,y,attribute)
        
    if y>max_adj_line and x==max_adj_col:
        c3=up_y(x,y,attribute, max_adj_col)
        sc3=is_shape_col_valid_y(x,y,attribute)
    
    if x>max_adj_col and y==max_adj_line:
        c2=back_x(x,y,attribute,max_adj_line)
        sc2=is_x_shape_colour_valid(x,y,attribute)
        
    if x<0 and (y > 0 and y <max_adj_line) :
        c1=for_x(x,y,attribute,max_adj_col,max_adj_line)
        sc1=is_shape_col_valid_x(x,y,attribute,max_adj_col,max_adj_line)
        
    if y<0 and (x>0 and x<max_adj_col ):
        c4=down_y(x,y,attribute,max_adj_line,max_adj_col)
        sc4=y_is_shape_col_valid(x,y,attribute,max_adj_line)

        
    if x>max_adj_col and (y> 0 and y < max_adj_line ):
        c2=back_x(x,y,attribute,max_adj_line)
        sc2=is_x_shape_colour_valid(x,y,attribute)
    
    if y>max_adj_line and (x >0 and x <max_adj_col ):
        c3=up_y(x,y,attribute, max_adj_col)
        sc3=is_shape_col_valid_y(x,y,attribute)
        
    if x==0 and y==0:
        c1=for_x(x,y,attribute,max_adj_col,max_adj_line)
        c4=down_y(x,y,attribute,max_adj_line,max_adj_col)
        sc4=y_is_shape_col_valid(x,y,attribute,max_adj_line)
        sc1=is_shape_col_valid_x(x,y,attribute,max_adj_col,max_adj_line)

        
    if x==max_adj_col and y==0:
        c4=down_y(x,y,attribute,max_adj_line,max_adj_col)
        c2=back_x(x,y,attribute,max_adj_line)
        sc4=y_is_shape_col_valid(x,y,attribute,max_adj_line)
        sc2=is_x_shape_colour_valid(x,y,attribute)
  
    if y==max_adj_line and x==0:
        c1=for_x(x,y,attribute,max_adj_col,max_adj_line)
        c3=up_y(x,y,attribute, max_adj_col)
        sc3=is_shape_col_valid_y(x,y,attribute)
        sc1=is_shape_col_valid_x(x,y,attribute,max_adj_col,max_adj_line)
    
    if x==max_adj_col and y==max_adj_line:
        c2=back_x(x,y,attribute,max_adj_line)
        c3=up_y(x,y,attribute, max_adj_col)
        sc3=is_shape_col_valid_y(x,y,attribute)
        sc2=is_x_shape_colour_valid(x,y,attribute)
        
    if y==0 and (x > 0 and x < max_adj_col ):
        c1=for_x(x,y,attribute,max_adj_col,max_adj_line)
        c2=back_x(x,y,attribute,max_adj_line)
        c4=down_y(x,y,attribute,max_adj_line,max_adj_col)
        sc4=y_is_shape_col_valid(x,y,attribute,max_adj_line)
        sc2=is_x_shape_colour_valid(x,y,attribute)
        sc1=is_shape_col_valid_x(x,y,attribute,max_adj_col,max_adj_line)

        
    if x==0 and (y >0 and y <max_adj_line):
        c1=for_x(x,y,attribute,max_adj_col,max_adj_line)
        c3=up_y(x,y,attribute, max_adj_col)
        c4=down_y(x,y,attribute,max_adj_line,max_adj_col)
        sc4=y_is_shape_col_valid(x,y,attribute,max_adj_line)
        sc3=is_shape_col_valid_y(x,y,attribute)
        sc1=is_shape_col_valid_x(x,y,attribute,max_adj_col,max_adj_line)
        
    if y== max_adj_line and (x >0 and x < max_adj_col):
        c1=for_x(x,y,attribute,max_adj_col,max_adj_line)
        c2=back_x(x,y,attribute,max_adj_line)
        c3=up_y(x,y,attribute, max_adj_col)
        sc3=is_shape_col_valid_y(x,y,attribute)
        sc2=is_x_shape_colour_valid(x,y,attribute)
        sc1=is_shape_col_valid_x(x,y,attribute,max_adj_col,max_adj_line)
    if x== max_adj_col and (y >0 and y < max_adj_line):
        c2=back_x(x,y,attribute,max_adj_line)
        c3=up_y(x,y,attribute, max_adj_col)
        c4=down_y(x,y,attribute,max_adj_line,max_adj_col)
        sc4=y_is_shape_col_valid(x,y,attribute,max_adj_line)
        sc3=is_shape_col_valid_y(x,y,attribute)
        sc2=is_x_shape_colour_valid(x,y,attribute)

       
    if (x>=1 and x<= max_adj_col-1) and (y>=1 and y<=max_adj_line-1)  :
        c1=for_x(x,y,attribute,max_adj_col,max_adj_line)
        c2=back_x(x,y,attribute,max_adj_line)
        c3=up_y(x,y,attribute, max_adj_col)
        c4=down_y(x,y,attribute,max_adj_line,max_adj_col)
        sc4=y_is_shape_col_valid(x,y,attribute,max_adj_line)
        sc3=is_shape_col_valid_y(x,y,attribute)
        sc2=is_x_shape_colour_valid(x,y,attribute)
        sc1=is_shape_col_valid_x(x,y,attribute,max_adj_col,max_adj_line)
    
    if c1==False or c2==False or c3==False or c4==False or sc1 == False or sc2 == False or sc3 == False or sc4==False :
        return False
    else:
        return True
        
    
    

    
            
def pos_taken(position,dico_example_2):
    if position in dico_example_2:
        return True
    else:
        return False
        
    
def refill(joueurs,player_num):
    while len(paquet)>0 and len(joueurs[player_num])<6:
        joueurs[player_num].append(paquet.pop(0))
        


        
            
def main():
    # Une tuile = un tuple <(forme, couleur)>
    # Préparer le jeu (108 cartes = 6 formes * 6 couleurs * 3)
    global paquet
    paquet = []
    for i in range(NOMBRE_DE_TUILES_IDENTIQUES):
        for forme in FORMES:
            for couleur in COULEURS:
                tuile = (forme, couleur)
                paquet.append(tuile)
    random.shuffle(paquet)
    random.shuffle(paquet)
    random.shuffle(paquet)

    # Piocher 6 cartes par personne
    joueurs = {}
    for i in range(NOMBRE_DE_JOUEURS):
        joueurs[i] = []
        for j in range(NOMBRE_DE_CARTE_PAR_MAIN):
            joueurs[i].append(paquet.pop(0))

    #for joueur in joueurs:
     #   print(joueur, "\t", render_hand(joueurs[joueur]))
    
    
    first_player = get_first_player(joueurs)
    print("The player n°{player_num} will play first, because he has the biggest set ({category}), "
          "with {number} {type_}.".format(player_num=first_player[0],
                                          category=first_player[1][0],
                                          number=first_player[1][1][1],
                                          type_=first_player[1][1][0]))
    

    player_num=first_player[0] 
   
        
    print("Player ",player_num," starts !")
    print("Player",player_num,"'hand :",render_hand(joueurs[player_num]))
    x=get_bigger_set_of_cards(joueurs[player_num])
    count=0
    nums_to_pop=[]
    if x[0]=='forme':
        for i in range(len(joueurs[player_num])):
            if joueurs[player_num][i][0]==x[1][0]:
                dupli=joueurs[player_num][i] in dico_example_2.values()
                if dupli == False:
                    dico_example_2[(count,0)]=joueurs[player_num][i]
                    nums_to_pop.append(i)
                    count+=1
                
        
    if x[0]=='couleur':
        for i in range(len(joueurs[player_num])):
            if joueurs[player_num][i][1]==x[1][0]:
                dupli=joueurs[player_num][i] in dico_example_2.values()
                if dupli == False:
                    dico_example_2[(count,0)]=joueurs[player_num][i]
                    nums_to_pop.append(i)
                    count+=1
                    
    for x in dico_example_2.values():
        if x in joueurs[player_num]:
            joueurs[player_num].remove(x)
    
         
    refill(joueurs,player_num)    
    render_board(dico_example_2)
    print("The score for player n° :",player_num)
    print(count)
    if player_num==NOMBRE_DE_JOUEURS-1:
        player_num=0
    else:
        player_num+=1
    fail=0
    while len(paquet)>0:
        print("Player",player_num,"'s turn")
        print("Player",player_num,"'hand :",render_hand(joueurs[player_num]))
        trade=input("Do you want to trade tiles (Y/N) ?")
        if trade=="y" or trade == "Y":
            num_tiles_to_exchange=int(input("How many tiles you want to exchange? \n"))
            for i in range(num_tiles_to_exchange):
                print("Player",player_num,"'hand :",render_hand(joueurs[player_num]))
                nums_to_pop=int(input("Which tile you want to exchange(1-6)"))-1
                paquet.append(joueurs[player_num].pop(nums_to_pop))
                random.shuffle(paquet)
                joueurs[player_num].append(paquet.pop(0))
            print("Player",player_num,"'hand :",render_hand(joueurs[player_num]))
            if player_num==NOMBRE_DE_JOUEURS-1:
                player_num=0
            else:
                player_num+=1
                 
        else:
            end_turn="N"
            print("Player",player_num,"'s turn")
            print("\n")
            render_board(dico_example_2)
            print("Player",player_num,"'hand :",render_hand(joueurs[player_num]))
            num_to_pop=int(input("Input number of the tile you want to play(1-6)"))-1
            #test_list=render_hand(joueurs[player_num]).strip().split('\t')
            attribute=joueurs[player_num].pop(num_to_pop)
            position=eval(input("Input position in tuple form i.e (row,column)/-ve row means up and -ve column means left"))


            while (pos_taken(position,dico_example_2)== True) or (adjacent_checks(position,dico_example_2,attribute) == False) or (is_row_col_valid(dico_example_2,position,attribute)==False):
                fail +=1
                joueurs[player_num].insert(num_to_pop,attribute)
                print("Player",player_num,"'hand :",render_hand(joueurs[player_num]),'\n')
                if fail >= 1:
                    end_turn=input("Invalid position,Do you want to end turn (Y/N)?")
                    if end_turn =="Y" or end_turn=="y":
                        fail=0
                        refill(joueurs,player_num)
                        if player_num==NOMBRE_DE_JOUEURS-1:
                            player_num=0

                        else:
                            player_num+=1

                        break

                    else:
                        print(" Enter tile and position again")
                        print("Player",player_num,"'s turn")
                        print("\n")
                        print("Player",player_num,"'hand :",render_hand(joueurs[player_num]))
                        num_to_pop=int(input("Input number of the tile you want to play"))-1
                        attribute=joueurs[player_num].pop(num_to_pop)
                        position=eval(input("Input position where you want the tile to be place"))


            if end_turn != "Y" or end_turn != "y":
                if len(paquet)==1:
                    scores[player_num]+=6
                scores[player_num]+=score(dico_example_2,position,attribute)
                dico_example_2[position]=attribute
                print("Player",player_num,"'hand :",render_hand(joueurs[player_num]))
                print("\n")
                render_board(dico_example_2)
                print("The score for player n° :",player_num) 
                print(scores[player_num])
                end_turn=input("Do you want to end turn (Y/N)?")
                if end_turn == "Y" or end_turn =="y":
                    refill(joueurs,player_num)
                    if player_num==NOMBRE_DE_JOUEURS-1:
                        player_num=0
                    else:
                        player_num+=1
                        

def main_2():
    NOMBRE_DE_JOUEURS = 2
    
    global paquet
    paquet = []
    for i in range(NOMBRE_DE_TUILES_IDENTIQUES):
        for forme in FORMES:
            for couleur in COULEURS:
                tuile = (forme, couleur)
                paquet.append(tuile)
    random.shuffle(paquet)
    random.shuffle(paquet)
    random.shuffle(paquet)

    # Piocher 6 cartes par personne
    joueurs = {}
    for i in range(NOMBRE_DE_JOUEURS):
        joueurs[i] = []
        for j in range(NOMBRE_DE_CARTE_PAR_MAIN):
            joueurs[i].append(paquet.pop(0))

    #for joueur in joueurs:
    #    print(joueur, "\t", render_hand(joueurs[joueur]))
    
    
    first_player = get_first_player(joueurs)
    print("The player n°{player_num} will play first, because he has the biggest set ({category}), "
          "with {number} {type_}.".format(player_num=first_player[0],
                                          category=first_player[1][0],
                                          number=first_player[1][1][1],
                                          type_=first_player[1][1][0]))
    

    player_num=first_player[0] 
    x=get_bigger_set_of_cards(joueurs[player_num])

    print(colored("AI's Turn !","red"),'\n')
    
    #attributes_ai=[]
    possible_moves=[]
    count=0
    nums_to_pop=[]
    #print(render_hand(joueurs[player_num]))
    if x[0]=='forme':
        for i in range(len(joueurs[player_num])):
            if joueurs[player_num][i][0]==x[1][0]:
                dupli=joueurs[player_num][i] in dico_example_2.values()
                if dupli == False:
                    dico_example_2[(count,0)]=joueurs[player_num][i]
                    nums_to_pop.append(i)
                    count+=1
                
        
    if x[0]=='couleur':
        for i in range(len(joueurs[player_num])):
            if joueurs[player_num][i][1]==x[1][0]:
                dupli=joueurs[player_num][i] in dico_example_2.values()
                if dupli == False:
                    dico_example_2[(count,0)]=joueurs[player_num][i]
                    nums_to_pop.append(i)
                    count+=1
                    
    for x in dico_example_2.values():
        if x in joueurs[player_num]:
            joueurs[player_num].remove(x)
    
    
        
        
    refill(joueurs,player_num)    
    
    print("\n")
    render_board(dico_example_2)
    print("The score for the A.I is",count)
    scores[player_num]+=count
    if player_num==NOMBRE_DE_JOUEURS-1:
        player_num=0

    else:
        player_num+=1
    
    fail=0   
    while len(paquet)>0:

        if player_num != first_player[0]:
            print("Player",player_num,"'s turn")
            print("Player",player_num,"'hand :",render_hand(joueurs[player_num]))
            trade=input("Do you want to trade tiles (Y/N) ?")
            if trade=="y" or trade == "Y":
                num_tiles_to_exchange=int(input("How many tiles you want to exchange? \n"))
                for i in range(num_tiles_to_exchange):
                    print("Player",player_num,"'hand :",render_hand(joueurs[player_num]))
                    nums_to_pop=int(input("Which tile you want to exchange(1-6)"))-1
                    paquet.append(joueurs[player_num].pop(nums_to_pop))
                    random.shuffle(paquet)
                    joueurs[player_num].append(paquet.pop(0))
                print("Player",player_num,"'hand :",render_hand(joueurs[player_num]))
                if player_num==NOMBRE_DE_JOUEURS-1:
                    player_num=0
                else:
                    player_num+=1

            else:
                end_turn="N"
                print("Player",player_num,"'s turn")
                render_board(dico_example_2)
                print("\n")
                print("Player",player_num,"'hand :",render_hand(joueurs[player_num]))
                num_to_pop=int(input("Input number of the tile you want to play(1-6)"))-1
                #test_list=render_hand(joueurs[player_num]).strip().split('\t')
                attribute=joueurs[player_num].pop(num_to_pop)
                position=eval(input("Input position in tuple form i.e (row,column)/-ve row means up and -ve column means left"))


                while (pos_taken(position,dico_example_2)== True) or (adjacent_checks(position,dico_example_2,attribute) == False) or (is_row_col_valid(dico_example_2,position,attribute)==False):
                    fail +=1
                    joueurs[player_num].insert(num_to_pop,attribute)
                    print("Player",player_num,"'hand :",render_hand(joueurs[player_num]),'\n')
                    if fail >= 1:
                        end_turn=input("Invalid position,Do you want to end turn (Y/N)?")
                        if end_turn =="Y" or end_turn=="y":
                            fail=0
                            refill(joueurs,player_num)
                            if player_num==NOMBRE_DE_JOUEURS-1:
                                player_num=0

                            else:
                                player_num+=1

                            break

                        else:
                            print(" Enter tile and position again")
                            print("Player",player_num,"'s turn")
                            print("Player",player_num,"'hand :",render_hand(joueurs[player_num]))
                            num_to_pop=int(input("Input number of the tile you want to play"))-1
                            attribute=joueurs[player_num].pop(num_to_pop)
                            position=eval(input("Input position where you want the tile to be place"))


                if end_turn != "Y" or end_turn != "y":
                    if len(paquet)==1:
                        scores[player_num]+=6
                    scores[player_num]+=score(dico_example_2,position,attribute)
                    dico_example_2[position]=attribute
                    print("Player",player_num,"'hand :",render_hand(joueurs[player_num]))
                    render_board(dico_example_2)
                    print("The score for player n° :",player_num) 
                    print(scores[player_num])
                    end_turn=input("Do you want to end turn (Y/N)?")
                    if end_turn == "Y" or end_turn =="y":
                        refill(joueurs,player_num)
                        if player_num==NOMBRE_DE_JOUEURS-1:
                            player_num=0
                        else:
                            player_num+=1
        else:
            print('\n')
            print(colored("AI's Turn !","red"),'\n')
            for key in dico_example_2:

                scale_x_n=(0,-1)
                scale_y_p=(-1,0)
                scale_x_p=(0,1)
                scale_y_n=(1,0)
                result_1=tuple(p+q for p, q in zip(key,scale_x_n ))
                result_2=tuple(p+q for p, q in zip(key,scale_y_p ))
                result_3=tuple(p+q for p, q in zip(key,scale_x_p ))
                result_4=tuple(p+q for p, q in zip(key,scale_y_n ))
                possible_moves.append(result_1)
                possible_moves.append(result_2)
                possible_moves.append(result_3)
                possible_moves.append(result_4)

            for positions in possible_moves:
                if pos_taken(positions,dico_example_2) == True:
                    possible_moves.remove(positions)


            #i is the attribute, j is the position

            attribute_bestmove={}
            for i in joueurs[player_num]:
                for j in possible_moves:
                    if (is_row_col_valid(dico_example_2,j,i)==True):
                        pos_score_dico={}
                        score_ai=score(dico_example_2,j,i)
                        pos_score_dico[j]=score_ai

                        max_key = max(pos_score_dico, key=pos_score_dico.get)
                        attribute_bestmove[max_key]=i
                        pos_score_dico.clear()

           
            best_dic={}
            for key,value in attribute_bestmove.items():
                if value not in best_dic.values():
                    best_dic[key]=value



      
            
            for key,value in best_dic.items():
                if (is_row_col_valid(dico_example_2,key,value) is True) and (pos_taken(key,dico_example_2)== False):
                    dico_example_2[key]=value
                    print('\n')
                    render_board(dico_example_2)
                    print("\n")
                    scores[player_num]+=score(dico_example_2,key,value)
                    for i in joueurs[player_num]:
                        if i == value:
                            joueurs[player_num].remove(i)
                            
            print("The score for the A.I is",scores[player_num])            
            refill(joueurs,player_num)  
              
            if player_num==NOMBRE_DE_JOUEURS-1:
                player_num=0
            else:
                player_num+=1
            
def main_3():
    

    NOMBRE_DE_JOUEURS = 2
    
    global paquet
    paquet = []
    for i in range(NOMBRE_DE_TUILES_IDENTIQUES):
        for forme in FORMES:
            for couleur in COULEURS:
                tuile = (forme, couleur)
                paquet.append(tuile)
    random.shuffle(paquet)
    random.shuffle(paquet)
    random.shuffle(paquet)

    # Piocher 6 cartes par personne
    joueurs = {}
    for i in range(NOMBRE_DE_JOUEURS):
        joueurs[i] = []
        for j in range(NOMBRE_DE_CARTE_PAR_MAIN):
            joueurs[i].append(paquet.pop(0))

   # for joueur in joueurs:
    #    print(joueur, "\t", render_hand(joueurs[joueur]))
    
    
    first_player = get_first_player(joueurs)
    print("The player n°{player_num} will play first, because he has the biggest set ({category}), "
          "with {number} {type_}.".format(player_num=first_player[0],
                                          category=first_player[1][0],
                                          number=first_player[1][1][1],
                                          type_=first_player[1][1][0]))
    

    player_num=first_player[0] 
    x=get_bigger_set_of_cards(joueurs[player_num])

    print(colored("AI's Turn !","red"),'\n')
    
    #attributes_ai=[]
    possible_moves=[]
    count=0
    nums_to_pop=[]
    #print(render_hand(joueurs[player_num]))
    if x[0]=='forme':
        for i in range(len(joueurs[player_num])):
            if joueurs[player_num][i][0]==x[1][0]:
                dupli=joueurs[player_num][i] in dico_example_2.values()
                if dupli == False:
                    dico_example_2[(count,0)]=joueurs[player_num][i]
                    nums_to_pop.append(i)
                    count+=1
                
        
    if x[0]=='couleur':
        for i in range(len(joueurs[player_num])):
            if joueurs[player_num][i][1]==x[1][0]:
                dupli=joueurs[player_num][i] in dico_example_2.values()
                if dupli == False:
                    dico_example_2[(count,0)]=joueurs[player_num][i]
                    nums_to_pop.append(i)
                    count+=1
                    
    for x in dico_example_2.values():
        if x in joueurs[player_num]:
            joueurs[player_num].remove(x)
    
    
        
        
    refill(joueurs,player_num)    
    print("\n")
    render_board(dico_example_2)
    print("The score for the A.I is",count)
    scores[player_num]+=count
    if player_num==NOMBRE_DE_JOUEURS-1:
        player_num=0
    else:
        player_num+=1
    
    fail=0   
    while len(paquet)>0:

        if player_num != first_player[0]:
            print("Player",player_num,"'s turn")
            print("Player",player_num,"'hand :",render_hand(joueurs[player_num]))
            trade=input("Do you want to trade tiles (Y/N) ?")
            if trade=="y" or trade == "Y":
                num_tiles_to_exchange=int(input("How many tiles you want to exchange? \n"))
                for i in range(num_tiles_to_exchange):
                    print("Player",player_num,"'hand :",render_hand(joueurs[player_num]))
                    nums_to_pop=int(input("Which tile you want to exchange(1-6)"))-1
                    paquet.append(joueurs[player_num].pop(nums_to_pop))
                    random.shuffle(paquet)
                    joueurs[player_num].append(paquet.pop(0))
                print("Player",player_num,"'hand :",render_hand(joueurs[player_num]))
                if player_num==NOMBRE_DE_JOUEURS-1:
                    player_num=0
                else:
                    player_num+=1

            else:
                end_turn="N"
                print("Player",player_num,"'s turn")
                render_board(dico_example_2)
                print("\n")
                print("Player",player_num,"'hand :",render_hand(joueurs[player_num]))
                num_to_pop=int(input("Input number of the tile you want to play(1-6)"))-1
                #test_list=render_hand(joueurs[player_num]).strip().split('\t')
                attribute=joueurs[player_num].pop(num_to_pop)
                position=eval(input("Input position in tuple form i.e (row,column)/-ve row means up and -ve column means left"))


                while (pos_taken(position,dico_example_2)== True) or (adjacent_checks(position,dico_example_2,attribute) == False) or (is_row_col_valid(dico_example_2,position,attribute)==False):
                    fail +=1
                    joueurs[player_num].insert(num_to_pop,attribute)
                    print("Player",player_num,"'hand :",render_hand(joueurs[player_num]),'\n')
                    if fail >= 1:
                        end_turn=input("Invalid position,Do you want to end turn (Y/N)?")
                        if end_turn =="Y" or end_turn=="y":
                            fail=0
                            refill(joueurs,player_num)
                            if player_num==NOMBRE_DE_JOUEURS-1:
                                player_num=0

                            else:
                                player_num+=1

                            break

                        else:
                            print(" Enter tile and position again")
                            print("Player",player_num,"'s turn")
                            print("Player",player_num,"'hand :",render_hand(joueurs[player_num]))
                            num_to_pop=int(input("Input number of the tile you want to play"))-1
                            attribute=joueurs[player_num].pop(num_to_pop)
                            position=eval(input("Input position where you want the tile to be place"))


                if end_turn != "Y" or end_turn != "y":
                    if len(paquet)==1:
                        scores[player_num]+=6
                    scores[player_num]+=score(dico_example_2,position,attribute)
                    dico_example_2[position]=attribute
                    print("Player",player_num,"'hand :",render_hand(joueurs[player_num]))
                    render_board(dico_example_2)
                    print("The score for player n° :",player_num) 
                    print(scores[player_num])
                    end_turn=input("Do you want to end turn (Y/N)?")
                    if end_turn == "Y" or end_turn =="y":
                        refill(joueurs,player_num)
                        if player_num==NOMBRE_DE_JOUEURS-1:
                            player_num=0
                        else:
                            player_num+=1
        else:
            print('\n')
            print(colored("AI's Turn !","red"),'\n')
            for key in dico_example_2:

                scale_x_n=(0,-1)
                scale_y_p=(-1,0)
                scale_x_p=(0,1)
                scale_y_n=(1,0)
                result_1=tuple(p+q for p, q in zip(key,scale_x_n ))
                result_2=tuple(p+q for p, q in zip(key,scale_y_p ))
                result_3=tuple(p+q for p, q in zip(key,scale_x_p ))
                result_4=tuple(p+q for p, q in zip(key,scale_y_n ))
                possible_moves.append(result_1)
                possible_moves.append(result_2)
                possible_moves.append(result_3)
                possible_moves.append(result_4)

            for positions in possible_moves:
                if pos_taken(positions,dico_example_2) == True:
                    possible_moves.remove(positions)


            #i is the attribute, j is the position

            attribute_bestmove={}
            for i in joueurs[player_num]:
                for j in possible_moves:
                    if (is_row_col_valid(dico_example_2,j,i)==True):
                        pos_score_dico={}
                        score_ai=score(dico_example_2,j,i)
                        pos_score_dico[j]=score_ai

                        max_key = max(pos_score_dico, key=pos_score_dico.get)
                        attribute_bestmove[max_key]=i
                        pos_score_dico.clear()

           
            best_dic={}
            for key,value in attribute_bestmove.items():
                if value not in best_dic.values():
                    best_dic[key]=value
                    
            attributes=[]
            positions=[]
            for key,value in best_dic.items():
                attributes.append(value)
                positions.append(key)
      
            
            position=positions[0]
            attribute=attributes[0]
            if (is_row_col_valid(dico_example_2,position,attribute) is True):
                dico_example_2[key]=value
                print('\n')
                render_board(dico_example_2)
                print("\n")
                scores[player_num]+=score(dico_example_2,position,attribute)
                for i in joueurs[player_num]:
                    if i == value:
                        joueurs[player_num].remove(i)
                            
            print("The score for the A.I is",scores[player_num])            
            refill(joueurs,player_num)  
              
            if player_num==NOMBRE_DE_JOUEURS-1:
                player_num=0
            else:
                player_num+=1
                
def main_4():
  #  the number of players 
#the number of colors
#the number shapes 
#the number of identical tiles.
    scores=[0,0,0,0]

    NOMBRE_DE_JOUEURS = int(input("Enter number of players (2-4)"))
    while NOMBRE_DE_JOUEURS <2 or NOMBRE_DE_JOUEURS >4:
        NOMBRE_DE_JOUEURS=int(input("Enter number of players (2-4)"))
        
    NOMBRE_DE_CARTE_PAR_MAIN = 6

    NOMBRE_DE_TUILES_IDENTIQUES = int(input("Enter Number of identical tile"))

   

    FORMES = {}
    COULEURS = {}
    
    SHAPES={
            "croix": "X",
            "losange": "♦",
            "cercle": "●",
            "carré": "■",
            "étoile": "☼",
            "trèfle": "♣"
            }
    
    
    COLOURS={"rouge": "red",
            "violet": "magenta",
            "bleu": "blue",
            "gris": "white",  # pas d'orange en console
            "vert": "green",
            "jaune": "yellow",
            
    }
    
    
    
    num_shapes=int(input("Enter number of shapes"))
    num_colours=int(input("Enter number of colours"))
    while (num_shapes <2) or (num_shapes>6):
        num_shapes=int(input("Enter number of shapes"))
    while (num_colours<2) or (num_colours>6):
        num_colours=int(input("Enter number of colours"))
        
    print("This is the options for shapes, for each shape, press yes till the number of shapes you want")
    count=0
    for key,value in SHAPES.items():
        print(value)
        choice=input("Press (Y/y) if you want this shape !",)
        if choice =="y" or choice =="Y":
            FORMES[key]=value
            count+=1  
            if count==num_shapes:
                break
          
    count_1=0
    for key,value in COLOURS.items():
        print(value)
        choice=input("Press (Y/y) if you want this colour !")
        if choice =="y" or choice=="Y":
            COULEURS[key]=value
            count_1 +=1
            if count_1==num_colours:
                break
    COULEUR = "couleur"
    FORME = "forme"
    
    
    global paquet
    paquet = []
    for i in range(NOMBRE_DE_TUILES_IDENTIQUES):
        for forme in FORMES:
            for couleur in COULEURS:
                tuile = (forme, couleur)
                paquet.append(tuile)
    random.shuffle(paquet)
    random.shuffle(paquet)
    random.shuffle(paquet)

    # Piocher 6 cartes par personne
    joueurs = {}
    for i in range(NOMBRE_DE_JOUEURS):
        joueurs[i] = []
        for j in range(NOMBRE_DE_CARTE_PAR_MAIN):
            joueurs[i].append(paquet.pop(0))

#    for joueur in joueurs:
#        print(joueur, "\t", render_hand(joueurs[joueur]))
    
    
    first_player = get_first_player(joueurs)
    print("The player n°{player_num} will play first, because he has the biggest set ({category}), "
          "with {number} {type_}.".format(player_num=first_player[0],
                                          category=first_player[1][0],
                                          number=first_player[1][1][1],
                                          type_=first_player[1][1][0]))
    

    player_num=first_player[0] 
   
        
    print("Player ",player_num," starts !")
    print("Player",player_num,"'hand :",render_hand(joueurs[player_num]))
    x=get_bigger_set_of_cards(joueurs[player_num])
    count=0
    nums_to_pop=[]
    if x[0]=='forme':
        for i in range(len(joueurs[player_num])):
            if joueurs[player_num][i][0]==x[1][0]:
                dupli=joueurs[player_num][i] in dico_example_2.values()
                if dupli == False:
                    dico_example_2[(count,0)]=joueurs[player_num][i]
                    nums_to_pop.append(i)
                    count+=1
                
        
    if x[0]=='couleur':
        for i in range(len(joueurs[player_num])):
            if joueurs[player_num][i][1]==x[1][0]:
                dupli=joueurs[player_num][i] in dico_example_2.values()
                if dupli == False:
                    dico_example_2[(count,0)]=joueurs[player_num][i]
                    nums_to_pop.append(i)
                    count+=1
                    
    for x in dico_example_2.values():
        if x in joueurs[player_num]:
            joueurs[player_num].remove(x)
    
         
    refill(joueurs,player_num)    
    render_board(dico_example_2)
    print("The score for player n° :",player_num)
    print(count)
    if player_num==NOMBRE_DE_JOUEURS-1:
        player_num=0
    else:
        player_num+=1
    fail=0
    while len(paquet)>0:
        print("Player",player_num,"'s turn")
        print("Player",player_num,"'hand :",render_hand(joueurs[player_num]))
        trade=input("Do you want to trade tiles (Y/N) ?")
        if trade=="y" or trade == "Y":
            num_tiles_to_exchange=int(input("How many tiles you want to exchange? \n"))
            for i in range(num_tiles_to_exchange):
                print("Player",player_num,"'hand :",render_hand(joueurs[player_num]))
                nums_to_pop=int(input("Which tile you want to exchange(1-6)"))-1
                paquet.append(joueurs[player_num].pop(nums_to_pop))
                random.shuffle(paquet)
                joueurs[player_num].append(paquet.pop(0))
            print("Player",player_num,"'hand :",render_hand(joueurs[player_num]))
            if player_num==NOMBRE_DE_JOUEURS-1:
                player_num=0
            else:
                player_num+=1
                 
        else:
            end_turn="N"
            print("Player",player_num,"'s turn")
            print("\n")
            render_board(dico_example_2)
            print("Player",player_num,"'hand :",render_hand(joueurs[player_num]))
            num_to_pop=int(input("Input number of the tile you want to play(1-6)"))-1
            #test_list=render_hand(joueurs[player_num]).strip().split('\t')
            attribute=joueurs[player_num].pop(num_to_pop)
            position=eval(input("Input position in tuple form i.e (row,column)/-ve row means up and -ve column means left"))


            while (pos_taken(position,dico_example_2)== True) or (adjacent_checks(position,dico_example_2,attribute) == False) or (is_row_col_valid(dico_example_2,position,attribute)==False):
                fail +=1
                joueurs[player_num].insert(num_to_pop,attribute)
                print("Player",player_num,"'hand :",render_hand(joueurs[player_num]),'\n')
                if fail >= 1:
                    end_turn=input("Invalid position,Do you want to end turn (Y/N)?")
                    if end_turn =="Y" or end_turn=="y":
                        fail=0
                        refill(joueurs,player_num)
                        if player_num==NOMBRE_DE_JOUEURS-1:
                            player_num=0

                        else:
                            player_num+=1

                        break

                    else:
                        print(" Enter tile and position again")
                        print("Player",player_num,"'s turn")
                        print("\n")
                        print("Player",player_num,"'hand :",render_hand(joueurs[player_num]))
                        num_to_pop=int(input("Input number of the tile you want to play"))-1
                        attribute=joueurs[player_num].pop(num_to_pop)
                        position=eval(input("Input position where you want the tile to be place"))


            if end_turn != "Y" or end_turn != "y":
                if len(paquet)==1:
                    scores[player_num]+=6
                scores[player_num]+=score(dico_example_2,position,attribute)
                dico_example_2[position]=attribute
                print("Player",player_num,"'hand :",render_hand(joueurs[player_num]))
                print("\n")
                render_board(dico_example_2)
                print("The score for player n° :",player_num) 
                print(scores[player_num])
                end_turn=input("Do you want to end turn (Y/N)?")
                if end_turn == "Y" or end_turn =="y":
                    refill(joueurs,player_num)
                    if player_num==NOMBRE_DE_JOUEURS-1:
                        player_num=0
                    else:
                        player_num+=1
                        

    
                
        
                
def render_board(board: dict):
    # Analyser les coordonnées pour avoir la dimension de la future matrice
    list_of_numline = []
    list_of_numcol = []
    for key in board:
        list_of_numline.append(key[0])
        list_of_numcol.append(key[1])
   
    # Avoir les bornes de chaque dimension pour faire un range(min, max)
    # TODO: faire ça avec la méthode de recherche min/max vue en cours
    min_line = min(list_of_numline)
    max_line = max(list_of_numline)
    min_col = min(list_of_numcol)
    max_col = max(list_of_numcol)

    valeur_case_vide = None

    global matrix_output
    matrix_output=[]
    for numline in range(min_line, max_line+1):
        line_temp = []
        for numcol in range(min_col, max_col+1):
            line_temp.append(board.get((numline, numcol),
                                       valeur_case_vide))
        matrix_output.append(line_temp)

    line_of_numcols = ""
    for i in range(min_col, max_col+1):
        line_of_numcols += str(i) + "\t"
    print("\t", termcolor.colored(line_of_numcols, "grey"))
    list_of_numlines = list(range(min_line, max_line+1))
    for i, ligne in enumerate(matrix_output):
        print(termcolor.colored(list_of_numlines[i], "grey"),
              "\t", render_hand(ligne))


  
if __name__ == "__main__":
        
    print(        colored("           Welcome to Qwirkle","green"))
    print("==========================================",'\n')
    print(colored("Menu board","red"))
    print(colored("1: Human vs Human","blue"))
    print(colored("2: Human vs Machine (Machine plays multiple tiles)","blue"))
    print(colored("3: Human vs Machine (Machine plays one tile)","blue"))
    print(colored("4: Customize your game","blue"))
    
    choice=input(colored("Enter choice (1/2/3/4)","red"))
       
    if choice =="1":
        main()
    if choice=="2":
        main_2()
    if choice=='3':
        main_3()
    if choice=='4':
        main_4()
"""
import json
file_name= input('please the name of your file with .json and replace space by_')
 # players = {Player_id : [hand]} --> players = {player_id: {hand: list
 #                                                           score: int
 #                                                             age: int, optional}}
 # for save :
 # first you run to create create_game_dict 
 
 def create_game_dict(NOMBRE_DE_JOUEURS: int,joueurs : dict, scores: list, dico_example_2: dict, paquet: list, player_num: int):
   game_dict = {}
   game_dict['Players']= {}
   game_dict['deck']= paquet 
   game_dict['num_player'] = player_num
   game_dict['positions'] = dico_example_2
   for i in range(number_of_player):
      game_dict['Players'][i] = {}
      game_dict['Players'][i]['hand'] = joueurs[i]
      game_dict['Players'][i]['score']= scores[i]
  return game_dict
# then you run to_save
def to_save(game_dict: dict, file_name:str):
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dumps(game_dict, file)
    file.close()
# to charge the previous game
def to_charge(file_name):
    score = []
    game_dict = json.loads(file_name)
    players = game_dict['joueurs'] # --> this is the dictionary describe at the begining 
    dico_example_2 = game_dict['positions']
    paquet = game_dict['deck']
    player_playing = game_dict['player_num']
  for i in range(len(players)):
    score.append(players[i]['score'])
    charge = (game, player, matrix_board, deck, player_playing, score)
    # the output is a tuple the you can access to each value like in a list and put them as variables to continue the game
  return charge
"""
  
   
  

    
    


# In[ ]:



    


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




