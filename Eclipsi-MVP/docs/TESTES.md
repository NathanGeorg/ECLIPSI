# Testes

## Instalar
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
```

## Executar
```powershell
python -m compileall backend scripts
python -m pytest tests -q
```

O conjunto cobre cadastro/login, guardas de papel, e-mail duplicado, conflito de consulta, privacidade de registros, avaliação, ganhos e estatísticas administrativas.

## Resultado obtido
- Python 3.12.10
- `python -m compileall -q backend scripts tests`: passou.
- `python -m pytest tests -q`: `6 passed`, com 13 warnings de depreciação da biblioteca/testes.
- `python scripts\bootstrap.py`: banco SQLite local criado com dados sintéticos.
- Após alinhamento ao PDF anexado, `python -m compileall -q backend scripts tests` passou e `python -m pytest tests -q` passou com `6 passed`.
