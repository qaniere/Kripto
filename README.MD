# Chat Python avec chiffrement asymétrique RSA

## Description du projet

*En cours de rédaction*

## Fonctionalités

*En cours de rédaction*

## Fonctionnement

*En cours de rédaction*

## Liste de fonctionnalités à implémenter 

- Gérér le serveur en fond

- Gestion des paramétres : 

    - Gérer les paramètres du serveur 
        - Nombre de participants maximums
        - Mot de passe (Asynchrone)
    - Empêcher l'écriture du séparateur

- Pouvoir revenir en arrière lors du choix "Hôte/Client"

- Nombre d'utilisateur connectés maximums

- Afficher nombres d'utilisateurs connectés

- Ajouter des commandes :
  
    - [ ] /stop : Commande pour stopper le serveur (Confirmation demandée)
    - [ ] /lock - /unlock : Commande pour empêcher l'arrivé de nouveaux utilisateurs
    - [ ] /ban : Commande pour bannir un utilisateur 
    - [ ] /kick : Commande pour jeter l'utilisateur dehors 
    - [ ] /op : Commande qui permet de changer le rôle (Hôte à client, client à hôte)*

- Transformer la fonction réception en thread

- Implémenter le Pierre Feuille Ciseaux :

    - [ ] /play pour défier quelqu'un 
    - [ ] /play ok ou /play non pour accepter / refuser la partie
    - [ ] Afficher dans le chat "{user} vient de défier {user2} !"
    - [ ] implémenter le jeu en lui même
    - [ ] Afficher un message de victoire
    
- Envoyer des fichiers :

    - [ ] Chiffrer les fichiers très vite (Threads)
    - [ ] Télécharger fichier coté serveur
    - [ ] Serveur qui propose fichier => "PhotoChat.jpg est dispo, (1.3mo), faite /fichier 1 pour télécharger
    - [ ] Téléchargement du fichier (Mettre une liste d'attente pour pas pénaliser ?)
    - [ ] Suppresion des fichiers à la fin du serveur

 - Enlever toutes les fast string pour des raisons de compatibilité

 - Rédiger l'aide en TopLevel
