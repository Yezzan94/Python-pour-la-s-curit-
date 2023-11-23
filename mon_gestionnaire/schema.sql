-- Crée la table users si elle n'existe pas déjà
CREATE TABLE IF NOT EXISTS users (
    -- Définition de la colonne 'id'
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- Un identifiant unique pour chaque utilisateur, auto-incrémenté
    username TEXT UNIQUE NOT NULL, -- Le nom d'utilisateur, doit être unique et non nul
    password TEXT NOT NULL -- Le mot de passe, requis et ne peut pas être nul
);
