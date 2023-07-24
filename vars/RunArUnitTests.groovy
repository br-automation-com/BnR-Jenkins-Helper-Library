def call(Map config = [:]){
    config.tests = config.tests  ?: 'all'
	config.configuration = config.configuration  ?: 'UnitTest'
    powershell(script: "python '${GetResources()}/scripts/CreateArSimInstallation.py' --project '${config.project}' --configuration '${config.configuration}' --simulationDirectory '${config.project}/ArSim'");
    powershell(script: "python '${GetResources()}/scripts/StartArSim.py' --simulationDirectory '${config.project}/ArSim'");
    powershell(script: "python '${GetResources()}/scripts/RunUnitTests.py' --test ${config.tests} --output '${config.project}/TestResults'");
    powershell(script: "python '${GetResources()}/scripts/StopArSim.py' --simulationDirectory '${config.project}/ArSim'");
}