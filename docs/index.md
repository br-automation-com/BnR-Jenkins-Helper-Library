# B&R Jenkins Helper Scripts

## Groovy Scripts
Groovy scripts can be called directly from your jenkins pipeline

### General Purpose

* [ExportASLibrary](./groovy/general_purpose/#exportaslibrary) - Exports a library from an Automation Studio project in binary format
* [FrameworkExport](./groovy/general_purpose/#frameworkexport) - Creates a zip file for importing using the mapp Framework Import tool
* [SendNotifications](./groovy/general_purpose/#sendnotifications) - Sends notifications to a MS Teams channel
* [GetResources](./groovy/general_purpose/#getresources) - Helper script which returns the path the resources used by this library
* [UploadToGitHub](./groovy/general_purpose/#uploadtogithub) - Uploads a file to a GitHub project

### Project/Version Information

* [Version](./groovy/version/#version) - Returns the version number in the V&lt;Major&gt;.&lt;Minor&gt;.&lt;Bugfix&gt;.&lt;Number&gt; format.  Version information is based on the latest repository tag and the branch name
* [MajorVersionNumber](./groovy/version/#majorversionnumber) - Returns just the Major version number
* [MinorVersionNumber](./groovy/version/#minorversionnumber) - Returns just the Minor version number
* [BugFixVersionNumber](./groovy/version/#bugfixversionnumber) - Returns just the BugFix version number
* [IsReleaseCandidate](./groovy/version/#isreleasecandidate) - Returns true if the branch is a release candidate branch (release/*)
* [IsReleaseBranch](./groovy/version/#isreleasebranch) - Returns true if this is the main branch, false otherwise
* [IsHotFix](./groovy/version/#ishotfix) - Returns true if this is a hotfix branch, false otherwise
* [BranchName](./groovy/version/#branchname) - Returns the branch name from the repository
* [Tag](groovy/version/#tag) - returns the latest tag from the repository

### Build Scripts

* [BuildASProject](./groovy/build/#buildasproject) - Builds an Automation Studio project configuration
* [BuildARsimStructure](./groovy/build/#buildarsimstructure) - Builds the ARSim directory structure
* [MSBuild](./groovy/build/#msbuild) - Builds a Visual Studio project

### Test Scripts

* [RunArUnitTests](./groovy/test#runarunittests) - Starts an ArSim instance and runs the available unit tests
* [RunMappViewIntegrationTests](./groovy/test#runmappviewintegrationtests) - Runs the mapp View integration tests
* [ProcessArTestResults](./groovy/test#processartestresults) - Converts the output of the AR unit tests into a format for Jenkins
 
## Python Scripts

Python scripts can not be called directly from your Jenkins pipeline, most of these are used internally in the Groovy

For others you can call them from a Jenkins pipeline using the following syntax

```
powershell(script: "python '${GetResources()}/scripts/Export.py' --arg1 'argument'");)
```

### Automation Studio Helpers

* [ASProject](./python/automation_studio/#asproject) - Loads an Automation Studio project into a python class
* [AsProjectCompile](./python/automation_studio/#asprojectcompile) - Builds an Automation Studio project
* [CreateArSimInstallation](./python/automation_studio/#createarsiminstallation) - Creates the ArSim install folder
* [Export](./python/automation_studio/#export) - Exports a zip file for importing with the mapp Framework Import tool
* [InstalledAS](./python/automation_studio/#installedas) - Returns a list of all Automation Studio installations on the computer
* [LibraryExport](./python/automation_studio/#libraryexport) - Exports a binary version of a library
* [ModuleOK](./python/automation_studio/#moduleok) - Verifies that all module's ModuleOK input is being monitored
* [ProcessCodeCoverage](./python/automation_studio/#processcodecoverage) - Generates a html and xml file with the code coverage data
* [RunUnitTests](./python/automation_studio/#rununittests) - Runs the unit tests in ArSim
* [StartArSim](./python/automation_studio/startarsim) - Starts an ArSim instance and wait for it to be in run mode before returning
* [StopArSim](./python/automation_studio/stoparsim) - Stops an ArSim instance


### General
* [DirUtils](./python/general/#dirutils) - Directory helper utility functions used by other scripts
* [UploadToGitHub](./python/general/#updatetogithub) - Uploads a file to GitHub
* [Zip](./python/general/#zip) - Creates a Zip archive of a directory