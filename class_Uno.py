#Programme réalisé par Lenny Cohen TG6
from class_carte_et_packet import *
from class_bot1 import*


class Packet_Uno(Packet_carte):       # Sous class Packet_Uno qui reprend la liste et le nom de de la class mere et contient l'enssemble des methode pour jouer au Uno
    def __init__(self, nom, liste_carte=[], sens = 1, index=0, couleur_tempo = None):
        super().__init__("Uno", liste_carte)
        self.sens = sens
        self.index = index
        self.couleur_tempo = couleur_tempo
    
    def create_packet (self):          # Methode qui crée le packet de carte Uno 
        liste_couleur_carte_uno = ["rouge", "bleu", "jaune", "vert"]  #liste des couleur
        packet=[]
        for y in range (4):
            couleur = liste_couleur_carte_uno[y]
            for i in range (1,10) :
                for x in range(2):
                    packet.append(Carte(str(i),i,couleur))
                packet.append(Carte(str(0),0,couleur))
        for i in range (4):
            couleur = liste_couleur_carte_uno[i]
            for y in range(2):
                packet.append(Carte("+2", None, couleur, "+ 2 carte"))
                packet.append(Carte("X", None, couleur, "passe le tour"))
                packet.append(Carte("<->", None, couleur, "change le sens"))
            packet.append(Carte("+4", None, "", "+ 4 carte choisi la couleur"))
            packet.append(Carte("joker", None, "", "choisie la couleur"))
        self.liste_carte = packet
        
        
    def demende_joueur(self, index, dernier_carte, nb_joueur):  #Demande au joueur le numero de la carte qu'il veut jouer jouer puis l'envois a tour qui va verrifier que l'on peut la jouer
        print("Joueur numero :",self.index+1)
        print(dernier_carte)
        print(self.affiche())
        print()
        carte_jouer = int(input("Inseré le numéro de la carte selectionné ou 0 pour pioché : "))
        if carte_jouer == 0:
            self.pioche(1, index, nb_joueur)
            return None
        elif carte_jouer - 1 <= len(self.liste_carte[index]):
            return carte_jouer-1
        else :
            self.demende_joueur(index, dernier_carte, nb_joueur)
        
        
    def change_sens(self):    #Methode pour la carte changement de sens , change la valeur de sens de 1 a -1 ou l'inverse
        if self.sens == 1:
            self.sens = -1
        else :
            self.sens = 1
    
    def pioche(self, nb_carte, index_joueur, nb_joueur):         #Methode qui fait piocher un nombre_carte a une personne avec l'index
        index_joueur = index_joueur % nb_joueur
        for i in range(nb_carte):
            self.liste_carte[index_joueur].append(self.liste_carte[-1][0])
            self.liste_carte[-1].pop(0)
            
    def choisie_couleur(self,couleur = None):                 #Methode qui change la valeur couleur_tempo pour ce tour mais garde la valeur None en couleur de la carte si on doit la repiocher de la carte par celle selectionné par la personne
        if couleur == ["rouge", "bleu", "jaune", "vert"]:
            self.couleur_tempo = couleur
        couleur = input("Choisie la couleur entre vert, rouge, jaune, bleu :")
        liste_couleur_carte_uno = ["rouge", "bleu", "jaune", "vert"]
        if couleur not in liste_couleur_carte_uno :
            self.choisie_couleur(index, index_carte_jouer)
        else :
            self.couleur_tempo = couleur
    
    def passe_tour(self, index):      #Methode qui passe le tour d'un joueur en modifiant l'index et faisant sauté le tour de la personne d'apré
        self.index += self.sens
    
    
    def tour_joueur(self, index, dernier_carte, nb_joueur):   #Methode essentiel de la class Uno verrifie que la carte donné par le joueur peut etres utilisé et agis en fonction sur les carte spécial 
        index_carte_jouer = self.demende_joueur(index, dernier_carte, nb_joueur)
        
        if index_carte_jouer == None:
            return dernier_carte
        carte_jouer = self.liste_carte[index][index_carte_jouer]
        
        if carte_jouer.get_element("couleur") == "": #Verrifie si ses une carte qui peut se jouer tout le temp
            if carte_jouer.get_element("nom") == "+4":
                self.pioche(4,index+self.sens, nb_joueur)
            self.choisie_couleur()
            self.liste_carte[-1].append(dernier_carte)
            dernier_carte = carte_jouer
            self.liste_carte[index].pop(index_carte_jouer)
            return dernier_carte

        elif carte_jouer.get_element("couleur") == dernier_carte.get_element("couleur") or carte_jouer.get_element("nom") == dernier_carte.get_element("nom") or carte_jouer.get_element("couleur") == self.couleur_tempo : #Verrifie si la carte a la meme couleur ou le meme nom si oui il la pose et si est une carte special agis en fonction
            if carte_jouer.get_element("nom") == "+2":
                self.pioche(2, index+self.sens, nb_joueur)
            elif carte_jouer.get_element("nom") == "X":
                self.passe_tour(index)
            elif carte_jouer.get_element("nom") == "<->":
                self.change_sens()
            self.liste_carte[-1].append(dernier_carte)
            dernier_carte = carte_jouer
            self.liste_carte[index].pop(index_carte_jouer)
            self.couleur_tempo = None
            return dernier_carte
        
        else:                                     #Relance la fonction si la carte ne peut t'etres posé
            return self.tour_joueur( index, dernier_carte, nb_joueur)
    
    def affiche(self):
        liste_renvoyer =[]
        for i in range (len(self.liste_carte[self.index])):
            liste_renvoyer.append(i+1)
            liste_renvoyer.append(self.liste_carte[self.index][i])
        return  liste_renvoyer
    
    def play(self, nb_joueur, bot=False):    #Methode principal qui s'occupent d'initialisé l'enssemble et gèrent le jeux et comment il se passe 
        self.create_packet()
        self.melange(10)
        self.liste_carte = self.distribuer(nb_joueur, 7)
        dernier_carte = self.liste_carte[-1][0]
        self.liste_carte[-1].pop(0)
        if bot == False :
            while [] not in self.liste_carte :
                dernier_carte = self.tour_joueur(self.index, dernier_carte, nb_joueur)
                self.index += self.sens
                self.index = self.index % nb_joueur
            print("joueur :", self.index-self.sens," Win the game")
            return None



if __name__ == "__main__":  #Test que le programme fonctionne correctement
    uno =  Packet_Uno("Uno")
    uno.play(2,bot = True)
        


