def call(Map config = [:]) {
	config.buildpip = config.buildpip ?: false
    powershell(script: "python '${GetResources()}/scripts/ASProjectCompile.py' --project '${config.project}' --configuration ${config.configuration} --maxwarnings ${config.max_warnings} --buildpip ${config.buildpip}");
}