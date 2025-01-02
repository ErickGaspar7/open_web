[Setup]
AppName=Open Web
AppVersion=1.0
DefaultDirName={pf}\Open Web
DefaultGroupName=Open Web
OutputBaseFilename=setup_open_web
Compression=lzma
SolidCompression=yes
UninstallDisplayName=Open Web


[Files]
; Verifique se os caminhos dos arquivos estão corretos
Source: "dist\main.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "ico.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "sites.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Criando o atalho no Menu Iniciar
Name: "{group}\Open Web"; Filename: "{app}\main.exe"
; Criando o atalho na área de trabalho (desktop)
Name: "{userdesktop}\Open Web"; Filename: "{app}\main.exe"; IconFilename: "{app}\ico.ico"

[Registry]
; Caso deseje adicionar ao registro para facilitar a desinstalação
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\OpenWeb"; ValueType: string; ValueName: "DisplayName"; ValueData: "Open Web"
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\OpenWeb"; ValueType: string; ValueName: "UninstallString"; ValueData: "{uninstallexe}"
