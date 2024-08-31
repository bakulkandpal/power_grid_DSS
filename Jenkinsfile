pipeline {
    agent any

    options {
        timeout(time: 1, unit: 'HOURS')
        disableConcurrentBuilds()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup Python') {
            steps {
                bat '''
                    python -m venv venv
                    call venv\\Scripts\\activate.bat
                    python -m pip install --upgrade pip
                '''
            }
        }
        
        stage('Install Dependencies') {
            steps {
                bat '''
                    call venv\\Scripts\\activate.bat
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('PyInstaller Build') {
            steps {
                bat '''
                    call venv\\Scripts\\activate.bat
                    pip install pyinstaller==6.1.0
                    set FILE_NAME=power_grid_DSS_%BUILD_NUMBER%
                    echo Safe filename: %FILE_NAME%
                    pyinstaller --onefile --name "%FILE_NAME%" reconfiguration.py
                '''
            }
        }
    }

    post {
        success {
            archiveArtifacts artifacts: '**/dist/*', fingerprint: true
        }
        always {
            cleanWs()
        }
    }
}
