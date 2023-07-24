def call(Map config = [:]){
    def branch = "develop";
    if (env.BRANCH_NAME) {
        branch = "${env.BRANCH_NAME}";
    }else {
        try {
            powershell(returnStdout: true, script: "git -C ${config.workspace} branch --show-current").trim();
        }catch (err){ 

        }
    }
    return "$branch";
}