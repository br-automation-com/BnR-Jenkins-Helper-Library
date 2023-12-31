def call(Map config = [:]){
    config.tests = config.tests  ?: 'all'
	config.configuration = config.configuration  ?: 'UnitTest'
    config.output = config.output ?: 'TestResults'
    config.port = config.port ?: 80
    powershell(script: "python '${GetResources()}/scripts/CreateArSimInstallation.py' --project '${config.project}' --configuration '${config.configuration}' --simulationDirectory '${config.project}/ArSim'");
    powershell(script: "python '${GetResources()}/scripts/StartArSim.py' --simulationDirectory '${config.project}/ArSim'");
    powershell(script: "python '${GetResources()}/scripts/RunUnitTests.py' --test ${config.tests} --output '${config.project}/${config.output}' --port ${config.port}");
    powershell(script: "python '${GetResources()}/scripts/StopArSim.py' --simulationDirectory '${config.project}/ArSim'");
}