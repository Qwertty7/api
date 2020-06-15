pipeline {
    agent { docker { image 'python:3.8.3-alpine3.11' } }
    stages {
        stage('Test') {
            steps {
                echo 'Testing..'
               sh "python test/my_test.py"
            }
        }
    }
}