import winreg
from packaging import version

def PVIPath(project):
  return InstalledAS.PVI(project.workingVersion)

def ASInstallPath(project):
    AutomationStudioList = InstalledAS.Info()
    for AS in AutomationStudioList:
       if project.IsCompatibleVersion(AS[0]):
            return AS[1]
       if AS == AutomationStudioList[-1]:
            print ('AS version not installed')
            return None


class InstalledAS:
  """Provides information on the installed Automation Studio versions"""

  def PVI(projectVersion = ''):
    REGISTRY = r'SOFTWARE\WOW6432Node' #This registry has information on installed programs
    Info = []
    PVI = ""
    root_key= winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, REGISTRY, 0, winreg.KEY_READ)
    for i in range(0, winreg.QueryInfoKey(root_key)[0]):
      try:
        asubkey_name=winreg.EnumKey(root_key, i)
        if ("BR_Automation" == asubkey_name) and (version.parse(projectVersion) < version.parse("6.0")):
          asubkey = winreg.OpenKey(root_key,asubkey_name)
          BuRSharedFilesPath, null = winreg.QueryValueEx(asubkey, "BuRAutStudioPath")
          break
        elif ("BR_PVI6" == asubkey_name) and (version.parse(projectVersion) >= version.parse("6.0")):
          asubkey = winreg.OpenKey(root_key,asubkey_name)
          BuRSharedFilesPath, null = winreg.QueryValueEx(asubkey, "InstallationPath")
          break
      except EnvironmentError as ex:
        continue
    winreg.CloseKey(root_key)
    return BuRSharedFilesPath

  def Info():
    """Info() Returns - [ (Version, Install-path, Shared-Path), ...]  e.g. [('4.5.2.102', 'C:\\BrAutomation\\AS45', 'C:\\BrAutomation\\AS'), ...] """
    __versions = InstalledAS.__browse()
    return __versions

  def __browse():
    REGISTRY = r'SOFTWARE\WOW6432Node' #This registry has information on installed programs
    Info = []
    PVI = ""
    root_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, REGISTRY, 0, winreg.KEY_READ)
    print(winreg.QueryInfoKey(root_key))
    for i in range(0, winreg.QueryInfoKey(root_key)[0]):
      try:
        asubkey_name=winreg.EnumKey(root_key,i)
        asubkey_found = "BR_AS_" in asubkey_name #Reading programs with BR_AS string in it
        if asubkey_found:
          asubkey = winreg.OpenKey(root_key,asubkey_name)
          BuRAutStudioPath, null = winreg.QueryValueEx(asubkey, "BuRSharedFilesPath")
          BuRSharedFilesPath, null = winreg.QueryValueEx(asubkey, "BuRAutStudioPath")
          asubkey = winreg.OpenKey(root_key,asubkey_name + r"\ControlStudio")
          BuRAutStudioVersion, null = winreg.QueryValueEx(asubkey, "ProgrVersion")
          Info.append((BuRAutStudioVersion,BuRAutStudioPath,BuRSharedFilesPath))#B&R has BuRAutStudioPath as shared path & BuRSharedFilesPath is the actual path
          print(f'{asubkey_name} {BuRAutStudioPath} {BuRSharedFilesPath} {BuRAutStudioVersion}')
      except EnvironmentError:
        break
    winreg.CloseKey(root_key)
    return Info
