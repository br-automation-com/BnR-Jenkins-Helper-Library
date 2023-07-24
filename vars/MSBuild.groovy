def call(){
    if (fileExists("C:\\Program Files (x86)\\Microsoft Visual Studio\\2019\\BuildTools\\MSBuild") == true){
        return "C:\\Program Files (x86)\\Microsoft Visual Studio\\2019\\BuildTools\\MSBuild";
    }
    if (fileExists("C:\\Program Files (x86)\\Microsoft Visual Studio\\2022\\BuildTools\\MSBuild") == true){
        return "C:\\Program Files (x86)\\Microsoft Visual Studio\\2022\\BuildTools\\MSBuild";
    }
    return "";
}
