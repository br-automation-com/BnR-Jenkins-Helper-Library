def call(Map config = [:]) {
	powershell(script: "python '${GetResources()}/scripts/LibraryExport.py' --project '${config.project}' --library ${config.library} --directory ${config.directory}");
}