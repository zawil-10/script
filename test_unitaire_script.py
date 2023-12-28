import unittest
import tempfile
from script import*


class Test_fonctions_fichier(unittest.TestCase):

    def setUp(self):
        # Créer un fichier temporaire pour lire
        self.fichier_test = tempfile.NamedTemporaryFile(mode='w', delete=False)
        self.fichier_test.write('Contenu du fichier de test.')
        self.fichier_test.close()

        # Créer un fichier temporaire pour concaténer
        self.fichier1 = tempfile.NamedTemporaryFile(mode='w', delete=False)
        self.fichier1.write('Contenu fichier 1')
        self.fichier1.close()

        # Créer un autre fichier temporaire pour concaténer
        self.fichier2 = tempfile.NamedTemporaryFile(mode='w', delete=False)
        self.fichier2.write('Contenu fichier 2')
        self.fichier2.close()

    def tearDown(self):
        # Supprimer les fichiers temporaires créés pour les tests
        import os
        os.unlink(self.fichier_test.name)
        os.unlink(self.fichier1.name)
        os.unlink(self.fichier2.name)

    def test_lire_fichier(self):
        # Teste si la fonction lire_fichier renvoie le contenu attendu d'un fichier existant
        contenu = lire_fichier(self.fichier_test.name)
        self.assertEqual(contenu, "Contenu du fichier de test.")

        # Teste si la fonction lire_fichier renvoie un message si le fichier n'existe pas
        resultat = lire_fichier('fichier_inexistant.txt')
        self.assertEqual(resultat, "Le fichier 'fichier_inexistant.txt' n'existe pas")

    # ... Les autres tests ...


if __name__ == '__main__':
    unittest.main()
