
# General 

## DirUtils

Directory helper utility functions used by other scripts

### removeDir

Deletes the directory and all content in it

**Usage:**
```python 
    removeDir(rf'C:\ArSim')
```

**Options:**

| Name | Type | Description |
| | | |
| directory | String | Path to the directory to delete |

### CleanDirectory

Deletes all content in the directory but does not delete the directory itself

**Usage:**
```python 
    CleanDirectory(r'C:\ArSim')
```

**Options:**

| Name | Type | Description |
| | | |
| directory | String | Path to the directory to clean |

### CreateDirectory

Creates a directory if it does not already exist

**Usage:**
```python 
    CreateDirectory(r'C:\ArSim')
```

**Options:**

| Name | Type | Description |
| | | |
| directory | String | Path to the directory to clean |

### ZipDirectory

Creates a Zip archive with the contents of the directory

**Usage:**
```python 
    ZipDirectory(r'C:\ArSim', r'C:\ArSim')
```

**Options:**

| Name | Type | Description |
| | | |
| directory | String | Path to the directory to zip |
| zipfile | String | Filename of the zip file |

## UploadToGitHub

Uploads a file to GitHub

**Usage:**
``` console 
    C:\>UploadToGitHub.ps1 V1.0.0 br-automation-com mappFramework 'C:\ArSim.zip'
```

**Options:**

| Type | Description |
| | |
| string | Version tag |
| string | User or Organization |
| string | Repository name |
| string | Filename |


## Zip

Creates a Zip archive of a directory

**Usage:**
``` console 
    C:\>python Zip.py --folder 'C:\ArSim'
```

**Options:**

| Name | Description | Default |
| | | |
| --folder,<br>-f | Path to the directory to zip | None |

