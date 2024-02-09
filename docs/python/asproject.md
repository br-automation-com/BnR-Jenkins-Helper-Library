``` mermaid
classDiagram
  ASProject <|-- ASConfiguration
  ASProject <|-- ASPackage
  ASPackage <|-- ASTask
  ASPackage <|-- ASLibrary
  
  class ASProject{
    +string version
    +string workingVersion
    +string projectName
    -string _projectDir
    -List~ASConfiguration~ _configurations
    -List~ASPackage~ _packages
    
    +IsCompatibleVersion(string version)
    +CleanProject()
    +findLibrary(string libraryName)
    +exportLibrary(string libraryName, string directory)
    +export(list files, string directory, string name)
  }
  class ASConfiguration{
    -string _name
    -string _directory
    -string _cpuName
    -string _arVersion
    -string _plcType
    +readIoMap()
    +areAllModuleSupervised()
    +modulesNotSupervised()
  }

  class ASPackage{
    -string _name
    -string _directory
    +List~ASPackage~ packages
    +List~ASTask~ tasks
    +List~ASLibrary~ libraries
    +List files
  }

  class ASTask{
    -string _name
    -string _directory
  }

  class ASLibrary{
    +export(string directory)
  }
```