def call(Map config = [:]) {
    def fileName = config.file.trim();
    def downloadURL = pwsh(returnStdout: true, script: ". '${GetResources()}/scripts/UploadToGitHub.ps1' V${config.version} ${config.organization} ${config.name} '${fileName}'").trim();
    return "${downloadURL}";
}
    