# AudioLocker

Aplicativo de console em Python para controlar o volume de áudio do Windows.

O AudioLocker mantém o volume bloqueado em um limite definido e permite que um atendente libere temporariamente o áudio mediante senha.

## Funcionamento

O AudioLocker deverá funcionar seguindo este fluxo:

                 ┌──────────────┐
                 │   BLOQUEADO  │
                 └──────┬───────┘
                        │
                   senha correta
                        │
                        ▼
                 ┌──────────────┐
                 │   LIBERADO   │
                 └──────┬───────┘
                        │
                    tempo acaba
                        │
                        ▼
                 ┌──────────────┐
                 │   BLOQUEADO  │
                 └──────────────┘

### BLOQUEADO

O volume não pode ultrapassar o limite definido em `MAX_VOLUME`.

### LIBERADO

O usuário pode controlar normalmente o volume durante o período de liberação.

Quando o tempo termina, o sistema volta automaticamente para o estado `BLOQUEADO`.

## Estrutura

```text
audiolocker/
├── main.py        # Lógica do AudioLocker
├── audio.py       # Controle do áudio do Windows
├── requirements.txt
└── README.md
```

## Tecnologias

* Python
* [pycaw](https://github.com/AndreMiras/pycaw)
* comtypes
* Windows Core Audio

## Configuração

O limite de volume é definido pela constante:

```python
MAX_VOLUME = 0
```

O valor corresponde à porcentagem máxima permitida.

Por exemplo:

```python
MAX_VOLUME = 20
```

permite volume de até 20%.

## Execução

Ative o ambiente virtual:

```powershell
.venv\Scripts\Activate.ps1
```

Execute:

```powershell
python main.py
```

## Observação

A detecção automática de fones não faz parte do projeto atualmente. A liberação do áudio será feita manualmente pelo atendente através de senha.
