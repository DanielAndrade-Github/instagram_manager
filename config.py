"""
Configurações das contas de Instagram - Sistema de Geração de Conteúdo
"""

CONTAS = {
    "click_newborn": {
        "nome": "Click Newborn",
        "nicho": "Roupas e acessórios artesanais premium para fotografia newborn e primeira infância",
        "publico": "Fotógrafas newborn e mães (classe A/B) que valorizam estética sofisticada, exclusividade e praticidade",
        "tom": "sofisticado, afetivo e aspiracional (linguagem de curadoria, arte e legado)",
        
        "volume": {
            "posts": 3,
            "reels": 2,
            "carrosseis": 2,
            "stories": 42
        },
        
        "pilares": [
            "Curadoria como diferencial - peça como composição estética pensada",
            "Elevação estética do trabalho da fotógrafa - diferenciação profissional",
            "Bastidores artesanais e valor do feito à mão - exclusividade tangível",
            "Tempo como escassez - coleções limitadas e drops sazonais",
            "Construção de identidade visual autoral - assinatura estética reconhecível"
        ],
        
        "personas": {
            "fotografa_diferenciacao": {
                "perfil": "Fotógrafa newborn 2-5 anos mercado, portfólio inconsistente, insegura sobre valor",
                "dor_oculta": "Medo de ser vista como mediana. Ansiedade ao comparar portfolio com concorrentes de sucesso",
                "conflito": "Sabe fazer boas fotos mas resultado final não transmite sofisticação - falta assinatura visual",
                "desejo": "Ter acervo que imediatamente comunique profissionalismo premium, sem precisar explicar valor",
                "gatilhos": ["diferenciação", "identidade visual", "portfólio autoral", "reconhecimento", "sofisticação"],
                "objecoes": ["custo", "não saber combinar peças", "medo de investir e não usar"]
            },
            "fotografa_sobrecarga": {
                "perfil": "Fotógrafa estabelecida, agenda cheia, zero tempo para curadoria de figurino",
                "dor_oculta": "Exaustão de decisões - cada sessão exige escolhas estéticas que somam carga mental",
                "conflito": "Quer ensaios únicos mas não tem energia/tempo para procurar peças e montar composições",
                "desejo": "Solução pronta de alto padrão - pegar e usar sem pensar, sabendo que está impecável",
                "gatilhos": ["praticidade premium", "tempo economizado", "decisões prontas", "confiança"],
                "objecoes": ["preferir controle total", "já ter fornecedores"]
            },
            "mae_perfeicao": {
                "perfil": "Mãe de primeira viagem, classe A/B, consome Pinterest/Instagram, quer ensaio especial",
                "dor_oculta": "Ansiedade de que fotos não façam jus à importância do momento - perfeccionismo maternal",
                "conflito": "Vê ensaios incríveis online, quer esse nível mas não sabe como garantir/escolher",
                "desejo": "Certeza de que bebê será fotografado com cuidado estético digno da história familiar",
                "gatilhos": ["delicadeza", "exclusividade", "beleza atemporal", "momento único", "perfeição"],
                "objecoes": ["preço", "medo de peça não servir no bebê"]
            },
            "medo_comum": {
                "perfil": "Persona transversal - fotógrafa E mãe",
                "dor_oculta": "Terror de investir tempo/dinheiro e resultado ser 'comum' - saturação visual",
                "conflito": "Mercado saturado de newborn genérico - como garantir diferenciação real?",
                "desejo": "Estética tão marcante que seja reconhecida - 'assinatura' visual imediata",
                "gatilhos": ["exclusividade real", "autoral", "atemporal", "reconhecimento instantâneo"],
                "objecoes": ["descrença na diferença real", "achar que é só marketing"]
            }
        },
        
        "keywords_pesquisa": [
            "newborn styling trends 2025",
            "fotografia newborn curadoria",
            "roupas artesanais newborn premium",
            "identidade visual fotografia infantil",
            "diferenciação portfolio newborn",
            "paleta cores newborn atemporal"
        ],
        
        "posicionamento_chave": {
            "nao_somos": "Loja de roupas de bebê / Fast fashion infantil / Revenda genérica",
            "somos": "Ateliê de produção própria de roupas para fotografia de bebês / curadoria especial de roupas para bebês usarem nas sessões de fotos / curadoria estética para fotografia de bebês direcionada aos fotógrafos materno-infantil / Fornecedor de diferenciação profissional",
            "transformacao": "De 'mais uma fotografia newborn' para 'aquele ensaio que todos perguntam onde foi feito'",
            "preco_ancora": "Não é gasto com roupa, é investimento em identidade profissional, estéteica e harmonização visual / memória atemporal"
        }
    },
    
    "estudio_maternum": {
        "nome": "Estúdio Maternum",
        "nicho": "Fotografia de famílias — gestante, newborn, acompanhamento de bebês e ensaios temáticos (natal, páscoa, dia dos pais, dia das mães)",
        "publico": "Mulheres e famílias classe B/C, em fase de maternidade (gestação até primeira infância)",
        "tom": "acolhedor, emocional, sofisticado (linguagem de legado e memória), linguagem leve como uma conversa entre a fotógrafa e a mãe, entre a fotógrafa e a gestante",
        
        "volume": {
            "posts": 1,
            "reels": 1,
            "carrosseis": 1,
            "stories": 36
        },
        
        "pilares": [
            "Validação emocional - nomear sentimentos não verbalizados da maternidade",
            "Resgate de identidade e beleza real - mulher além da mãe, sem negar maternidade",
            "Memória como legado - fotografia como patrimônio emocional intergeracional",
            "Tradição e pertencimento familiar - ritual de preservação da história",
            "Quebra do pensamento imediato - elevar de custo para investimento emocional"
        ],
        
        "personas": {
            "gestante": {
                "perfil": "21-40 anos, primeira, segunda ou terceira gestação, sensação de perda de identidade",
                "dor_oculta": "Luto silencioso pela mulher pré-maternidade - ninguém valida essa perda",
                "conflito": "Ama a gestação mas não se reconhece no espelho - corpo e identidade em transformação",
                "dor":"Achar que não vai dar conta de tudo depois do nascimento do filho",
                "dor_profunda": "a dor da solidão do puerpério. A dor silenciosa do luto do primeiro filho que se torna irmão mais velho",
                "desejo": "Recuperar senso de feminilidade e beleza DENTRO da maternidade, não apesar dela, e afirmar que o amor não muda depois da chegada do segundo filho; ele ganha um novo espaço de acolhimento para o irmão mais novo e amadurecimento para o mais velho",
                "gatilhos": ["reconhecimento", "beleza real", "feminilidade", "identidade", "transformação"],
                "medos": ["não voltar a se sentir bonita", "perder-se completamente na maternidade"]
            },
            "newborn": {
                "perfil": "Puérpera 0-3 meses pós-parto, exausta, insegura, sobrecarga emocional",
                "dor_oculta": "Sentimento de inadequação constante - 'não estou sendo boa o suficiente', além da dor silenciosa e do cansaço do puerpério",
                "conflito": "Amor imenso coexiste com exaustão e medo de falhar - ambivalência emocional",
                "desejo": "Validação de que está fazendo o melhor - acolhimento sem julgamento",
                "gatilhos": ["acolhimento", "segurança", "validação", "cuidado", "refúgio"],
                "medos": ["não criar vínculo adequado", "não conseguir dar conta", "ser julgada"]
            },
            "acompanhamento": {
                "perfil": "Mãe de criança 6 meses-5 anos, culpa e sensação do tempo passar rápido",
                "dor_oculta": "Culpa silenciosa - sente que está perdendo momentos importantes na correria",
                "conflito": "Mil fotos no celular mas nenhuma memória construída - caos digital vs legado",
                "desejo": "Parar o tempo - garantir que memórias não se percam no esquecimento",
                "gatilhos": ["tempo", "memória", "infância preservada", "história familiar", "legado"],
                "medos": ["esquecer detalhes preciosos", "criança crescer rápido demais", "arrependimento futuro"]
            },
            "tematico": {
                "perfil": "Família completa, busca momento de conexão e tradição",
                "dor_oculta": "Medo da desintegração familiar - rotina separa, conexão diminui",
                "conflito": "Desejo de união forte mas realidade de correria e distanciamento",
                "desejo": "Afirmar pertencimento, criar tradições visuais, reforçar laços",
                "gatilhos": ["união familiar", "tradição", "pertencimento", "raízes", "história compartilhada"],
                "medos": ["perder conexão com família", "não criar memórias significativas juntos"]
            }
        },
        
        "keywords_pesquisa": [
            "fotografia maternidade emocional",
            "ensaio gestante identidade",
            "newborn acolhimento puerpério",
            "memória afetiva família",
            "legado fotográfico familiar",
            "fotografia resgate feminilidade gestante",
            "fotografia de gestante",
            "fotografia de recém-nascido",
            "fotografia lif style newborn"
        ],
        
        "posicionamento_chave": {
            "nao_somos": "Estúdio de fotos genérico / Serviço apenas estético / Produto final sem alma",
            "somos": "Espaço de resgate emocional / Guardião de memórias afetivas / Validador de maternidade real. Somos lugar de descanso durante a sessão newborn com ambiente calmo e acolhedor",
            "transformacao": "De 'mais um ensaio' para 'momento que validou minha jornada maternal'",
            "preco_ancora": "Não é custo de foto, é investimento em patrimônio emocional que atravessa gerações"
        }
    }
}

CONFIGURACOES = {
    "dia_geracao": "domingo",
    "horario_geracao": "08:00",
    "pasta_output": "conteudo_gerado",
    "buscar_tendencias": True,
    "max_hashtags": 15
}
