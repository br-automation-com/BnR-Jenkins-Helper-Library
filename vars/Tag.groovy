def call(Map config = [:]){
    def tag = "V0.0.1"
    try {
        tag = powershell(returnStdout: true, script: "git -C ${config.workspace} describe --abbrev=0 --always").trim();
    }
    catch (err){
    }
    return "$tag";
}