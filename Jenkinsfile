pipeline {
    agent any
    triggers {
        cron('H/5 * * * *') // run every 5 minutes
     }
    environment {
        APP_NAME = "python-ci-app"
        PYTHON = "python3"
        VENV_DIR = ".venv"
        GITHUB_TOKEN = credentials('github-token') // Jenkins credential ID
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main', 
                    url: 'https://github.com/Aissam234/Jenkins-CI-CD.git',
                    credentialsId: 'github-token'
            }
        }

        stage('Setup Python Environment') {
            steps {
                echo 'Creating and activating virtual environment...'
                sh '''
                    set -e
                    ${PYTHON} -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
    when {
        not {
            changeset "**/README.md"
        }
    }
    parallel {
        stage('Test File 1') {
            steps {
                echo 'Running test_app.py...'
                sh '''
                    set -e
                    . ${VENV_DIR}/bin/activate
                    pytest test_app.py --maxfail=1 --disable-warnings -q
                '''
            }
        }

        stage('Test File 2') {
            steps {
                echo 'Running test_app_2.py...'
                sh '''
                    set -e
                    . ${VENV_DIR}/bin/activate
                    pytest test_app_2.py --maxfail=1 --disable-warnings -q
                '''
            }
        }
    }
}

        stage('Deploy (Local with Gunicorn)') {
            steps {
                echo 'Starting application with Gunicorn...'
                sh '''
                    set -e
                    . ${VENV_DIR}/bin/activate
                    nohup gunicorn app:app --bind 0.0.0.0:8000 &
                    echo "App is running on http://localhost:8000"
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Build and deployment successful!'
            emailext(
                to: 'EMAIL_TO_PLACEHOLDER',
                subject: "✅ SUCCESS: ${APP_NAME} Build #${BUILD_NUMBER}",
                body: "Good job! The pipeline for ${APP_NAME} completed successfully."
            )
        }
        failure {
            echo '❌ Build failed!'
            emailext(
                to: 'EMAIL_TO_PLACEHOLDER',
                subject: "❌ FAILURE: ${APP_NAME} Build #${BUILD_NUMBER}",
                body: "The pipeline for ${APP_NAME} failed. Please check the Jenkins logs."
            )
        }
    }
}
