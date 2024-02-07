
import com.lesfurets.jenkins.unit.BasePipelineTest
import org.junit.jupiter.api.BeforeEach
import org.junit.jupiter.api.Test
import io.qameta.allure.Description;

class BranchNameTest extends BasePipelineTest {

    Object script

    @Override
    @BeforeEach
    void setUp() throws Exception {
        super.setUp()
        this.script = loadScript('vars/BranchName.groovy')
    }

    @Test
    @Description("Checks the returned value from the git command line")
    void masterFromGitTest() {
        helper.registerAllowedMethod('powershell', [HashMap], { return 'master' })
        def result = script(workspace: 'test')
        assert result == 'master'
    }

    @Test
    @Description("Checks the returned value from the environment variable")
    void masterFromEnvTest() {
        binding.setVariable('env', [BRANCH_NAME:"master"])
        def result = script(workspace: 'test')
        assert result == 'master'
    }

    @Test
    @Description("Checks the returned value from the git command line")
    void developFromGitTest() {
        helper.registerAllowedMethod('powershell', [HashMap], { return 'develop' })
        def result = script(workspace: 'test')
        assert result == 'develop'
    }

    @Test
    @Description("Checks the returned value from the environment variable")
    void developFromEnvTest() {
        binding.setVariable('env', [BRANCH_NAME:"develop"])
        def result = script(workspace: 'test')
        assert result == 'develop'
    }

}
