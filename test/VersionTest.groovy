
import com.lesfurets.jenkins.unit.BasePipelineTest
import org.junit.jupiter.api.BeforeEach
import org.junit.jupiter.api.Test

class VersionTest extends BasePipelineTest {

    Object script
    String WorkspaceName = 'test'
    String MockTag = 'V1.0.0'
    @Override
    @BeforeEach
    void setUp() throws Exception {
        super.setUp()
        this.script = loadScript('vars/Version.groovy')
    }

    @Test
    void developVersionTest() {
        helper.registerAllowedMethod('Tag', [Map], { return MockTag  })
        helper.registerAllowedMethod('powershell', [HashMap], { 
            HashMap map -> 
                switch (map.script){
                    case "git -C $WorkspaceName rev-list HEAD --count":
                        return '53'
                    break
                    case "git -C $WorkspaceName rev-list ${MockTag}..HEAD --count":
                        return '23'
                }
                return '0'
            })
        helper.registerAllowedMethod('IsReleaseBranch', [Map], { return false })
        helper.registerAllowedMethod('BranchName', [Map], { return 'develop' })
        helper.registerAllowedMethod('IsReleaseCandidate', [Map], { return false })

        def result = script(workspace: "$WorkspaceName")
        assert result == '1.1.0.9023'
    }

    @Test
    void masterVersionTest() {
        helper.registerAllowedMethod('Tag', [Map], { return MockTag  })
        helper.registerAllowedMethod('powershell', [HashMap], { 
            HashMap map -> 
                switch (map.script){
                    case "git -C $WorkspaceName rev-list HEAD --count":
                        return '53'
                    break
                    case "git -C $WorkspaceName rev-list ${MockTag}..HEAD --count":
                        return '23'
                }
                return '0'
            })
        helper.registerAllowedMethod('IsReleaseBranch', [Map], { return true })
        helper.registerAllowedMethod('BranchName', [Map], { return 'master' })
        helper.registerAllowedMethod('IsReleaseCandidate', [Map], { return false })

        def result = script(workspace: "$WorkspaceName")
        assert result == '1.0.0.23'
    }

    @Test
    void featureVersionTest() {
        helper.registerAllowedMethod('Tag', [Map], { return MockTag  })
        helper.registerAllowedMethod('powershell', [HashMap], { 
            HashMap map -> 
                switch (map.script){
                    case "git -C $WorkspaceName rev-list HEAD --count":
                        return '53'
                    break
                    case "git -C $WorkspaceName rev-list ${MockTag}..HEAD --count":
                        return '23'
                }
                return '0'
            })
        helper.registerAllowedMethod('IsReleaseBranch', [Map], { return false })
        helper.registerAllowedMethod('BranchName', [Map], { return 'feature/my_new_feature' })
        helper.registerAllowedMethod('IsReleaseCandidate', [Map], { return false })

        def result = script(workspace: "$WorkspaceName")
        assert result == '1.1.0.8023'
    }

    @Test
    void releaseCandidateVersionTest() {
        helper.registerAllowedMethod('Tag', [Map], { return MockTag  })
        helper.registerAllowedMethod('powershell', [HashMap], { 
            HashMap map -> 
                switch (map.script){
                    case "git -C $WorkspaceName rev-list HEAD --count":
                        return '53'
                    break
                    case "git -C $WorkspaceName rev-list ${MockTag}..HEAD --count":
                        return '23'
                    case "git -C $WorkspaceName rev-list origin/develop..release/V1.2.0 --count --no-merges":
                        return '62'
                }
                return '0'
            })
        helper.registerAllowedMethod('IsReleaseBranch', [Map], { return false })
        helper.registerAllowedMethod('BranchName', [Map], { return 'release/V1.2.0' })
        helper.registerAllowedMethod('IsReleaseCandidate', [Map], { return true })

        def result = script(workspace: "$WorkspaceName")
        assert result == '1.2.0.7062'
    }

    @Test
    void unrecognizedTagVersionTest() {
        helper.registerAllowedMethod('Tag', [Map], { return 'V1.0'  })
        helper.registerAllowedMethod('powershell', [HashMap], { 
            HashMap map -> 
                switch (map.script){
                    case "git -C $WorkspaceName rev-list HEAD --count":
                        return '53'
                    break
                    case "git -C $WorkspaceName rev-list ${MockTag}..HEAD --count":
                        return '23'
                    case "git -C $WorkspaceName rev-list origin/develop..release/V1.2.0 --count --no-merges":
                        return '62'
                }
                return '0'
            })
        helper.registerAllowedMethod('IsReleaseBranch', [Map], { return false })
        helper.registerAllowedMethod('BranchName', [Map], { return 'develop' })
        helper.registerAllowedMethod('IsReleaseCandidate', [Map], { return false })

        def result = script(workspace: "$WorkspaceName")
        assert result == 'V0.0.1.9000'
    }
}
