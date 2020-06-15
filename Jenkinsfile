pipeline {
    agent { docker { image 'python:3.8.1' } }
    stages {
        stage('Test') {
            steps {
                echo 'Testing..'
               sh "python test/my_test.py"
            }
        }
    }
}