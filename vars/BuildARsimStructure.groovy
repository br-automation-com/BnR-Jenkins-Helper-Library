def call(Map config = [:]){
    powershell(script: "python '${GetResources()}/scripts/CreateArSimInstallation.py' --project '${config.project}' --configuration '${config.configuration}' --simulationDirectory '${config.project}/ArSim'");
	powershell(script: "python '${GetResources()}/scripts/Zip.py' --folder '${config.project}/ArSim'");	
}