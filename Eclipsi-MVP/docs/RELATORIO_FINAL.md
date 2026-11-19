# Relatório final

## Resultado
O MVP consolidado foi implementado em `Eclipsi-MVP/` sem alterar o código original em `Eclipsi/`.

## Cobertura
Autenticação por papel, cadastro de paciente/profissional, busca, agendamento protegido, conflitos, registros privados, avaliações, rendimentos e administração.

## Segurança
PBKDF2 com salt, token assinado HMAC, expiração, papel e isolamento de dados por usuário.

## Validação
Executado em Python 3.12.10:

- `python -m compileall -q backend scripts tests`: passou.
- `python -m pytest tests -q`: `6 passed`.
- `python scripts\bootstrap.py`: banco local criado com dados sintéticos.

## Alinhamento ao portfólio
O cadastro profissional valida registro e UF; a busca aceita nome, especialidade e descrição; agendamento preserva preço; conclusão precede avaliação; ganhos somam o preço histórico das consultas concluídas; administração oferece listagem, alteração e desativação.
