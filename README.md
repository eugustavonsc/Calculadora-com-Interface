# Calculadora Profissional (Python + Tkinter)

Aplicação desktop de calculadora com interface gráfica em Python, empacotada como executável Windows e com instalador criado no Inno Setup.

## O que este projeto faz

Este projeto implementa uma calculadora com interface moderna usando Tkinter.

Funcionalidades principais:
- Operações matemáticas: soma, subtração, multiplicação e divisão.
- Proteção contra divisão por zero, com mensagem de erro amigável.
- Entrada decimal com vírgula na interface e conversão interna para ponto.
- Botão de limpar (C), inversão de sinal (+/-) e backspace no teclado.
- Encadeamento de operações (exemplo: 2 + 3 * 4 em fluxo sequencial).
- Formatação de número para reduzir ruído de ponto flutuante (exemplo: evita -0 e excessos de casas).
- Atalhos de teclado:
  - 0-9 para dígitos
  - Enter para calcular
  - Esc/Delete para limpar
  - Backspace para apagar último dígito

## Estrutura do projeto

- main.py: código-fonte da aplicação (interface, regras de cálculo e ponto de entrada).
- main.spec: configuração do PyInstaller para gerar o executável.
- calculadora-pro.iss: script do Inno Setup para gerar o instalador Windows.
- dist/main.exe: executável gerado pelo PyInstaller.
- Instalador_Calculadora.exe: instalador final gerado pelo Inno Setup.
- calculadora_pro.ico: ícone usado no app e no instalador.

## Como o executável foi gerado

O executável foi criado com PyInstaller usando o arquivo main.spec.

Passos:

1. Criar/ativar ambiente virtual (opcional, recomendado)

No PowerShell:

python -m venv .venv
.\.venv\Scripts\Activate.ps1

2. Instalar PyInstaller

pip install pyinstaller

3. Gerar o executável

pyinstaller main.spec

Resultado esperado:
- dist/main.exe

Observações do spec:
- O ícone calculadora_pro.ico é incluído no pacote.
- O app roda em modo janela (sem console), adequado para interface gráfica.

## Como o instalador foi gerado (Inno Setup)

O instalador foi criado a partir do arquivo calculadora-pro.iss.

### Configuração de diretório no arquivo .iss

No arquivo calculadora-pro.iss, existe a constante abaixo para definir o diretório base do projeto:

```iss
#define ProjetoDir "INSIRA_O_CAMINHO_DOS_ARQUIVOS"
```

Antes de compilar no Inno Setup, substitua INSIRA_O_CAMINHO_DOS_ARQUIVOS pelo caminho da pasta do projeto na sua máquina.

Exemplo:
```iss
#define ProjetoDir "C:\\CAMINHO\\DO\\PROJETO"
```

Passos para gerar o instalador:

1. Abra o Inno Setup.
2. Abra o arquivo calculadora-pro.iss.
3. Clique em Compile.

Resultado esperado:
- Instalador_Calculadora.exe

## Como executar em desenvolvimento

No PowerShell:

python main.py

## Tecnologias usadas

- Python 3
- Tkinter
- PyInstaller
- Inno Setup

## Melhorias futuras

- Histórico de operações
- Suporte a porcentagem e raiz quadrada
- Testes automatizados para funções matemáticas
- Pipeline de release automática com GitHub Actions
