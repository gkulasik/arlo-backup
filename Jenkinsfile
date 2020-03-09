pipeline {
    agent { dockerfile true }
    stages {
        stage('Run') {
            steps {
                sh './arlo_backup.bash'
            }
        }
    }
}