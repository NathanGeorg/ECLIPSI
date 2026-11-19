# AGENTS.md

## Escopo
Este diretório é o MVP consolidado do ECLIPSI. O código em `Eclipsi/` é original e deve permanecer disponível como fonte histórica.

## Diretrizes
- Use Python, FastAPI, SQLAlchemy e SQLite no backend canonical.
- Use dados sintéticos somente.
- Não adicione credenciais reais, chaves privadas, bancos de produção ou dados pessoais.
- Toda operação sensível deve validar usuário autenticado e papel.
- Mantenha migração e seed reproduzíveis.
- Prefira mudanças pequenas e testáveis.

## Executar
```powershell
cd Eclipsi-MVP
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
python scripts\bootstrap.py
python -m uvicorn backend.app:app --reload --port 8000
```

