pipeline {
    agent any

    environment {
        PROJECT_DIR = "/home/nbgecdpsvr/nextbloom_jen"
        BACKEND_DIR = "${PROJECT_DIR}/backend"
        FRONTEND_DIR = "${PROJECT_DIR}/frontend"
        VENV_DIR = "${PROJECT_DIR}/env"
        PYTHON = "${VENV_DIR}/bin/python3"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', credentialsId: 'github-ssh', url: 'git@github.com:punishermortal/ecomerce_web.git'
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh '''
                cd $PROJECT_DIR
                if [ ! -d "$VENV_DIR" ]; then
                    python3 -m venv $VENV_DIR
                fi
                source $VENV_DIR/bin/activate
                pip install --upgrade pip
                pip install -r $BACKEND_DIR/requirements.txt
                '''
            }
        }

        stage('Install Frontend Dependencies') {
            steps {
                sh '''
                cd $FRONTEND_DIR
                npm install
                '''
            }
        }

        stage('Build Frontend') {
            steps {
                sh '''
                cd $FRONTEND_DIR
                npm run dev &
                '''
            }
        }

        stage('Run Backend') {
            steps {
                sh '''
                cd $BACKEND_DIR
                pkill -f "manage.py runserver" || true
                nohup $PYTHON manage.py runserver 0.0.0.0:8000 > backend.log 2>&1 &
                '''
            }
        }

        stage('Restart Services') {
            steps {
                sh '''
                echo "Restarting Nextbloom services..."
                pkill -f "manage.py runserver" || true
                pkill -f "npm run dev" || true
                nohup $PYTHON $BACKEND_DIR/manage.py runserver 0.0.0.0:8000 > $BACKEND_DIR/backend.log 2>&1 &
                nohup npm --prefix $FRONTEND_DIR run dev > $FRONTEND_DIR/frontend.log 2>&1 &
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Nextbloom deployed successfully!"
        }
        failure {
            echo "❌ Deployment failed. Please check logs."
        }
    }
}