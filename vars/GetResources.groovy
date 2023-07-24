// vars/get_resource_dir.groovy
import groovy.transform.SourceURI
import java.nio.file.Path
import java.nio.file.Paths

class ScriptSourceUri {
    @SourceURI
    static URI uri
}

@com.cloudbees.groovy.cps.NonCPS
def resourceLocation(String value) {
    def scriptLocation = Paths.get(ScriptSourceUri.uri);
    def location = scriptLocation.getParent().getParent().resolve('resources').toString()
    return "$location"
}

def call() {
    def location = resourceLocation()
    echo "$location"
    
    def testPath = powershell(returnStdout: true, script: "Test-Path '${location}'").trim()
    echo "$testPath"

    if ("$testPath" != "True") {
        echo "does not exist"
        location = location.replaceFirst('E', 'C')
    }
    return location
    
}

