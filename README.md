# Sistema de Gerenciamento e Acompanhamento da Manutenção da Frota — DER-DF

\<p align="center">   \*\*MVP — Produto Mínimo Viável\*\*

Sistema web para gerenciamento e acompanhamento dos serviços de manutenção dos veículos oficiais do Departamento de Estradas de Rodagem do Distrito Federal (DER-DF).

\</p>

---

## Sobre o projeto

O Sistema de Gerenciamento e Acompanhamento da Manutenção da Frota do DER-DF é uma aplicação web desenvolvida como parte de um projeto acadêmico do curso de Análise e Desenvolvimento de Sistemas.

A proposta consiste em oferecer uma solução digital para organizar e acompanhar as informações relacionadas à manutenção dos veículos oficiais, contribuindo para reduzir a dependência de controles manuais e facilitar o acesso ao histórico de serviços realizados.

O projeto foi desenvolvido no formato MVP (Minimum Viable Product), contemplando as funcionalidades essenciais para demonstrar a viabilidade da solução.

## Objetivo

Desenvolver uma aplicação web que permita centralizar informações sobre os veículos oficiais e seus respectivos registros de manutenção, proporcionando maior organização, rastreabilidade e facilidade de acompanhamento das solicitações.

## Funcionalidades

O sistema contempla as seguintes funcionalidades:

- **Cadastro de veículos:** registro das informações de identificação dos veículos oficiais.
- **Consulta de veículos:** visualização dos veículos cadastrados.
- **Registro de manutenção:** criação de registros de serviços relacionados a cada veículo.
- **Acompanhamento de status:** atualização das situações das manutenções.
- **Histórico de manutenção:** consulta dos registros associados a cada veículo.
- **Painel principal:** visualização resumida das informações e atividades do sistema.
- **Autenticação:** acesso ao sistema por meio de tela de login.

### Situações das manutenções

As solicitações podem apresentar os seguintes status:

- Pendente;
- Em andamento;
- Concluída.

## Tecnologias utilizadas

| Tecnologia    | Aplicação                                    |
| ------------- | -------------------------------------------- |
| Python 3.12   | Linguagem de programação                     |
| Flask 3.x     | Framework para desenvolvimento web           |
| SQLite        | Banco de dados                               |
| HTML5         | Estrutura das páginas                        |
| CSS3          | Estilização das interfaces                   |
| Bootstrap 5.3 | Componentes e responsividade                 |
| Jinja2        | Renderização dos templates                   |
| Pytest 8.x    | Testes automatizados                         |
| Git e GitHub  | Controle de versão e armazenamento do código |
| Render        | Hospedagem da aplicação                      |

## Arquitetura do projeto

A aplicação utiliza uma arquitetura monolítica organizada em camadas, separando a lógica da aplicação, as interfaces e os arquivos estáticos.

```text
der-frota-mvp/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── static/
│   └── css/
│       └── style.css
│
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── error.html
│   ├── login.html
│   ├── maintenance_form.html
│   ├── maintenances.html
│   ├── vehicle_detail.html
│   ├── vehicle_form.html
│   └── vehicles.html
│
└── tests/
    ├── conftest.py
    └── test_app.py
```

## Instalação e execução local

Para executar o projeto em ambiente local, é necessário ter o Python 3.12 instalado.

### 1. Clonar o repositório

```bash
git clone https://github.com/eduardo230920-glitch/der-frota-mvp.git
```

### 2. Acessar a pasta

```bash
cd der-frota-mvp
```

### 3. Criar o ambiente virtual

```bash
python -m venv .venv
```

### 4. Ativar o ambiente virtual

**Windows — PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows — Prompt de Comando (CMD):**

```cmd
.venv\Scripts\activate.bat
```

### 5. Instalar as dependências

```bash
python -m pip install -r requirements.txt
```

### 6. Executar a aplicação

```bash
python app.py
```

### 7. Acessar o sistema

Abra o navegador e acesse:

[http://127.0.0.1:5000](http://127.0.0.1:5000)

## Hospedagem

A aplicação está preparada para execução em servidor utilizando Gunicorn e foi publicada na plataforma Render.

**Acessar o sistema:**
[DER-FROTA-MVP — Aplicação Web](https://der-frota-mvp.onrender.com)

**Repositório do projeto:**
[GitHub — der-frota-mvp](https://github.com/eduardo230920-glitch/der-frota-mvp)

A disponibilidade da aplicação depende do serviço de hospedagem. Em instâncias gratuitas, pode ocorrer suspensão temporária por inatividade.

## Testes

O projeto possui estrutura de testes automatizados utilizando Pytest.

Para executar os testes, utilize:

```bash
python -m pytest
```

## Limitações do MVP

Esta versão tem finalidade acadêmica e demonstrativa. Não contempla:

- Integração com os sistemas institucionais do DER-DF;
- Aplicativo nativo para dispositivos móveis;
- Gestão financeira de contratos e serviços;
- Controle de estoque e aquisição de peças;
- Processamento automático de ordens de serviço externas.

A utilização institucional dependerá de avaliação técnica, adequações de segurança, infraestrutura, persistência de dados e autorização dos setores competentes.

## Segurança e dados

O sistema utiliza mecanismos básicos de autenticação, validação de informações e proteção de formulários.

Os dados utilizados na demonstração devem ser fictícios. A versão acadêmica não está homologada para armazenar informações institucionais ou dados operacionais reais.

**Atenção:** a configuração SQLite em hospedagens com armazenamento efêmero não garante a preservação dos dados após reinicializações ou novas implantações. Uma implantação definitiva exige armazenamento persistente e estratégia de backup.

## Objetivo de Desenvolvimento Sustentável

O projeto está relacionado ao **ODS 9 — Indústria, Inovação e Infraestrutura**, da Organização das Nações Unidas, por incentivar a modernização de processos administrativos por meio da utilização de soluções tecnológicas.

## Autor

**Eduardo Rodrigues**

Projeto acadêmico desenvolvido no curso de Análise e Desenvolvimento de Sistemas.

---

\<p align="center">
&#x20; \*\*DER-FROTA-MVP\*\*

Organização, tecnologia e inovação na gestão da frota pública.

\</p>
