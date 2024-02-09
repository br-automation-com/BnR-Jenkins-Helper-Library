# Test

## RunArUnitTests

Starts an ArSim instance and runs the available unit tests
**Usage:**
```
RunArUnitTests(project: "$PROJECT_DIR", configuration: "UnitTest", tests: "all", output: 'TestResults', port: 80);
```

**Options:**

| Name | Description | Default |
| | | |
| project | Full path to the Automation Studio project | None |
| configuration | Name of the configuration to build | UnitTest |
| tests | Which test suite to run | all |
| output | Path to save the test results to | TestResults |
| port | Which port number ArSim's webserver is running on | 80 |

## RunMappViewIntegrationTests

Runs the mapp View integration tests
**Usage:**
```
RunMappViewIntegrationTests(project: "$PROJECT_DIR", configuration: "Simulation", integrationTestDir: "IntegrationTests");
```

**Options:**

| Name | Description | Default |
| | | |
| project | Full path to the Automation Studio project | None |
| configuration | Name of the configuration to build | Simulation |
| integrationTestDir | Full path to location of integration tests folder | None |

## ProcessArTestResults

Converts the output of the AR unit tests into a format for Jenkins
**Usage:**
```
ProcessArTestResults(testResults: "TestResults");
```

**Options:**

| Name | Description | Default |
| | | |
| testResults | Relative path the test results | TestResults |
