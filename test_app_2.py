stage('Run Tests') {
    parallel {
        stage('Test File 1') {
            steps {
                sh """
                . ${VENV_DIR}/bin/activate
                python -m pytest test_app.py -v
                """
            }
        }

        stage('Test File 2') {
            steps {
                sh """
                . ${VENV_DIR}/bin/activate
                python -m pytest test_app_2.py -v
                """
            }
        }
    }
}
