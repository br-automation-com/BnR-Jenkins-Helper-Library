def call(Map config = [:]) {
    def tag = Tag(workspace: config.workspace)
    def count = Integer.parseInt(powershell(returnStdout: true, script: "git -C ${config.workspace} rev-list HEAD --count").trim())
    try {
        count = Integer.parseInt(powershell(returnStdout: true, script: "git -C ${config.workspace} rev-list $tag..HEAD --count").trim())
    }
    catch (err) {
    }
    tag = tag.substring(1)
    if (IsReleaseBranch(workspace: config.workspace)) {
        return "$tag.$count"
    }
    def branch = BranchName(workspace: config.workspace)
    if (IsReleaseCandidate(workspace: config.workspace)) {
        count = Integer.parseInt(powershell(returnStdout: true, script: "git -C ${config.workspace} rev-list origin/develop..$branch --count --no-merges").trim())
        tag = branch =~ /(\d+)\.(\d+)\.(\d+)/
        if (tag.size() == 0) {
            echo "version number not found in branch name: $branch"
            echo "V0.0.1.$count"
            return "V0.0.1.$count"
        }
        def major = tag[0][1]
        def minor = tag[0][2]
        def bugfix = tag[0][3]
        count += 7000
        def version = "${major}.${minor}.${bugfix}.${count}"
        print "Release Candidate tag found to be $version"
        return "$version"
    }
    else if (branch.matches('feature/(.*)')) {
        count += 8000
    }
    else {
        count += 9000
    }

    def match = tag =~ /(\d+)\.(\d+)\.(\d+)/
    if (match.size() == 0) {
        print "tag is not in recognized format $tag"
        print "V0.0.1.$count"
        return "V0.0.1.$count"
    }
    def major = match[0][1]
    def minor = Integer.parseInt(match[0][2]) + 1
    def bugfix = match[0][3]

    if (minor == 100) {
        minor = 0
        major = Integer.parseInt(major) + 1
    }
    
    tag = "${major}.${minor}.${bugfix}"
    print "$tag"
    return "$tag.$count"
}
