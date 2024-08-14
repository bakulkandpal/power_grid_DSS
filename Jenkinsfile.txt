pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Checkout the code from the GitHub repository, specifying the main branch
                git branch: 'main', url: 'https://github.com/bakulkandpal/power_grid_DSS.git'
            }
        }

        stage('Setup Python Environment') {
            steps {
                // Create and activate a virtual environment, then install dependencies
                bat '''
                python -m venv venv
                call venv\\Scripts\\activate
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Application') {
            steps {
                // Placeholder for running your application or scripts
                echo 'Running application...'
                // bat 'python your_script.py'  # Uncomment and replace with your script
            }
        }
    }

    post {
        always {
            // Clean up the workspace after the pipeline runs
            cleanWs()
        }
        success {
            echo 'Pipeline executed successfully!'
        }
        failure {
            echo 'Pipeline execution failed.'
        }
    }
}