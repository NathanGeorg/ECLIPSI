# EcliPsi Backend - P.I. 1

API inicial do EcliPsi para a primeira entrega.

## Escopo

- Cadastro de usuário
- Login
- Usuários paciente/profissional
- Listagem de profissionais
- Filtros por especialidade, abordagem e modalidade
- Visualização do perfil profissional
- SQLite
- Seed com dados fictícios

Agendamento não faz parte desta versão.

## Executar

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

Linux/macOS:
```bash
source .venv/bin/activate
```

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Swagger:
http://127.0.0.1:8000/docs

## Usuários fictícios

João Banana:
- e-mail: joao@eclipsi.test
- senha: 123456
- tipo: paciente

Maria Demal:
- e-mail: maria@eclipsi.test
- senha: 123456
- tipo: profissional

Carlos Souza:
- e-mail: carlos@eclipsi.test
- senha: 123456
- tipo: profissional

## Endpoints

POST /auth/register
POST /auth/login

GET /professionals
GET /professionals/{professional_id}

Filtros:
- specialty
- approach
- modality

O banco eclipsi.db é criado localmente e está no .gitignore.
