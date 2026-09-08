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
        stage('Package Framework') {
            steps {
                bat 'powershell -Command "Compress-Archive -Path api,config,data,schemas,testdata,tests,utils,conftest.py,Dockerfile,Jenkinsfile,pytest.ini,README.md,requirements.txt,.gitignore -DestinationPath REST-API-AUTOMATION-FRAMEWORK.zip -Force"'
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
            
            archiveArtifacts(
               artifacts: 'REST-API-AUTOMATION-FRAMEWORK.zip',
               allowEmptyArchive: false
            )
        }
    }
}