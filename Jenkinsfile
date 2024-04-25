pipeline {
    agent any
    environment {
        GIT_EXECUTABLE = "/opt/homebrew/Cellar/git/2.44.0/bin/git"
        PATH = "/usr/local/bin:$PATH"
    }
    stages {
        stage('Prepare Workspace and Checkout Code') {
            steps {
                sh 'whoami'
                sh 'echo $PATH'
                sh 'docker-compose version'
                sh 'docker info'
                deleteDir()
                checkout scm
                echo 'Checking out source code from GitHub...'
                git branch: 'PipelineTesting',
                    url: 'https://github.com/archie2808/FileConversionService.git'
            }
        }
        stage('Build and Start Docker Containers') {
            steps {
                sh 'docker-compose -f docker-compose.yml up -d --build'
            }
        }
        stage('Test') {
            steps {
                retry(3) {
                    echo 'Starting tests after a brief delay to allow for environment initialization...'
                    sleep(time: 15, unit: 'SECONDS')
                    sh 'docker-compose exec app sh -c "python -m unittest discover -s tests"'
                    echo 'Tests execution completed.'
                }
            }
        }
        stage('Teardown Environment') {
            steps {
                echo 'Tearing down Docker environment...'
                sh 'docker-compose down -v'
                echo 'Docker environment teardown complete.'
            }
        }
    }
    post {
        always {
            script {
                echo 'Cleaning up any remaining resources...'
                sh 'docker-compose down -v'
                echo 'Cleanup complete.'
            }
        }
    }
}