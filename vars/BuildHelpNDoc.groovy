def call(Map config = [:]) {
    echo config.template;
    if (config.template != "") {
        updateTemplate(config.template);
    }
    powershell(returnStdout: true, script: "New-Item -ItemType Directory -Force -Path ${config.output}");
    if (config.type == "PDF") {
        powershell(script: "& \"$HelpNDoc\" \"${config.file}\" -s build -x=\"Build PDF documentation\" -o=\"Build PDF documentation:${config.output}\"");
    }

    else if (config.type == "HTML") {
        powershell(script: "& \"$HelpNDoc\" \"${config.file}\" -s build -x=\"Build HTML documentation\" -o=\"Build HTML documentation:${config.output}\"");
    }
    def created = powershell(returnStdout: true, script: "Test-Path ${config.output}").trim();
    echo "$created"
    if (created != "True") {
        error('Failing build because help not created, check license activation');
    }
    sleep 5;
}

def updateTemplate(String templateDir) {
    echo "updating the template directory";
    def helpNDocTemplateDir = 'C:\\Users\\buchananw\\Documents\\HelpNDoc\\Templates';
    powershell(returnStdout: true, script: "New-Item -ItemType Directory -Force -Path ${helpNDocTemplateDir}");
    powershell(returnStdout: true, script: "Remove-Item ${helpNDocTemplateDir}\\* -Recurse -Force" );
    powershell(returnStdout: true, script: "Copy-Item -Recurse \"${templateDir}\\*\" -Destination \"${helpNDocTemplateDir}\"");
}