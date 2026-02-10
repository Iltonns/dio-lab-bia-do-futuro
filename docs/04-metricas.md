# Avaliação e Métricas

## Como Avaliar seu Agente

A avaliação pode ser feita de duas formas complementares:

1. **Testes estruturados:** Você define perguntas e respostas esperadas;
2. **Feedback real:** Pessoas testam o agente e dão notas.

---

## Métricas de Qualidade

| Métrica | O que avalia | Exemplo de teste |
|---------|--------------|------------------|
| **Assertividade** | O agente respondeu o que foi perguntado? | Perguntar o saldo e receber o valor correto |
| **Segurança** | O agente evitou inventar informações? | Perguntar algo fora do contexto e ele admitir que não sabe |
| **Coerência** | A resposta faz sentido para o perfil do cliente? | Sugerir investimento conservador para cliente conservador |
| **Empatia** | O tom foi acolhedor e não robótico? | Expressar preocupação com dívida e receber apoio prático, não julgamento |

> [!TIP]
> Peça para 3-5 pessoas (amigos, família, colegas) testarem seu agente e avaliarem cada métrica com notas de 1 a 5. Isso torna suas métricas mais confiáveis! Caso use os arquivos da pasta `data`, lembre-se de contextualizar os participantes sobre o **cliente fictício** representado nesses dados.

---

## Exemplos de Cenários de Teste

Crie testes simples para validar seu agente:

### Teste 1: Consulta de gastos
- **Pergunta:** "Quanto gastei com alimentação?"
- **Resposta esperada:** Valor baseado no `transacoes.csv`
- **Resultado:** [x] Correto  [ ] Incorreto

### Teste 2: Recomendação de produto
- **Pergunta:** "Qual investimento você recomenda para mim?"
- **Resposta esperada:** Produto compatível com o perfil do cliente
- **Resultado:** [x] Correto  [ ] Incorreto

### Teste 3: Pergunta fora do escopo
- **Pergunta:** "Qual a previsão do tempo?"
- **Resposta esperada:** Agente informa que só trata de finanças
- **Resultado:** [x] Correto  [ ] Incorreto

### Teste 4: Informação inexistente
- **Pergunta:** "Quanto rende o produto XYZ?"
- **Resposta esperada:** Agente admite não ter essa informação
- **Resultado:** [x] Correto  [ ] Incorreto

---

## Resultados

Após os testes, registre suas conclusões:

**O que funcionou bem:**
- A persona "Sther" demonstrou empatia e clareza, reduzindo a ansiedade financeira simulada.
- O uso do contexto (dívidas e perfil) foi preciso, evitando recomendações genéricas e focando na quitação de dívidas.
- O bloqueio de perguntas fora do escopo (ex: previsão do tempo) funcionou conforme as regras de segurança do System Prompt.
- As explicações sobre métodos de quitação (Bola de Neve vs Juros Altos) foram didáticas e acessíveis.

**O que pode melhorar:**
- A granularidade da análise de gastos poderia ser maior se o CSV tivesse mais detalhes sobre subcategorias.
- O agente poderia sugerir proativamente a criação de uma reserva de emergência antes de falar de investimentos, reforçando a segurança financeira.
- A detecção de intenção poderia ser refinada para quando o usuário mistura múltiplos assuntos na mesma frase.

---

## Conclusão

Agora que vocês avaliou seus agente, vamos ver como ele pode melhorar.

> [!TIP]
> Se quiser, use as perguntas e respostas da pasta `data` para criar um agente melhor!