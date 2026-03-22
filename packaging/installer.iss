#define AppName "My App"               ; TODO: your app display name
#define AppVersion "1.0.0"              ; TODO: initial version
#define AppPublisher "your-username"    ; TODO: shown in Add/Remove Programs
#define AppURL "https://your-store.lemonsqueezy.com/"  ; TODO: publisher URL
#define AppExeName "MyApp.exe"          ; TODO: must match name= in MyApp.spec
#define AppId "{{00000000-0000-0000-0000-000000000000}}"  ; TODO: generate a new GUID — NEVER reuse one

#ifndef ProjectRoot
  #define ProjectRoot ".."
#endif

#ifndef DistDir
  #define DistDir AddBackslash(ProjectRoot) + "dist"
#endif

#define AppIconPath AddBackslash(ProjectRoot) + "assets\\app_icon.ico"
#define EULAPath AddBackslash(ProjectRoot) + "docs\\EULA.txt"
#define SourceDir AddBackslash(DistDir) + "MyApp"  ; TODO: rename to match COLLECT name= in spec

[Setup]
AppId={#AppId}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
AppPublisherURL={#AppURL}
AppSupportURL={#AppURL}
AppUpdatesURL={#AppURL}
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
UninstallDisplayIcon={app}\{#AppExeName}
SetupIconFile={#AppIconPath}
OutputDir={#DistDir}
OutputBaseFilename=MyApp-Setup  ; TODO: rename
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