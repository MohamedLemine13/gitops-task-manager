# GitOps Task Manager 🚀

Application web de gestion de tâches conçue pour être déployée via une pipeline **CI/CD GitOps** complète (GitHub Actions → Jenkins → Ansible).

---

## 📋 Description

**GitOps Task Manager** permet de :

- ✅ Afficher toutes les tâches
- ➕ Ajouter une nouvelle tâche
- 🔄 Changer le statut d'une tâche (TODO → IN_PROGRESS → DONE)
- 🗑️ Supprimer une tâche
- 💚 Endpoint `/health` pour les health-checks CI/CD

### Stack technique

| Composant       | Technologie         |
|-----------------|---------------------|
| Backend         | Python Flask        |
| Frontend        | HTML / CSS / Jinja2 |
| Base de données | SQLite              |
| ORM             | SQLAlchemy          |
| Tests           | pytest              |
| Serveur prod    | Gunicorn            |

---

## 🛠️ Installation

### 1. Prérequis

- Python 3.10+
- pip

> **Note :** SQLite est intégré à Python – aucune installation de base de données externe n'est nécessaire.

### 2. Cloner le projet

```bash
git clone <URL_DU_REPO>
cd gitops-task-manager
```

### 3. Configurer les variables d'environnement

```bash
cp .env.example .env
```

Contenu du fichier `.env` :

```env
DATABASE_URL=sqlite:///tasks.db
SECRET_KEY=change-me-to-a-random-string
```

### 4. Installer les dépendances Python

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 5. Lancer l'application

```bash
source venv/bin/activate
python app.py
```

L'application sera accessible sur : **http://localhost:5000**

La base de données `tasks.db` sera **créée automatiquement** au premier lancement.

---

## 🚀 Déploiement production (Gunicorn)

```bash
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

---

## 🧪 Tests

Les tests utilisent une base **SQLite en mémoire** – isolés et rapides.

```bash
source venv/bin/activate
pytest -v
```

Résultat attendu :

```
tests/test_app.py::TestHealthEndpoint::test_health_returns_ok           PASSED
tests/test_app.py::TestIndexPage::test_index_returns_200                PASSED
tests/test_app.py::TestIndexPage::test_index_contains_title             PASSED
tests/test_app.py::TestTaskCRUD::test_add_task                          PASSED
tests/test_app.py::TestTaskCRUD::test_add_task_empty_title_ignored      PASSED
tests/test_app.py::TestTaskCRUD::test_update_status                     PASSED
tests/test_app.py::TestTaskCRUD::test_delete_task                       PASSED
tests/test_app.py::TestTaskCRUD::test_delete_nonexistent_task_returns_404 PASSED
```

---

## 📁 Structure du projet

```
gitops-task-manager/
│
├── app.py                 # Application Flask (factory pattern)
├── config.py              # Configuration (base + testing)
├── models.py              # Modèle SQLAlchemy Task
├── requirements.txt       # Dépendances Python
├── pyproject.toml         # Configuration pytest
├── .env.example           # Template des variables d'environnement
├── README.md              # Ce fichier
│
├── templates/
│   ├── base.html          # Template de base Jinja2
│   └── index.html         # Page principale
│
├── static/
│   └── style.css          # Feuille de style
│
└── tests/
    └── test_app.py        # Tests pytest
```

---

## 🔗 Routes API

| Méthode | Route                  | Description             |
|---------|------------------------|-------------------------|
| GET     | `/`                    | Page principale         |
| POST    | `/tasks`               | Ajouter une tâche       |
| POST    | `/tasks/<id>/status`   | Changer le statut       |
| POST    | `/tasks/<id>/delete`   | Supprimer une tâche     |
| GET     | `/health`              | Health-check (`{"status": "ok"}`) |

---

## 🔄 Pipeline CI/CD

Ce projet est conçu pour s'intégrer dans :

1. **GitHub Actions** – Build, tests, lint
2. **Jenkins** – Pipeline de déploiement
3. **Ansible** – Provisioning et déploiement automatique

### Avantages de SQLite pour le CI/CD

- ✅ Aucune installation de base de données requise
- ✅ Aucun user/password à configurer
- ✅ Fichier unique `tasks.db` – facile à sauvegarder/restaurer
- ✅ Déploiement simplifié avec Ansible (pas de service PostgreSQL)
- ✅ Compatible avec toutes les machines Linux sans dépendance

---

## 📜 Licence

Projet académique – IRT43.
