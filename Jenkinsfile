pipeline {
    agent any

    stages {
        stage('Preparation') {
            steps {
                git branch: 'Production',
                    url: 'https://github.com/archie2808/FileConversionService.git'
            }
        }
        stage('Check Environment') {
            steps {
                script {
                    sh 'docker --version'
                    sh 'docker-compose --version'
                }
            }
        }
        stage('Build and Test') {
            steps {
                script {
                    sh 'docker-compose -f docker-compose.yml up -d --build'
                    sh 'docker-compose -f docker-compose.yml exec app python -m unittest discover -s tests'
                }
            }
        }
    }
    post {
        always {
            script {
                sh 'docker-compose -f docker-compose.yml down'
            }
        }
    }
}
