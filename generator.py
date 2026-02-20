"""
Gerador de conteúdo para Instagram usando Groq API (gratuito)
"""

import os
from datetime import datetime
from groq import Groq
from config import CONTAS, CONFIGURACOES
from prompts import (
    get_post_prompt,
    get_reel_prompt,
    get_carrossel_prompt,
    get_stories_prompt
)

class InstagramContentGenerator:

    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"
        
    def pesquisar_tendencias(self, keywords):
        """Pesquisa tendências usando web search do Claude"""
        
        search_query = " ".join(keywords[:3])  # Usa as 3 primeiras keywords
        
        prompt = f"""
Pesquise as principais tendências atuais sobre: {search_query}

Foque em:
- Tendências visuais e estéticas
- Hashtags em alta
- Formatos de conteúdo que estão funcionando
- Músicas/áudios populares para Reels

Resuma em até 200 palavras as descobertas mais relevantes para criação de conteúdo.
"""
        
        try:
            message = self.client.chat.completions.create(
                model=self.model,
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )

            return message.choices[0].message.content
            
        except Exception as e:
            print(f"Erro na pesquisa de tendências: {e}")
            return "Tendências não disponíveis - gerando conteúdo baseado em conhecimento base."
    
    def gerar_conteudo(self, prompt_text, max_tokens=2000):
        """Gera conteúdo usando Claude"""
        
        try:
            message = self.client.chat.completions.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt_text}]
            )

            return message.choices[0].message.content
            
        except Exception as e:
            print(f"Erro na geração de conteúdo: {e}")
            return None
    
    def gerar_posts(self, conta_id, quantidade=1):
        """Gera posts informativos"""
        
        conta = CONTAS[conta_id]
        tendencias = self.pesquisar_tendencias(conta['keywords_pesquisa'])
        
        posts = []
        for i in range(quantidade):
            print(f"Gerando post {i+1}/{quantidade}...")
            
            prompt = get_post_prompt(conta, tendencias)
            conteudo = self.gerar_conteudo(prompt)
            
            if conteudo:
                posts.append(conteudo)
        
        return posts
    
    def gerar_reels(self, conta_id, quantidade=1):
        """Gera roteiros de Reels"""
        
        conta = CONTAS[conta_id]
        tendencias = self.pesquisar_tendencias(conta['keywords_pesquisa'] + ["reels tendências"])
        
        reels = []
        for i in range(quantidade):
            print(f"Gerando reel {i+1}/{quantidade}...")
            
            prompt = get_reel_prompt(conta, tendencias)
            conteudo = self.gerar_conteudo(prompt)
            
            if conteudo:
                reels.append(conteudo)
        
        return reels
    
    def gerar_carrosseis(self, conta_id, quantidade=1):
        """Gera carrosséis educacionais"""
        
        conta = CONTAS[conta_id]
        tendencias = self.pesquisar_tendencias(conta['keywords_pesquisa'])
        
        carrosseis = []
        for i in range(quantidade):
            print(f"Gerando carrossel {i+1}/{quantidade}...")
            
            prompt = get_carrossel_prompt(conta, tendencias)
            conteudo = self.gerar_conteudo(prompt, max_tokens=3000)
            
            if conteudo:
                carrosseis.append(conteudo)
        
        return carrosseis
    
    def gerar_stories_por_dia(self, conta_id, stories_por_dia):
        """Gera stories por dia com quantidade variável."""

        conta = CONTAS[conta_id]
        all_stories = []
        total_dias = len(stories_por_dia)

        for dia, quantidade_dia in enumerate(stories_por_dia, 1):
            if quantidade_dia <= 0:
                all_stories.append({
                    "dia": dia,
                    "quantidade": 0,
                    "conteudo": "Sem stories planejados para este dia."
                })
                continue

            print(f"Gerando stories do dia {dia}/{total_dias} ({quantidade_dia} stories)...")

            prompt = get_stories_prompt(conta, quantidade=quantidade_dia)
            conteudo = self.gerar_conteudo(prompt, max_tokens=2500)

            all_stories.append({
                "dia": dia,
                "quantidade": quantidade_dia,
                "conteudo": conteudo or "Falha ao gerar stories para este dia."
            })

        return all_stories

    def gerar_stories(self, conta_id, quantidade=36):
        """Compatibilidade: mantém fluxo antigo dividindo em blocos de 6 stories."""

        dias = max(1, quantidade // 6)
        return self.gerar_stories_por_dia(conta_id, [6] * dias)
    
    def salvar_conteudo(self, conta_id, posts, reels, carrosseis, stories):
        """Salva todo conteúdo em arquivos markdown organizados"""
        
        # Criar estrutura de pastas
        data_hoje = datetime.now().strftime("%Y-%m-%d")
        pasta_base = os.path.join(CONFIGURACOES['pasta_output'], f"semana_{data_hoje}", conta_id)
        
        # Criar diretórios
        os.makedirs(os.path.join(pasta_base, "posts"), exist_ok=True)
        os.makedirs(os.path.join(pasta_base, "reels"), exist_ok=True)
        os.makedirs(os.path.join(pasta_base, "carrosseis"), exist_ok=True)
        os.makedirs(os.path.join(pasta_base, "stories"), exist_ok=True)
        
        # Salvar posts
        for i, post in enumerate(posts, 1):
            caminho = os.path.join(pasta_base, "posts", f"post_{i}.md")
            with open(caminho, 'w', encoding='utf-8') as f:
                f.write(f"# Post {i}\n\n")
                f.write(post)
        
        # Salvar reels
        for i, reel in enumerate(reels, 1):
            caminho = os.path.join(pasta_base, "reels", f"reel_{i}.md")
            with open(caminho, 'w', encoding='utf-8') as f:
                f.write(f"# Reel {i}\n\n")
                f.write(reel)
        
        # Salvar carrosséis
        for i, carrossel in enumerate(carrosseis, 1):
            caminho = os.path.join(pasta_base, "carrosseis", f"carrossel_{i}.md")
            with open(caminho, 'w', encoding='utf-8') as f:
                f.write(f"# Carrossel {i}\n\n")
                f.write(carrossel)
        
        # Salvar stories
        for story_dia in stories:
            caminho = os.path.join(pasta_base, "stories", f"stories_dia_{story_dia['dia']}.md")
            with open(caminho, 'w', encoding='utf-8') as f:
                f.write(f"# Stories - Dia {story_dia['dia']}\n\n")
                f.write(story_dia['conteudo'])
        
        # Criar arquivo índice
        self._criar_indice(pasta_base, conta_id, data_hoje, posts, reels, carrosseis, stories)
        
        print(f"\n✅ Conteúdo salvo em: {pasta_base}")
        return pasta_base
    
    def _criar_indice(self, pasta_base, conta_id, data, posts, reels, carrosseis, stories):
        """Cria arquivo índice com resumo da semana"""
        
        conta = CONTAS[conta_id]
        caminho = os.path.join(pasta_base, "README.md")
        
        with open(caminho, 'w', encoding='utf-8') as f:
            f.write(f"# Conteúdo Semanal - {conta['nome']}\n\n")
            f.write(f"**Semana de:** {data}\n\n")
            f.write(f"**Gerado em:** {datetime.now().strftime('%d/%m/%Y às %H:%M')}\n\n")
            f.write("---\n\n")
            f.write("## 📊 Resumo\n\n")
            f.write(f"- **Posts:** {len(posts)}\n")
            f.write(f"- **Reels:** {len(reels)}\n")
            f.write(f"- **Carrosséis:** {len(carrosseis)}\n")
            f.write(f"- **Stories:** {len(stories)} dias (6 stories/dia)\n\n")
            f.write("---\n\n")
            f.write("## 📁 Estrutura\n\n")
            f.write("```\n")
            f.write("posts/\n")
            for i in range(len(posts)):
                f.write(f"  ├── post_{i+1}.md\n")
            f.write("\nreels/\n")
            for i in range(len(reels)):
                f.write(f"  ├── reel_{i+1}.md\n")
            f.write("\ncarrosseis/\n")
            for i in range(len(carrosseis)):
                f.write(f"  ├── carrossel_{i+1}.md\n")
            f.write("\nstories/\n")
            for story in stories:
                f.write(f"  ├── stories_dia_{story['dia']}.md\n")
            f.write("```\n\n")
            f.write("---\n\n")
            f.write("## 🎯 Pilares Estratégicos\n\n")
            for pilar in conta['pilares']:
                f.write(f"- {pilar}\n")
            f.write("\n---\n\n")
            f.write("## 💡 Instruções\n\n")
            f.write("1. Revise cada arquivo individualmente\n")
            f.write("2. Ajuste conforme necessário\n")
            f.write("3. Programe no Meta Business Suite ou ferramenta de sua preferência\n")
            f.write("4. Monitore engajamento para feedback do próximo ciclo\n")
