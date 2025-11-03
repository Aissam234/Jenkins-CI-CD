pipeline {
    agent any

    environment {
        GITHUB_TOKEN = credentials('github-token')  // must exist in Jenkins credentials
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
                    credentialsId: 'github-token'
            }
        }

        stage('Setup Virtual Environment') {
            steps {
                sh '''
                python3 -m venv ${VENV_DIR}
                source ${VENV_DIR}/bin/activate
                python -m pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            when {
                not {
                    changeset "README.md"
                }
            }
            parallel {
                stage('Test File 1') {
                    steps {
                        sh '''
                        source ${VENV_DIR}/bin/activate
                        python -m pytest test_app.py -v
                        '''
                    }
                }
                stage('Test File 2') {
                    steps {
                        sh '''
                        source ${VENV_DIR}/bin/activate
                        python -m pytest test_app_2.py -v
                        '''
                    }
                }
            }
        }

        stage('Deploy (Local with Gunicorn)') {
            steps {
                echo '🚀 Starting Flask app locally using Gunicorn...'
                sh '''
                #!/bin/bash
                source ${VENV_DIR}/bin/activate
                nohup gunicorn --bind ${HOST}:${PORT} ${APP_MODULE} \
                    --pid gunicorn.pid > gunicorn.log 2>&1 &
                echo "✅ Gunicorn started on http://${HOST}:${PORT}"
                '''
            }
        }
    }

    post {
        success {
            emailext(
                to: "EMAIL_TO_PLACEHOLDER",
                from: "EMAIL_FROM_PLACEHOLDER",
                replyTo: "EMAIL_REPLY_PLACEHOLDER",
                subject: "✅ SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                mimeType: 'text/html',
                body: """\
                <p>Good news!</p>
                <p>Build <b>${env.JOB_NAME} #${env.BUILD_NUMBER}</b> succeeded.</p>
                <p>Check details: <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                """
            )
        }

        failure {
            emailext(
                to: "EMAIL_TO_PLACEHOLDER",
                from: "EMAIL_FROM_PLACEHOLDER",
                replyTo: "EMAIL_REPLY_PLACEHOLDER",
                subject: "❌ FAILURE: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                mimeType: 'text/html',
                body: """\
                <p>Uh oh...</p>
                <p>Build <b>${env.JOB_NAME} #${env.BUILD_NUMBER}</b> failed.</p>
                <p>Check logs: <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                """
            )
        }
    }
}

