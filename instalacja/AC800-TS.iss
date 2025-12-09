; Inno Setup Script - Bramster AC
[Setup]
AppName=AC800-TS 
AppVerName=AC800-TS
AppPublisher=Sonfy
AppPublisherURL=https://www.sonfy.pl
AppSupportURL=https://www.sonfy.pl
AppUpdatesURL=https://www.sonfy.pl
DefaultDirName={sd}\sonfy\AC800-TS
DefaultGroupName=Sonfy\AC800-TS
DisableProgramGroupPage=yes
OutputDir=C:\Users\gramsz\Desktop\AC800-TS\instalacja\instalka
OutputBaseFilename=AC800-TS
Compression=lzma
SolidCompression=yes
AlwaysRestart=no
PrivilegesRequired=admin

[Languages]
Name: pl; MessagesFile: "compiler:Languages\Polish.isl"; LicenseFile: ".\LicencjaPL.txt"

[Messages]
pl.BeveledLabel=Polish

[CustomMessages]
pl.MyDescription=Opis
pl.FileMissingError=Plik %1 nie zosta³ znaleziony w katalogu instalacyjnym. SprawdŸ, czy plik istnieje w folderze Ÿród³owym.
pl.DriverInstallPrompt=W trakcie instalacji sterownika kliknij "Zainstaluj" w pojawiaj¹cych siê oknach.

[Files]
Source: "C:\Users\gramsz\Desktop\AC800-TS\instalacja\LicencjaPL.txt"; DestDir: "{tmp}"; Flags: ignoreversion deleteafterinstall; Languages: pl
Source: "C:\Users\gramsz\Desktop\AC800-TS\instalacja\CH343SER.exe"; DestDir: "{tmp}"; Flags: ignoreversion deleteafterinstall; MinVersion: 0,5.0
Source: "C:\Users\gramsz\Desktop\AC800-TS\instalacja\AC800-TS.exe"; DestDir: "{app}"; Flags: ignoreversion

[INI]
Filename: "{tmp}\Internet shortcutPL.url"; Section: "InternetShortcut"; Key: "URL"; String: "http://www.sonfy.pl"

[Icons]
Name: "{group}\AC800-TS"; Filename: "{app}\AC800-TS.exe"; WorkingDir: "{app}"
Name: "{group}\Strona internetowa sonfy.pl"; Filename: "{tmp}\Internet shortcutPL.url"; Languages: pl
Name: "{userdesktop}\AC800-TS"; Filename: "{app}\AC800-TS.exe"; WorkingDir: "{app}"

[Run]
Filename: "{tmp}\CH343SER.exe"; Parameters: "/silent"; StatusMsg: "Instalowanie sterownika CH343"; Flags: waituntilterminated
;Filename: "{app}\Bramster.exe"; Description: "Uruchom Bramster AC"; Flags: nowait postinstall skipifsilent

[Code]
procedure CurStepChanged(CurStep: TSetupStep);
var
  FilePath: String;
begin
  if CurStep = ssInstall then
  begin
    FilePath := ExpandConstant('{tmp}\CH343SER.exe');
    if FileExists(FilePath) then
    begin
      //MsgBox(CustomMessage('pl.DriverInstallPrompt'), mbInformation, MB_OK);
    end;
  end;
  if CurStep = ssPostInstall then
  begin
    FilePath := ExpandConstant('{app}\AC800-TS.exe');
    if not FileExists(FilePath) then
    begin
      //MsgBox(Format(CustomMessage('pl.FileMissingError'), ['Bramster.exe']), mbError, MB_OK);
    end;
  end;
end;
