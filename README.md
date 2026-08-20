# AudioLocker

O **AudioLocker** é um utilitário para Windows que executa na bandeja do sistema (*System Tray*) para controlar o volume mestre do SO, impedindo que ultrapasse um limite definido enquanto o sistema estiver **BLOQUEADO**.

A liberação é feita manualmente mediante senha por um tempo determinado.

---

## 🛠️ Tecnologias e Dependências

* **Python 3.10+**
* **pycaw**: Interface com a API *Windows Core Audio*.
* **pystray**: Gerenciamento de ícones e menus na bandeja do sistema.
* **Pillow**: Renderização dinâmica dos ícones de status (vermelho/verde).
* **Tkinter**: Interfaces nativas para os pop-ups de senha e assistente de configuração.

---

## 📁 Estrutura do Projeto

```text
audiolocker/
├── main.py              # Ponto de entrada e leitor de configurações
├── config_wizard.py     # Setup inicial (GUI) e gerenciamento do JSON
├── tray.py              # Interface na bandeja, menus e janelas de senha
├── audio.py             # Encapsulamento da API de áudio do Windows (pycaw)
├── requirements.txt     # Dependências do projeto
└── README.md            # Documentação técnica
```
---
##  ⚙️ Arquivo de Configuração (config.json)
O projeto armazena suas configurações em um arquivo JSON local chamado config.json.

### **Localização do Arquivo**: 
- No ambiente de desenvolvimento: Salvo na raiz da pasta do projeto.
- No Executável Compilado (.exe): Salvo no diretório local onde o .exe for executado (por exemplo, dentro de shell:startup).

### Estrutura do JSON
```
JSON
{
    "MAX_VOLUME": 0,
    "UNLOCK_TIME": 3600,
    "PASSWORD": "sua_senha_aqui"
}
```

MAX_VOLUME: Porcentagem máxima permitida quando bloqueado (ex: 0 a 100).

UNLOCK_TIME: Tempo de liberação em segundos (ex: 1800 = 30min, 3600 = 1h).

PASSWORD: Senha necessária para desbloquear e encerrar a aplicação.

---
## 🔄 Reset de Senha / Reconfiguração
Se a senha for esquecida ou for necessário reconfigurar o sistema do zero:

- Finalize o processo AudioLocker.exe pela opção SAIR na bandeja do sistema
- Localize e apague o arquivo config.json.
- Inicie o AudioLocker.exe novamente.

O assistente de Configuração Inicial abrirá automaticamente solicitando uma nova senha.

🚀 Compilação e Deploy (.exe)
1. Requisitos para Build
Certifique-se de estar com o ambiente virtual ativo e as dependências instaladas:

PowerShell
pip install pycaw pystray Pillow pyinstaller
2. Gerar o Executável
Execute o PyInstaller com a flag --noconsole para ocultar o terminal:

PowerShell
pyinstaller --noconsole --onefile --name="AudioLocker" main.py
O executável compilado será gerado na pasta dist/AudioLocker.exe.

3. Configurar Inicialização Automática (Startup)
Pressione Win + R, digite shell:startup e pressione Enter.

Cole o arquivo AudioLocker.exe (ou um atalho dele) dentro dessa pasta.

No primeiro boot do Windows, o assistente abrirá solicitando a senha inicial e salvará o config.json no local.