; Defina o caminho base do projeto antes de compilar no Inno Setup.
; Exemplo: #define ProjetoDir "C:\\CAMINHO\\DO\\PROJETO"
#define ProjetoDir "INSIRA_O_CAMINHO_DOS_ARQUIVOS"

[Setup]
AppName=Calculadora Profissional
AppVersion=1.0
DefaultDirName={autopf}\CalculadoraPro
DefaultGroupName=Calculadora Pro
; Define o ícone que vai aparecer no arquivo do instalador pra não ficar aquele padrão feio
SetupIconFile={#ProjetoDir}\calculadora_pro.ico
Compression=lzma
SolidCompression=yes
OutputDir=.
OutputBaseFilename=Instalador_Calculadora

[Files]
; Puxando o executável que o PyInstaller gerou lá na pasta dist
Source: "{#ProjetoDir}\dist\main.exe"; DestDir: "{app}"; DestName: "CalculadoraPro.exe"; Flags: ignoreversion
; Copiando o ícone pra pasta de instalação só pra garantir que os atalhos não fiquem sem imagem
Source: "{#ProjetoDir}\calculadora_pro.ico"; DestDir: "{app}"

[Icons]
Name: "{group}\Calculadora Pro"; Filename: "{app}\CalculadoraPro.exe"; IconFilename: "{app}\calculadora_pro.ico"
Name: "{commondesktop}\Calculadora Pro"; Filename: "{app}\CalculadoraPro.exe"; IconFilename: "{app}\calculadora_pro.ico"

[Registry]
;cria a chave no registro pro Windows abrir o app sozinho no boot
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; \
    ValueType: string; ValueName: "CalculadoraProTask"; ValueData: """{app}\CalculadoraPro.exe"""; \
    Flags: uninsdeletevalue