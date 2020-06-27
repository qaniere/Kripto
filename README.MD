# Kripto

Kripto est un chat chiffré peer to peer. Tous les messages sont chiffrés avec l'algorithme RSA, ce qui le rend sécurisé. Les messages peuvent être
échangés au sein d'un réseau local mais également à travers Internet, à condition d'avoir mis en place des redirections NAT (Voir la page installation).

Ce projet a été réalisé par Calixte Pistolet et Quentin Aniere dans le cadre de l'enseignement de spécialité "Numérique et Sciences Informatiques". Il est sous license MIT. Toute contribution est la bienvenue.

## Fonctionalités

 - Discussion peer to peer chiffrée : Seuls les participants de la conversation peuvent voir les messages (Même en cas d'attaque Man in the Middle)
 - Protection du serveur avec un mot de passe : Seules les personnes qui ont le mot de passe peuvent accéder au serveur
 - Panel de commandes pour les hôtes :
    
    - /stop : Permet d'arrêter le serveur (Commande pour l'hôte de la disscusion uniquement)
    - /lock : Verrouile le serveur et empêche l'arrivée de nouveaux clients 
    - /unlock : Déverouiller le serveur pour autoriser l'arrivée de nouveaux clients
    - /ban {NomDuClient} : Permet de bannir un client du serveur : Banni son IP
    - /kick {NomDuClient} : Force la déconnexion d'un client
    - /op : Permet de promouvoir  un client au rang d'administrateur, il pourra alors bannir et kicker du serveur. Pour rétrograder, utiliser la même commande.

 - Sauvegarde des messages chiffrée avec mot de passe
 - Notification sur le bureau quand l'application est inactive (Windows 10 uniquement)
 - Personnalisation des sons de réception et d'envoi
 - Possibilité de choisir son propre son d'envoi (Au format Wav)
 - Report de bug avec un bot qui créée Issues Git
 
## Instalation

  ### Version Portable
 
    Téléchargez le fichier zip disponible dans la dernière release, et exécutez "Kripto.exe"
    
   ### Installateur 
   
     Téléchargez le setup et suivez les instructions
  
   ### Depuis le code source
   
    - Installez au moins la version 3.6 de Python
    - Installez les dépendances avec la commande `pip install -r requirements.txt`
    - Exécutez "Application.pyw"

## Pour communiquer en dehors d'un résau local

  Il faut mettre en place des redirections NAT sur votre routeur / box. Pour ce faire, suivez ces étapes :

    - Connectez vous à l'interface web de votre router / box (Généralement http://192.168.1.1)
    - Trouvez l'option "NAT.PAT" (Le nom est peut être différent selon les constructeurs )
    - Redirigez les requêtes sur la machine qui fait tourner Kripto en mode hôte. Exemple, je fais 
      tourner Kripto sur mon ordinateur qui a l'Ip 192.168.1.29. Le port que j'ai choisi est le 1234, 
      je dois donc redirigez les requêts vers mon ordinateur sur le port 1234.
    - Communiquez votre adresse Ip publique à vos clients : https://api.ipify.org/
    

## Fonctionnement

*En cours de rédaction*
