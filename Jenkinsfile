pipeline {
    agent any

    stages {

       stage('Prepare Workspace and Checkout Code') {
    steps {
        deleteDir()  // This clears the workspace
        checkout scm // This re-checkouts the code from the current SCM configuration
        echo 'Checking out source code from GitHub...'
        git branch: 'PipelineTesting',
            url: 'https://github.com/archie2808/FileConversionService.git'
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
