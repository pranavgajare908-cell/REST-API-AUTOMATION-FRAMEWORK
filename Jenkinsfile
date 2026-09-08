pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker --version'
                bat 'docker build -t rest-api-automation-framework .'
            }
        }

        stage('Run Tests in Docker') {
            steps {
                bat 'if not exist allure-results mkdir allure-results'
                bat 'if not exist logs mkdir logs'
                bat 'if not exist docker-results mkdir docker-results'

                bat 'docker run --rm -v "%CD%\\allure-results:/app/allure-results" -v "%CD%\\logs:/app/logs" -v "%CD%\\docker-results:/app/docker-results" rest-api-automation-framework'
            }
        }

        stage('Package Framework') {
            steps {
                bat 'powershell -Command "Compress-Archive -Path api,config,data,schemas,testdata,tests,utils,conftest.py,Dockerfile,Jenkinsfile,pytest.ini,README.md,requirements.txt,.gitignore,.dockerignore -DestinationPath REST-API-AUTOMATION-FRAMEWORK.zip -Force"'
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
                testResults: 'docker-results/test-results.xml',
                allowEmptyResults: true
            )

            archiveArtifacts(
                artifacts: 'logs/**/*.log',
                allowEmptyArchive: true
            )

            archiveArtifacts(
                artifacts: 'REST-API-AUTOMATION-FRAMEWORK.zip',
                allowEmptyArchive: true
            )
        }
    }
}