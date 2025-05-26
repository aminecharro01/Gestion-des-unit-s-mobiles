# Gestion des Unités Mobiles

Un système de gestion pour les unités mobiles médicales, permettant de suivre les unités, le personnel, les équipements et les interventions.

## Fonctionnalités

- Gestion des unités mobiles
- Suivi du personnel médical et de support
- Gestion des équipements
- Suivi des interventions
- Tableau de bord administratif
- Système de notifications
- Interface utilisateur moderne avec Tailwind CSS

## Prérequis

- Python 3.8+
- Django 5.1+
- pip

## Installation

1. Cloner le repository :
```bash
git clone https://github.com/aminecharro01/Gestion-des-unit-s-mobiles.git
cd Gestion-des-unit-s-mobiles
```

2. Créer un environnement virtuel :
```bash
python -m venv myenv
source myenv/bin/activate  # Linux/Mac
myenv\Scripts\activate     # Windows
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

4. Appliquer les migrations :
```bash
python manage.py migrate
```

5. Créer un superutilisateur :
```bash
python manage.py createsuperuser
```

6. Lancer le serveur :
```bash
python manage.py runserver
```

## Structure du Projet

- `units/` : Application principale
  - `models.py` : Modèles de données
  - `views.py` : Vues et logique
  - `templates/` : Templates HTML
  - `static/` : Fichiers statiques
  - `urls.py` : Configuration des URLs

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou à soumettre une pull request.

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails. 