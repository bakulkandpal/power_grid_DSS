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
                sh 'pip install -r requirements.txt'
            }
        }
        
        stage('Run Tests') {
            steps {
                sh 'python -m unittest discover tests'  // Assuming you have tests in a 'tests' directory
            }
        }
        
        stage('PyInstaller Build') {
            steps {
                script {
                    def VERSION = sh(script: "grep '^## Version' README.md | awk '{print \$3}'", returnStdout: true).trim()
                    def BRANCH = env.BRANCH_NAME.replaceAll(/[:\/ ]/, '_')
                    def FILE_NAME = "power_grid_DSS_${VERSION}_${env.BUILD_NUMBER}_${BRANCH}"
                    
                    sh "pip install pyinstaller==6.1.0"
                    sh "pyinstaller --onefile --name ${FILE_NAME} your_main_script.py"  // Replace with your actual main script
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        success {
            archiveArtifacts artifacts: 'dist/*', fingerprint: true
        }
    }
}
