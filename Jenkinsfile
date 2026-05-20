pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/MohamedLemine13/gitops-task-manager.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    rm -rf venv
                    python3 -m venv venv
                    . venv/bin/activate
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest
                '''
            }
        }

        stage('Deploy with Ansible') {
            steps {
                sh '''
                    ansible-playbook -i ansible/inventory.ini ansible/deploy.yml
                '''
            }
        }
    }
}
