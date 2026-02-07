# Base de Conhecimento

[!TIP]
**Prompt sugerido para esta etapa:**

Preciso organizar as minhas finanças, sair das dívidas e encontrar equilíbrio financeiro. Como posso ajudar?

---

## Dados Utilizados

Descreva se usou os arquivos da pasta `data`, por exemplo:

| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `financeiro_2026.csv` | CSV | **(Dados Reais)** Analisar padrão de gastos e fluxo de caixa real |
| `perfil_investidor.json` | JSON | Definir o momento financeiro (foco em sair das dívidas) |
| `dividas.json` | JSON | Listar credores, taxas de juros e vencimentos para estratégias de quitação |
| `produtos_financeiros.json` | JSON | Fornecer explicações didáticas sobre investimentos (`explicacao_simples`) |

> [!TIP]
> **Quer um dataset mais robusto?** Você pode utilizar datasets públicos do [Hugging Face](https://huggingface.co/datasets) relacionados a finanças, desde que sejam adequados ao contexto do desafio.

---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

- **`financeiro_2026.csv`**: Substituição do `transacoes.csv` por dados reais, permitindo uma análise verdadeira do orçamento.
- **`perfil_investidor.json`**: Adaptado para um cenário de "reorganização financeira" (reserva zerada e patrimônio baixo), testando a capacidade de acolhimento da Sther.
- **`dividas.json`**: Criado em formato JSON (substituindo CSV) para facilitar a manipulação de taxas de juros e datas para o cálculo do método "Bola de Neve".
- **`produtos_financeiros.json`**: Enriquecido com o campo `explicacao_simples` para que o agente explique conceitos técnicos de forma acessível, sem "alucinar" definições complexas.

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

Existem duas possibilidades de carregamento: 
1. Injetar os dados diretamente no prompt;
2. Carregar os arquivos via código como exemplo abaixo.

```python
import json
import pandas as pd

# 1. Carregamento dos JSONs (Perfil, Dívidas, Produtos)
def carregar_json(caminho):
    with open(caminho, 'r', encoding='utf-8') as f:
        return json.load(f)

perfil = carregar_json('data/perfil_investidor.json')
dividas = carregar_json('data/dividas.json')
produtos = carregar_json('data/produtos_financeiros.json')

# 2. Processamento do CSV Real (Resumo de Gastos)
df_financeiro = pd.read_csv('data/financeiro_2026.csv')
# Exemplo: Agrupamento por categoria para economizar tokens no prompt
resumo_gastos = df_financeiro.groupby('Categoria')['Valor'].sum().to_dict()
```

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

As informações críticas (Dívidas e Perfil) compõem o "Estado Atual do Cliente" no System Prompt para garantir que todas as respostas considerem a situação de endividamento.

---

'''teste
DADOS DO CLIENTE:
{
  "nome": "Eleilton Santos",
  "idade": 32,
  "profissao": "Analista de dados",
  "renda_mensal": 3500.00,
  "perfil_investidor": "moderado",
  "objetivo_principal": "Sair das dívidas e organizar o orçamento",
  "patrimonio_total": 500.00,
  "reserva_emergencia_atual": 0.00,
  "aceita_risco": false,
  "metas": [
    {
      "meta": "Quitar dívida do cartão",
      "valor_necessario": 1000.00,
      "prazo": "2026-12"
    },
    {
      "meta": "Entrada do apartamento",
      "valor_necessario": 50000.00,
      "prazo": "2027-12"
    }
  ]
}


DÍVIDAS EM ABERTO:
[
  {
    "credor": "Cartão de Crédito Banco X",
    "valor_total": 1000.00,
    "taxa_juros_mensal": 12.0,
    "vencimento": "2026-02-15"
  },
  {
    "credor": "Empréstimo Pessoal",
    "valor_total": 5000.00,
    "taxa_juros_mensal": 3.0,
    "vencimento": "2026-02-20"
  },
  {
    "credor": "Parcela de Financiamnto de Veículo",
    "valor_total": 1125.00,
    "taxa_juros_mensal": 9.0,
    "vencimento": "2026-01-21"
  },
  {
    "credor": "Faculdade Universitária",
    "valor_total": 1600.00,
    "taxa_juros_mensal": 5.0,
    "vencimento": "2026-01-10"
  },
  {
    "credor": "Internet Movel e Residencial",
    "valor_total": 350.00,
    "taxa_juros_mensal": 7.0,
    "vencimento": "2026-01-10"
  },
  {
    "credor": "Aluguel do Imóvel",
    "valor_total": 2000.00,
    "taxa_juros_mensal": 0.0,
    "vencimento": "2026-02-23"
  },
  {
    "credor": "Viagem",
    "valor_total": 1000.00,
    "taxa_juros_mensal": 0.0,
    "vencimento": "2026-01-21"
  }
   
]

ÚLTIMAS TRANSACOES:
- 01/11: Supermercado - R$ 450
- 03/11: Streaming - R$ 55
...
'''

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

O exemplo de contexto montado segue o padrão abaixo, se baseia nos dados originais da base de conhecimento, mas os sintetiza deixando apenas as informações relevantes, assim o consumo de tokens diminui. Entretanto, vale lembrar que mais importante do que economizar tokens, é ler  todas as informações relevantes disponíveis em seu contexto.

```json
DADOS DO CLIENTE:
{
  "nome": "Eleilton Santos",
  "idade": 32,
  "profissao": "Analista de dados",
  "renda_mensal": 3500.00,
  "perfil_investidor": "moderado",
  "objetivo_principal": "Sair das dívidas e organizar o orçamento",
  "patrimonio_total": 500.00,
  "reserva_emergencia_atual": 0.00,
  "aceita_risco": false,
  "metas": [
    {
      "meta": "Quitar dívida do cartão",
      "valor_necessario": 1500.00,
      "prazo": "2026-12"
    },
    {
      "meta": "Entrada do apartamento",
      "valor_necessario": 50000.00,
      "prazo": "2027-12"
    }
  ]
}


DÍVIDAS EM ABERTO:
[
  {
    "credor": "Cartão de Crédito Banco X",
    "valor_total": 2000.00,
    "taxa_juros_mensal": 12.0,
    "vencimento": "2026-02-15"
  },
  {
    "credor": "Empréstimo Pessoal",
    "valor_total": 5000.00,
    "taxa_juros_mensal": 3.0,
    "vencimento": "2026-02-20"
  }
]

ÚLTIMAS TRANSACOES:
- 01/11: Supermercado - R$ 450
- 03/11: Streaming - R$ 55
...
'''
