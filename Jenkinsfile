def TEAMS_CHANNEL_URL = "PasteYourURLhere"
def EMAIL_LIST = "Wesley.Buchanan@br-automation.com;"

pipeline {
    agent { node { label 'gradle' } }
    tools
    {
        gradle '7.3.3'
    }
    stages {
        stage('Test') {
            parallel {
                stage('Python Script Tests') {
                    steps {
                        powershell(returnStdout: true, script: "cd resources; python -m pytest 'tests' --junit-xml='TestResults.xml' --alluredir='AllureReport' --suppress-tests-failed-exit-code");
                        junit(testResults: '**/resources/*.xml');
                    }
                }
                stage('Groovy Tests') {
                    steps {
                        script {
                            try {
                                bat 'gradlew clean test'
                            } finally {
                                junit '**/build/test-results/test/*.xml'
                            }
                        }
                    }
                }
            }
        }
    }
    post {
        always {
            script {
                allure(results: [[path: "resources\\AllureReport"], [path: "allure-results"]])
                SendNotifications(recipients: "${EMAIL_LIST}", buildStatus: currentBuild.result);
            }
        }
    }
}
