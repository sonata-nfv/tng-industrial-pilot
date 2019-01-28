#!groovy

pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                echo 'Stage: Checkout...'
                checkout scm
            }
        }
        stage('VNF build') {
            steps {
                echo 'Stage: VNF build...'
                sh "pipeline/build/build.sh"
            }
        }
        stage('Service packaging') {
            steps {
                echo 'Stage: Service packaging...'
                sh "pipeline/build/pack.sh"
            }
        }
        stage('VNF publication') {
            when {
                branch 'master'
            }
            steps {
                echo 'Stage: VNF publication...'
                sh "pipeline/publish/publish.sh"
            }
        }
    }

    post {
         success {
                 emailext(from: "jenkins@sonata-nfv.eu", 
                 to: "manuel.peuster@upb.de", 
                 subject: "SUCCESS: ${env.JOB_NAME}/${env.BUILD_ID} (${env.BRANCH_NAME})",
                 body: "${env.JOB_URL}")
         }
         failure {
                 emailext(from: "jenkins@sonata-nfv.eu", 
                 to: "manuel.peuster@upb.de", 
                 subject: "FAILURE: ${env.JOB_NAME}/${env.BUILD_ID} (${env.BRANCH_NAME})",
                 body: "${env.JOB_URL}")
         }
    }
}
