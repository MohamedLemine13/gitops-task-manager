-- ============================================================
-- GitOps Task Manager – PostgreSQL Initialization Script
-- ============================================================
-- Usage:
--   sudo -u postgres psql -f init.sql
-- ============================================================

-- Create the database (ignore error if it already exists)
SELECT 'CREATE DATABASE gitops_tasks'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'gitops_tasks')\gexec

-- Connect to the database
\c gitops_tasks

-- Create the tasks table
CREATE TABLE IF NOT EXISTS tasks (
    id          SERIAL PRIMARY KEY,
    title       VARCHAR(200) NOT NULL,
    description TEXT DEFAULT '',
    status      VARCHAR(20) NOT NULL DEFAULT 'TODO'
                CHECK (status IN ('TODO', 'IN_PROGRESS', 'DONE')),
    created_at  TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Insert sample data (only if table is empty)
INSERT INTO tasks (title, description, status)
SELECT * FROM (VALUES
    ('Configurer le pipeline CI/CD',
     'Mettre en place GitHub Actions avec les étapes build, test et deploy.',
     'TODO'),
    ('Écrire les tests unitaires',
     'Couvrir les endpoints /health, / et /tasks avec pytest.',
     'IN_PROGRESS'),
    ('Déployer avec Ansible',
     'Créer le playbook Ansible pour le déploiement automatique sur le serveur.',
     'DONE')
) AS data(title, description, status)
WHERE NOT EXISTS (SELECT 1 FROM tasks);
