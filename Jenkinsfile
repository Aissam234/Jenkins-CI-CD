pipeline {
    agent any

    environment {
        VENV_DIR = ".venv"
        HOST = "0.0.0.0"
        PORT = "5000"
        APP_MODULE = "app:app"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Aissam234/Jenkins-CI-CD.git',
            }
        }

        stage('Setup Virtual Environment') {
            steps {
                sh """
                python3 -m venv ${VENV_DIR}

                . ${VENV_DIR}/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                """
            }
        }

        stage('Run Tests') {
            steps {
                sh """
                . ${VENV_DIR}/bin/activate
                python -m pytest test_app.py -v
                """
            }
        }

        stage('Deploy (Local with Gunicorn)') {
            steps {
                echo 'Starting Flask app locally using Gunicorn...'
                sh """#!/bin/bash
                # Activate virtual environment
                source ${VENV_DIR}/bin/activate

                gunicorn --bind ${HOST}:${PORT} ${APP_MODULE} \
                    --pid gunicorn.pid \
                    > gunicorn.log 2>&1 &

                echo "✔️  Gunicorn started on http://${HOST}:${PORT}"
                """
            }
        }

    }
}