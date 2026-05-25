⚡ Rodrigue – Multi-Outils Pro v5.0
PythonTkinter48 outilsCode sizeLicence

Application bureautique tout-en-un développée en Python avec Tkinter. 48 outils regroupés dans une interface moderne avec sidebar navigation et thème sombre épuré.

🖥️ Aperçu
Interface : Sidebar navigation, thème sombre professionnel
48 outils accessibles depuis le menu latéral
Responsive : la sidebar s'adapte automatiquement à la taille de la fenêtre
Historique : sauvegarde et export de tous vos calculs
Taux de change en temps réel via API
✅ Prérequis
Python 3.8 ou supérieur
Modules Python (installés automatiquement) :
pip install requests psutil

text


---

## 🚀 Installation

1. **Clonez le dépôt** :
 ```bash
 git clone https://github.com/ton_username/Multi_Outils_Pro.git
 cd Multi_Outils_Pro
Installez les dépendances :
bash

pip install requests psutil
Lancez l'application :
bash

python rodrigue_multi_outils_v5.py
📦 Compiler en .exe (Windows)
bash

pip install pyinstaller
py -m PyInstaller --onefile --windowed --name "Multi_Outils_Pro_v5" rodrigue_multi_outils_v5.py
Le fichier .exe sera dans le dossier dist/.

🛠️ Liste des 48 Outils
📊 Calcul & Mathématiques
#
Outil
Description
1	🧮 Calculatrice Standard	Opérations basiques, mémoire (MC/MR/M+/M-/MS), mode DEG/RAD
2	🔬 Calculatrice Scientifique	sin/cos/tan, log/ln, factoriel, constantes (π, e, φ)
3	📊 Pourcentages	% d'un nombre, augmentation, réduction, valeur initiale
4	📐 Solveur d'Équations	Équations du 1er et 2nd degré (discriminant, racines)
5	📐 Calculateur Géométrique	9 figures : cercle, rectangle, triangle, sphère, cylindre, cône, cube...
6	🔢 Convertisseur de Bases	Binaire, Octal, Décimal, Hexadécimal + ASCII
7	🔢 PGCD / PPCM	Plus Grand Commun Diviseur et Plus Petit Commun Multiple
8	⌨️ Bitwise	Opérations binaires (AND, OR, XOR, NOT, shift)
9	ℏ Constantes Physiques	15 constantes fondamentales + convertisseur eV → Joules
10	📈 Pente	Calcul de la pente entre deux points

💰 Finance & Commerce
#
Outil
Description
11	💱 Convertisseur Devises	EUR, USD, GBP, CAD, XOF — taux en temps réel via API
12	💰 Calculatrice d'Emprunt	Mensualité, intérêts totaux, coût de l'emprunt
13	📈 Intérêts Composés	Calcul d'intérêts composés avec période personnalisée
14	📈 Rentabilité (ROI)	Calcul du retour sur investissement
15	🏷️ Remise	Prix final après remise, montant de la remise
16	🧮 Pourboire	Note + % + partage par personne

📏 Conversions
#
Outil
Description
17	💾 Convertisseur Stockage	bits, B, KB, MB, GB, TB, PB
18	📏 Convertisseur d'Unités	10 catégories : longueur, masse, température, volume, aire, vitesse, pression, énergie, temps, données
19	🎨 Convertisseur Couleurs	HEX ↔ RGB ↔ HSL, preview, couleur complémentaire
20	Ⅶ Nombres Romains	Conversion Arabe ↔ Romain (1-3999)
21	💾 Binaire ↔ Texte	Convertir du texte en binaire et inversement
22	📡 Code Morse	Convertir du texte en code Morse et inversement
23	🆔 UUID	Générer des identifiants uniques universels
24	📍 GPS DMS / Décimal	Conversion de coordonnées GPS

🔐 Sécurité & Texte
#
Outil
Description
25	🔐 Générateur Mots de Passe	Générateur personnalisable + analyseur de force
26	🔐 Hash (MD5/SHA)	Hash en MD5, SHA1, SHA256, SHA512
27	🤫 Chiffrement César / ROT13	Chiffrer/déchiffrer avec décalage personnalisé
28	📝 Outils Texte	Analyse, minuscule/majuscule, Base64, URL encoding
29	🔤 Compteur Avancé	Mots, phrases, temps de lecture, score Flesch
30	🔤 Nombre → Lettres	Convertir un nombre en texte (français)

📅 Dates & Temps
#
Outil
Description
31	📅 Calculateur de Dates	Différence entre dates, ajouter/retirer des jours
32	⏱️ Chronomètre & Minuteur	Chronomètre précis (ms), compte à rebours configurable
33	🗓️ Jours Ouvrables	Calcul de jours ouvrés entre deux dates
34	⏰ Timestamp	Convertir timestamp Unix ↔ date lisible
35	⏰ Calcul d'Heures	Additionner/soustraire des durées

🌐 Réseau & Système
#
Outil
Description
36	🌐 Outils Réseau	CIDR, DNS, IP publique, convertisseur IP
37	💻 Infos Système	CPU, RAM, disque, OS (via psutil)

📊 Statistiques & Probabilités
#
Outil
Description
38	📊 Statistiques	Moyenne, médiane, variance, écart-type
39	🧬 Générateur Aléatoire	Nombre aléatoire, dés, pile/face, loto 6/49
40	📊 Moyenne Pondérée	Calcul de moyenne avec coefficients
41	🔤 Fréquence de Caractères	Analyse de la fréquence de chaque caractère
42	📐 Triangle	Résolution de triangles (angles, côtés, aire)

🏥 Santé & Vie Quotidienne
#
Outil
Description
43	🏥 IMC & Santé	IMC, poids idéal, métabolisme de base (BMR)
44	🎂 Âge	Calcul précis de l'âge en années/mois/jours
45	🌡️ Indice Météo	Wind Chill + Heat Index avec niveaux d'alerte

⚡ Sciences
#
Outil
Description
46	⚡ Électricité	Loi d'Ohm & Puissance (V=RI, P=VI)
47	🏎️ Vitesse	Convertir km/h ↔ mph ↔ m/s ↔ nœuds
48	⛽ Carburant	Consommation, coût par trajet, autonomie

🆕 Nouveautés v5.0
#
Outil
Description
-	📋 JSON	Formater et valider du JSON
-	🔍 Regex	Tester des expressions régulières
-	🔤 Nombre → Lettres	Convertir un nombre en texte français
-	🎂 Âge	Calcul précis de l'âge
-	📈 Intérêts Composés	Intérêts composés avec périodes
-	📡 Code Morse	Encodage/décodage Morse
-	🔗 PGCD / PPCM	Calcul du PGCD et PPCM
-	🆔 UUID	Générateur d'identifiants uniques
-	⏰ Calcul d'Heures	Addition/soustraction de durées
-	📍 GPS DMS/Décimal	Conversion de coordonnées GPS

⌨️ Raccourcis Clavier
Raccourci
Action
Entrée	Calculer
Échap	Effacer (dans certains champs)
Tab / Shift+Tab	Parcourir les champs
Ctrl+C / Ctrl+V	Copier / Coller
Alt + lettres	Menus (Fichier, Outils, Aide)
Molette	Scroller la sidebar et le contenu

📁 Structure
text

Multi_Outils_Pro/
├── rodrigue_multi_outils_v5.py    # Fichier principal (3263 lignes)
├── historique_rodrigue_v5.txt     # Historique (auto-généré)
├── README.md                      # Ce fichier
└── .gitignore                     # Fichiers ignorés par Git
🔧 Dépendances
Module
Version
Requis
Usage
tkinter	—	✅	Interface graphique
requests	2.0+	✅	Taux de change, IP publique
psutil	5.0+	⚡ Optionnel	Infos système détaillées

📜 Licence
Ce projet est sous licence MIT. Libre d'utilisation, modification et distribution.

👨‍💻 Auteur
Rodrigue — Développeur Python

N'hésitez pas à contribuer, reporter des bugs ou proposer de nouveaux outils !
