pipeline {
    agent any

    stages {
        stage('Test') {
            steps {
                echo 'Testing..'
                python test/my_test.py
            }
        }
    }
}