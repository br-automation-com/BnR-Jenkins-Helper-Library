def call(Map config = [:]){
    powershell(script: "python '${GetResources()}/scripts/Export.py' --project '${config.project}' --config '${config.config}' --output '${config.output}' --physical '${config.physical}'");
}