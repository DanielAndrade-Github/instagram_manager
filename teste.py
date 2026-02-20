"""
Script de teste rápido - gera apenas 1 exemplo de cada tipo
Útil para testar sem consumir muita API
"""

import os
from dotenv import load_dotenv
from generator import InstagramContentGenerator
from config import CONTAS

def teste_rapido():
    """Gera apenas 1 exemplo de cada tipo de conteúdo"""
    
    print("🧪 MODO TESTE - Gerando 1 exemplo de cada tipo\n")
    
    load_dotenv()
    api_key = os.getenv('GROQ_API_KEY')

    if not api_key:
        print("❌ ERRO: chave da Groq não encontrada!")
        print("Adicione GROQ_API_KEY=gsk_... no .env (chave gratuita em console.groq.com)")
        return
    
    generator = InstagramContentGenerator(api_key)

    for conta_id, conta in CONTAS.items():
        print(f"📱 Testando com: {conta['nome']}\n")

        print("1️⃣ Gerando 1 post...")
        posts = generator.gerar_posts(conta_id, 1)

        print("\n2️⃣ Gerando 1 reel...")
        reels = generator.gerar_reels(conta_id, 1)

        print("\n3️⃣ Gerando 1 carrossel...")
        carrosseis = generator.gerar_carrosseis(conta_id, 1)

        print("\n4️⃣ Gerando 6 stories (1 dia)...")
        stories = generator.gerar_stories(conta_id, 6)

        print("\n💾 Salvando exemplos...")
        pasta = generator.salvar_conteudo(conta_id, posts, reels, carrosseis, stories)

        print(f"\n✅ {conta['nome']} concluído!")
        print(f"📁 Exemplos salvos em: {pasta}\n")
        print("-" * 50 + "\n")

    print("🎉 Todas as contas geradas!")
    print("\n👀 Revise os arquivos para validar a qualidade antes de rodar em produção.")

if __name__ == "__main__":
    teste_rapido()
