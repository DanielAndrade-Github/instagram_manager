"""
Script principal para geração automatizada de conteúdo Instagram
Execução: python main.py
"""

import os
from dotenv import load_dotenv
from generator import InstagramContentGenerator
from config import CONTAS

def main():
    """Função principal de execução"""
    
    print("=" * 60)
    print("📱 GERADOR DE CONTEÚDO INSTAGRAM")
    print("=" * 60)
    print()
    
    # Carregar variáveis de ambiente
    load_dotenv()
    # Compatibilidade: aceita nome antigo (API_KEY) e nome explícito.
    api_key = os.getenv('ANTHROPIC_API_KEY') or os.getenv('API_KEY')
    
    if not api_key:
        print("❌ ERRO: chave da Anthropic não encontrada!")
        print("Crie um arquivo .env com sua chave:")
        print("ANTHROPIC_API_KEY=sk-ant-...")
        print("ou API_KEY=sk-ant-...")
        return
    
    # Inicializar gerador
    generator = InstagramContentGenerator(api_key)
    
    # Processar cada conta
    for conta_id, conta_info in CONTAS.items():
        print(f"\n🎯 Processando: {conta_info['nome']}")
        print("-" * 60)
        
        volume = conta_info['volume']
        
        # Gerar conteúdos
        print("\n📝 Gerando posts...")
        posts = generator.gerar_posts(conta_id, volume['posts'])
        
        print("\n🎬 Gerando reels...")
        reels = generator.gerar_reels(conta_id, volume['reels'])
        
        print("\n📊 Gerando carrosséis...")
        carrosseis = generator.gerar_carrosseis(conta_id, volume['carrosseis'])
        
        print("\n📲 Gerando stories...")
        stories = generator.gerar_stories(conta_id, volume['stories'])
        
        # Salvar tudo
        print("\n💾 Salvando conteúdo...")
        pasta = generator.salvar_conteudo(
            conta_id, 
            posts, 
            reels, 
            carrosseis, 
            stories
        )
        
        print(f"\n✅ Concluído para {conta_info['nome']}!")
        print(f"📁 Arquivos salvos em: {pasta}")
    
    print("\n" + "=" * 60)
    print("✨ GERAÇÃO COMPLETA!")
    print("=" * 60)
    print("\nPróximos passos:")
    print("1. Revise os arquivos .md gerados")
    print("2. Faça ajustes necessários")
    print("3. Use o conteúdo no Instagram")
    print()

if __name__ == "__main__":
    main()
