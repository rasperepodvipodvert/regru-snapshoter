import java.text.SimpleDateFormat

pipeline {
    agent {
        node(label: 'python3')
    }

    environment {
        API_KEY = credentials('REGRU_API_KEY')
        TIME_DELTA = 3
        VENV_NAME = 'venv'
        MM_WEBHOOK_URL = credentials('s76-mattermost-webhook')
        MM_CHANNEL = 'alerts-sincerity'
        LOG = ''
    }

    triggers {
        cron('0 7 * * 1-5')
    }

    stages {
        stage('Create virtualenv') {
            steps {
                sh '''
                    python3 -m venv $VENV_NAME && pwd && ls -liah
                    . ${WORKSPACE}/$VENV_NAME/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Python Script') {
            steps {
                script {
                    def proc = sh(script: '. ${WORKSPACE}/$VENV_NAME/bin/activate && python -V && python index.py', returnStdout: true)
                    LOG = proc.trim()
                }
            }
        }
    }

    post {
        always {
            deleteDir()
            notifyMM("good" , "$LOG")
        }
        failure {
            notifyMM("danger" , "$LOG")
        }
    }
}

def notifyMM(String color, String message) {
    def ndate = new Date()
    BUILD_TIMESTAMP = new SimpleDateFormat("yyyy-MM-dd H-mm-ss")
    mattermostSend (
        color: "$color",
        channel: "$MM_CHANNEL",
        endpoint: "$MM_WEBHOOK_URL",
        icon: "https://www.reg.ru/favicon.ico",
        text: "[${BUILD_TIMESTAMP.format(ndate)}] - Build | [${env.BUILD_NUMBER}](${env.BUILD_URL}) - ${currentBuild.currentResult}: #${env.JOB_NAME}",
        message: "$message"
        )
}