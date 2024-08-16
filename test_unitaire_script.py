import unittest
from unittest.mock import mock_open, patch
import tempfile
import os
from script import lire_fichier, ecrire_fichier, concatener_fichiers, vider_fichier

class TestFonctionsManipulationFichiers(unittest.TestCase):

    def setUp(self):
        self.contenu_test = "Contenu de test"
        self.fichiers_temp = []

    def tearDown(self):
        for fichier in self.fichiers_temp:
            if os.path.exists(fichier):
                os.remove(fichier)

    def creer_fichier_temporaire(self, contenu=''):
        fichier_temp = tempfile.NamedTemporaryFile(mode='w', delete=False)
        fichier_temp.write(contenu)
        fichier_temp.close()
        self.fichiers_temp.append(fichier_temp.name)
        return fichier_temp.name

    def test_lire_fichier_existant(self):
        nom_fichier_temp = self.creer_fichier_temporaire(self.contenu_test)
        contenu_lu = lire_fichier(nom_fichier_temp)
        self.assertEqual(contenu_lu, self.contenu_test)
    #test au cas ou le fichier n'existe pas 
    def test_lire_fichier_inexistant(self):
        fichier_inexistant = os.path.join("nonexistent_directory", "fichier_inexistant.txt")
        contenu_lu = lire_fichier(fichier_inexistant)
        self.assertEqual(contenu_lu, f"Le fichier '{fichier_inexistant}' n'existe pas")

    def test_ecrire_fichier_nouveau(self):
        nom_fichier_temp = self.creer_fichier_temporaire()
        resultat = ecrire_fichier(nom_fichier_temp, self.contenu_test)
        self.assertEqual(resultat, f"Le contenu a bien été écrit dans '{nom_fichier_temp}'")
        with open(nom_fichier_temp, 'r') as f:
            self.assertEqual(f.read(), self.contenu_test)
  # on fait des teste pour voir si le fichier existe 
    def test_ecrire_fichier_existant(self):
        nom_fichier_temp = self.creer_fichier_temporaire("Ancien contenu")
        resultat = ecrire_fichier(nom_fichier_temp, self.contenu_test)
        self.assertEqual(resultat, f"Le contenu a bien été écrit dans '{nom_fichier_temp}'")
        with open(nom_fichier_temp, 'r') as f:
            self.assertEqual(f.read(), self.contenu_test)

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    def test_ecrire_fichier_erreur_acces(self, mock_file, mock_exists):
        mock_file.side_effect = OSError("Erreur d'accès")
        resultat = ecrire_fichier('fichier_test.txt', self.contenu_test)
        self.assertIn("Erreur d'accès au fichier", resultat)
# on fait des teste pour voir si le fichier existe 
    def test_concatener_fichiers_existants(self):
        fichier_temp1 = self.creer_fichier_temporaire("Contenu 1\n")
        fichier_temp2 = self.creer_fichier_temporaire("Contenu 2\n")
        fichier_dest = self.creer_fichier_temporaire()
        resultat = concatener_fichiers([fichier_temp1, fichier_temp2], fichier_dest)
        self.assertEqual(resultat, f"Fichiers concaténés dans '{fichier_dest}'")
        with open(fichier_dest, 'r') as f:
            self.assertEqual(f.read(), "Contenu 1\n\nContenu 2\n\n")

    def test_concatener_fichiers_inexistants(self):
        fichier_dest = self.creer_fichier_temporaire()
        resultat = concatener_fichiers(['inexistant1.txt', 'inexistant2.txt'], fichier_dest)
        self.assertEqual(resultat, "Certains fichiers n'ont pas été trouvés, la concaténation est incomplète.")

    def test_vider_fichier_existant(self):
        temp_file = self.creer_fichier_temporaire("Contenu à vider")
        resultat = vider_fichier(temp_file)
        self.assertEqual(resultat, f"Contenu du fichier '{temp_file}' vidé.")
        with open(temp_file, 'r') as f:
            self.assertEqual(f.read(), '')

    def test_vider_fichier_inexistant(self):
        fichier_inexistant = os.path.join(tempfile.gettempdir(), 'fichier_inexistant.txt')
        
        # on supprime le fichier s'il existe déjà
        if os.path.exists(fichier_inexistant):
            os.remove(fichier_inexistant)
        
        resultat = vider_fichier(fichier_inexistant)

        # comparer uniquement la partie importantant du message 
        self.assertIn("n'existe pas", resultat)

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    def test_lire_fichier_erreur_acces(self, mock_file, mock_exists):
        mock_file.side_effect = IOError("Erreur d'accès")
        contenu_lu = lire_fichier('fichier_test.txt')
        self.assertIn("Erreur d'accès au fichier 'fichier_test.txt'", contenu_lu)

    def test_concatener_fichiers_vides(self):
        fichier_vide1 = self.creer_fichier_temporaire('')
        fichier_vide2 = self.creer_fichier_temporaire('')
        fichier_dest = self.creer_fichier_temporaire()
        
        resultat = concatener_fichiers([fichier_vide1, fichier_vide2], fichier_dest)
        self.assertEqual(resultat, f"Fichiers concaténés dans '{fichier_dest}'")
        with open(fichier_dest, 'r') as f:
            self.assertEqual(f.read(), '\n\n')

if __name__ == '__main__':
    unittest.main()
