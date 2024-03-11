def call(Map config = [:]) {
    def fileName = config.file.trim();
    def credentialsId = config.credentialId
    if (config.organization == 'br-na-pm') {
        credentialsId = 'Jenkins-BR-NA'
    }
    else if (config.orginzation == 'br-automation-com') {
        credentialsId = 'br-automation-com-github'
    }
    withCredentials([usernamePassword(credentialsId: "$credentialsId",
                                          usernameVariable: 'GITHUB_APP',
                                          passwordVariable: 'GITHUB_ACCESS_TOKEN')])
    {
        return pwsh(returnStdout: true, script: ". '${GetResources()}/scripts/UploadToGitHub.ps1' V${config.version} ${config.organization} ${config.name} '${fileName}'").trim();
    }
}
    