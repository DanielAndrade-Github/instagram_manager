"""
Sistema de Prompts Otimizado - Geração de Conteúdo Premium
"""

def get_post_prompt(conta_info, tendencias):
    if conta_info['nome'] == "Click Newborn":
        return _post_click_newborn(conta_info, tendencias)
    return _post_emocional(conta_info, tendencias)

def get_reel_prompt(conta_info, tendencias):
    if conta_info['nome'] == "Click Newborn":
        return _reel_click_newborn(conta_info, tendencias)
    return _reel_emocional(conta_info, tendencias)

def get_carrossel_prompt(conta_info, tendencias):
    if conta_info['nome'] == "Click Newborn":
        return _carrossel_click_newborn(conta_info, tendencias)
    return _carrossel_emocional(conta_info, tendencias)

def get_stories_prompt(conta_info, quantidade=6, dia_numero=1):
    if conta_info['nome'] == "Click Newborn":
        return _stories_click_newborn(conta_info, quantidade)
    return _stories_emocional(conta_info, quantidade, dia_numero)

# ===========================================
# CLICK NEWBORN - PREMIUM E-COMMERCE
# ===========================================

def _post_click_newborn(conta_info, tendencias):
    persona = _escolher_persona(conta_info)
    return f"""Você é diretor criativo de marca premium especializado em copywriting aspiracional.

MISSÃO: Criar post que posicione Click Newborn como ateliê de curadoria (não loja de roupas).

MARCA:
- Essência: {conta_info['posicionamento_chave']['somos']}
- Transformação: {conta_info['posicionamento_chave']['transformacao']}
- NÃO somos: {conta_info['posicionamento_chave']['nao_somos']}

PÚBLICO-ALVO DESTE POST:
Perfil: {persona['perfil']}
Dor oculta: {persona['dor_oculta']}
Conflito: {persona['conflito']}
Desejo profundo: {persona['desejo']}
Gatilhos emocionais: {', '.join(persona['gatilhos'])}
Objeções: {', '.join(persona['objecoes'])}

TENDÊNCIAS: {tendencias}

ESTRUTURA DO POST (seguir rigorosamente):

1. GANCHO (1-2 linhas)
   - Afirmação provocativa que identifica DOR ou DESEJO oculto
   - Exemplo: "Não é uma roupinha. É a diferença entre portfolio comum e trabalho memorável."

2. IDENTIFICAÇÃO (2-3 parágrafos curtos)
   - Valide o conflito interno sem nomear diretamente
   - Use "porque quando você..." para criar intimidade
   - Mostre que entende a frustração profunda

3. ELEVAÇÃO (1 parágrafo)
   - Introduza conceito de curadoria vs compra aleatória
   - Contraste: amador vs profissional / comum vs autoral
   - Use estrutura "Entre X e Y, existe Z"

4. REPOSICIONAMENTO (lista ou bullets)
   - 3 elementos concretos de diferenciação
   - Formato: "→ Benefício tangível"
   - Foque em RESULTADO, não processo

5. CTA ELEGANTE (1-2 linhas)
   - Convite aspiracional, nunca agressivo
   - "Se você sente...", "Para quem busca...", "A curadoria está aqui."

DIRETRIZES DE ESCRITA:
✓ Tom: Sofisticado mas acessível, nunca esnobe
✓ Frases: Curtas. Impacto. Respiração visual.
✓ Evite: Adjetivos excessivos, clichês ("incrível", "maravilhoso"), emojis
✓ Use: Contraste, repetição elegante, pausas estratégicas
✓ Palavra-chave: "curadoria" (usar 1-2x), "identidade visual", "assinatura"
✓ NUNCA: Mencionar preço, promoção, desconto, "compre agora"

QUEBRA DE OBJEÇÕES (integrar sutilmente):
{_listar_objecoes(persona)}

OUTPUT:
---
TIPO: Post Premium
PERSONA: {list(conta_info['personas'].keys())[0]}
PILAR: [escolha 1 dos 5 pilares]

LEGENDA:
[220-280 palavras]

VISUAL:
[1 linha: flat lay clean OU close textura OU composição harmônica]

HASHTAGS:
[13-15 tags: mix nicho + marca + estética]

CTA:
[Convite elegante sem pressão]
---"""

def _reel_click_newborn(conta_info, tendencias):
    return f"""Você é diretor criativo de vídeo premium para marcas de luxo artesanal.

OBJETIVO: Reel que demonstre transformação visual tangível (antes→depois OU processo→resultado).

CONCEITOS PERMITIDOS:
A) ANTES x DEPOIS - Ensaio comum vs com curadoria Click
B) PROCESSO ARTESANAL - Bastidor de criação da peça
C) COMPOSIÇÃO COMPLETA - Caos de peças → harmonia curada
D) DETALHE MACRO - Close em textura/costura/tecido premium

TENDÊNCIAS: {tendencias}

ESTRUTURA OBRIGATÓRIA:

HOOK (0-3s):
- Contraste visual IMEDIATO
- Split screen OU texto provocativo
- Objetivo: Parar scroll instantaneamente
- Exemplo: "Mesma fotógrafa. Mesma luz. Figurino diferente."

DESENVOLVIMENTO (3-20s):
- Sequência lógica mostrando TRANSFORMAÇÃO
- 4-6 cortes suaves (nunca bruscos)
- Cada cena: 2-4 segundos
- Progresso visual claro: comum → elevado

RESULTADO (20-25s):
- 2-3 fotos finais impecáveis
- Identidade visual coesa óbvia
- Estética editorial/Pinterest premium

CTA (25-28s):
- Texto minimalista na tela
- Logo discreto
- NÃO usar "link na bio" explícito

PALETA VISUAL:
- Cores: Neutros (off-white, bege, terracota, verde sage)
- Iluminação: Natural, suave, nunca harsh/amarelada
- Enquadramento: Clean, ar respirável, minimalista
- Fonte: Sans-serif moderna, discreta

ÁUDIO:
- Instrumental suave trending OU lo-fi aesthetic
- EVITAR: Música com letra em português, funk, sertanejo

TRANSIÇÕES:
- Fade elegante, zoom suave, wipe vertical
- NUNCA: Cortes bruscos, efeitos chamativos, glitch

LEGENDA (50-80 palavras):
- Reforce conceito visual
- 1-2 parágrafos curtos
- Finalize com mini-CTA elegante
- Sem hashtags na legenda (usar campo separado)

OUTPUT:
---
TIPO: Reel Premium
CONCEITO: [A/B/C/D]
DURAÇÃO: 25-28s
ÁUDIO: [nome trending suave]

ROTEIRO_DETALHADO:
[Timing preciso de cada cena]

DESCRIÇÃO_VISUAL:
[Paleta, lighting, composição]

LEGENDA_CAPTION:
[50-80 palavras]

HASHTAGS:
[13-15 tags]
---"""

def _carrossel_click_newborn(conta_info, tendencias):
    return f"""Você é curador de conteúdo educacional para marcas premium.

OBJETIVO: Carrossel que EDUCA enquanto POSICIONA autoridade.

TEMAS PREMIUM (escolher 1):
1. "5 erros que fazem seu portfolio parecer amador"
2. "Como construir identidade visual autoral em newborn"
3. "Por que peças artesanais elevam seu trabalho"
4. "Paleta de cores que nunca sai de moda"
5. "Curadoria vs compra aleatória: o que muda no resultado"

ESTRUTURA (8 slides exatos):

SLIDE 1 - CAPA:
Título: [Provocativo + promessa clara]
Subtítulo: [Complemento que gera curiosidade]
Design: Minimalista, tipografia forte, fundo neutro

SLIDE 2 - CONTEXTO:
Identifica problema/dor comum
Cria identificação imediata
Não dá solução ainda (gera interesse)

SLIDES 3-6 - INSIGHTS (4 dicas):
Cada slide: 1 insight actionable
Estrutura: "ERRO: X / SOLUÇÃO: Y" OU "DICA X: conteúdo"
Seja específico, não genérico
Inclua exemplo concreto quando possível

SLIDE 7 - ELEVAÇÃO:
Reforce valor de investir em curadoria
Quebra objeção principal sutilmente
Não seja vendedor, seja consultor

SLIDE 8 - CTA:
Resumo: "O que muda quando você..."
Call elegante: "A curadoria Click está aqui."
Design: Limpo, call discreto

DESIGN:
- Paleta: Máximo 3 cores (neutros + 1 acento suave)
- Tipografia: 2 fontes (título + corpo)
- Layout: Consistente, ar respirável
- Elementos: Ícones minimalistas se usar

LEGENDA (120-150 palavras):
- Aprofunde 1 ponto do carrossel
- Adicione camada de reflexão
- Não repita exatamente o que está nos slides
- Finalize com pergunta ou mini-CTA

OUTPUT:
---
TIPO: Carrossel Educacional
TEMA: [título completo]
SLIDES: 8

[Detalhar cada slide com título + conteúdo + nota de design]

LEGENDA:
[120-150 palavras]

HASHTAGS:
[13-15 tags educacionais]

PALETA:
[3 cores específicas hex]
---"""

def _stories_click_newborn(conta_info, quantidade):
    return f"""Você é estrategista de stories para e-commerce premium.

OBJETIVO: Vender com sofisticação - gerar desejo sem agressividade.

{quantidade} STORIES - ESTRATÉGIA DIÁRIA:

MIX OBRIGATÓRIO:
- 2 Stories: Produto/lançamento (mostrar peças)
- 2 Stories: Bastidor/artesania (processo de criação)
- 1 Story: Social proof (cliente usando/depoimento)
- 1 Story: Interativo (enquete/quiz estético)
- 1 Story: Escassez elegante (últimas unidades/coleção limitada)

REGRAS DE OURO:
✓ Estética impecável SEMPRE - sem fotos amadoras
✓ CTA discreto integrado ao design
✓ Texto curto e direto (máximo 2 linhas)
✓ Coerência visual entre stories do dia
✓ Botões: "Ver acervo" não "Compre já"

FORMATO CADA STORY:

STORY [número]:
Tipo: [lançamento/bastidor/prova/interativo/escassez]
Objetivo: [vender/engajar/educar/criar desejo]

VISUAL:
[Descrição fotográfica precisa - sempre editorial/clean]

TEXTO NA TELA:
[Máximo 2 linhas - direto e elegante]

ELEMENTO INTERATIVO:
[Sticker/botão/link se aplicável]

CTA:
[Ação desejada - sempre suave]

VARIAR FORMATOS:
- Flat lay produto isolado
- Close macro em textura
- Hands in frame ajeitando peça
- Resultado final em ensaio
- Behind-the-scenes ateliê
- Screenshot depoimento (design clean)

OUTPUT:
---
SEQUÊNCIA: {quantidade} Stories Coesos

[Detalhar cada story numerado]

COERÊNCIA VISUAL:
[Paleta do dia, filtro/preset se usar]
---"""

# ===========================================
# ESTÚDIO MATERNUM - EMOCIONAL
# ===========================================

def _post_emocional(conta_info, tendencias):
    persona = _escolher_persona(conta_info)
    return f"""Você é copywriter emocional especializado em maternidade e memória afetiva.

MISSÃO: Post que VALIDA emoção oculta + REPOSICIONA fotografia como legado (não produto).

ESTÚDIO:
- Essência: {conta_info['posicionamento_chave']['somos']}
- Transformação: {conta_info['posicionamento_chave']['transformacao']}

PERSONA DESTE POST:
{persona['perfil']}
Dor não verbalizada: {persona['dor_oculta']}
Conflito interno: {persona['conflito']}
Desejo profundo: {persona['desejo']}
Gatilhos: {', '.join(persona['gatilhos'])}
Medos: {', '.join(persona['medos'])}

TENDÊNCIAS: {tendencias}

ESTRUTURA EMOCIONAL (seguir):

1. ABERTURA (1-3 linhas)
   - Nomeie sentimento que ela sente mas não verbaliza
   - Segunda pessoa: "Você..."
   - Exemplo: "Você se olha no espelho e quase não se reconhece."

2. VALIDAÇÃO (2-3 parágrafos)
   - Descreva experiência interna dela
   - Mostre que entende SEM julgar
   - "Porque..." para explicar contexto emocional
   - Contraste: expectativa social vs realidade sentida

3. RESSIGNIFICAÇÃO (1-2 parágrafos)
   - "E está tudo bem sentir isso."
   - Reframe: transformação não é perda
   - Poesia acessível, não piegas

4. CONVITE (1 parágrafo)
   - Apresente fotografia como validação/memória
   - NÃO como solução do problema emocional
   - "É sobre..." (repetição estrutural)

5. CTA SUAVE (1-2 linhas)
   - Convite acolhedor, nunca vendedor
   - "Se você sente...", "Este momento merece..."

TOM E ESTILO:
✓ Intimista, verdadeiro, acolhedor
✓ Frases variadas: longas reflexivas + curtas impactantes
✓ Pausas para respiração emocional
✓ Evite: Lugares comuns ("mágico", "incrível"), infantilização
✓ Use: Contraste de emoções, verdade crua com delicadeza
✓ Palavra-chave: "memória", "legado" (1-2x cada)

VALIDAÇÕES ESSENCIAIS:
- Nomear sentimento taboo sem julgamento
- Reconhecer ambivalência (amor E cansaço, alegria E perda)
- Normalizar experiência "negativa"
- Não romantizar maternidade

OUTPUT:
---
TIPO: Post Emocional
PERSONA: {list(conta_info['personas'].keys())[0]}
PILAR: [escolha 1 dos 5]

LEGENDA:
[200-260 palavras]

VISUAL:
[1 linha: intimista, autêntico, humano - nunca pose forçada]

HASHTAGS:
[12-15 tags: emocional + local + serviço]

CTA:
[Acolhedor e suave]
---"""

def _reel_emocional(conta_info, tendencias):
    persona = _escolher_persona(conta_info)
    return f"""Você é roteirista de conteúdo emocional viral para maternidade.

OBJETIVO: Reel que IDENTIFICA dor silenciosa → VALIDA → OFERECE acolhimento.

PERSONA:
{persona['perfil']}
Dor: {persona['dor_oculta']}
Conflito: {persona['conflito']}
Gatilhos: {', '.join(persona['gatilhos'])}

TENDÊNCIAS: {tendencias}

ESTRUTURA NARRATIVA:

HOOK (0-3s):
- Frase que nomeia sentimento TABOO
- Texto na tela + expressão facial autêntica
- Objetivo: "Ela está falando de MIM"
- Exemplos: "Ninguém te preparou pra essa solidão." / "Você não se reconhece mais."

DESENVOLVIMENTO (3-20s):
- 5-7 frases curtas (1-2 segundos cada)
- Progressão: dor → validação → esperança
- Cada frase: novo corte visual
- Contraste: expectativa social vs realidade sentida
- Ritmo: pausado, respira emoção

VALIDAÇÃO (meio):
- "E está tudo bem..." (ponto de virada)
- Normaliza experiência "negativa"
- Não romantiza, não minimiza

RESSIGNIFICAÇÃO (15-20s):
- Fotografia como VALIDAÇÃO (não solução)
- "Então você guarda essa memória..."
- Visual: resultado do ensaio (beleza autêntica)

CTA (20-25s):
- Frase final de acolhimento
- "Você vai olhar pra trás e lembrar: estava fazendo o melhor."
- Texto: "Preserve essa memória."

VISUAL:
- Estética: Intimista, luz natural, imperfeito-autêntico
- Expressões: Genuínas, lágrimas ok, sorrisos verdadeiros
- Enquadramento: Closes emocionais, detalhes (mãos, olhos)
- Paleta: Tons quentes, naturais, nunca frio ou clínico
- Contraste: Caos da maternidade → Beleza da foto profissional

ÁUDIO:
- Instrumental emocional (piano, strings, ambient)
- Exemplos: "The Night We Met", "Experience" (Ludovico Einaudi)
- EVITAR: Upbeat, alegre demais, desconexo da emoção

LEGENDA (70-120 palavras):
- Aprofunda emoção do reel
- Não repete textualmente
- Adiciona camada de verdade
- Finalize: "Fotografia que acolhe." ou similar

OUTPUT:
---
TIPO: Reel Emocional
PERSONA: {list(conta_info['personas'].keys())[0]}
DURAÇÃO: 23-27s
ÁUDIO: [nome música emocional]

ROTEIRO:
[Timing + frase + descrição visual de cada corte]

VISUAL:
[Paleta, lighting, estética geral]

LEGENDA:
[70-120 palavras]

HASHTAGS:
[12-15 tags emocionais]
---"""

def _carrossel_emocional(conta_info, tendencias):
    persona = _escolher_persona(conta_info)
    return f"""Você é criador de conteúdo educacional-emocional para maternidade.

OBJETIVO: Carrossel que EDUCA sobre valor emocional + QUEBRA objeção de preço.

PERSONA:
{persona['conflito']}
Objeção: "É só uma foto, por que tão caro?"
Desejo real: {persona['desejo']}

TEMAS (escolher 1):
1. "Por que você não precisa de 'mais fotos' - você precisa de memória construída"
2. "O que vai restar quando seu celular quebrar? Legado vs arquivo digital"
3. "Como explicar pra sua filha porque você não tem fotos dessa fase"
4. "Investimento que atravessa gerações vs gasto que desaparece"
5. "Por que você adia preservar o que mais importa"

ESTRUTURA (7-8 slides):

SLIDE 1 - CAPA:
Título: [Pergunta provocativa que toca desejo/medo]
Design: Foto autêntica de fundo, texto sobreposto

SLIDE 2 - IDENTIFICAÇÃO:
Pensamento comum que ela tem
"Você pensa: 'Vou fazer quando tiver tempo/dinheiro/bebê maior...'"
Cria conexão imediata

SLIDE 3 - REALIDADE:
Verdade dura mas necessária
"Mas a verdade é: esse momento não volta."
Evoque urgência emocional (não comercial)

SLIDES 4-6 - INSIGHTS:
3 reframes sobre valor:
- Memória vs arquivo digital
- Patrimônio emocional vs consumo
- Legado vs foto casual
Cada slide: 1 conceito bem desenvolvido

SLIDE 7 - QUEBRA DE OBJEÇÃO:
Sem mencionar preço diretamente
"Não é sobre ter fotos bonitas. É sobre..."
Reposiciona investimento

SLIDE 8 - CTA:
"Este momento merece ser guardado."
Convite acolhedor para conversar

DESIGN:
- Fotos reais do estúdio (nunca stock)
- Tipografia: legível, emocional mas profissional
- Cores: Quentes, acolhedoras
- Espaço: Ar para respirar emoção

LEGENDA (100-140 palavras):
- História real (pode ser compilação anônima)
- OU reflexão aprofundada de 1 slide
- Valide objeção antes de reframe
- Não seja defensivo sobre valor

OUTPUT:
---
TIPO: Carrossel Educacional-Emocional
TEMA: [título completo]
SLIDES: 7-8

[Detalhar cada slide]

LEGENDA:
[100-140 palavras]

HASHTAGS:
[12-15 tags]
---"""

def _stories_emocional(conta_info, quantidade, dia_numero=1):
    _temas_validacao = [
        "Aceitação do corpo que mudou — você é mais do que sua aparência agora.",
        "Ambivalência emocional — amar profundamente e ao mesmo tempo se sentir perdida é completamente real.",
        "Identidade além da maternidade — quem você era antes ainda existe dentro de você.",
        "Presença no caos — estar aqui, mesmo imperfeita, já é o suficiente.",
        "Força invisível — o quanto você suporta sem pedir reconhecimento de ninguém.",
        "Memória que escorrega — tudo que parece longo é, na verdade, uma fase passageira.",
        "Celebração silenciosa — olhar para trás e ver o quanto você cresceu sem perceber.",
    ]
    _interativos = [
        ("Enquete", "Qual fase mais te surpreendeu? (Gravidez / Newborn / Primeira infância)"),
        ("Caixinha de perguntas", "O que ninguém te contou sobre ser mãe?"),
        ("Slider de reação", "O quanto você consegue estar presente hoje? (de 😴 a 🌟)"),
        ("Quiz", "Qual tipo de mãe você é? (A que planeja tudo / A que improvisa / As duas)"),
        ("Enquete", "O que você mais sente falta de antes de ser mãe?"),
        ("Caixinha de perguntas", "Se você pudesse voltar, qual momento da maternidade guardaria primeiro?"),
        ("Votação", "Próxima sessão — Gestante ou Newborn? Você decide!"),
    ]
    _ctas_chamada = [
        "Tenho 2 datas em abril abertas. Se você sente que esse momento merece ser guardado, vamos conversar? 💌",
        "Ainda tenho espaço na agenda de março. Sem compromisso — só uma conversa sobre o que você quer preservar. 🤍",
        "Tenho 1 data especial disponível este mês. É para você que está esperando o momento certo chegar. Vamos falar? ✨",
        "Abri algumas datas para maio. Se a maternidade está passando rápido demais, talvez seja a hora. Conversa? 💌",
        "Sabe aquela sessão que você fica adiando? Tenho data em abril. Vamos planejar juntas? 🤍",
        "Tenho 2 sessões disponíveis em março e abril. Para quem quer guardar mais do que uma foto — uma memória. 💌",
        "Última semana com datas livres neste mês. Para a mãe que merece ser lembrada exatamente como é hoje. 🌿",
    ]
    _bastidores = [
        "Flores frescas sendo arranjadas com luz natural entrando pelo estúdio — detalhe de bastidor real",
        "Xícara de café ou chá sendo preparada num cantinho aconchegante antes da cliente chegar",
        "Mesa de boas-vindas sendo organizada com capricho — pequenos detalhes que fazem a diferença",
        "Equipamentos fotográficos dispostos com cuidado em ambiente silencioso e calmo",
        "Cantinho especial com almofadas e manta sendo preparado para o conforto da cliente",
        "Playlist e aromatizador sendo configurados — clima pensado antes mesmo de a porta abrir",
        "Último ajuste no espaço antes da sessão — detalhe que mostra o quanto cada cliente importa",
    ]
    _depoimentos = [
        "gestante — foco em como ela se sentiu vista e bonita pela primeira vez na gravidez",
        "puérpera — foco no acolhimento e no quanto a sessão a fez sentir que estava fazendo o suficiente",
        "mãe de bebê 6 meses a 1 ano — foco na memória preservada antes do tempo escapar",
        "família completa — foco na conexão e no momento de pausa que a sessão proporcionou",
        "mãe que adiou e quase perdeu a fase — foco no alívio de ter feito mesmo com medo",
        "mãe que recebeu a sessão de presente — foco na surpresa e na emoção de ser presenteada",
        "mãe de segundo filho — foco em registrar cada filho com o mesmo amor e presença",
    ]

    idx = (dia_numero - 1) % 7
    tema_validacao = _temas_validacao[idx]
    tipo_interativo, pergunta_interativo = _interativos[idx]
    cta_chamada = _ctas_chamada[idx]
    bastidor_cenario = _bastidores[idx]
    depoimento_foco = _depoimentos[idx]

    personas = list(conta_info["personas"].values())
    persona = personas[idx % len(personas)]
    persona_resumo = f"{persona['perfil']} | Dor: {persona['dor_oculta']}"

    return f"""Você é estrategista de stories para serviços emocionais.

OBJETIVO: Humanizar marca + criar conexão + agenda suave.

PERSONA DO DIA (DIA {dia_numero}):
{persona_resumo}
Oriente o tom e os textos de validação e bastidor para ressoar com essa persona.

{quantidade} STORIES - MIX EMOCIONAL:

TIPOS:
- 2 Stories: Bastidor acolhedor (preparação ambiente, cuidado com cliente)
- 1 Story: Depoimento real (texto cliente + foto resultado)
- 1 Story: Validação emocional (frase reflexiva sobre maternidade)
- 1 Story: Interativo (enquete ou pergunta)
- 1 Story: Chamada suave agenda (disponibilidade próximos meses)

ATENÇÃO — DIRETRIZES EXCLUSIVAS DESTE DIA:
- Cenário dos Bastidores: {bastidor_cenario}
- Foco do Depoimento: {depoimento_foco}
- Tema da Validação: {tema_validacao}
- Formato do Interativo: {tipo_interativo} — "{pergunta_interativo}"
- CTA da Chamada (adapte o texto, não copie literalmente): {cta_chamada}

REGRAS:
✓ Autenticidade > perfeição estética
✓ Humanize: mostre processo, não só resultado
✓ Textos: acolhedores, nunca vendedores
✓ CTA: "Vamos conversar?" não "Agende já"
✓ Fotos: naturais, não posadas
✓ PROIBIDO copiar as diretrizes acima — use-as como inspiração de tema e tom
✓ Crie frases 100% originais; nunca transcreva os textos de referência

FORMATO:

STORY [número]:
Tipo: [bastidor/depoimento/validação/interativo/chamada]
Objetivo: [humanizar/provar/conectar/engajar/converter]

VISUAL:
[Descrição - sempre autêntico, nunca frio/comercial]

TEXTO:
[Máximo 3 linhas - acolhedor e verdadeiro]

ELEMENTO:
[Caixinha pergunta/enquete/botão se aplicável]

TOM:
[Como se estivesse conversando com amiga]

OUTPUT:
---
SEQUÊNCIA: {quantidade} Stories Autênticos

[Detalhar cada story]
---"""

# ===========================================
# FUNÇÕES AUXILIARES
# ===========================================

def _format_personas(personas):
    texto = ""
    for tipo, dados in personas.items():
        texto += f"\n{tipo.upper()}:\n"
        texto += f"  Dor: {dados['dor_oculta']}\n"
        texto += f"  Conflito: {dados['conflito']}\n"
        texto += f"  Desejo: {dados['desejo']}\n"
    return texto

def _escolher_persona(conta_info):
    """Retorna primeira persona do dict - pode ser aleatorizado depois"""
    return list(conta_info['personas'].values())[0]

def _listar_objecoes(persona):
    if 'objecoes' in persona:
        return "\n".join([f"- {obj}" for obj in persona['objecoes']])
    return "N/A"