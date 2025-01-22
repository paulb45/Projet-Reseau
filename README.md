# Evolutionary-Game-of-Life
 
## Bibliothèques nécessaires :
- `pygame`
- `pygame_menu`
- `numpy`
- `shapely`
- `TKinter`

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

| Type d'action | id joueur | Coord x | Coord y |
|---------------|-----------|---------|---------|
|      `ANP`    |     id    |    x    |    y    |

#### Céder une propriété réseau
| Type d'action | id joueur | Coord x | Coord y | id Bob | Masse Bob | id nourriture | Energie |
|---------------|-----------|---------|---------|--------|-----------|---------------|---------|
|      `GNP`    |     id    |    x    |    y    |   id   |     M     |       id      |    E

#### Réfuser de céder une propriété réseau
| Type d'action | Coord x | Coord y | 
|---------------|---------|---------|
|      `RNP`    |    x    |    y    |

#### Annonce de déconnexion
| Type d'action | id joueur |
|---------------|-----------|
|      `DEC`    |     id    | 

---

#### **Connexion d'un joueur**

Le protocole pour rejoindre une partie en cours est le suivant :

1. Le nouveau joueur envoie un id et attend 5s.
1. 1. Si il reçoit un de non acceptation d'id (parce qu'un autre joueur utilise cet id), il refait 1.
2. Le joueur place ses items.

#### **Déconnexion d'un joueur**

Cas 1 - déconnexion propre :
1. Le joueur envoie un message de déconnexion

Cas 2 - déconnexion non propre :
1. Un joueur demande une propriété d'un joueur déconnecté de façon non propre
2. Au bout de 3 demande sans réponse (5s d'attente après la 3ème demande), il envoie un message pour annoncer la deconnexion du joueur


A noter : Dès qu'une personne demande la propriété réseau d'une personne deconnecté, il fait deux demande en broadcast et si personne ne répond, il s'approprit la propriété réseau. 


## Test Réseau
### Test du fichier c
#### Test de python vers du broadcast
On a besoin de 3 consoles (A, B, C)
Console A :
`gcc -o main_network main_network.c network.c; ./main_network 10000 10001 10002 10003`

Console B :
pour tester la réception d'un envoi en broadcast 
`netcat -ul 10001`

Console C :
pour simuler l'envoi d'un message python
`echo -n "PLC12345678901234500050005B010000010001" > /dev/udp/localhost/10000`

#### Test du broadcast vers du python
On a besoin de 3 consoles (A, B, C)
Console A :
`gcc -o main_network main_network.c network.c; ./main_network 10000 10001 10002 10003`

Console B :
pour tester la réception d'un envoi en broadcast 
`netcat -ul 10001`

Console C :
pour simuler l'envoi d'un message python
`echo -n "PLC12345678901234500050005B010000010001" > /dev/udp/localhost/10000`
