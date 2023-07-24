def call(Map config = [:]){
    return BranchName(workspace: "${config.workspace}").matches("release/(.*)");
}