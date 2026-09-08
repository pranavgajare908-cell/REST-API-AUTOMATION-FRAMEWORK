pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python --version'
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'pytest -v --junitxml=test-results.xml'
            }
        }
    }

    post {

        always {
            allure([
                includeProperties: false,
                jdk: '',
                results: [
                    [path: 'allure-results']
                ]
            ])

            junit(
                testResults: 'test-results.xml',
                allowEmptyResults: true
            )

            archiveArtifacts(
                artifacts: 'logs/**/*.log',
                allowEmptyArchive: true
            )
        }
    }
}