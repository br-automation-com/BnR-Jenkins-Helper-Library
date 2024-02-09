# Build

## BuildASProject

Builds an Automation Studio project configuration

**Usage:**
```
BuildASProject(project: "${PROJECT_DIR}", configuration: "${CONFIG_NAME}", max_warnings: -1, buildpip: true);
```

**Options:**

| Name | Description | Default |
| | | |
| project | Full path to the Automation Studio project | None |
| configuration | name of the configuration to build | None |
| max_warnings | Maximum number of warnings before the build is considered failed | None |
| buildpip | whether to build the **P**roject **I**nstallation **P**ackage | false |

## BuildARsimStructure

Builds the ARSim directory structure

**Usage:**
```
BuildARsimStructure(project: "${PROJECT_DIR}", configuration: "${CONFIG_NAME}");
```

**Options:**

| Name | Description | Default |
| | | |
| project | Full path to the Automation Studio project | None |
| configuration | Name of the configuration to build | None |

## MSBuild

Returns the path of the MS build tool

**Usage:**
```
MSBuild_Path = MSBuild();
```
