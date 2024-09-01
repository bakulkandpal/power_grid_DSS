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
                    python -m venv venv || exit /b
                    call venv\\Scripts\\activate.bat || exit /b
                    python -m pip install --upgrade pip || exit /b
                '''
            }
        }
        
        stage('Install Dependencies') {
            steps {
                bat '''
                    call venv\\Scripts\\activate.bat || exit /b
                    pip install -r requirements.txt || exit /b
                '''
            }
        }
        
        stage('PyInstaller Build') {
            steps {
                bat '''
                    call venv\\Scripts\\activate.bat || exit /b
                    pip install pyinstaller==6.1.0 || exit /b
                    set FILE_NAME=power_grid_DSS_%BUILD_NUMBER%
                    echo Safe filename: %FILE_NAME%
                    pyinstaller --onefile --name "%FILE_NAME%" reconfiguration.py || exit /b
                    echo Directory contents after PyInstaller:
                    dir /s
                    mkdir artifacts
                    move dist\\* artifacts\\ || echo No files to move
                    echo Contents of artifacts directory:
                    dir artifacts
                '''
            }
        }
    }

    post {
        always {
            bat 'echo Current directory:'
            bat 'cd'
            bat 'echo Directory contents:'
            bat 'dir /s'
            archiveArtifacts artifacts: 'artifacts\\*', fingerprint: true, allowEmptyArchive: true
        }
    }
}
