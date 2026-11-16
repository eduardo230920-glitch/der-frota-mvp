# MVP — Gestão de Manutenção da Frota do DER-DF

Aplicação web demonstrativa para cadastro de veículos oficiais, registro de solicitações de manutenção, atualização de situação e consulta ao histórico.

## Requisitos

- Python 3.12
- pip

## Instalação no Windows (Prompt de Comando)

1. Extraia o arquivo ZIP.
2. Abra o Prompt de Comando na pasta `der_frota_mvp`.
3. Crie o ambiente virtual:

```bat
py -3.12 -m venv .venv
```

4. Ative o ambiente:

```bat
.venv\Scripts\activate
```

5. Instale as dependências:

```bat
python -m pip install -r requirements.txt
```

6. Inicie a aplicação:

```bat
python app.py
```

7. Abra no navegador:

`http://127.0.0.1:5000`

## Acesso demonstrativo

- Usuário: `servidor.der`
- Senha: `Der@12345`

A base SQLite `der_frota.db` é criada automaticamente na primeira execução.

## Executar os testes

Com o ambiente virtual ativado:

```bat
python -m pytest -v
```

## Estrutura

```text
der_frota_mvp/
├── app.py
├── requirements.txt
├── README.md
├── der_frota.db        (criado na execução)
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── vehicles.html
│   ├── vehicle_form.html
│   ├── vehicle_detail.html
│   ├── maintenances.html
│   ├── maintenance_form.html
│   └── error.html
├── static/
│   └── css/style.css
└── tests/
    ├── conftest.py
    └── test_app.py
```

## Funcionalidades implementadas

- Autenticação demonstrativa com senha armazenada em hash.
- Cadastro e consulta de veículos.
- Pesquisa por placa, modelo ou patrimônio.
- Registro de manutenção vinculado a veículo.
- Situação: Pendente, Em andamento e Concluída.
- Consulta ao histórico de manutenção por veículo.
- Painel com indicadores e solicitações recentes.
- Validação de campos, consultas parametrizadas e proteção CSRF básica.
- Interface responsiva com Bootstrap.

## Observações importantes

Este código é um MVP acadêmico para demonstração e validação. Não está homologado nem autorizado para uso com dados operacionais do DER-DF. Antes de qualquer implantação institucional, é necessário substituir a chave secreta, configurar HTTPS, revisar autenticação e perfis de acesso, reforçar proteção CSRF e auditoria, definir política de backup e obter autorização da área de TI. O login demonstrativo não representa integração com credenciais institucionais.
