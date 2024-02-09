
# Build

## ASProject

Loads an Automation Studio project into a python class

**Usage:**
``` py
    project = ASProject(r'C:\project\TestProject')
```

**Options:**

| Name | Type | Description | Default |
| | | | |
| projectDir | String | Full path to the Automation Studio project | None |


## AsProjectCompile

Builds an Automation Studio project

**Usage:**
``` console 
    python AsProjectCompile.py --project C:\project\TestProject --configuration arsim
```

**Options:**

| Name | Description | Default |
| | | |
| --project,<br>-p | Full path to the Automation Studio project | None |
| --configuration,<br>-c | Name of the configuration to build | None |
| --maxwarnings,<br>-w | Max number of warning before the build is considered failed | -1 |
| --buildpip,<br>-b| Whether to build the **P**roject **I**nstation **P**ackage | False |
| --no-clean,<br>-n| Whether to clean the project before building | False |

## CreateArSimInstallation

Creates the ArSim install folder

**Usage:**
``` console 
    python CreateArSimInstallation.py --project C:\project\TestProject --configuration arsim --simulationDirectory C:\ArSim
```

**Options:**

| Name | Description | Default |
| | | |
| --project,<br>-p | Full path to the Automation Studio project | None |
| --configuration,<br>-c | Name of the configuration to build | None |
| --simulationDirectory,<br>-s | Max number of warning before the build is considered failed | None |

## Export

Exports a zip file for importing with the mapp Framework Import tool

**Usage:**
``` console 
    python Export.py --project C:\project\TestProject --configuration Test.json --physical Physical\Simulation --output Installer
```

**Options:**

| Name | Description | Default |
| | | |
| --project,<br>-p | Full path to the Automation Studio project | None |
| --config,<br>-c | Name of the configuration to build | None |
| --physical,<br>-s | Relative path to the physical directory location | None |
| --output,<br>-o| Output directory where the export files are saved to | None |
| --zip,<br>-z| Whether to zip the directory or not | True |

## InstalledAS

Returns information on Installed Automation Studio versions

**Usage:**
``` python 
    project = ASProject(r'C:\projects\Test')
    asPath = InstalledAS.ASInstallPath(project)
```

## LibraryExport

Exports a binary version of a library

**Usage:**
``` console 
    python LibraryExport.py --project C:\project\TestProject --library MyLib
```

**Options:**

| Name | Description | Default |
| | | |
| --project,<br>-p | Full path to the Automation Studio project | None |
| --library,<br>-l | Name of the library to build | None |
| --directory,<br>-d| Directory to store the compiled library | .\\ |


## ModuleOk

Verifies that all module's ModuleOK input is being monitored

**Usage:**
``` console 
    python ModuleOk.py --project C:\project\TestProject --configuration arsim
```

**Options:**

| Name | Description | Default |
| | | |
| --project,<br>-p | Full path to the Automation Studio project | None |
| --configuration,<br>-c | Name of the configuration to build | None |
| --output,<br>-o | Whether to output a warning or an error if a ModuleOk is not monitored | Warning |


## ProcessCodeCoverage

Generates a html and xml file with the code coverage data

**Usage:**
``` console 
    python ProcessCodeCoverage.py --project C:\project\TestProject --configuration arsim
```

**Options:**

| Name | Description | Default |
| | | |
| --project,<br>-p | Full path to the Automation Studio project | None |
| --config,<br>-c | Name of the configuration to build | None |
| --output,<br>-o | Output directory for generated files| CodeCoverage |

## RunUnitTests

Runs the unit tests in ArSim

**Usage:**
``` console 
    python RunUnitTests.py --test all
```

**Options:**

| Name | Description | Default |
| | | |
| --test,<br>-t | Name of the tests to run (all to run all tests discovered) | None |
| --output,<br>-o | Output directory to store the test results in | TestsResults |
| --port,<br>-p | Port number that AR's webserver is running on | 80 |


## StartArSim

Starts an ArSim instance and wait for it to be in run mode before returning

**Usage:**
``` console 
    python StartArSim.py --simulationDirectory C:\ArSim
```

**Options:**

| Name | Description | Default |
| | | |
| --simulationDirectory,<br>-s | Path to the ArSim installation directory to start | None |

## StopArSim

 Stops an ArSim instance

**Usage:**
``` console 
    python StopArSim.py --simulationDirectory C:\ArSim
```

**Options:**

| Name | Description | Default |
| | | |
| --simulationDirectory,<br>-s | Path to the ArSim installation directory to start | None |
