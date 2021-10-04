import numpy as np
import copy


Gammes= [ [1,2,3],
          [2,1,3],
          [1,2,3]
        ]

S = [ [1,2,3],
      [2,1,3],
      [1,2,3]
    ]#s est une solution. On a une machine sur chaque ligne

N =3 #nb de pièces
M = 3 #nb dem
#numero_noeuds = 1 + (n -1)*m + n 
INF = float('inf')

#conventions
print("quand deux neuds sont tels que aucun arc ne les relient, on adopte quelle convention?: None ou 0 ?")
dico = {0: 0, 1:None}
NOLINK = dico[int(input( "entrer 0=>Erivez 0  ou  None=> Ecrivez 1: " ))]
Valeur = {0:(1,1), None: (0,1)}
ECART = {0:0, None:2}

def t(G,i,j):
    if G[i][j] != NOLINK and i!=0: #l'arc existe et i n'est pas le debut
        return 1
    else: #i est le debut ou soit il y a pas d'arc
        return 0



def afficher_matrice(A):#A est une matrice (n*m) contenant des entiers et des none
    #on gere None qui est de longueur 4
    B = copy.deepcopy(A); 
    B[B==NOLINK]=10**3; 
    R = int(np.max(np.array(B)))+1
    
    ecart = ECART[NOLINK] #definit la distance entre deux colonnes
    
    for i in range(len(A)):
        for j in range(len(A[0])):
            str = (ecart + int(np.log(R)/np.log(10))- int(np.log(B[i][j])/np.log(10)) ) * " " if A[i][j]!=0 else (ecart+ int(np.log(R)/np.log(10))- int(np.log(1)/np.log(10)))*" "
            print(A[i][j],end=str)
        print("\n")
    print("fin matrice")




def trouver_indice_couple(indice_piece,indice_machine,n=N,m=M):  #chaque couple est indexé entre 1 et ....; 0 est l'index du debut
    matrice_des_indices = np.zeros((n,m))
    pos = 1
    for i in range(n):
        for j in range (m):
            matrice_des_indices[i][j] = pos
            pos +=1
    return int(matrice_des_indices[indice_piece][indice_machine])

def trouver_couple_dIndice(indice_pièceETmachine,n=N,m=M):
    pos = 1
    for i in range(n):
        for j in range (m):
            if pos == indice_pièceETmachine:
                return (i,j)
            pos +=1
    print("a huge pb")
    return 


# for i in range(3):
    # for j in range (3):
        # print("trouver_indice_couple",trouver_indice_couple(i,j))





def trouver_indice_machine_dans_la_gamme(Gammes,indice_piece, position): #dans la gamme de chaque piece (ie chaque ligne de Gammes), une position est associèe à une machine
    return Gammes[indice_piece][position] - np.min(np.array(Gammes))

def trouver_indice_piece_dans_la_solution_s(s,indice_machine,position): #pour chaque machine (ligne de s), chaque position est associée à une pièce 
    return s[indice_machine][position] - np.min(np.array(s))

###test
# for i in range (n):
    # for j in range (m):
        # print("r")
        # print(trouver_indice_couple(i,j))



def fct_Matrice_Adjacence(Gammes,afficher_commentaires=False): #Gammes est une matrice
    #initialisation du graphe
    nb_noeuds =  2 + len(Gammes)*len(Gammes[0])
    taille_matrice = nb_noeuds
    A = np.full((taille_matrice,taille_matrice),NOLINK)


    #la même pièce i passe par des machines j: arcs noirs
    for i  in range(len(Gammes)):
        for j in range (len(Gammes[0])-1): #on parcours les machines sauf la dernière
            pièce = i + 1;indice_pièce = i
            indice_machine1 = trouver_indice_machine_dans_la_gamme(Gammes,indice_pièce, j)
            indice_machine2 = trouver_indice_machine_dans_la_gamme(Gammes,indice_pièce, j+1)
            pos1 = trouver_indice_couple(indice_pièce,indice_machine1,len(Gammes),len(Gammes[0]))
            pos2 = trouver_indice_couple(indice_pièce,indice_machine2,len(Gammes),len(Gammes[0]))
            if afficher_commentaires: print("arc noir ",(pos1,pos2))
            A[pos1][pos2] = Valeur[NOLINK][1]

    #le debut et la fin liés débuts des pièces: arcs verts
    for indice_pièce in range (len(Gammes)):
        #lier le début à (piècei, première machine associée)
        indice_debut = 0
        première_machine = trouver_indice_machine_dans_la_gamme(Gammes,indice_pièce, 0); 
        indice_pièceETmachine = trouver_indice_couple(indice_pièce,première_machine,len(Gammes),len(Gammes[0]) )
        if afficher_commentaires: print("arc vert ",(indice_debut,indice_pièceETmachine)); 
        A[indice_debut][indice_pièceETmachine] = Valeur[NOLINK][0]
        #lier la fin à (piècei, premièrdernière machine associée)
        indice_fin = len(A)-1
        dernière_machine = trouver_indice_machine_dans_la_gamme(Gammes,indice_pièce, -1+len(Gammes[i]));
        indice_pièceETmachine = trouver_indice_couple(indice_pièce,dernière_machine,len(Gammes),len(Gammes[0]))
        if afficher_commentaires: print("arcrouge ",(indice_pièceETmachine,indice_fin)); 
        A[indice_pièceETmachine][indice_fin] = Valeur[NOLINK][1]

    return A





#question1
def GRAPHE(s,gamme = Gammes,afficher_commentaires=False):
    #j'initialise le graphe et j'ajoute les arcs, verts, rouge et noirs
    graphe = fct_Matrice_Adjacence(gamme,afficher_commentaires)
    
    #je m'assure que la solution et la gamme sont deux matrices
    if 2+ len(s)*len(s[0]) != len(graphe):
        print("erreur: le nombre de ligne de la gamme doit être égal au nombre de colonne de la solution et inversément")
        print("len(graphe)=",len(graphe))
        print("2+ {}*{} = {}".format( len(s),len(s[0]),2+ len(s)*len(s[0]) ) )
        return np.zeros((1,1))
        
    #plusieurs pièces passent en ordre sur une même machine: les arcs bleus q
    for j  in range(len(s)):
        indice_machine = j
        for i in range (len(s[0])-1): #on parcours les pieces sauf la dernière
            indice_piece1 = trouver_indice_piece_dans_la_solution_s(s,j,i)
            indice_piece2 = trouver_indice_piece_dans_la_solution_s(s,j,i+1)
            pos1 = trouver_indice_couple(indice_piece1,indice_machine,len(gamme),len(gamme[0]))
            pos2 = trouver_indice_couple(indice_piece2,indice_machine,len(gamme),len(gamme[0]))
            if afficher_commentaires: print("arc bleu ",(pos1,pos2))
            graphe[pos1][pos2] = Valeur[NOLINK][1]
    return graphe
            
S = [ [1,2,3],
      [2,1,3],
      [1,2,3]
    ]#s est une solution. On a une machine sur chaque ligne
afficher_matrice( GRAPHE(S,afficher_commentaires=True))

print("fin question 1", end = "\n\n\n\n\n")














#questiion2
#deterliner le plus long chemin du devbut à chaque point


#fct preliminaires
def predecesseurs(G,s):
    predecesseurs = [i for i in range(len(G)) if G[i][s]!=NOLINK]+int(G[0][s]==Valeur[NOLINK][0])*[0]
    return list(set(predecesseurs))
def successeurs(G,s):
    successeurs=[j for j in range(len(G[0])) if G[s][j]!=NOLINK]+[len(G)-1]
    return successeurs
    
def intersection(lst1, lst2):  #intersection de deux listes
    return list(set(lst1) & set(lst2)) 
    


def PLC(G,sommet_depart=0,afficher_commentaires=False): #G graphe orienté sans circuit; G est une matrice (n,n) et s, un entier entre 0 et len(A)-1, est le sommet de départ
    #des vérifications
    A = G; B = np.array(A)
    if sommet_depart not in range(0,len(A)): 
        print("sommet inexistant")
        return
    if (B.diagonal()!=NOLINK).any():
        print("retranchez les valeurs des diagonales")
        return

    #des initialisations 
    λ = [INF for i in range(len(A))];plc = λ  #liste des distances à sommet_depart 
    λ[sommet_depart] = 0
    rang = 0
    S = [sommet_depart]#liste des sommets en cours S
    r = [0 for i in range(len(G))] #liste des rangs des sommets
    liste_sommets = [i for i in range(len(G))]

    while len(S)!=len(A):
        rang +=1
        if afficher_commentaires: print("A: ",A)
        listeDesSommes_prive_de_S = [i for i in liste_sommets if i not in S]
        W = [i for i in listeDesSommes_prive_de_S if intersection(predecesseurs(G,i) , listeDesSommes_prive_de_S)==[]  ] 
        if afficher_commentaires: print(intersection(predecesseurs(G,7) , listeDesSommes_prive_de_S))
        #l'ensemble des sommets qui ne sont pas dans S et qui n'ont pars de prédecesseurs
        #on pose rang(v)=rang pour tout les éléments de W
        for v in W:
            r[v]=rang
        S.extend(W)
        

    for k in range(1,rang+1):
        for v in [ v  for v in liste_sommets if r[v]==k]:
            N_moins = predecesseurs(G,v)
            
            plc[v] = max([ plc[w] + t(G, w, v)  for w in N_moins])
            if afficher_commentaires:print("distance max entre {} et {} trouvé = {}".format(sommet_depart,v,plc[v]))           
    return λ

##########test
S = [ [1,2,3],
      [2,1,3],
      [1,2,3]
    ]#s est une solution. On a une machine sur chaque ligne
print("plc = ",PLC(GRAPHE(S),sommet_depart=0,afficher_commentaires=True),end="\n\n")


def plc(i,j,G=GRAPHE(S)):
    liste_plc = PLC(G,sommet_depart=0)
    indice_piece = i-1; indice_machine= j-1
    indice_pièceETmachine = trouver_indice_couple(indice_piece,indice_machine,len(S[0]),len(S))
    return liste_plc[indice_pièceETmachine]

print("plc(2,1)= ", plc(2,1))

print("fin question 2", end = "\n\n\n\n\n")

Gammes= [ [1,2,3],[2,1,3],[1,2,3]]
S= [ [1,2,3],[2,1,3],[1,2,3]]#s est une solution. On a une machine sur chaque ligne









#question3

#trouver pour chaque tâche (pièce, machine), l'heure de démarrage au plus tard



def AuPlusTard(Gammes,solution,sommet_fin,afficher_commentaires=False):#G graphe orienté sans circuit; G est une matrice (n,n) et s, un entier entre 0 et len(A)-1, est le sommet de départ
    Graphe = GRAPHE(solution,Gammes)
    #des vérifications
    A = Graphe; B = np.array(A)
    if sommet_fin not in range(0,len(A)): 
        print("sommet inexistant")
        return
    if (B.diagonal()!=NOLINK).any():
        print("retranchez les valeurs des diagonales")
        return
    if ( [len(Gammes),len(Gammes[0])] != [len(solution[0]),len(solution)] ):
        print("la solution et la gamme ne correspondent pas")
        return

    #des initialisations 
    auplustard = [INF for i in range(len(A))] #liste des distances à sommet_depart 
    auplustard[sommet_fin] = PLC(Graphe,sommet_depart=0)[-1]
    rang = 0
    S = [sommet_fin]#liste des sommets en cours s
    r = [0 for i in range(len(Graphe))] #liste des rangs des sommets 
    liste_sommets = [i for i in range(len(Graphe))]

    while len(S)!=len(A):
        rang +=1
        if afficher_commentaires:print("S",S)
        listeDesSommes_prive_de_S = [i for i in liste_sommets if i not in S]
        W = [i for i in listeDesSommes_prive_de_S if intersection(successeurs(Graphe,i) , listeDesSommes_prive_de_S)==[]  ]
        #l'ensemble des sommets qui ne sont pas dans S et qui n'ont pars de prédecesseur
        #on pose rang(v)=rang pour tout les éléments de W
        for v in W:
            r[v]=rang
        S.extend(W)
        
        #print("\n")
        

        
    for k in range(1,rang+1):
        for v in [ v  for v in liste_sommets if r[v]==k]:
            N_plus = successeurs(Graphe,v)
            auplustard[v] = min([ auplustard[w] - t(Graphe, v,w)  for w in N_plus])
           
        
           
    return auplustard

Gammes= [ [1,2,3],[2,1,3],[1,2,3]]
def AUPLUTARD(s,afficher_commentaires=False,sommet_fin=len(GRAPHE(S))-1):
    sommet_fin = len(GRAPHE(s))-1
    solution = s
    return AuPlusTard(Gammes,solution,sommet_fin, afficher_commentaires)
    
    
def auplustard(i,j,G=GRAPHE(S),solution = S,sommet_fin=len(GRAPHE(S))-1):
    liste_plc = AUPLUTARD(solution,sommet_fin)
    indice_piece = i-1; indice_machine= j-1
    indice_pièceETmachine = trouver_indice_couple(indice_piece,indice_machine,len(solution[0]),len(solution) )
    print(indice_pièceETmachine)
    return liste_plc[indice_pièceETmachine]

print("auplustard")
print(AUPLUTARD(S,afficher_commentaires=True),end="\n\n")


S = [ [1,2,3],[2,1,3],[1,2,3]]#s est une solution. On a une machine sur chaque ligne
print(PLC(GRAPHE(S)))
print(AUPLUTARD(S),end="\n\n")
print("2")
# S = [ [3,2,1],[2,1,3],[1,2,3]]#s est une solution. On a une machine sur chaque ligne
# print(PLC(GRAPHE(S)))
# print(AUPLUTARD(S),end="\n\n")
# print("3")
# S = [ [3,2,1],[2,1,3],[3,2,1]]#s est une solution. On a une machine sur chaque ligne
# print(PLC(GRAPHE(S)))
# print(AUPLUTARD(S),end="\n\n")



print("auplustard(2,1)= ", auplustard(2,1))
print("fin question 3")





#question 4
#cette fonction donne les tâches critiques pour une solution s donnée
def CRITIQUE(s):
    auplustard = AUPLUTARD(s)
    Graphe = GRAPHE(s)
    plc = PLC(Graphe)
    if len(plc)!=len(auplustard):
        print("erreur")
    return [i for i in range(len(plc)) if plc[i]==auplustard[i] ]
    
print("les tâches critiques sont d'indices: ", CRITIQUE(S))
print("fin question 4")

#question 5
#cette fonction identifie pour une machine i, les tâches consecutives et critiques
def CRITIQUESucc(machine,s=S):
    CRITIQUESucc =[] #la liste des paires de noeuds (v,w) tq v et w sont critiques et consecutifs (sur une même machine)
    indice_machine = machine-1
    liste_pieces = s[indice_machine]
    for j in range (len(liste_pieces)-1):
        indice_piece1 = trouver_indice_piece_dans_la_solution_s(s,indice_machine,j)
        indice_piece2 = trouver_indice_piece_dans_la_solution_s(s,indice_machine,j+1)
        indice_pièce1ETmachine = trouver_indice_couple(indice_piece1,indice_machine,N,M)
        indice_pièce2ETmachine = trouver_indice_couple(indice_piece2,indice_machine,N,M)
        if indice_pièce1ETmachine in CRITIQUE(s) and indice_pièce2ETmachine in CRITIQUE(s):
            CRITIQUESucc.append((indice_pièce1ETmachine,indice_pièce2ETmachine))
         
    return CRITIQUESucc #liste de paires (tuples) de tâches 

print("CRITIQUESucc(1)",CRITIQUESucc(1))
print("CRITIQUESucc(2)",CRITIQUESucc(2))
print("CRITIQUESucc(3)",CRITIQUESucc(3))
print("\n\n")
# print("fin question 5")



#exercice 6

#pour une machine donnée, on échange deux pièces 
def PERMUTER(s,x,y): #x et y sont les indices des couples
    (piece1,machine1) = trouver_couple_dIndice(x) 
    (piece2,machine2) = trouver_couple_dIndice(y)
    if machine1!=machine2:
        print("on doit permute des tâches sur la même machine!"); return
    machine = machine1
    s_modifié = copy.deepcopy(s)
    s_modifié[machine][piece1],s_modifié[machine][piece2] = s_modifié[machine][piece2],s_modifié[machine][piece1]
    return (s_modifié, GRAPHE(s_modifié))

# print("affichage de PERMUTER(S,1,4)")
# print("nouvelle solution")
# afficher_matrice(PERMUTER(S,6,9)[0])
# print("nouveau graohe")
# afficher_matrice(PERMUTER(S,6,9)[1])

print("fin question 6")


#exercice7
def INITIALISATION(nb_pieces=N,nb_machines=M):
    n= nb_pieces
    m = nb_machines
    s = [ [i for i in range (n)] for i in range(m) ]
    return s
print("INITIALISATION(): ",INITIALISATION())
print("fin question 7")

##exercice  8
# def RechercheTabou():
    # s = INITIALISATION() #premiere solution donnée par l'initialisation
    # Graphe = GRAPHE(s)
    # F = PLC(Graphe,sommet_depart=0)[-1] #makespan est la date de fin d'une tâche donnée #la date de fin du projet
    # compteur = 0
    # iteration = 0
    # S_etoile = copy.deepcopy(s) #meilleur solution
    # F_etoile = F #meilleur objectif
    # nb_pieces,nb_machines = len(s[0]), len(s)
    # taille_graphe = 2 + nb_pieces*nb_machines
    # tabou = np.zeros((taille_graphe,taille_graphe)) #pour interdie des mvt
    
    # while(compteur<100):
        # compteur+=1
        # iteration+=1
        ##determination de N: l'ensemble des paires de tâches critiques pour les échanger
        # N=[]
        # for indice_machine in range(nb_machines):
            # machine = indice_machine+1
            # N.extend( CRITIQUESucc( machine,S_etoile))
        # Best = INF
       ## xBest = yBest = 0
        # for (x,y) in N:
     ##       permuter la paire, calculer son objectif et voir si c'est meilleur
            # G_prime = PERMUTER(s,x,y)[1]
            # print(G_prime)
            # F = PLC(G_prime,sommet_depart=0)[-1] #le makespan
            ##verifier si (x,y) est tel que l'objectif F obtenu par permutation est le meilleur
            # if (F<Best and ( tabou[x][y] < iteration or F<F_etoile) and x!=0 and y!=0):
                # Best = F
                # xBest = x
                # yBest = y
    ##le meilleur (x,y) est trouvé
   ## modifier s par permutation pour en tenir compte
    # s_ap_permutation = PERMUTER(S,xBest,yBest)[0]
    # tabou[xBest][yBest] = iteration+10
    # tabou[yBest][xBest] = iteration+10
    # if Best < F_etoile:
        # S_etoile = s_ap_permutation
        # F_etoile = Best
        # compteur = 0
    # return Best
            
#print("RechercheTabou()",RechercheTabou())      
            
        
                
# print("fin question 8")

