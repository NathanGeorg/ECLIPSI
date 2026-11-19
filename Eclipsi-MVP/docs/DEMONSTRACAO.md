# Demonstração

1. Execute `python scripts\bootstrap.py`.
2. Inicie `python -m uvicorn backend.app:app --reload --port 8000`.
3. Abra `/docs`.
4. Faça login com `pac1@example.com` / `Demo123!`.
5. Use o Swagger para listar profissionais e buscar por especialidade.
6. Teste um agendamento com um intervalo futuro.
7. Faça login como profissional `ana.psi@example.com` para agenda, registros e ganhos.
8. Faça login como administrador para o dashboard.
9. Opcionalmente sirva `frontend/` na porta 8080 e teste busca/login.
