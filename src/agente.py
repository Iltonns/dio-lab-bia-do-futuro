import json
import os
import pandas as pd
from openai import OpenAI
from config import OPENAI_API_KEY, DATA_DIR

class StherAgent:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.dados_cliente = self._carregar_json('perfil_investidor.json')
        self.produtos = self._carregar_json('produtos_financeiros.json')
        self.dividas = self._carregar_json('dividas.json')
        # Tenta carregar o CSV mais recente ou o padrão
        self.transacoes = self._carregar_dados_financeiros(['financeiro_2026.csv', 'transacoes.csv'])

    def _carregar_json(self, filename):
        """Carrega arquivos JSON da pasta data."""
        caminho = os.path.join(DATA_DIR, filename)
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except Exception as e:
            return {"erro": str(e)}

    def _carregar_dados_financeiros(self, filenames):
        """Carrega dados financeiros (CSV) e retorna um resumo."""
        for filename in filenames:
            caminho = os.path.join(DATA_DIR, filename)
            if os.path.exists(caminho):
                try:
                    df = pd.read_csv(caminho)
                    # Cria um resumo simples para o prompt não ficar muito grande
                    if 'Categoria' in df.columns and 'Valor' in df.columns:
                        resumo = df.groupby('Categoria')['Valor'].sum().to_dict()
                        return str(resumo)
                    return df.head(10).to_string()
                except Exception:
                    continue
        return "Sem dados de transações disponíveis."

    def _montar_system_prompt(self):
        """Monta o prompt do sistema com base no template e dados carregados."""
        
        template = """
Você é a **Sther**, uma educadora financeira pessoal, empática, paciente e didática.
Seu objetivo é ajudar o usuário a organizar suas finanças, sair das dívidas e encontrar equilíbrio financeiro, sempre com clareza e tranquilidade.

### CONTEXTO DO USUÁRIO
Os dados abaixo representam a situação atual do usuário. Use-os para personalizar suas respostas.

**Dados do Cliente:**
{{DADOS_CLIENTE}}

**Dívidas em Aberto:**
{{DIVIDAS}}

**Resumo de Gastos/Transações:**
{{RESUMO_GASTOS}}

**Produtos Financeiros Disponíveis (para explicação):**
{{PRODUTOS}}

### DIRETRIZES DE PERSONALIDADE
1. **Acolhimento:** Problemas financeiros geram ansiedade. Comece com frases que acalmem. Nunca julgue gastos passados.
2. **Didática:** Explique conceitos complexos de forma simples (ex: use analogias).
3. **Tom de Voz:** Informal, acessível, mas profissional. Use "a gente" para gerar proximidade.

### REGRAS DE OURO (SEGURANÇA)
1. **Anti-Alucinação:** Só cite dados que estão no contexto. Se não souber, diga "Não tenho essa informação no momento".
2. **Limites de Atuação:** NÃO recomende compra de ativos específicos. NÃO negocie dívidas diretamente. NÃO peça senhas.
3. **Foco na Dívida:** Se houver dívidas, a prioridade é a organização para quitação (Método Bola de Neve vs Maior Juros).

### ESTRUTURA DE RESPOSTA
- Valide o sentimento do usuário.
- Analise os dados fornecidos.
- Proponha um próximo passo prático e pequeno.
"""
        # Substituição das variáveis
        prompt = template.replace("{{DADOS_CLIENTE}}", json.dumps(self.dados_cliente, indent=2, ensure_ascii=False))
        prompt = prompt.replace("{{DIVIDAS}}", json.dumps(self.dividas, indent=2, ensure_ascii=False))
        prompt = prompt.replace("{{RESUMO_GASTOS}}", self.transacoes)
        prompt = prompt.replace("{{PRODUTOS}}", json.dumps(self.produtos, indent=2, ensure_ascii=False))
        
        return prompt

    def responder(self, historico_mensagens):
        """Gera resposta usando a LLM."""
        system_prompt = self._montar_system_prompt()
        messages = [{"role": "system", "content": system_prompt}] + historico_mensagens
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo", # Pode ser alterado para gpt-4 ou outro modelo
            messages=messages,
            temperature=0.7
        )
        return response.choices[0].message.content