def call(Map config = [:]){
    config.vc4 = config.vc4  ?: 'true'
    powershell(script: "python '${GetResources()}/scripts/Export.py' --project '${config.project}' --config '${config.config}' --output '${config.output}' --physical '${config.physical}' --vc4 '${config.vc4}'");
}