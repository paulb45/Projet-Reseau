# Evolutionary-Game-of-Life
 
## Bibliothèques nécessaires :
- `pygame`
- `pygame_menu`
- `numpy`
- `shapely`

Toutes ces bibliothèques sont installables avec l'outil **pip**.

---

## Protocole Réseaux

### Principe du protocole
Le protocole du jeu fonctionnera sur le principe suivant :
- Le **header** permettra de contrôler le type d'action à effectuer ainsi qu'un l'item à son origine qui servira au séquencement des actions. Cette partie est de **taille fixe**.
- Une **partie data**, de taille variable, dépendra entièrement du type d'action précisé dans le header.

Pour l'ensemble des champs, on utilisera la convention suivante :
- Les **actions** sont sur **3 caractères**.
- Les id sont sur 10 caractères.
- Les **coordonnées** sont sur **10 caractères**.
- Les **masses**, **énergies**, et **mouvements** sont sur **5 caractères**.
- Le **type d'item** est sur **1 caractère**.

Important après un champs **type d'item** et nécessairement suivi d'un niveau d'énergie.
Si le type d'item est un Bob, alors le niveau d'énergie est suivi d'une masse et d'un mouvement

#### Exemple de message

| Type d'action (3 char) | id de l'item qui fait l'action | Data (taille variable) |
|------------------------|--------------------------------|------------------------|
|        `PLC`           |               id               |          [DATA]        |

Tous les messages seront analysés comme des chaînes de caractères.

---

### Les événements du jeu

#### **Déplacement**
- **Origine x (10 char)** : La coordonnée x d'origine (avant déplacement). Vaut `0` si le bit de déplacement n'est pas fixé.
- **New x (10 char)** : La coordonnée x qui sera le nouvel emplacement de l'objet.

Un message de déplacement aura la structure suivante :

| Type d'action | acteur | Origine x | Origine y | New x | New y |
|---------------|--------|-----------|-----------|-------|-------|
|     `DPL`     |   id   |    x1     |    y1     |   x2  |   y2  |

---

#### **Placement**

Un message de placement aura la structure suivante :

| Type d'action | acteur | Coord x | Coord y | Type d'item | Energie | (Masse) | (Mouvement) |
|---------------|--------|---------|---------|-------------|---------|---------|-------------|
|      `PLC`    |   id   |    x1   |    y1   |     item    |    E    |    M    |      M      |

---

#### **Manger**
- **Max to eat** : La quantité maximale que l'entité souhaite consommer.
- **Coordonnées** : Coordonnées de l'entité (ex. Bob) et de la nourriture.

Un message pour manger aura la structure suivante :

| Type d'action | acteur | Coord x | Coord y | Energie gagnée | Cible |
|---------------|--------|---------|---------|----------------|-------|
|     `EAT`     |   id   |    x1   |    y1   |       E        |   id  |

---

#### **Attaquer**
- **Coordonnées** : Coordonnées de l'attaque.

Un message d'attaque aura la structure suivante :

| Type d'action | acteur | Coord x | Coord y | Cible |
|---------------|--------|---------|---------|-------|
|      `ATK`    |   id   |    x1   |    y1   |  id   |

---

#### **Disparition**
- **Coordonnées** : Coordonnées de l'objet à faire disparaître.

Un message de disparition aura la structure suivante :

| Type d'action | acteur  | Coord x | Coord y |
|---------------|---------|---------|---------|
|      `DSP`    |   id    |    x1   |    y1   |

#### Annonce de nouveau joueur

| Type d'action | id joueur |
|---------------|-----------|
|      `NEW`    |     id    |

#### Utilisation d'un id

| Type d'action |
|---------------|
|      `UID`    |

#### Demande de propriété réseau

| Type d'action | Coord x | Coord y |
|---------------|---------|---------|
|      `ANP`    |    x    |    y    |

#### Céder une propriété réseau
| Type d'action | id joueur | Coord x | Coord y | Type d'item1 | Energie1 | (Masse1) | (Mouvement1) | Type d'item2 | Energie2 |
|---------------|-----------|---------|---------|--------------|----------|----------|--------------|--------------|----------|
|      `GNP`    |     id    |    x    |    y    |     item1    |    E1    |    M1    |      M1      |     item2    |    E2    |

#### Réfuser de céder une propriété réseau
| Type d'action | Coord x | Coord y | 
|---------------|---------|---------|
|      `RNP`    |    x    |    y    |

---

#### **Connexion d'un joueur**

Le protocole pour rejoindre une partie en cours est le suivant :

1. Le nouveau joueur envoie un id et attend 5s.
1. 1. Si il reçoit un de non acceptation d'id (parce qu'un autre joueur utilise cet id), il refait 1.
2. Le joueur place ses items.

#### **Déconnexion d'un joueur**

A DEFINIR
