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
- Le **header** permettra de contrôler le type d'action à effectuer ainsi qu'un **timestamp** qui servira au séquencement des actions. Cette partie est de **taille fixe**.
- Une **partie data**, de taille variable, dépendra entièrement du type d'action précisé dans le header.

Pour l'ensemble des champs, on utilisera la convention suivante :
- Les **actions** sont sur **3 caractères**.
- Les **coordonnées** sont sur **10 caractères**.
- Les **masses**, **énergies**, et **mouvements** sont sur **5 caractères**.
- Le **type d'item** est sur **1 caractère**.

#### Exemple de message

| Type d'action (3 char) | Data (taille variable) |
|-------------------------|------------------------|
|        `PLC`           |         [DATA]        |

Tous les messages seront analysés comme des chaînes de caractères.

---

### Les événements du jeu

#### **Déplacement**
- **Origine x (10 char)** : La coordonnée x d'origine (avant déplacement). Vaut `0` si le bit de déplacement n'est pas fixé.
- **New x (10 char)** : La coordonnée x qui sera le nouvel emplacement de l'objet.

Un message de déplacement aura la structure suivante :

| Type d'action | Origine x | Origine y | New x | New y |
|---------------|-----------|-----------|-------|-------|
|      `DPL`    |    x1     |    y1     |   x2  |   y2  |

---

#### **Placement**

Un message de placement aura la structure suivante :

| Type d'action | Timestamp  | Coord x | Coord y | Type d'item | Energie | Masse | Mouvement |
|---------------|------------|---------|---------|-------------|---------|-------|-----------|
|      `PLC`    | hh:mm:ss   |    x1   |    y1   |     item    |    E    |   M   |     M     |

---

#### **Manger**
- **Max to eat** : La quantité maximale que l'entité souhaite consommer.
- **Coordonnées** : Coordonnées de l'entité (ex. Bob) et de la nourriture.

Un message pour manger aura la structure suivante :

| Type d'action | Timestamp  | Max to eat | Coord x | Coord y |
|---------------|------------|------------|---------|---------|
|      `EAT`    | hh:mm:ss   |     V      |    x1   |    y1   |

---

#### **Attaquer**
- **Coordonnées** : Coordonnées de l'attaque.

Un message d'attaque aura la structure suivante :

| Type d'action | Timestamp  | Coord x | Coord y |
|---------------|------------|---------|---------|
|      `ATK`    | hh:mm:ss   |    x1   |    y1   |

---

#### **Disparition**
- **Coordonnées** : Coordonnées de l'objet à faire disparaître.
- **Type d'item (1 char)** : `B` pour Bob, `F` pour nourriture.

Un message de disparition aura la structure suivante :

| Type d'action | Timestamp  | Coord x | Coord y | Type d'item |
|---------------|------------|---------|---------|-------------|
|      `DSP`    | hh:mm:ss   |    x1   |    y1   |     item    |

---

#### **Connexion d'un joueur**

Le protocole pour rejoindre une partie en cours est le suivant :

1. Un nouveau joueur envoie un message en broadcast pour annoncer qu'il rejoint la partie en indiquant les stats de ses Bobs. Si les stats totales ne sont pas cohérentes avec les règles du jeu, les joueurs en cours ignorent la demande.
2. Les joueurs lui envoient une **snapshot** du jeu. Il retient la première snapshot reçue comme valide.
3. Tout en faisant évoluer le jeu en local, il cherche à placer l'ensemble de ses Bobs. Une fois tous les Bobs placés, il commence à "jouer".

##### Contenu des messages dans l'ordre d'envoi :

| Type d'action | Timestamp  | Masse | Mouvement des Bobs |
|---------------|------------|-------|--------------------|
|      `NEW`    | hh:mm:ss   |   M   |         M          |

---

#### **Déconnexion d'un joueur**

La déconnexion d'un joueur n'est pas gérée. Un joueur déconnecté n'effectuera plus d'actions, et ses entités (ex. Bobs) disparaîtront au fur et à mesure du jeu.
