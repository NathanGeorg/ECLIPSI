# ECLIPSI MVP consolidado

MVP acadêmico de demonstração com FastAPI, SQLAlchemy e SQLite. Todos os usuários e dados são sintéticos.

## Início rápido

```powershell
cd Eclipsi-MVP
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
python scripts\bootstrap.py
python -m uvicorn backend.app:app --reload --port 8000
```

- API: `http://127.0.0.1:8000`
- Swagger: `http://127.0.0.1:8000/docs`
- Frontend estático: abra `frontend/index.html` com um servidor local ou sirva a pasta.

```powershell
python -m http.server 8080 --directory frontend
```

## Credenciais sintéticas
Estas contas existem apenas no banco local criado pelo seed:

| Papel | E-mail | Senha |
|---|---|---|
| administrador | admin@example.com | Demo123! |
| profissional | ana.psi@example.com | Demo123! |
| paciente | pac1@example.com | Demo123! |

