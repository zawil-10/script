import unittest
from unittest.mock import mock_open, patch
import tempfile
import os
from script import lire_fichier, ecrire_fichier, concatener_fichiers, vider_fichier

class TestFileManipulationFunctions(unittest.TestCase):

    def setUp(self):
        self.test_content = "Contenu de test"
        self.temp_files = []

    def tearDown(self):
        for file in self.temp_files:
            if os.path.exists(file):
                os.remove(file)

    def create_temp_file(self, content=''):
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        temp_file.write(content)
        temp_file.close()
        self.temp_files.append(temp_file.name)
        return temp_file.name

    """def test_lire_fichier(self):
        temp_file_name = self.create_temp_file(self.test_content)
        read_content = lire_fichier(temp_file_name)
        self.assertEqual(read_content, self.test_content)

    def test_lire_fichier_fichier_inexistant(self):
        read_content = lire_fichier('fichier_inexistant.txt')
        self.assertEqual(read_content, "Le fichier 'fichier_inexistant.txt' n'existe pas")"""

    def test_ecrire_fichier(self):
        temp_file_name = self.create_temp_file()
        try:
            result = ecrire_fichier(temp_file_name, self.test_content)
            with open(temp_file_name, 'r') as read_file:
                read_content = read_file.read()
            self.assertEqual(result, f"Le contenu a bien été écrit dans '{temp_file_name}'")
            self.assertEqual(read_content, self.test_content)
        finally:
            os.remove(temp_file_name)

    @patch('builtins.open', new_callable=mock_open)
    def test_ecrire_fichier_fichier_non_accessible(self, mock_open):
        mock_open.side_effect = OSError("Erreur d'accès")
        result = ecrire_fichier('fichier_non_accessible.txt', self.test_content)
        self.assertIn("Erreur d'accès", result)

    def test_concatener_fichiers(self):
        temp_file1 = self.create_temp_file(self.test_content)
        temp_file2 = self.create_temp_file(self.test_content)
        temp_file_dest = self.create_temp_file()
        result = concatener_fichiers([temp_file1, temp_file2], temp_file_dest)
        with open(temp_file_dest, 'r') as read_file:
            read_content = read_file.read()
            expected_content = self.test_content + '\n' + self.test_content + '\n'
            self.assertEqual(read_content, expected_content)
        self.assertEqual(result, f"Fichiers concaténés dans '{temp_file_dest}'")

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', side_effect=lambda x: False)  # Simule l'absence de tous les fichiers
    def test_concatener_fichiers_fichiers_inexistants(self, mock_exists, mock_open):
        temp_file_dest = self.create_temp_file()
        result = concatener_fichiers(['fichier_inexistant1.txt', 'fichier_inexistant2.txt'], temp_file_dest)
        self.assertEqual(result, "Certains fichiers n'ont pas été trouvés, la concaténation est incomplète.")

    @patch('builtins.open', new_callable=mock_open)
    def test_vider_fichier(self, mock_open):
        # Mock l'appel à open pour simuler l'écriture dans le fichier
        mock_open.return_value.write = mock_open()
        temp_file_name = 'fichier_test.txt'
        result = vider_fichier(temp_file_name)
        self.assertEqual(result, f"Contenu du fichier '{temp_file_name}' vidé.")

if __name__ == '__main__':
    unittest.main()
