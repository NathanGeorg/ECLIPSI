# Arquitetura

```text
frontend/ -> HTTP -> backend FastAPI -> SQLAlchemy -> SQLite
                            |
                            +-> autenticação HMAC/PBKDF2
                            +-> guards por papel
```

## Persistência
`database/schema.sql` documenta o esquema; `backend/app.py` cria o esquema via SQLAlchemy; `scripts/bootstrap.py` cria dados sintéticos e é repetível.

## Entidades
Usuário, perfil profissional, consulta, registro clínico e avaliação.
