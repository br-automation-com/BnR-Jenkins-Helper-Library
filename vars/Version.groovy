def call(Map config = [:]) {
    def tag = Tag(workspace: config.workspace);
    def count = Integer.parseInt(powershell(returnStdout: true, script: "git -C ${config.workspace} rev-list HEAD --count").trim());
    try {
        count = Integer.parseInt(powershell(returnStdout: true, script: "git -C ${config.workspace} rev-list $tag..HEAD --count").trim());
    }
    catch (err){
    }
    tag = tag.substring(1)
    if (IsReleaseBranch(workspace: config.workspace)) {
        return "$tag.$count";
    }
    def branch = BranchName(workspace: config.workspace)
    if (IsReleaseCandidate(workspace: config.workspace)) {
        count = Integer.parseInt(powershell(returnStdout: true, script: "git -C ${config.workspace} rev-list origin/develop..$branch --count --no-merges").trim());
        branch = branch.substring(branch.lastIndexOf('/') + 2);
        count += 7000;
    }
    else if (branch.matches("feature/(.*)")) {
        count += 8000;
    }
    else {
        count += 9000
    }

    def match = tag =~ /(\d+)\.(\d+)\.(\d+)/;
    if (match.size() == 0) {
        return "V0.0.1.$count"
    }
    def major = match[0][1];
    def minor = Integer.parseInt(match[0][2]) + 1;
    def bugfix = match[0][3];
    tag = "${major}.${minor}.${bugfix}";
    echo "$tag";
    return "$tag.$count";
}
