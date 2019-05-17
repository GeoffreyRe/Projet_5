# Projet_5 : Utilisez les données publiques de l'OpenFoodFacts
---------------------------------------------------------------
Ce projet est le 5ème projet de ma formation de "Développeur d'application python" auprès
de l'établissement formateur "OpenClassrooms". OpenClassrooms est un établissement privé
d'enseignement à distance déclaré au rectorat de l'Académie de Paris.

## 1.Informations générales
---------------------------

### 1.1 Nom du projet
---------------------
projet_5 : Utilisez les données publiques de l'OpenFoodFacts

### 1.2 Description du projet
-----------------------------

Le but de ce projet est de créer un programme qui interagirait avec la base Open Food Facts
pour en récupérer les aliments, les comparer et proposer à l'utilisateur un substitut
plus sain à l'aliment qui lui fait envie.  
Plus concrètement, le programme devra pouvoirrécupérer un ensemble de produits grâce à l'API
OpenFoodFact. Ensuite, ce programme sera capable d'insérer un ensemble d'informations au sein
d'une base de données (crée spécialement pour le projet).  
Enfin l'utilisateur pourra alors intéragir avec la base de données par l'intermédiaire du programme. 
  
### 1.3 Description du parcours utilisateur
-------------------------------------------
L'utilisateur est sur le terminal et lance le fichier main.py.
Après un message d'acceuil ainsi qu'un remplissage de la base de données
(qui peut prendre plusieurs minutes), le programme lui affiche les choix suivants :
1. Quels aliments souhaitez-vous remplacer ?
2. Retrouvez mes aliments substitués
3. Quittez le programme 
    
L'utilisateur doit alors faire un choix entre les propositions
(En indiquant le chiffre associé au choix voulu).  
Voyons ensemble les détails de ces différents choix.

#### 1.3.1 Quels aliments souhaitez-vous remplacer
---------------------------------------------------
Si l'utilisateur choisit la première proposition, le programme lui demande ensuite de choisir
parmi un ensemble de catégories (Produits laitiers, Boissons, Petit-déjeuners, Viandes, Desserts).
L'utilisateur choisit une des catégories proposées. En fonction de la catégorie selectionnée par
l'utilisateur, le programme lui retourne un ensemble de sous-catégories et celui-ci demande à
l'utilisateur de faire un choix. L'utilisateur indique au programme quelle sous-catégorie
il souhaite consulter. Le programme retourne à l'utilisateur (au maximum) 10 produits de
cette sous-catégorie sous forme de tableau. Pour chaque produit, un résumé lui est affiché.
L'utilisateur a alors la possibilité d'avoir plus de détails sur chaque produit proposé en
indiquant le chiffre qui lui est associé. Ensuite il indique au programme quel produit il
souhaite substituer. Le programme lui retourne alors (au maximum) 10 produits de cette même
sous-catégorie qui ont un meilleur nutriscore (c'est à dire un nutriscore plus faible).
A nouveau, L'utilisateur peut consulter les détails de chaque substitut avant de faire son
choix. Lorsque le choix est fait, le programme propose à l'utilisateur si il souhaite enregistrer
son choix. L'utilisateur a la possibilité d'accepter ou de refuser cet enregistrement.
Enfin, l'utilisateur est redirigé au niveau du choix de la sous-catégorie.

#### 1.3.2 retrouvez mes aliments substitués
--------------------------------------------

Si l'utilisateur choisit la deuxième proposition, le programme lui affiche un résumé de l'ensemble
des couples produit/substitut que l'utilisateur a enregistré précédemment. L'utilisateur peut alors
consulter le détail de chaque couple de produits en indiquant au programme le numéro associé à la ligne
qu'il souhaite consulter.

#### 1.3.3 Quittez le programme
-------------------------------
Si l'utilisateur choisit la troisième proposition, le programme va simplement se fermer avec un message de
remerciement.

#### 1.3.4 Détails concernant la navigation au sein du menu
-----------------------------------------------------------
Pour "naviguer" au sein du menu, l'utilisateur devra intéragir avec le programme via son clavier.
Le plus souvent, il s'agira d'indiquer au programme le numéro associé au choix voulu. Ensuite, il
suffit juste d'appuyer sur "Enter" pour que le programme prenne en compte ce choix. Dans certains cas,
une réponse de type Oui/Non sera nécessaire. Dans ce cas, il suffit juste d'introduire O pour Oui et
N pour Non avant d'appuyer sur "Enter" pour transmettre le choix au programme.  
Si l'utilisateur souhaite retourner vers un menu précédent, il lui suffit juste d'introduire le chiffre
'0' lorsque le programme lui demande d'effectuer un choix (sauf lorsque le programme attend une réponse
de type Oui/Non).  
Enfin, chaque réponse est vérifiée et si la réponse n'est pas une réponse "possible" (c'est-à-dire si
l'utilisateur entre un mot alors que le programme attend un chiffre, ou lorsque le choix demandé n'existe
pas,...) alors le programme indique à l'utilisateur que la réponse n'est pas correcte et lui propose
d'introduire à nouveau son choix.

## 1.4. Fonctionnalités du projet
---------------------------------
- Recherche d'aliments dans la base Open Food Facts.

- L'utilisateur interagit avec le programme dans le terminal

- Si l'utilisateur entre un caractère qui n'est pas un chiffre,
  le programme doit lui répéter la question,

- La recherche doit s'effectuer sur une base MySql.

## 2. Prérequis pour l'utilisation du projet
-------------------------------------------

### 2.1. Langages utilisés
-------------------------
le langage de programmation utilisé dans ce projet est python.  
Lien pour télécharger python : https://www.python.org/downloads/  
version de python lors du développement : 3.7  
  
Le langage utilisé pour communiquer avec la base de données est le SQL.

### 2.2. Base de données
-----------------------
Dans ce projet, une base de données est utilisée.  
Le système de gestion de base de données relationnelle utilisé est MySQL  
lien pour télécharger MySQL : https://www.mysql.com/downloads/  
version de MySQL lors du développement: 8.0  
De plus, un fichier de création des différentes tables nécessaires
vous est fourni. Vous devez donc, avant toute utilisation du programme,
créer ces tables via ce fichier dans la base de données de votre choix
(avec l'utilisateur MySQL de votre choix).

### 2.3. librairies utilisées:
-----------------------------
Vous pouvez retrouver l'ensemble des librairies utilisées pour ce projet dans le
fichier requirements.txt et tout installer directement via ce fichier grâce à une
commande pip.

### 2.4. fichier "config.json":
------------------------------
Ce fichier au format json contient les informations necessaires permettant la connexion
à la base de données. Vous devez, avant toute utilisation du programme,
spécifier dans ce fichier les différents informations nécessaires.  
Voyons chaque information à fournir:  
  
- "User" = l'utilisateur MySQL avec lequel vous pouvez accéder à la base de données
contenant les tables du projet.  
Exemple: "User" : "Utilisateur1"  
  
- "Initialisation" = paramètre qui permet de savoir si la base de données est déjà remplie ou non.  
Ce paramètre doit valoir 0 si la base n'a pas encore été remplie et 1 si la base de données a déjà 
été remplie.
Ce paramètre se modifie tout seul de 0 à 1 lors du remplissage de la base à la première utilisation.

- "Pw" = Le mot de passe associé à l'utilisateur MySQL fourni dans "User".  
Exemple: "Pw" : "Mon_mot_de_passe"  
  
- "Database" = La base de données MySQL dans laquelle les tables ont été créées.  
Exemple: "Database" : "Projet_5" 

- "Command" = La commande de votre système d'exploitation qui permet "d'effacer" l'affichage du texte
qui est inscrit dans le terminal. Sous windows la commande est "cls", sous Unix (linux, ...) la commande
est "clear",...
la valeur par défaut est "cls"
Exemple : - pour les utilisateurs Windows : "Command" : "cls"
          - pour les utilisateurs linux : "Command" : "clear" 
  
## 3. Structure du projet
-------------------------
Il est à noter que le code associé au projet respecte la PEP8  
Le projet est subdivisé en différents fichiers:  
- Api.py
- ProductClassifier.py
- Bdd.py
- BddIni.py
- Display.py
- Launch.py 
- Main.py 
- config.json 
- dtb_project_5_save.sql
- requirements.txt
  
Chaque fichier contient une seule classe, du même nom que le fichier

### 3.1. Api.py
---------------
Cette classe a la responsabilité de gérer les appels avec l'API 
"OpenFoodFacts" ainsi que de récupérer, grâce à cette API, les informations
nécessaires pour chaque produit.

### 3.2. ProductClassifier.py
-----------------------------
Cette classe a la responsabilité d'analyser et de traiter les informations
des produits récupérés depuis l'API. Par exemple, cette classe permet de vérifier
la pertinence des magasins associés à chaque produit, etc...

### 3.3. Bdd.py
---------------
Cette classe a la responsabilité de récupérer les informations stockées dans
la base de données associée au projet.

### 3.4. BddIni.py
-------------------
Cette classe a la responsabilité d'insérer les différentes données dans les tables
de la base de données associée au projet.

### 3.5. Display.py
-------------------
Cette classe a la responsabilité de gérer l'affichage du menu et la navigation de l'utilisateur
au sein de ce dernier.

### 3.6. Launch.py
------------------
Cette petite classe a la responsabilité de gérer le lancement du programme

### 3.7. Main.py
----------------
Ce fichier est le fichier sur lequel il faut cliquer pour lancer le programme

### 3.8. config.json
-------------------
Ce fichier contient des informations indispensables pour le bon fonctionnement du programme

### 3.9. dtb_project_5_save.sql
------------------------------
Ce fichier au format .sql contient la sauvegarde de la structure de la base de données.
Celui ci permet de créer les différentes tables de la base de données.

### 3.10. requirements.txt
--------------------------
Ce fichier contient les différents packages python nécessaires au projet. 
Il faut installer tous ces packages, sans quoi le programme ne peut fonctionner.

## 4. Informations complémentaires
----------------------------------

### 4.1. Acteurs
----------------
développeur = Geoffrey Remacle

### 4.2. Utilisation d'API
--------------------------
Le projet utilise l'API "OpenFoodFacts"  
lien vers la documentation : https://fr.openfoodfacts.org/data  
Le module requests de python permet la communication avec cette API.

### 4.3. Langue du code
-----------------------
les noms de classes, fonctions, variables, les commentaires, les docstrings,... sont écrits en anglais.

### 4.4. Liens
--------------
Lien vers le repository github:  
https://github.com/GeoffreyRe/Projet_5  
  
Lien vers la page de la formation "Développeur d'Application python":  
https://openclassrooms.com/fr/paths/68-developpeur-dapplication-python  