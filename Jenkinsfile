pipeline {
    agent any
    stages {
        stage('Run') {
            steps {
                withPythonEnv('python3') {
                    sh 'echo Using python version:'
                    sh 'python3 --version'

                    sh 'echo Pulling latest Arlo Backup code'
                    git url: "$GIT_URL"

                    sh 'echo Starting bash script...'
                    sh "./arlo_backup.bash"
                }
            }
        }
    }
}