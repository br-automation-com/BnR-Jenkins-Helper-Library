# General Purpose


## ExportASLibrary

Exports a library from an Automation Studio project in binary format.
The library must already be compiled before the export is called.

**Usage:**
``` groovy
ExportASLibrary(project: "$PROJECT_DIR", library: "MyLib", directory: "Export")
```
**Options:**

| Name | Description | Default |
| | | |
| project | Full path to the directory containing the Automation Studio Project | None |
| library | Name of the source code library | None |
| directory | Relative path to the directory to export the library to | None |

## FrameworkExport

Creates a zip file for importing using the mapp Framework Import tool

**Usage:**
``` groovy
FrameworkExport(project: "$PROJECT_DIR", config: "Documentation.json", output: "Framework\\Services", physical: "Physical\\Simulation");
```

**Options:**

| Name | Description | Default |
| | | |
| project | Full path to the directory containing the Automation Studio Project | None |
| config | Name of the export configuration json file | None |
| output | Relative path to the location where the export file(s) will be placed | None |
| phsyical | Relative path to the physical directory | None |


## SendNotifications

Sends notifications to a MS Teams channel
**Usage:**
``` groovy
SendNotifications(recipients: "${EMAIL_LIST}", buildStatus: currentBuild.result);
```

**Options:**

| Name | Description | Default |
| | | |
| recipients | semicolon seperated email list of users to notify | None |
| buildStatus | build result | None |

## GetResources

Helper script which returns the path the resources used by this library
**Usage:**
``` groovy
GetResources();
```

## UploadToGitHub

Uploads a file to a GitHub project

**Usage:**
``` groovy
UploadToGitHub(version: "${RELEASE_VERSION}", organization: "${REPO_ORGANIZATION}", name: "${REPO_NAME}", file: "${WORKSPACE}\\${fileNameArSim}");
```

**Options:**

| Name | Description | Default |
| | | |
| version | version number of this release | None |
| organization | GitHub organization name | None |
| name | Name of the repository | None |
| file | relative path to the file | None |
