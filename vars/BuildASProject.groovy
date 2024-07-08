def call(Map config = [:]) {
	config.buildpip = config.buildpip ?: false
    def clean = ''
    if (config.clean == false)
        clean = '--no-clean'
    
    powershell(script: 'E:/BrAutomation/AS410/Bin-en/BR.AS.Build.exe "E:/workspace/mapp_Framework_develop_2/BaseProject/mappFramework/mappFramework.apj" -cleanAll -t C:/Temp/Simulation -o C:/Temp/Binaries/Simulation');
    
    //powershell(script: "python '${GetResources()}/scripts/ASProjectCompile.py' --project '${config.project}' --configuration ${config.configuration} --maxwarnings ${config.max_warnings} --buildpip ${config.buildpip} ${clean}");
}