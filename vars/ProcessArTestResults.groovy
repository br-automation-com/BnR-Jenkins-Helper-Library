def call(Map config = [:]){
    config.testResults = config.testResults ?: 'TestResults'
    junit(testResults: "**/${config.testResults}/*.xml");
}