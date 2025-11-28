pipeline {
    agent any

    environment {
        VENV_DIR = ".venv"
        HOST = "0.0.0.0"
        PORT = "5000"
        APP_MODULE = "app:app"  
    }

    triggers { 
        cron('H/5 * * * *') // exécution toutes les 5 minutes 
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Aissam234/Jenkins-CI-CD.git'
            }
        }

        stage('Setup Virtual Environment') {
            steps {
                bat """
                python -m venv ${VENV_DIR}
                call ${VENV_DIR}\\Scripts\\activate
                python -m pip install --upgrade pip
                pip install -r requirements.txt
                """
            }
        }

        stage('Run Tests') {
            when {
                not {
                    changeset "README.md"
                }
            }
            parallel {
                // Option pour arrêter tous les tests si un échoue
                failFast false
                
                stage('Test File 1 - Unit Tests') {
                    steps {
                        script {
                            echo '🧪 Running Unit Tests (test_app.py)...'
                        }
                        bat """
                        call ${VENV_DIR}\\Scripts\\activate
                        python -m pytest test_app.py -v --junitxml=test-results-1.xml
                        """
                    }
                    post {
                        always {
                            junit 'test-results-1.xml'
                        }
                        success {
                            echo '✅ Unit Tests passed!'
                        }
                        failure {
                            echo '❌ Unit Tests failed!'
                        }
                    }
                }
                
                stage('Test File 2 - Integration Tests') {
                    steps {
                        script {
                            echo '🧪 Running Integration Tests (test_app_2.py)...'
                        }
                        bat """
                        call ${VENV_DIR}\\Scripts\\activate
                        python -m pytest test_app_2.py -v --junitxml=test-results-2.xml
                        """
                    }
                    post {
                        always {
                            junit 'test-results-2.xml'
                        }
                        success {
                            echo '✅ Integration Tests passed!'
                        }
                        failure {
                            echo '❌ Integration Tests failed!'
                        }
                    }
                }
                
                stage('Code Coverage') {
                    steps {
                        script {
                            echo '📊 Generating Code Coverage Report...'
                        }
                        bat """
                        call ${VENV_DIR}\\Scripts\\activate
                        python -m pytest --cov=app --cov-report=html --cov-report=xml
                        """
                    }
                    post {
                        success {
                            echo '✅ Coverage report generated!'
                            // Publier le rapport de couverture si le plugin est installé
                            // publishHTML(target: [reportDir: 'htmlcov', reportFiles: 'index.html', reportName: 'Coverage Report'])
                        }
                    }
                }
            }
        }

        stage('Deploy (Local with Gunicorn)') {
            steps {
                echo 'Starting Flask app locally using Gunicorn...'
                bat """
                call ${VENV_DIR}\\Scripts\\activate
                start /B gunicorn --bind ${HOST}:${PORT} ${APP_MODULE} > gunicorn.log 2>&1
                echo ✅ Gunicorn started on http://${HOST}:${PORT}
                """
            }
        }
    }

    post {
        success {
            emailext(
                to: "issamlakhyari452@gmail.com",
                from: "issamlakhyari452@gmail.com",
                replyTo: "issamlakhyari452@gmail.com",
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
                to: "issamlakhyari452@gmail.com",
                from: "issamlakhyari452@gmail.com",
                replyTo: "issamlakhyari452@gmail.com",
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
