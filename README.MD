# Chat Python avec chiffrement asymétrique RSA

## Description du projet

*En cours de rédaction*

## Fonctionalités

*En cours de rédaction*

## Fonctionnement

*En cours de rédaction*

## Liste de fonctionnalités à implémenter 

- Réparer et nettoyer le chiffrement vignère

- Ajouter un délai pour éviter le spam

- Gérer OverFlow et ValueError 

- Confirmation de fermeture de la fenêtre

- Empêcher les noms d'utilisateur très long (16 caractères max)

- Onglets logs chiffré, l'user choisi un ficher à déchiffré (Qui seront nommées date et heure de début de la conv). A la fermeture du programme / au clic sur un boutton, le fichier sera rechiffré.

- Gestion des paramétres : 

    - [ ] Personaliser le son des messages (Envoi et réception) parmi une sélection 
    - [ ] Choisir un son (Envoi et réception) perso, voir niveau conversion (Faut que ça marche en local)
    - [ ] Choisir un nom d'utilisateur par défaut
    - [ ] Modifier la couleur de la fenêtre
    - [ ] Coordonées de serveur par défaut 
    - [ ] Gestion des logs : Activation / Désativation, choix du mot de passe de chiffrement
    
- Fusioner clé publique et module de chiffrement au niveau de la structure des données, avec un tupple ?

- Pouvoir revenir en arrière lors du choix "Hôte/Client"

- Nombre d'utilisateur connectés maximums

- Afficher nombres d'utilisateurs connectés (Liste ?)

- Ajouter des commandes :
  
    - [ ] /stop : Commande pour stopper le serveur (Confirmation demandée)
    - [ ] /lock - /unlock : Commande pour empêcher l'arrivé de nouveaux utilisateurs
    - [ ] /ban : Commande pour bannir un utilisateur 
    - [ ] /kick : Commande pour jeter l'utilisateur dehors 
    - [ ] /op : Commande qui permet de changer le rôle (Hôte à client, client à hôte)

- Pouvoir enregistrer des serveurs : Leur ip, leur port, leur nom (Sorte d'annuaire)

- Implémenter le Pierre Feuille Ciseaux :

    - [ ] /play pour défier quelqu'un 
    - [ ] /play ok ou /play non pour accepter / refuser la partie
    - [ ] Afficher dans le chat "{user} vient de défier {user2} !"
    - [ ] implémenter le jeu en lui même
    - [ ] Afficher un message de victoire
    
- Envoyer des fichiers :

    - [ ] Chiffrer les fichiers très vite (Threads, ou alors zip avec MDP)
    - [ ] Télécharger fichier coté serveur
    - [ ] Serveur qui propose fichier => "PhotoChat.jpg est dispo, (1.3mo), faite /fichier 1 pour télécharger
    - [ ] Téléchargement du fichier (Mettre une liste d'attente pour pas pénaliser ?)
    - [ ] Suppresion des fichiers à la fin du serveur
    

## Quand tout cela sera fait

- Rédiger l'aide en TopLevel
- Rédiger le rapport

## Fonction bonus :

- Interface avec canvas
