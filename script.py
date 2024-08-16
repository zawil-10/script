import argparse
import os

"""
Utilisation d'argparse pour un script Python qui
manipule des fichiers texte en fonction d'options spécifiées en ligne de commande.
Ce script permet de lire, écrire, concaténer ou vider des fichiers texte.
"""

def lire_fichier(racine_un):
    """
    Préconditions :
    Le fichier spécifié par racine_un doit exister sur le système de fichiers.

    Postconditions :
    Si le fichier existe, la fonction lit et retourne son contenu.
    Si le fichier n'existe pas, la fonction renvoie un message indiquant que le fichier n'a pas été trouvé.
    """
    #print(f"Chemin du fichier à lire : {racine_un}")
    if os.path.exists(racine_un):
        #print("Le fichier existe.")
        try:
            with open(racine_un, 'r') as file:
                contenu = file.read()
                return contenu
        except IOError as e:
            #print(f"Erreur d'accès au fichier '{racine_un}': {str(e)}")
            return f"Erreur d'accès au fichier '{racine_un}': {str(e)}"
    else:
        message = f"Le fichier '{racine_un}' n'existe pas"
        #print(f"Message retourné : '{message}'")
        return message

def ecrire_fichier(racine_deux, contenu):
    """
    Préconditions :
    Le fichier spécifié par racine_deux doit être accessible en écriture sur le système de fichiers.
    
    Postconditions :
    Si le fichier existe et peut être ouvert en mode écriture, la fonction écrit le contenu passé en paramètre dans
    le fichier spécifié et renvoie un message de confirmation.
    Si le fichier n'existe pas, la fonction renvoie un message indiquant que le fichier n'a pas été trouvé.
    """
    try:
        with open(racine_deux, 'w') as file:
            file.write(contenu)
            return f"Le contenu a bien été écrit dans '{racine_deux}'"
    except FileNotFoundError:
        return f"Le fichier '{racine_deux}' n'existe pas"
    except OSError as e:
        return f"Erreur d'accès au fichier '{racine_deux}': {e}"

def concatener_fichiers(racine_trois, fichier_destination):
    """
    Préconditions :
    Chaque chemin de fichier dans la liste racine_trois doit pointer vers un fichier existant.
    Le fichier spécifié par fichier_destination doit être accessible en écriture sur le système de fichiers.

    Postconditions :
    Si tous les fichiers spécifiés dans racine_trois existent et peuvent être ouverts en lecture, leur contenu est
    concaténé dans le fichier spécifié par fichier_destination, avec un saut de ligne ajouté à la fin de chaque
    fichier.
    Si un fichier dans racine_trois n'est pas trouvé, un message est imprimé pour indiquer son absence.
    Si une erreur d'entrée/sortie survient pendant la lecture ou l'écriture des fichiers, un message d'erreur
    approprié est renvoyé.
    """
    fichier_manquant = False
    try:
        with open(fichier_destination, 'a') as destination:
            for fichier in racine_trois:
                if os.path.exists(fichier):
                    try:
                        with open(fichier, 'r') as source:
                            contenu = source.read()
                            destination.write(contenu)
                            destination.write('\n')
                    except IOError as e:
                        print(f"Erreur d'entrée/sortie lors de la lecture du fichier '{fichier}': {e}")
                else:
                    print(f"Le fichier '{fichier}' n'existe pas.")
                    fichier_manquant = True
        if fichier_manquant:
            return "Certains fichiers n'ont pas été trouvés, la concaténation est incomplète."
        else:
            return f"Fichiers concaténés dans '{fichier_destination}'"
    except IOError as e:
        return f"Erreur d'entrée/sortie lors de l'ouverture du fichier de destination '{fichier_destination}': {e}"

def vider_fichier(racine_quatre):
    """
    Préconditions :
    racine_quatre doit spécifier un chemin vers un fichier existant ou non existant.
    Le fichier spécifié par racine_quatre doit être accessible en écriture sur le système de fichiers.

    Postconditions :
    Si le fichier spécifié par racine_quatre existe, son contenu est vidé, et un message confirmant cette opération
    est renvoyé.
    Si le fichier spécifié par racine_quatre n'existe pas, un message est renvoyé pour indiquer son absence.
    """
    racine_quatre = os.path.abspath(racine_quatre)  # Convertir en chemin absolu
    print(f"Vérification de l'existence du fichier : {racine_quatre}")

    # Vérifier si c'est un fichier et non un répertoire
    if os.path.isdir(racine_quatre):
        return f"Erreur : '{racine_quatre}' est un répertoire, pas un fichier."

    if not os.path.exists(racine_quatre):
        #print(f"Le fichier '{racine_quatre}' n'existe pas.")
        return f"Le fichier '{racine_quatre}' n'existe pas."
    
    try:
        #print(f"Vidage du fichier : {racine_quatre}")
        with open(racine_quatre, 'w') as file:
            file.write('')
        return f"Contenu du fichier '{racine_quatre}' vidé."
    except IOError as e:
        #print(f"Erreur d'accès au fichier '{racine_quatre}': {str(e)}")
        return f"Erreur d'accès au fichier '{racine_quatre}': {str(e)}"

# 123 test 
def main():
    parser = argparse.ArgumentParser(description='Manipulation de fichiers')
    parser.add_argument('action', choices=['lire', 'ecrire', 'concatener', 'vider'], help='Action à effectuer')
    parser.add_argument('fichiers', nargs='*', help='Fichier(s) à utiliser')
    parser.add_argument('--destination', help='Chemin du fichier de destination (pour concaténer)')

    args = parser.parse_args()

    if args.action == 'lire':
        for fichier in args.fichiers:
            if os.path.exists(fichier):
                print(lire_fichier(fichier))
            else:
                print(f"Erreur : le fichier '{fichier}' n'a pas été trouvé.")
    elif args.action == 'ecrire':
        if len(args.fichiers) != 1:
            print("Erreur : veuillez spécifier un fichier valide pour l'écriture.")
        else:
            contenu = input("Entrez le contenu à écrire : ")
            print(ecrire_fichier(args.fichiers[0], contenu))
    elif args.action == 'concatener':
        if not args.destination or len(args.fichiers) < 2:
            print("Erreur : veuillez spécifier au moins deux fichiers existants et un fichier de destination.")
        else:
            print(concatener_fichiers(args.fichiers, args.destination))
    elif args.action == 'vider':
        for fichier in args.fichiers:
            if os.path.exists(fichier):
                print(vider_fichier(fichier))
            else:
                print(f"Erreur : le fichier '{fichier}' n'a pas été trouvé.")

if __name__ == '__main__':
    main()
