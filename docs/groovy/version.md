# Version

## Version

Returns the version number in the V&lt;Major&gt;.&lt;Minor&gt;.&lt;Bugfix&gt;.&lt;Number&gt; format.  Version information is based on the latest repository tag and the branch name

**Usage:**
```
Version(workspace:  "${WORKSPACE}");
```

**Options:**

| Name | Description | Default |
| | | |
| workspace | Full path workspace | None |

## MajorVersionNumber

Returns just the Major version number

**Usage:**
```
MajorVersionNumber(workspace:  "${WORKSPACE}");
```

**Options:**

| Name | Description | Default |
| | | |
| workspace | Full path workspace | None |

## MinorVersionNumber

Returns just the Minor version number

**Usage:**
```
MinorVersionNumber(workspace:  "${WORKSPACE}");
```

**Options:**

| Name | Description | Default |
| | | |
| workspace | Full path workspace | None |

## BugFixVersionNumber

Returns just the BugFix version number

**Usage:**
```
BugFixVersionNumber(workspace:  "${WORKSPACE}");
```

**Options:**

| Name | Description | Default |
| | | |
| workspace | Full path workspace | None |

## IsReleaseCandidate

Returns true if the branch is a release candidate branch (release/*)

**Usage:**
```
IsReleaseCandidate(workspace:  "${WORKSPACE}");
```

**Options:**

| Name | Description | Default |
| | | |
| workspace | Full path workspace | None |

## IsReleaseBranch

Returns true if this is the main branch, false otherwise

**Usage:**
```
IsReleaseBranch(workspace:  "${WORKSPACE}");
```

**Options:**

| Name | Description | Default |
| | | |
| workspace | Full path workspace | None |

## IsHotFix

Returns true if this is a hotfix branch, false otherwise

**Usage:**
```
IsHotFix(workspace:  "${WORKSPACE}");
```

**Options:**

| Name | Description | Default |
| | | |
| workspace | Full path workspace | None |

## BranchName

Returns the branch name from the repository

**Usage:**
```
BranchName(workspace:  "${WORKSPACE}");
```

**Options:**

| Name | Description | Default |
| | | |
| workspace | Full path workspace | None |

## Tag

returns the latest tag from the repository

**Usage:**

```
Tag(workspace:  "${WORKSPACE}");
```

**Options:**

| Name | Description | Default |
| | | |
| workspace | Full path workspace | None |
