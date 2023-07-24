def call(Map config = [:]){
    junit(testResults: '**/TestResults/*.xml');
}