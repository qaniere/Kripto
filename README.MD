# Chat Python avec chiffrement asymétrique RSA

## Description du projet

*En cours de rédaction*

## Fonctionalités

*En cours de rédaction*

## Fonctionnement

*En cours de rédaction*

## Liste de choses essentielles à faire

- Corriger le problème de librarie sonore : simpleaudio nécessite le VC++14BT, donc il faut passer sur Winsound

- Gérer les déconnexions coté serveur : Supprimer les données des clients déconnectés.

- Gérer les déconnexions coté client : échec d'envoi du message, déconnexion du serveur.

- Confirmation de fermeture de la fenêtre coté client

- Fermeture du serveur quand l'hôte ferme sa fenêtre

- Chiffrer les conversations : Le client envoi sa clé publique au serveur,  le serveur envoit sa clé au client. Le client chiffre avec la clé du serveur, le serveur déchiffre et réchiffre spécifiquement pour chaque client.

- Gestion des paramétres : Son et remplissage automatique des champs

- Ajouter des commandes : /stop pour stopper le serveur, /ban pour bannir un utilisateur, /op pour le promouvoir

- Pouvoir retourner facilement au menu

- Pouvoir enregistrer des serveurs : Leur ip, leur port, leur nom

## Quand tout cela sera fait

Il faudra alors rédiger de l'aide et de la documentation, à la fois en toplevel dans l'application et aussi faire une page HTML, si jamais le programme ne marche pas. Ensuite, remplir ce README.MD. On pourra alors envisager d'implémenter des fonctions bonus.

## Fonctions bonus :

- Envoyer des fichiers. Il faudrait que chaque client valide le téléchargement du fichier
- Librarie sonore pour Linux et osX
- Petit jeu => PierreFeuilleCiseaux, Pong ect..
- Interface avec bulles de discussion dans Canvas avec Scrollbar
- Appels vocaux ?
