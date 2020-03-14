pipeline {
    agent any
    stages {
        stage('Run') {
            steps {
                withPythonEnv('python3') {
                    sh 'echo Using python version:'
                    sh 'python3 --version'

                    sh 'printenv'

                    sh 'echo Pulling latest Arlo Backup code'
                    git url: 'https://github.com/gkulasik/arlo-backup.git/'

                    sh 'echo Starting bash script...'
                    sh "./arlo_backup.bash"
                }
            }
        }
    }
}