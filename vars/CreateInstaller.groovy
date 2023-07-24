def call(Map config = [:]){
    powershell(script: "python '${GetResources()}/scripts/CreateInstaller.py' --project '${config.project}' --name ${config.name} --output '${config.output}' --version '${config.version}'");
}