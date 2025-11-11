pipeline {
    agent any

    environment {
        PROJECT_DIR = '/var/www/nextbloom'
        BACKEND_DIR = "${PROJECT_DIR}/backend"
        FRONTEND_DIR = "${PROJECT_DIR}/frontend"
        VENV_PATH = "${BACKEND_DIR}/venv"
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code from GitHub...'
                checkout scm
            }
        }

        stage('Backend Setup') {
            steps {
                script {
                    echo 'Setting up backend...'
                    sh """
                        cd ${BACKEND_DIR}
                        if [ ! -d venv ]; then
                            python3 -m venv venv
                        fi
                        source venv/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt
                    """
                }
            }
        }

        stage('Backend Migrations') {
            steps {
                script {
                    echo 'Running database migrations...'
                    sh """
                        cd ${BACKEND_DIR}
                        source venv/bin/activate
                        python manage.py migrate --noinput
                        python manage.py collectstatic --noinput
                    """
                }
            }
        }

        stage('Frontend Setup') {
            steps {
                script {
                    echo 'Setting up frontend...'
                    sh """
                        cd ${FRONTEND_DIR}
                        npm install
                    """
                }
            }
        }

        stage('Frontend Build') {
            steps {
                script {
                    echo 'Building frontend...'
                    sh """
                        cd ${FRONTEND_DIR}
                        npm run build
                    """
                }
            }
        }

        stage('Restart Services') {
            steps {
                script {
                    echo 'Restarting services...'
                    sh """
                        sudo systemctl restart nextbloom || true
                        sudo systemctl restart nginx || true
                        sleep 3
                    """
                }
            }
        }

        stage('Health Check') {
            steps {
                script {
                    echo 'Checking application health...'
                    sh """
                        sleep 5
                        curl -f http://localhost:8000/api/products/ || exit 1
                    """
                }
            }
        }
    }

    post {
        success {
            echo 'Deployment successful!'
        }
        failure {
            echo 'Deployment failed!'
            // Add notification here (email, Slack, etc.)
        }
        always {
            echo 'Cleaning up...'
        }
    }
}

