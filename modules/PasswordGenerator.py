import random

class PasswordGenerator():
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    numbers = '0123456789'
    symbols = '!#$%&()*+'

    def __init__(self, num_letters=8, num_symbols=2, num_numbers=2):
        # Les paramètres peuvent être personnalisés lors de la création de l'instance
        self.num_letters = num_letters
        self.num_symbols = num_symbols
        self.num_numbers = num_numbers

    def generatePassword(self) -> str:
        # Générer chaque type de caractère
        password_letters = [random.choice(self.letters) for _ in range(self.num_letters)]
        password_symbols = [random.choice(self.symbols) for _ in range(self.num_symbols)]
        password_numbers = [random.choice(self.numbers) for _ in range(self.num_numbers)]

        # Combinaison de tous les caractères
        password_list = password_letters + password_symbols + password_numbers
        random.shuffle(password_list)

        # Création du mot de passe final
        return ''.join(password_list)

    def get_password(self):
        # Générer un nouveau mot de passe à chaque appel
        return self.generatePassword()
