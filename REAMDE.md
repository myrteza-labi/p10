# SoftDesk Support API

## Table des matières

- [Introduction](#introduction)
- [Fonctionnalités](#fonctionnalités)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
  - [Lancer le serveur](#lancer-le-serveur)
  - [Authentification](#authentification)
  - [Endpoints de l'API](#endpoints-de-lapi)
- [Tests](#tests)
- [Notes](#notes)
- [Licence](#licence)

## Introduction

SoftDesk Support API est une API RESTful construite avec Django et Django REST Framework, destinée à gérer des projets, des issues (problèmes) et des commentaires. Elle permet aux utilisateurs de s'inscrire, de s'authentifier, de créer des projets, d'ajouter des contributeurs, de créer des issues et d'ajouter des commentaires aux issues. L'API respecte les normes RGPD et utilise l'authentification JWT.

## Fonctionnalités

- **Gestion des utilisateurs** : Inscription avec vérification de l'âge (minimum 15 ans), consentement RGPD, authentification JWT.
- **Gestion des projets** : Création, lecture, mise à jour, suppression de projets. Attribution d'auteurs et de contributeurs.
- **Gestion des issues** : Création, lecture, mise à jour, suppression des issues liées aux projets.
- **Gestion des commentaires** : Ajout et gestion des commentaires sur les issues.
- **Gestion des contributeurs** : Attribution et gestion des contributeurs aux projets.
- **Permissions et sécurité** : Contrôle d'accès basé sur les rôles et permissions.
- **Pagination** : Implémentation de la pagination pour les listes de ressources.

## Prérequis

- **Python** : 3.x
- **Django** : 3.x ou supérieur
- **Django REST Framework**
- **djangorestframework-simplejwt**
- **drf-nested-routers**

## Installation

1. Cloner le dépôt :

git clone https://github.com/myrteza-labi/p10
cd softdesk p10

2. Créer un environnement virtuel :

python -m venv venv  
source venv/bin/activate # Sur Windows : venv\Scripts\activate

3. Installer les dépendances :

pip install -r requirements.txt

Si le fichier `requirements.txt` n'est pas disponible, installez manuellement :

pip install django  
pip install djangorestframework  
pip install djangorestframework-simplejwt  
pip install drf-nested-routers

4. Appliquer les migrations :

python manage.py makemigrations  
python manage.py migrate

5. Créer un superutilisateur (optionnel) :

python manage.py createsuperuser

## Configuration

Fichier : `softdesk/settings.py`

Assurez-vous que les applications et configurations suivantes sont ajoutées :

INSTALLED_APPS = [
 'rest_framework',
 'rest_framework_simplejwt',
 'api',
]

AUTH_USER_MODEL = 'api.User'

REST_FRAMEWORK = {  
 'DEFAULT_AUTHENTICATION_CLASSES': (  
 'rest_framework_simplejwt.authentication.JWTAuthentication',  
 ),  
 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',  
 'PAGE_SIZE': 10,  
}

SIMPLE_JWT = {  
 'AUTH_HEADER_TYPES': ('Bearer',),  
}

## Utilisation

### Lancer le serveur

Démarrez le serveur de développement :

python manage.py runserver

L'API est accessible à `http://localhost:8000/`.

### Authentification

L'API utilise JWT (JSON Web Tokens) pour l'authentification.

#### Inscription

- Endpoint : `POST /api/signup/`
- Corps de la requête :

{  
 "username": "utilisateur1",  
 "password": "motdepasse123",  
 "age": 20,  
 "can_be_contacted": true,  
 "can_data_be_shared": false  
}

#### Connexion

- Endpoint : `POST /api/login/`
- Corps de la requête :

{  
 "username": "utilisateur1",  
 "password": "motdepasse123"  
}

- Réponse :

{  
 "refresh": "<token_refresh>",  
 "access": "<token_access>"  
}

Pour les requêtes nécessitant une authentification, ajoutez l'en-tête suivant :

Authorization: Bearer <token_access>

### Endpoints de l'API

#### Projets

- Lister les projets : `GET /api/projects/`
- Créer un projet : `POST /api/projects/`
- Détails d'un projet : `GET /api/projects/{project_id}/`
- Mettre à jour un projet : `PUT /api/projects/{project_id}/`
- Supprimer un projet : `DELETE /api/projects/{project_id}/`

#### Contributeurs

- Lister les contributeurs : `GET /api/projects/{project_id}/users/`
- Ajouter un contributeur : `POST /api/projects/{project_id}/users/`
- Supprimer un contributeur : `DELETE /api/projects/{project_id}/users/{user_id}/`

#### Issues

- Lister les issues : `GET /api/projects/{project_id}/issues/`
- Créer une issue : `POST /api/projects/{project_id}/issues/`
- Détails d'une issue : `GET /api/projects/{project_id}/issues/{issue_id}/`
- Mettre à jour une issue : `PUT /api/projects/{project_id}/issues/{issue_id}/`
- Supprimer une issue : `DELETE /api/projects/{project_id}/issues/{issue_id}/`

#### Commentaires

- Lister les commentaires : `GET /api/projects/{project_id}/issues/{issue_id}/comments/`
- Ajouter un commentaire : `POST /api/projects/{project_id}/issues/{issue_id}/comments/`
- Détails d'un commentaire : `GET /api/projects/{project_id}/issues/{issue_id}/comments/{comment_uuid}/`
- Mettre à jour un commentaire : `PUT /api/projects/{project_id}/issues/{issue_id}/comments/{comment_uuid}/`
- Supprimer un commentaire : `DELETE /api/projects/{project_id}/issues/{issue_id}/comments/{comment_uuid}/`

## Tests

Vous pouvez tester les endpoints de l'API à l'aide d'outils comme Postman, curl ou l'interface d'administration de Django REST Framework.

### Exemple de flux de test

- **Inscription d'un utilisateur** : Créez un nouvel utilisateur via l'endpoint `/api/signup/`.
- **Authentification** : Connectez-vous via l'endpoint `/api/login/` pour obtenir un token JWT.
- **Création d'un projet** : Utilisez le token JWT pour créer un projet via `/api/projects/`.
- **Ajout de contributeurs** : Ajoutez d'autres utilisateurs comme contributeurs au projet via `/api/projects/{project_id}/users/`.
- **Création d'issues** : Créez des issues pour le projet via `/api/projects/{project_id}/issues/`.
- **Ajout de commentaires** : Ajoutez des commentaires aux issues via `/api/projects/{project_id}/issues/{issue_id}/comments/`.

### Remarques sur les tests

#### Erreur courante

Si vous rencontrez l'erreur suivante lors de la création d'une ressource :

{  
 "project": [
 "Incorrect type. Expected pk value, received str."
 ]  
}

Cela signifie que vous avez fourni une chaîne de caractères au lieu d'une valeur de clé primaire (un entier). Assurez-vous de fournir l'ID numérique du projet.

Exemple corrigé :

{  
 "title": "Problème 1",  
 "description": "Description du problème",  
 "tag": "BUG",  
 "priority": "HIGH",  
 "assignee_user": 1,  
 "status": "TODO",  
 "project": 1  
}

#### Vérification des permissions

Assurez-vous que seuls les contributeurs d'un projet peuvent accéder aux ressources associées. Vérifiez que les permissions sont correctement appliquées pour les opérations de lecture, de création, de mise à jour et de suppression.

#### Pagination

Testez la pagination en ajoutant le paramètre de requête `?page=2` pour accéder aux pages suivantes.

## Notes

### Conformité RGPD

- Les utilisateurs de moins de 15 ans ne peuvent pas s'inscrire.
- Les utilisateurs peuvent choisir s'ils peuvent être contactés et si leurs données peuvent être partagées.

### Gestion des auteurs

- L'auteur d'une ressource est le seul à pouvoir la modifier ou la supprimer.
- Les autres contributeurs peuvent uniquement lire la ressource.

### Droit à l'oubli

Lorsqu'un utilisateur est supprimé, toutes les ressources associées sont également supprimées (`on_delete=models.CASCADE`).

### Architecture du code

Les modèles, sérialiseurs, vues et permissions sont organisés de manière modulaire pour faciliter la maintenance.

### Sécurité

L'API utilise des permissions personnalisées pour contrôler l'accès aux ressources.

<!--
///((/((((((((((((((#############################%#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%###%%%%#############################((((
//(((((((((((((((#(#########################%#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#%%%%#######################((
(((((((((((((((########################%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#%#######################
((((((((((((#######################%%%%%%%%%%%%%%%%%%%%%%%%%%%#(%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#%###################
((((((((((####################%#%%%%%%%%%%%%%%%%%%%%*,.......    ..../#%&%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#################
((((((((#################%##%%%%%%%%%%%%%%%%%%%%#  ..     .,,.  .......,..*&%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#############
(((((((#################%#%%%%%%%%%%%%%%%%%%%%%,         .,.,,,....,,.......(%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#%############
((((################%%%%%%%%%%%%%%%%%%%%%%%%%% .            ....,...,,.,....*&&&&&%%%%%%%%%%%%%%%%%%%%%%%%%%%%##########
((###############%%%%%%%%%%%%%%%%%%%%%%%&%%%,  .   ...                 .... ..#&&&&&&&&&&&%%%%%%%%%%%%%%%%%%%%%#########
((#############%%%%%%%%%%%%%%%%%%%%&&&&&&&%    ...,*//(***/(/,,,,**,..........,&&&&&&&&&&&&%%%%%%%%%%%%%%%%%%%%%########
############%%%%%%%%%%%%%%%%%%%%%&&&&&&&&&....,/(##%%%%&&&&&&&&&&&&&&&%%%##*...&&&&&&&&&&&&&&&&&&&%%%%%%%%%%%%%%%#######
##########%%%%%%%%%%%%%%%%%%%%&&&&&&&&&&&%....*(###%%%%&&&&&&@@@&&&&&&&&&%%%(..#&&&&&&&&&&&&&&&&&&&%%%%%%%%%%%%%%%%#####
#########%%%%#%%%%%%%%%%%%%&&&&&&&&&&&&&&#.,,,*(###%%%%&&&&&&&@@@@&&&&&&&&%%#*,/&&&&&&&&&&&&&&&&&&&&%%%%%%%%%%%%%%%%####
#######%%%%%%%%%%%%%%%%%&&&&&&&&&&&&&&&&&(,***(((##%%%&&&&&&&&&&@&&&&&&&%%%%#(/*&&&&&&&&&&&&&&&&&&&&&&&%%%%%%%%%%%%%####
######%%%%%%%%%%%%%%%%%%&&&&&&&&&&&&&&&&&(**//((((*/***/#%&&&&@@@@&&&&&&&%%%##//&&&&&&&&&&&&&&&&&&&&&&&&&%%%%%%%%%%%%%%#
#####%%%%%%%%%%%%%%%%%%&&&&&&&&&&&&&&&&&&(**////(##%%&%#(((##%%%%%%(//**/((/*/(/&&&&&&&&&&&&&&&&&&&&&&&&&&&%%%%%%%%%%%%%
####%#%%%%%%%%%%%%%&&&%&&&&&&&&&&&&&&&&&&/***/((((*/*,**((/((#%%%#(//(%&%((#(((/&&&&&&&&&&&&&&&&&&&&&&&&&&%%%%%%%%%%%%%%
##%%%%%%%%%%%%%%%%%%&&&&&&&&&&&&&&&&&&&%((/*/(###(/(#####%##(#%&%##%%#%#(((/##(/%%&&&&&&&&&&&&&&&&&&&&&&&&&&&%%%%%%%%%%%
%#%%%%%%%%%%%%%%%&%&&&&&&&&&&&&&&&&&&&%((//*/(###%%%%%%%%%#(##%%%##%%%%%%%&%%%#(#/&&&&&&&&&&&&&&&&&&&&&&&&&&%%%%%%%%%%%%
###%%%%%%%%%%%%%%%&&&&&&&&&&&&&&&&&&&&&(%#/**/(####%%%%&&%((#%&&&%##%%%&&%%%%%##&#&@&&&&&&&&&&&&&&&&&&&&&&&&&&%%%%%%%%%%
%#%%%%%%%%%%%%%%%%&&&&&&&&&&&&&&&&&&&&&(((/**/((###%%&&&%#//,,((( .##&&&&%%%%#((##&&@@@&&&&&&&&&&&&&&&&&&&&&&&%%%%%%%%%%
#%%%%%%%%%%%%%%%%%&&&&&&&&&&&&&&&&&&&&&%#(/,**/((##%%%%%%%%####%##%%%%%%%%%##(/(#&@@@@@&&&&&&&&&&&&&&&&&&&&&&&%%%%%%%%%%
#%%%%%%%%%%%%%%%&%&&&&&&&&&&&&&&&&&&&&&&&&/.,*//((###(//(((##%%&%%#(((((#####(*%&&&&&@&&&&&&&&&&&&&&&&&&&&&&&&&&%%%%%%%%
%%%%%%%%%%%%%%%%&&&&&&&&&&&&&&&&&&&&&&&&&&&,.,,*/(#%##(/***//(////(/*/(##%%#/**@&&@@@@@@@@&&&&&&&&&&&&&&&&&&&&&&%%%%%%%%
%%%%%%%%%%%%%%%%%&&&&&&&&&&&&&&&&&&&&&&&&&&%.,,****(##################%%%%(**,%&&@@@&@@@@&&&&&&&&&&&&&&&&&&&&&&%%%%%%%%%
#%%%%%%%%%%%%%%%&&&&&&&&&&&&&&&&&&&&&&&&&&&&,.,,,***/(((###%%%%%#%%%%###(/**,(&@@@@@@&&&&&&&&&&&&&&&&&&&&&&&&&&&&%%%%%%%
%%%%%%%%%%%%%%%%&&&&&&&&&&&&&&&&&&&&&&&&&&&&%...,,,,,*/*/(##%%%%%%%###(/**,,%&&@@@@@&&&@&&&&&&&&&&&&&&&&&&&&&&&%%%%%%%%%
##%%%%%%%%%%%%%%%&%&&&&&&&&&&&&&&&&&&&&&&&&&&*,,.,,,.,,****/((((#((//*,,,.,#&&&&@@@@@&&&&&&&&&&&&&&&&&&&&&&&&&&&%%%%%%%%
####%%%%%%%%%%%%&&&&&&&&&&&&&&&&&&&&&&&&&&&&@(/***,,.,,,,.,,,*****,...,,,/(#&@&&@@@@&&&&&&&&&&&&&&&&&&&&&&&&&&&&%%%%%%%%
##%%%%%%%%%%%%%%%%&&&&&&&&&&&&&&&&&&&&&&&&&@@@&////**,,,...,,,,,,,..,,**/(#/@&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&%&&%%%%%%%%
###%%%%%%%%%%%%%%%%%&&&&&&&&&&&&&&&&&&&&&@@@@@@@@&((((//****//////////(((###&@@@&&&&@&&&&&&&&&&&&&&&&&&&&&&&&&%&%%%%%%%%
#####%%%%%%%%%%%%%%%&&&&&&&&&&&&&&&&@@&@@@@&@@@@@@@@@####(((((((((########/%&@@@@@@@@@&&&&&&&&&&&&&&&&&&&&&&%%%%%%%%%%%%
######%#%%%%%%%%%%%%%%&&&&&&&&&&@@@@@@@@@@&&@@@@@@@@@@@@%###%%%%%%###%%##(*&&@@@@@@@@@@@@@@@&&&&&&&&&&&&&&&&%%%%%%%%%%%%
######%%%%%%%%%%%%%%%%%&%&%&@@@@@@@@@@@@@@@@&@@@@@@@@@@@@@@&%#%####%%%##(/&&@@@@@@@@@@@@@@@@@@@@@@&&&&&&&%&%%%%%%%%%%%%%
#########%%%%%%%%%%%%%%&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&@%%%%%%%%#(/&&@&&&&&@@@@@@@@@@@@@@@@@@@@@&%&%%%%%%%%%%%%%%%
##########%%%%%%%%%&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%%%%%#((&@&@@&@&&@@@@@@@@@@@@@@@@@@@@@@@@@&%%%%%%%%%%%%%
############%%%%&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%%%%##@@&@&&@@@@@&@@@@@@@@@@@@@@@@@@@@@@@&@&@%%%%%%%%%%%
((##########%&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&@@@@@%%#&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&&%%%%%####
(((######%%&&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%@@@@@@@@@@@@@@@&@@@@@@@@@@@@@@@@@@@@@@@@@@@@&&%%%####
((((((#&&&&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&@%#####
((((#&&&&@&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&@@@@@@@@&@@#####
(((%%&&&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&@@&####
(#%&&&&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&@@@@@@@@&@@&&###
%%&&&&&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&@&@@@&@@&@@&&###
%%&&&&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&@&@&@@@&@@&&@#(#
&&&&&&&@&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&&@&&@@@@@@&&&@(((
%&&&&&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&&&%@@&@@@@@&@@(((
%&@&&&@@@@@@@@@@@@@@@@@@@@@&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&&&&%&@@@@@@%@@@((
-->
