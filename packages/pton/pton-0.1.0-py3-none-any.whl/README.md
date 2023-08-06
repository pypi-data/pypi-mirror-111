Bonjour,

Voici notre projet Générateur aléatoire de villes dans le cours de PTON.

Vous trouverez dans ce dossier :

- un fichier README.md
- un dossier src/ avec comme fichier :
    - city.py
    - district.py
    - buildings.py
    - street.py
    - viewer.py
    - area.py
    - tests.py
    - tools.py

Tout d'abord, nous nous excusons, car nous n'avons pas réussi à lancer poetry pour des raisons techniques.
Nous vous demandons donc de lancer le programme tel que conseiller ci-dessous, à l'aide de PyCharm et du terminal.

Pour lancer le programme :
Le main se trouve dans le fichier city.py, qui génère actuellement une ville de 10000 habitants.
Le main de city est à lancer à l'aide de PyCharm.
Pour pouvoir afficher la ville générée par le programme, lancer dans le terminal :
``$ python[3] src/viewer.py /tmp/city.json``

On obtient alors une ville divisée par des rues principales en plusieurs quartier en fonction de sa taille.
La taille de la ville varie en fonction du nombre d’habitants.

La ville contient :
- des maisons en marron
- des parcs en vert foncé
- 10% d’hôtels particuliers parmi les maisons en gris/violet (à ne pas confondre avec les églises, plus claires)
- une église en violet pâle par quartier
- de grands points d’eau en bleu
- 0, 1 ou 2 marchés par quartier
- une cathédrale en bleu foncé

La ville peut avoir des murs tout autour, ainsi que des douves en mettant dans son constructeur les booléens respectifs has_walls et has_river à True.
Elle peut avoir un quartier dédié à son château-fort avec le booléen has_castle.

Merci.

Emma Rachlin
Maxence Ramos-Pariente