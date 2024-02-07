def call(Map config = [:]) {
	config.buildpip = config.buildpip ?: false
    def clean = ''
    if (config.clean == false)
        clean = '--no-clean'
    powershell(script: "python '${GetResources()}/scripts/ASProjectCompile.py' --project '${config.project}' --configuration ${config.configuration} --maxwarnings ${config.max_warnings} --buildpip ${config.buildpip} ${clean}");
}