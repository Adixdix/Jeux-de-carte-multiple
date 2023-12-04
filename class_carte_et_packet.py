#Code réalisé par Lenny Cohen
import random

class Carte ():                                                #Classe Carte qui definis les carte et a plusieur methodes differentes selon les jeux de carte 
    def __init__(self, nom:str, valeur:int, couleur:str, effet = None):   # et une methode get_element afin de ne pas brisé l'encapsulation
        self.nom = nom
        self.valeur = valeur
        self.couleur = couleur
        self.effet = effet
        
        
    def comparaison(self, comparable):
        """compare les valeur de l'element et de celle de comparable qui est insséré ,ne mettre qu'une autre cart"""
        if self.valeur > comparable.valeur:
            return self
        else:
            return comparable

    def type_couleur(self):
        """ A utilisé pour le packet de base afin de savoir quelle est la couleur entre rouge et noir"""
        if self.couleur == "Coeur" or self.couleur == "Carreaux":
            return "red"
        elif self.couleur == "Pick" or self.couleur == "Trefle":
            return "black"
        return self.couleur
    
    def get_element (self, nom : str):
        """ Permet de recupéré un elelment de la carte sans brisé l'encapsulation via "nom" qui peut etres seulement "couleur" "valeur" "effet" "nom" """
        if nom == "couleur" : return self.couleur
        if nom == "valeur" : return self.valeur
        if nom == "effet" : return self.effet
        if nom == "nom" : return self.nom
        else : return None
    
    def __repr__(self):
        return "nom :"+str(self.nom)+"   couleur :"+self.couleur + "\n"
    
        
    
class Packet_carte():
    def __init__(self, nom : str, liste_carte : list) :
        self.nom = nom
        self.liste_carte = liste_carte
        
    def melange (self, nb_fois = 1):       #Methode de la class Packet_carte qui melange l'enssemble du packet un nb de fois definis a 1 si pas changé
        index_tempo = 0                    #Change la valeur entre chaque carte de facon aleatoir et renvoi rien car modifie dirrectement la liste_carte
        val_tempo = 0
        for i in range(nb_fois):
            for y in range(len(self.liste_carte)):
                index_tempo = random.randint(0, len(self.liste_carte)-1)
                val_tempo = self.liste_carte[index_tempo]
                self.liste_carte[index_tempo] = self.liste_carte[i]
                self.liste_carte[i] = val_tempo
        """Melange les carte du packet de facon aleatoir avec 'nb_fois' qui defini le nombre de melange fait si pas precisé 1 seul melange"""
        
        
        
    def distribuer (self, nb_personne : int, nb_carte = None): #Methode de la class Packet_carte qui distribue les carte au differente partie via une liste de liste qui correspond a chaque personne
        liste_deck = [[]for i in range(nb_personne)]                         #on peut spécifier le nb de carte a distribué , si on le specifie pas sa distribu toutes les carte et si on specifie le nb de carte
        if nb_carte is None :                                 # alors la derniere liste est la pioche.
            for i in range(len(self.liste_carte)):
                liste_deck[i % nb_personne].append(self.liste_carte[i])
        else :
            for i in range(nb_carte*nb_personne):
                liste_deck[i % nb_personne].append(self.liste_carte[0])
                self.liste_carte.pop(0)
            liste_deck = liste_deck + [self.liste_carte]
        return liste_deck
    """Distribue les carte a nb_personne et nb_carte si il y a besoin de precisé si ses le cas , la dernier liste sera la pioche qui contiendra le reste des carte """
    def __repr__(self):
        return "nom : " + self.nom + "  packet : " + self.liste_carte
                


def create_packet_base(liste_type): #Crée le packet ded carte de 54 carte basique (Coeur, pick,etc)(As......roi)
    packet=[]
    for y in range (4):
        couleur = liste_type[y]
        for i in range (1,14) :
            if i == 13 :
                packet.append(Carte("As",i,couleur))
            elif i == 10 :
                packet.append(Carte("Valet",i,couleur))
            elif i == 11 :
                packet.append(Carte("Dame",i,couleur))
            elif i == 12 :
                packet.append(Carte("Roi",i,couleur))
            else:
                packet.append(Carte(str(i+1),i,couleur))
    return Packet_carte("carte de base", packet)


liste_type_carte = ["Coeur", "Carreaux", "Pick", "Trefle"]  #liste des type de carte pour le jeux basique des carte

packet_base = create_packet_base(liste_type_carte)     #variable contenan le packet de carte basique     

    
if __name__ == "__main__":
    print(Carte("As", 13, "Pick").comparaison(Carte("roi", 12, "Coeur")))   #quelsue test des class et methode
    packet_base.melange(10)
    deck =packet_base.distribuer(6)
    print(deck[0])
    print(deck[0][0].get_element("valeur"))











