# AudioLocker

O **AudioLocker** é um utilitário para Windows executado na **bandeja do sistema (System Tray)**, desenvolvido para controlar o volume mestre do sistema operacional.

Quando o sistema está **bloqueado**, o AudioLocker impede que o volume ultrapasse o limite máximo configurado. A liberação temporária do volume é realizada mediante uma senha e permanece válida pelo período definido nas configurações.

---

## 🛠️ Tecnologias e Dependências

O projeto utiliza:

* **Python 3.10+** — linguagem principal do projeto.
* **pycaw** — interface com a API de áudio do Windows.
* **pystray** — gerenciamento do ícone e do menu na bandeja do sistema.
* **Pillow** — criação e renderização dos ícones de status.
* **Tkinter** — criação das interfaces gráficas, incluindo o assistente de configuração e as janelas de senha.
* **PyInstaller** — compilação do projeto Python em um executável `.exe`.

As dependências de execução estão listadas no arquivo `requirements.txt`.

---

## 📁 Estrutura do Projeto

```text
audiolocker/
├── main.py              # Ponto de entrada da aplicação e carregamento das configurações
├── config_wizard.py     # Assistente de configuração inicial e gerenciamento do config.json
├── tray.py              # Interface da bandeja, menus e janelas de senha
├── audio.py             # Comunicação com a API de áudio do Windows através do pycaw
├── requirements.txt     # Dependências do projeto
└── README.md            # Documentação do projeto
```

---

## ⚙️ Arquivo de Configuração

O AudioLocker armazena suas configurações em um arquivo JSON chamado `config.json`.

### Localização

A localização do arquivo depende da forma como o programa está sendo executado:

* **Ambiente de desenvolvimento:** o arquivo é armazenado na raiz do projeto.
* **Executável compilado (`.exe`):** o arquivo é armazenado no diretório em que o executável está sendo executado.

Por exemplo, caso o `AudioLocker.exe` seja colocado na pasta de inicialização do Windows (`shell:startup`), o `config.json` será criado nesse mesmo diretório.

### Estrutura do `config.json`

```json
{
    "MAX_VOLUME": 0,
    "UNLOCK_TIME": 3600,
    "PASSWORD": "sua_senha_aqui"
}
```

### Parâmetros

| Parâmetro     | Descrição                                                                                           | Exemplo         |
| ------------- | --------------------------------------------------------------------------------------------------- | --------------- |
| `MAX_VOLUME`  | Volume máximo permitido enquanto o sistema estiver bloqueado. O valor deve estar entre `0` e `100`. | `50`            |
| `UNLOCK_TIME` | Tempo, em segundos, durante o qual o volume permanecerá desbloqueado.                               | `3600` = 1 hora |
| `PASSWORD`    | Senha utilizada para desbloquear o volume e encerrar a aplicação.                                   | `"minha_senha"` |

---

## 🔐 Funcionamento

O fluxo básico do AudioLocker é:

1. O programa é iniciado.
2. O AudioLocker verifica se existe um `config.json`.
3. Caso o arquivo não exista, o **Assistente de Configuração Inicial** é aberto.
4. O usuário define a senha, o limite de volume e o tempo de desbloqueio.
5. As configurações são armazenadas no `config.json`.
6. O programa é executado em segundo plano na bandeja do sistema.
7. Enquanto o sistema estiver bloqueado, o volume não poderá ultrapassar o limite configurado.
8. O desbloqueio temporário exige a senha.
9. Após o período definido em `UNLOCK_TIME`, o bloqueio de volume é aplicado novamente.

---

## 🔄 Reset de Senha / Reconfiguração

Caso a senha seja esquecida ou seja necessário reconfigurar o AudioLocker do zero:

1. Encerre o **AudioLocker** utilizando a opção **SAIR** disponível no menu da bandeja do sistema.
2. Localize o arquivo `config.json`.
3. Apague o arquivo.
4. Inicie o `AudioLocker.exe` novamente.

Como o arquivo de configuração não estará mais presente, o **Assistente de Configuração Inicial** será aberto automaticamente para criar uma nova configuração.

> **Atenção:** apagar o `config.json` remove a senha e todas as configurações atuais do programa.

---

# 🚀 Desenvolvimento

## 1. Criar o ambiente virtual

Recomenda-se utilizar um ambiente virtual Python para o desenvolvimento.

No PowerShell:

```powershell
python -m venv .venv
```

Ative o ambiente virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

Caso o ambiente virtual já exista, basta ativá-lo antes de executar o projeto.

---

## 2. Instalar as dependências

Com o ambiente virtual ativo, execute:

```powershell
pip install -r requirements.txt
```

Caso o `requirements.txt` ainda não exista ou seja necessário instalar as dependências manualmente:

```powershell
pip install pycaw pystray Pillow
```

Para instalar também o PyInstaller:

```powershell
pip install pyinstaller
```

---

## 3. Executar o projeto

Com o ambiente virtual ativo, execute:

```powershell
python main.py
```

O AudioLocker será iniciado e seu ícone ficará disponível na bandeja do sistema.

---

# 📦 Compilação do Executável

## 1. Instalar o PyInstaller

Caso ainda não esteja instalado:

```powershell
pip install pyinstaller
```

Ou:

```powershell
pip install -r requirements.txt
```

caso o PyInstaller esteja listado no arquivo de dependências.

---

## 2. Gerar o executável

Execute o seguinte comando na raiz do projeto:

```powershell
pyinstaller --noconsole --onefile --name="AudioLocker" main.py
```

### Parâmetros utilizados

* `--noconsole` — impede a abertura de uma janela de terminal junto com o programa.
* `--onefile` — gera um único arquivo executável.
* `--name="AudioLocker"` — define o nome do executável.

Após a compilação, o arquivo será gerado em:

```text
dist/
└── AudioLocker.exe
```

---

# 🖥️ Deploy e Inicialização Automática

Para iniciar o AudioLocker automaticamente junto com o Windows:

1. Pressione **Win + R**.
2. Digite:

```text
shell:startup
```

3. Pressione **Enter**.
4. Copie o `AudioLocker.exe` ou um atalho para essa pasta.

Ao iniciar o Windows, o AudioLocker será executado automaticamente.

Caso seja a primeira execução, o **Assistente de Configuração Inicial** será aberto para que a configuração seja criada.

O `config.json` será salvo no diretório em que o executável estiver sendo executado.

---

# 🔄 Configurando uma Nova Máquina

Para instalar o AudioLocker em outro computador:

### Passo 1 — Copiar o projeto

Copie os arquivos do projeto para a nova máquina.

### Passo 2 — Criar o ambiente virtual

No terminal do VS Code:

```powershell
python -m venv .venv
```

Ative o ambiente:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Passo 3 — Instalar as dependências

Com o ambiente virtual ativo:

```powershell
pip install -r requirements.txt
```

### Passo 4 — Executar

Para testar o projeto:

```powershell
python main.py
```

### Passo 5 — Gerar o executável

Caso seja necessário distribuir o programa como `.exe`:

```powershell
pyinstaller --noconsole --onefile --name="AudioLocker" main.py
```

O executável estará disponível em:

```text
dist/AudioLocker.exe
```

---

## 📌 Observações

* O AudioLocker foi desenvolvido especificamente para **Windows**.
* O `config.json` contém a senha utilizada pelo programa e, portanto, deve ser protegido contra alterações não autorizadas.
* O arquivo `config.json` **não deve ser versionado no Git** caso contenha uma senha real.
* Recomenda-se adicionar `config.json`, `.venv/`, `build/` e `dist/` ao `.gitignore` quando apropriado.

### Exemplo de `.gitignore`

```gitignore
.venv/
__pycache__/
build/
dist/
*.spec
config.json
```
