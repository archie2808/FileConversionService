pipeline {
    agent any

    stages {
        stage('Setup Environment') {
            steps {
                git branch: 'Production',
                    url: 'https://github.com/archie2808/FileConversionService.git'
                echo 'Setting up Docker environment...'
                sh 'echo $PATH'
                sh '''
                    echo "Checking operating system details..."
                    uname -a  # Print all system information
                    cat /etc/os-release  # This works on most Linux distros
                    '''
                sh 'docker-compose -f docker-compose.yml up -d --build'
            }
        }
        stage('Test') {
            steps {
                // Retry only the test command
                retry(3) {
                    script {
                        // Add a sleep time before running tests to allow all services to initialize properly
                        sleep(time: 15, unit: 'SECONDS')

                        sh 'exec /Applications/Python 3.12 -m unittest discover -s test_dependencies -v'
                    }
                }
            }
        }
        stage('Teardown Environment') {
            steps {
                echo 'Tearing down Docker environment...'
                sh 'docker-compose -f docker-compose.yml down'
            }
        }
    }
    post {
        always {
            script {
                echo 'Cleaning up any remaining resources...'
                sh 'docker-compose -f docker-compose.yml down --volumes'
            }
        }
    }
}