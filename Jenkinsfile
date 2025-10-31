pipeline {
    agent any   // Use any available Jenkins agent

    // ===== Global Environment Variables =====
    environment {
        GITHUB_REPO = 'https://github.com/Aissam234/Jenkins-CI-CD.git'
        HOST = '0.0.0.0'
        PORT = '8000'
        APP_MODULE = 'app:app'          // Flask app entry point (modify if needed)
        VENV = 'venv'
    }

    // ===== Automatic Triggers =====
    triggers {
        // Build every 5 minutes (cron syntax)
        cron('H/5 * * * *')
    }

    stages {

        // ===== 1️⃣ CHECKOUT =====
        stage('Checkout') {
            steps {
                echo 'Cloning source code from GitHub...'
                git branch: 'main',
                    credentialsId: 'github-token',
                    url: "${GITHUB_REPO}"
            }
        }

        // ===== 2️⃣ SETUP ENVIRONMENT =====
        stage('Setup Virtual Environment') {
            steps {
                echo 'Creating Python virtual environment and installing dependencies...'
                sh '''
                python3 -m venv ${VENV}
                . ${VENV}/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                python --version
                '''
            }
        }

        // ===== 3️⃣ RUN TESTS =====
        stage('Run Tests') {
            when {
                // Skip tests if only README.md changed
                not {
                    changeset pattern: "README.md", comparator: "INCLUDE"
                }
            }
            steps {
                echo 'Running pytest...'
                sh '''
                source ${VENV}/bin/activate
                pytest --maxfail=1 --disable-warnings -q
                '''
            }
        }

        // ===== 4️⃣ DEPLOY =====
        stage('Deploy') {
            steps {
                echo 'Starting Flask app with Gunicorn...'
                sh '''
                source ${VENV}/bin/activate
                nohup gunicorn --bind ${HOST}:${PORT} ${APP_MODULE} > gunicorn.log 2>&1 &
                '''
            }
        }
    }

    // ===== POST BUILD ACTIONS =====
    post {
        success {
            echo '✅ Build and deployment successful!'
            emailext(
                subject: "✅ Jenkins Build SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: "Good news! The build for ${env.JOB_NAME} #${env.BUILD_NUMBER} succeeded.\n\nCheck details at: ${env.BUILD_URL}",
                to: "your_email@gmail.com"
            )
        }
        failure {
            echo '❌ Build failed. Please check the Jenkins console output.'
            emailext(
                subject: "❌ Jenkins Build FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: "The build for ${env.JOB_NAME} #${env.BUILD_NUMBER} failed.\n\nSee logs at: ${env.BUILD_URL}",
                to: "your_email@gmail.com"
            )
        }
    }
}
