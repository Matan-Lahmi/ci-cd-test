pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Tests') {
            parallel {
                stage('Backend — flake8') {
                    steps {
                        dir('backend') {
                            sh 'pip install flake8 && flake8 .'
                        }
                    }
                }
                stage('Backend — pytest') {
                    steps {
                        dir('backend') {
                            sh 'pip install -r requirements.txt && pytest'
                        }
                    }
                }
                stage('Frontend — eslint') {
                    steps {
                        dir('frontend') {
                            sh 'npm install && npm run lint'
                        }
                    }
                }
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker compose build'
            }
        }

        stage('Trivy Scan') {
            parallel {
                stage('Scan Backend') {
                    steps {
                        sh 'trivy image --exit-code 1 --severity HIGH,CRITICAL matanlahmi/fullstack-backend'
                    }
                }
                stage('Scan Frontend') {
                    steps {
                        sh 'trivy image --exit-code 1 --severity HIGH,CRITICAL matanlahmi/fullstack-frontend'
                    }
                }
            }
        }

        stage('Docker Push') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'docker-hub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh 'echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin'
                    sh 'docker compose push'
                }
            }
        }
    }

    post {
        always {
            sh 'docker compose down'
            cleanWs()
        }
    }
}
