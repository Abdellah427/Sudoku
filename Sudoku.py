#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from copy import deepcopy

def afficher_grille(sudoku):
    """

    Parameters
    ----------
    sudoku : matrice 9x9 de chiffres

    Returns
    -------
    Affichage de la matrice dans la console

    """
    res=''
    for i in range(len(sudoku)):
        chaine=str(sudoku[i])
        j=0
        while j<len(chaine):
            if chaine[j]=='0':
                chaine = chaine[:j] + ' ' + chaine[j+1:]
                j+=1
            elif chaine[j]==',':
                chaine = chaine[:j] + chaine[j+1:]
            else:
                j+=1
        chaine='|' + chaine[1:6] + '|' + chaine[7:12]+'|'+ chaine[13:18] + '|\n'
        if i in [0,3,6]:
            res+=19*'—' + '\n'
        res+=chaine
    res+=19*'—' 
    print(res)
    
    
def check(sudoku,chiffre,i,j):
    """

    Verifie si un placement de chiffre est licit (et si la case modifiée est bien vide)

    Retourn un booléen
    True: placement licit
    False illicit
    
    
    """
    #Case vide
    if sudoku[i][j]!=0:
        return False
    
    for c in range(9):
    #Lignes
        if sudoku[i][c]==chiffre:
            return False
    #Colonnes
        if sudoku[c][j]==chiffre:
            return False
        
    #Carré
    a=i//3
    b=j//3
    for q in range(3):
        for r in range(3):
            if sudoku[3*a+q][3*b+r]==chiffre:
                return False
            
    return True
    
def check_2(sudoku,chiffre,i,j):
    
    """
    
    Pareil mais ne vérifie pas que la case est vide (utile dans la résolution pour les chemins)
    
    """
    for c in range(9):
    #Lignes
        if sudoku[i][c]==chiffre:
            return False
    #Colonnes
        if sudoku[c][j]==chiffre:
            return False
        
    #Carré
    a=i//3
    b=j//3
    for q in range(3):
        for r in range(3):
            if sudoku[3*a+q][3*b+r]==chiffre:
                return False
            
    return True
    
def solve_s(sudoku):
   
    """
    solveur naif: verifie ligne / colonne et carré les chiffres manquants et regarde ou on peut les placer
    place un chiffre quand c'est l'unique solution
    
    """
    
   
    compteur=1
    
    while compteur==1:
        compteur=0

        #Lignes
        for i in range(9):
            chiffres_manquants=[k for k in range(1,10)]
            for j in range(9):
                if sudoku[i][j]!=0:
                    chiffres_manquants.remove(sudoku[i][j])
            for k in range(len(chiffres_manquants)):
                L=[]
                for j in range(9):
                    if check(sudoku,chiffres_manquants[k],i,j):
                        L.append(j)
                if len(L)==1:
                    sudoku[i][L[0]]=chiffres_manquants[k]
                    compteur=1
                del L
            del chiffres_manquants
                
        #Colonnes
        for j in range(9):
            chiffres_manquants=[k for k in range(1,10)]
            for i in range(9):
                if sudoku[i][j]!=0:
                    chiffres_manquants.remove(sudoku[i][j])
            for k in range(len(chiffres_manquants)):
                L=[]
                for i in range(9):
                    if check(sudoku,chiffres_manquants[k],i,j):
                        L.append(i)
                if len(L)==1:
                    sudoku[L[0]][j]=chiffres_manquants[k]
                    compteur=1
                del L
            del chiffres_manquants
            
            
        #Carré
        for i in range(3):
            for j in range(3):
                chiffres_manquants=[k for k in range(1,10)]
                for k in range(3):
                    for l in range(3):
                        if sudoku[3*i+k][3*j+l]!=0:
                            chiffres_manquants.remove(sudoku[3*i+k][3*j+l])
                for p in range(len(chiffres_manquants)):
                    L=[]
                    for k in range(3):
                        for l in range(3):
                            if check(sudoku,chiffres_manquants[p],3*i+k,3*j+l):
                                L.append([k,l])
                    if len(L)==1:
                        sudoku[3*i+L[0][0]][3*j+L[0][1]]=chiffres_manquants[p]
                        compteur=1
                    del L
                del chiffres_manquants
        
    return sudoku


diabo=[[0,8,0,0,0,9,3,0,0],[9,7,0,0,5,0,0,1,0],[5,3,4,8,0,0,0,7,0],[0,0,0,3,0,1,0,0,0],[3,9,0,5,0,0,0,0,0],[0,4,0,0,0,0,0,0,0],[0,5,0,0,7,0,0,3,6],[7,0,0,0,3,0,8,0,0],[4,0,0,9,0,0,1,0,0]]
sudoku_plus_dur_du_monde=[[0,0,0,0,0,0,0,3,9],
                          [0,0,0,0,0,1,0,0,5],
                          [0,0,3,0,5,0,8,0,0],
                          [0,0,8,0,9,0,0,0,6],
                          [0,7,0,0,0,2,0,0,0],
                          [1,0,0,4,0,0,0,0,0],
                          [0,0,9,0,8,0,0,5,0],
                          [0,2,0,0,0,0,6,0,0],
                          [4,0,0,7,0,0,0,0,0]]

def check_end(sudoku):
    
    """
    Verifie qu'un sudoku est fini et juste
    """
    #Completude
    for i in range(9):
        for j in range(9):
            if sudoku[i][j]==0:
                return False
         
    #Lignes
    for i in range(9):
        L=[]
        for j in range(9):
            if sudoku[i][j] in L:
                return False
            else:
                L.append(sudoku[i][j])
        del L
    
    #Colonnes
    for j in range(9):
        L=[]
        for i in range(9):
            if sudoku[i][j] in L:
                return False
            else:
                L.append(sudoku[i][j])
        del L
        
    #Carrés
    for i in range(3):
        for j in range(3):
            L=[]
            for k in range(3):
                for l in range(3):
                    if sudoku[3*i+k][3*j+l] in L:
                        return False
                    else:
                        L.append(sudoku[3*i+k][3*j+l])
            del L
            
    return True


def coups_possibles(sudoku):
    """
    renvoie la liste de tout les coups possible sur la forme d'une liste
    contenant les element de la forme [ligne,colonne,[chiffres possibles]]
    
    """
    
    L=[]
    for i in range(9):
        for j in range(9):
            L1=[i,j]
            C=[]
            for a in range(1,10):
                if check(sudoku,a,i,j):
                    C.append(a)
            if len(C)!=0:
                L1.append(C)
                L.append(L1)
            del L1
            del C
    return L

def impossible(sudoku):
    if len(coups_possibles(sudoku))==0:
        return True
    return False



def solve_all(sudoku):
    """
    solveur complet:
        #1 utlise la fonction solve classique
        #2 verifie si c'est fini
        #3 essaye différents chemins possible et reinjecte le resultat dans la fonction
    
    """
    sudoku_solve=solve_s(sudoku)
    
    #Fini
    if check_end(sudoku_solve):
        return sudoku_solve,True
    
    coups=coups_possibles(sudoku_solve)
    
    #Impossible
    if len(coups)==0:
        return sudoku,False
    
    #Chemins
    min=coups[0]
    for k in range(1,len(coups)):
        if len(coups[k][2])<len(min[2]):
            min=coups[k]
    for p in range(len(min[2])):
        sudoku_solve[min[0]][min[1]]=min[2][p]
        sudoku_copy=deepcopy(sudoku_solve)
        sudoku_copy,G=solve_all(sudoku_copy)
        if G:
            return sudoku_copy,True
    
    return sudoku,False
    

imp=[[1,0,0,0,0,7,0,9,0],[0,3,0,0,2,0,0,0,8],[0,0,9,6,0,0,5,0,0],[0,0,5,3,0,0,9,0,0],[0,1,0,0,8,0,0,0,2],[6,0,0,0,0,4,0,0,0],[3,0,0,0,0,0,0,1,0],[0,4,0,0,0,0,0,0,7],[0,0,7,0,0,0,3,0,0]]




### A copier-coller: #########################################################



# Fonction principale
#Idée: 
    # 1_Utiliser le solveur simple
    # 2_Tester des chemins possibles
    # 3_Recursivité
def solve_all(sudoku):
    
    #Solveur classique
    sudoku_solve=solve_s(sudoku)
    
    #Fini ?
    if check_end(sudoku_solve):
        return sudoku_solve,True
    
    coups=coups_possibles(sudoku_solve)
    
    #Impossible ?
    if len(coups)==0:
        return sudoku,False
    
    
    
    #Chemins
    
    
    #On choisit la case avec le moins de coups possibles
    min=coups[0]
    for k in range(1,len(coups)):
        if len(coups[k][2])<len(min[2]):
            min=coups[k]
   
    #On teste les chemins
    for p in range(len(min[2])):
        sudoku_solve[min[0]][min[1]]=min[2][p]
        sudoku_copy=deepcopy(sudoku_solve)
        #Recursivité :
        sudoku_copy,G=solve_all(sudoku_copy)
        if G:
            return sudoku_copy,True
    
    return sudoku,False


# Idée
    # Créer une liste avec tout les coups jouables
    # Format: liste de liste de la forme [ligne,colonne,liste des chiffres jouables]
def coups_possibles(sudoku):    
    L=[]
    for i in range(9):
        for j in range(9):
            L1=[i,j]
            C=[]
            for a in range(1,10):
                if check(sudoku,a,i,j):
                    C.append(a)
            if len(C)!=0:
                L1.append(C)
                L.append(L1)
            del L1
            del C
    return L


# Idée
    # Verifier si un sudoku est possible
    # Methode : regarde si la liste des coups possibles est vides
def impossible(sudoku):
    if len(coups_possibles(sudoku))==0:
        return True
    return False


# Idée
    # Verifier qu'un sudoku est fini et juste
def check_end(sudoku):
    
    #Completude
    for i in range(9):
        for j in range(9):
            if sudoku[i][j]==0:
                return False
         
    #Lignes
    for i in range(9):
        L=[]
        for j in range(9):
            if sudoku[i][j] in L:
                return False
            else:
                L.append(sudoku[i][j])
        del L
    
    #Colonnes
    for j in range(9):
        L=[]
        for i in range(9):
            if sudoku[i][j] in L:
                return False
            else:
                L.append(sudoku[i][j])
        del L
        
    #Carrés
    for i in range(3):
        for j in range(3):
            L=[]
            for k in range(3):
                for l in range(3):
                    if sudoku[3*i+k][3*j+l] in L:
                        return False
                    else:
                        L.append(sudoku[3*i+k][3*j+l])
            del L
            
    return True


# Idée
    # Resoudre le sudoku de manière classique
    # On teste succesivment chaque ligne/colonne/carré
    # Si un chiffre manquant ne peut etre placer que sur une case possible, on le place
    # On s'arrete quand aucun coup n'a pu etre jouer sur un cycle complet de verification
def solve_s(sudoku):

    compteur=1
    # Incrementer uniquement lorsqu'on place un chiffre
    
    
    while compteur==1:
        compteur=0

        #Lignes
        for i in range(9):
            chiffres_manquants=[k for k in range(1,10)]
            
            # Determine les chiffres manquants sur une ligne
            for j in range(9):
                if sudoku[i][j]!=0:
                    chiffres_manquants.remove(sudoku[i][j])
            
            for k in range(len(chiffres_manquants)):
                L=[]
                
                # On ajoute à L les case pouvant accueillir un chiffre
                for j in range(9):
                    if check(sudoku,chiffres_manquants[k],i,j):
                        L.append(j)
                
                # On verifie qu'il n'y a qu'une solution
                if len(L)==1:
                    sudoku[i][L[0]]=chiffres_manquants[k]
                    compteur=1
                
                del L
            
            del chiffres_manquants
                
        #Colonnes
        for j in range(9):
            chiffres_manquants=[k for k in range(1,10)]
            
            # Determine les chiffres manquants sur une colonne
            for i in range(9):
                if sudoku[i][j]!=0:
                    chiffres_manquants.remove(sudoku[i][j])
            
            for k in range(len(chiffres_manquants)):
                L=[]
                # On ajoute à L les case pouvant accueillir un chiffre
                for i in range(9):
                    if check(sudoku,chiffres_manquants[k],i,j):
                        L.append(i)
                
                # On verifie qu'il n'y a qu'une solution
                if len(L)==1:
                    sudoku[L[0]][j]=chiffres_manquants[k]
                    compteur=1
                del L
            del chiffres_manquants
            
            
        #Carré
        for i in range(3):
            for j in range(3):
                chiffres_manquants=[k for k in range(1,10)]
                # Determine les chiffres manquants dans un carré
                for k in range(3):
                    for l in range(3):
                        if sudoku[3*i+k][3*j+l]!=0:
                            chiffres_manquants.remove(sudoku[3*i+k][3*j+l])
                
                for p in range(len(chiffres_manquants)):
                    L=[]
                    # Determine les chiffres manquants sur une colonne
                    for k in range(3):
                        for l in range(3):
                            if check(sudoku,chiffres_manquants[p],3*i+k,3*j+l):
                                L.append([k,l])
                    # On verifie qu'il n'y a qu'une solution
                    if len(L)==1:
                        sudoku[3*i+L[0][0]][3*j+L[0][1]]=chiffres_manquants[p]
                        compteur=1
                    
                    del L
                
                del chiffres_manquants
        
    return sudoku


# Idée
    # Verifie qu'un placement est autorisé
    # Case vide, même chiffre sur la même ligne/colonne et carré
def check(sudoku,chiffre,i,j):

    #Case vide
    if sudoku[i][j]!=0:
        return False
    
    
    for c in range(9):
       
        #Lignes
        if sudoku[i][c]==chiffre:
            return False
        
        #Colonnes
        if sudoku[c][j]==chiffre:
            return False
        
        
    #Carré
    a=i//3
    b=j//3
    for q in range(3):
        for r in range(3):
            if sudoku[3*a+q][3*b+r]==chiffre:
                return False
            
    return True

# Idée
    # Même chose mais sans vérifier que la case est vide
def check_2(sudoku,chiffre,i,j):
    
    for c in range(9):
    #Lignes
        if sudoku[i][c]==chiffre:
            return False
    #Colonnes
        if sudoku[c][j]==chiffre:
            return False
        
    #Carré
    a=i//3
    b=j//3
    for q in range(3):
        for r in range(3):
            if sudoku[3*a+q][3*b+r]==chiffre:
                return False
            
    return True



