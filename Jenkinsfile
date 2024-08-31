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
        
        stage('Install Dependencies') {
            steps {
                bat 'pip install -r requirements.txt'
            }
        }
        
        stage('Run Tests') {
            steps {
                bat 'python -m unittest discover tests'
            }
        }
        
        stage('PyInstaller Build') {
            steps {
                script {
                    def VERSION = bat(script: 'type README.md | findstr /R "^## Version" | for /f "tokens=3" %i in (\'more\') do @echo %i', returnStdout: true).trim()
                    def BRANCH = env.BRANCH_NAME.replaceAll(/[:\/ ]/, '_')
                    def FILE_NAME = "power_grid_DSS_${VERSION}_${env.BUILD_NUMBER}_${BRANCH}"
                    
                    bat 'pip install pyinstaller==6.1.0'
                    bat "pyinstaller --onefile --name ${FILE_NAME} your_main_script.py"
                }
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
