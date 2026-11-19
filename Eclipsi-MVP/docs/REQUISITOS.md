# Requisitos

| Código | Requisito | Cobertura |
|---|---|---|
| RF01 | Cadastro de pacientes | `POST /api/auth/register` |
| RF02 | Cadastro de profissionais | Cadastro com perfil e papel profissional |
| RF03 | Login por papel | Login assinado com guards |
| RF04 | Busca de profissionais | Filtros por especialidade e modalidade |
| RF05 | Agendamento | Validação de horário, sobreposição e conflito |
| RF06 | Agenda e prontuários | Endpoints de consulta e registro com privacidade |
| RF07 | Rendimentos | Estimativa por consultas concluídas e preço |
| RF08 | Avaliações | Nota 1-5 por consulta, uma avaliação por consulta |
| RF09 | Dashboard administrativo | Estatísticas protegidas por administrador |

Critérios adicionais do portfólio: cadastro profissional exige registro profissional e UF; busca aceita nome, especialidade e descrição; a consulta preserva o preço no momento do agendamento; a avaliação exige consulta concluída; o administrador pode listar, alterar papel/status e desativar usuários.
