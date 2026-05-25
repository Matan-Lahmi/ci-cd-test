pipeline {
    agent { label 'docker-agent' }
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
                            sh 'flake8 .'
                        }
                    }
                }
                stage('Backend — pytest') {
                    steps {
                        dir('backend') {
                            sh 'pip3 install -r requirements.txt --break-system-packages && python3 -m pytest'
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
                sh 'docker-compose build'
            }
        }

        stage('Trivy Download DB') {
            steps {
                sh 'trivy image --download-db-only'
            }
        }

stage('Trivy Scan') {
    parallel {
        stage('Scan Backend') {
            steps {
                sh 'trivy image --cache-dir /tmp/trivy-backend --exit-code 1 --severity HIGH,CRITICAL --ignore-unfixed matanlahmi/fullstack-backend'
            }
        }
        stage('Scan Frontend') {
            steps {
                sh 'trivy image --cache-dir /tmp/trivy-frontend --exit-code 1 --severity HIGH,CRITICAL --ignore-unfixed matanlahmi/fullstack-frontend'
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
                    sh 'docker-compose push'
                }
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    docker-compose pull
                    docker-compose up -d
                '''
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
