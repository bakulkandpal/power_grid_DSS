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
                    for /f "tokens=3" %%i in ('type README.md ^| findstr /R "^## Version"') do set VERSION=%%i
                    set BRANCH=%BRANCH_NAME%
                    set BRANCH=%BRANCH::=_%
                    set BRANCH=%BRANCH:/=_%
                    set FILE_NAME=power_grid_DSS_%VERSION%_%BUILD_NUMBER%_%BRANCH%
                    pyinstaller --onefile --name "%FILE_NAME%" reconfiguration.py
                '''
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        success {
            archiveArtifacts artifacts: 'dist\\*', fingerprint: true
        }
    }
}
