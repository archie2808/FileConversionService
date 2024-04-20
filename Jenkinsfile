pipeline {
    agent any

    stages {

        stage('Clean Workspace') {
            steps {
                deleteDir()  // This will clear the workspace
                    checkout scm // Re-checkout the code
                }
        }
        stage('Checkout SCM') {
            steps {
                echo 'Checking out source code from GitHub...'
                   git branch: 'Production',
                    url: 'https://github.com/archie2808/FileConversionService.git'
                echo 'Starting Docker environment setup...'
                sh 'docker-compose -f docker-compose.yml up -d --build'
                echo 'Docker environment setup complete..'
            }
        }
        stage('Test') {
            steps {
                retry(3) {
                    echo 'Starting tests after a brief delay to allow for environment initialization...'
                    sleep(time: 15, unit: 'SECONDS')
                    sh 'docker-compose exec app python -m unittest discover -s tests'
                    echo 'Tests execution completed.'
                }
            }
        }
        stage('Teardown Environment') {
            steps {
                echo 'Tearing down Docker environment...'
                sh 'docker-compose -f docker-compose.yml down'
                echo 'Docker environment teardown complete.'
            }
        }
    }
        post {
            always {
                script {
                    echo 'Cleaning up any remaining resources...'
                    sh 'docker-compose -f docker-compose.yml down --volumes'
                    echo 'Cleanup complete.'
                }
        }
    }
}
