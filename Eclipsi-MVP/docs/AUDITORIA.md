# Auditoria

## Melhorias no MVP
- Senhas armazenadas com PBKDF2-HMAC-SHA256 e salt aleatório.
- Token assinado localmente com HMAC-SHA256 e expiração de 24 horas.
- Guards de papel para paciente, profissional e administrador.
- E-mail único em índice e validação de duplicidade.
- Conflito de agenda no banco por profissional e horário inicial, além da validação de sobreposição.
- Registros clínicos isolados por consulta e usuário.
- Administração protegida por papel.

## Riscos conhecidos e limitações
- Não usar em produção sem TLS, armazenamento seguro de segredo, refresh/revogação e audit log.
- O SQLite é adequado a demonstrações acadêmicas e não substitui banco gerenciado.
- O frontend é mínimo e não cobre todos os fluxos da UI Expo original.
- Não há envio real de email, pagamentos, videoconferência ou LGPD completa.
- Os dados são sintéticos e não representam pacientes reais.
