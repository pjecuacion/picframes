#define AppName "PicFrames"
#define AppVersion "1.1.0"
#define AppPublisher "Prince Ecuacion"
#define AppURL ""
#define AppExeName "PicFrames.exe"
#define AppId "{{485A531B-A164-4A75-9C02-04055CF01149}"

#ifndef ProjectRoot
  #define ProjectRoot ".."
#endif

#ifndef DistDir
  #define DistDir AddBackslash(ProjectRoot) + "dist"
#endif

#define AppIconPath AddBackslash(ProjectRoot) + "assets\\app_icon.ico"
#define EULAPath AddBackslash(ProjectRoot) + "docs\\EULA.txt"
#define SourceDir AddBackslash(DistDir) + "PicFrames"

[Setup]
AppId={#AppId}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
UninstallDisplayIcon={app}\{#AppExeName}
SetupIconFile={#AppIconPath}
OutputDir={#DistDir}
OutputBaseFilename=PicFrames-Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequired=admin
LicenseFile={#EULAPath}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop icon"; GroupDescription: "Additional icons:"; Flags: unchecked

[Files]
Source: "{#SourceDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "{#ProjectRoot}\assets\THIRD_PARTY_NOTICES.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#ProjectRoot}\docs\EULA.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExeName}"; IconFilename: "{app}\{#AppExeName}"
Name: "{group}\Uninstall {#AppName}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon; IconFilename: "{app}\{#AppExeName}"

[Run]
Filename: "{app}\{#AppExeName}"; Description: "Launch {#AppName}"; Flags: nowait postinstall skipifsilent