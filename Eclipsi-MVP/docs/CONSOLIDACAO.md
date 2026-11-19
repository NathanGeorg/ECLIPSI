# Consolidação

Foi criada uma base canonical independente em `Eclipsi-MVP/`, mantendo `Eclipsi/` como código original.

O backend existente foi usado como evidência de domínio (usuário, profissional e busca), mas não reutilizado como runtime por não possuir autenticação assinada, agendamento, prontuário, avaliações e administração. O modelo do repositório ARKSTAR64 foi consultado como referência de domínio/PWA/dashboard; suas questões críticas de IDOR e migração não foram incorporadas.

O PDF do portfólio de Engenharia de Software foi incorporado como fonte acadêmica para histórias US01-US09 e critérios de aceitação. Os campos CRM/CRP/UF, o preço histórico da consulta e o fluxo de conclusão antes da avaliação foram alinhados ao documento.
