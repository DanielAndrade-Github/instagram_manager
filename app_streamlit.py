"""
App Streamlit para gerar plano semanal e exportar PDF.
"""

from __future__ import annotations

import hmac
import os
from datetime import date, datetime
import re
import unicodedata

import streamlit as st
from dotenv import load_dotenv

from config import CONTAS, CONFIGURACOES
from generator import InstagramContentGenerator
from pdf_exporter import exportar_conteudo_especifico_pdf, exportar_plano_pdf
from weekly_planner import gerar_plano_semanal, salvar_plano_em_markdown


def obter_api_key() -> str:
    key = os.getenv("GROQ_API_KEY", "")
    if key:
        return key
    try:
        return st.secrets.get("GROQ_API_KEY", "")
    except Exception:
        return ""


def obter_credenciais_login() -> tuple[str, str]:
    user = os.getenv("APP_LOGIN_USER", "")
    password = os.getenv("APP_LOGIN_PASSWORD", "")

    if not user or not password:
        try:
            user = user or st.secrets.get("APP_LOGIN_USER", "")
            password = password or st.secrets.get("APP_LOGIN_PASSWORD", "")
        except Exception:
            pass

    # Fallback solicitado para uso imediato.
    user = user or "camila_andrade"
    password = password or "danielmeuamor"
    return user, password


def exigir_login():
    if st.session_state.get("auth_ok"):
        return

    usuario_correto, senha_correta = obter_credenciais_login()
    st.title("Login")
    st.caption("Acesso restrito")

    with st.form("form_login", clear_on_submit=False):
        usuario = st.text_input("Usuario")
        senha = st.text_input("Senha", type="password")
        entrar = st.form_submit_button("Entrar", use_container_width=True, type="primary")

    if entrar:
        ok_user = hmac.compare_digest(usuario, usuario_correto)
        ok_senha = hmac.compare_digest(senha, senha_correta)
        if ok_user and ok_senha:
            st.session_state["auth_ok"] = True
            st.rerun()
        else:
            st.error("Usuario ou senha invalidos.")

    st.stop()


def aplicar_tema_pastel():
    st.markdown(
        """
        <style>
            :root {
                --bg: #f6f0e6;
                --card: #fffaf2;
                --border: #d8c7ad;
                --text: #3f3427;
                --accent: #b89974;
                --accent-hover: #a5845f;
            }

            .stApp {
                background: linear-gradient(180deg, #f6f0e6 0%, #f2e8d8 100%);
                color: var(--text);
            }

            .block-container {
                max-width: 920px;
                padding-top: 1.5rem;
                padding-bottom: 2rem;
            }

            h1, h2, h3, h4, p, label, div {
                color: var(--text);
            }

            [data-testid="stForm"] {
                background: var(--card);
                border: 1px solid var(--border);
                border-radius: 14px;
                padding: 1rem 1rem 0.5rem 1rem;
            }

            [data-testid="stDownloadButton"] button,
            [data-testid="stFormSubmitButton"] button {
                background-color: var(--accent) !important;
                color: #fff !important;
                border: 1px solid var(--accent) !important;
                border-radius: 10px !important;
            }

            [data-testid="stDownloadButton"] button:hover,
            [data-testid="stFormSubmitButton"] button:hover {
                background-color: var(--accent-hover) !important;
                border-color: var(--accent-hover) !important;
            }

            [data-baseweb="select"] > div,
            [data-baseweb="input"] > div {
                background: #fffefb !important;
                border-color: var(--border) !important;
            }

            [data-testid="stAlert"] {
                border-radius: 10px;
                border: 1px solid var(--border);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _resolver_contas(escolha_cliente: str, nome_para_id: dict, contas_disponiveis: list[str]) -> list[str]:
    if escolha_cliente == "Todos":
        return contas_disponiveis
    return [nome_para_id[escolha_cliente]]


def _slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^a-zA-Z0-9]+", "_", value.lower()).strip("_")
    return value or "cliente"


def _extrair_termos_tema(prompt_usuario: str, limite: int = 8) -> list[str]:
    stopwords = {
        "para", "com", "sem", "sobre", "entre", "depois", "antes", "quando",
        "como", "esse", "essa", "isso", "aquele", "aquela", "dessa", "desse",
        "uma", "umas", "uns", "das", "dos", "que", "ser", "sao", "nos", "nas",
        "por", "mais", "menos", "muito", "muita", "pelo", "pela", "tema",
        "conteudo", "publicacao", "pedido", "prompt",
    }
    tokens = re.findall(r"[A-Za-zÀ-ÿ0-9]+", (prompt_usuario or "").lower())
    termos = []
    for token in tokens:
        if len(token) < 4 or token in stopwords:
            continue
        if token not in termos:
            termos.append(token)
        if len(termos) >= limite:
            break
    return termos


def _validar_item_tema(conteudo: str, prompt_usuario: str) -> dict:
    termos = _extrair_termos_tema(prompt_usuario)
    conteudo_lower = (conteudo or "").lower()
    hits = [termo for termo in termos if termo in conteudo_lower]
    valido = len(hits) >= 1 if termos else prompt_usuario.lower()[:20] in conteudo_lower
    return {
        "valido": valido,
        "termos_base": termos,
        "termos_encontrados": hits,
    }


def _validar_resultado_especifico(resultado: dict) -> dict:
    itens = []
    aprovados = True
    for item in resultado["itens"]:
        check = _validar_item_tema(item.get("conteudo", ""), resultado.get("prompt_usuario", ""))
        if not check["valido"]:
            aprovados = False
        itens.append(
            {
                "conta_nome": item["conta_nome"],
                "valido": check["valido"],
                "termos_encontrados": check["termos_encontrados"],
            }
        )
    return {"aprovado": aprovados, "itens": itens}


def _salvar_markdown_conteudo_especifico(resultado: dict, pasta_output: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pasta_base = os.path.join(pasta_output, f"conteudo_especifico_{timestamp}")
    os.makedirs(pasta_base, exist_ok=True)

    for item in resultado["itens"]:
        nome_arquivo = _slugify(item["conta_nome"])
        caminho = os.path.join(pasta_base, f"{nome_arquivo}_{resultado['tipo']}.md")
        with open(caminho, "w", encoding="utf-8") as f:
            f.write("# Conteudo Especifico\n\n")
            f.write(f"Cliente: {item['conta_nome']}\n")
            f.write(f"Tipo: {resultado['tipo']}\n")
            f.write(f"Tema central: {resultado['prompt_usuario']}\n")
            if item.get("stories_quantidade"):
                dias = item.get("stories_dias", 1)
                total = dias * item["stories_quantidade"]
                f.write(
                    f"Stories solicitados: {item['stories_quantidade']} por dia, "
                    f"durante {dias} dia(s) (total {total})\n"
                )
            f.write("\n---\n\n")
            f.write(item["conteudo"])

    return pasta_base


def main():
    load_dotenv()
    st.set_page_config(page_title="Planejador Instagram", layout="centered")
    aplicar_tema_pastel()
    exigir_login()
    st.title("Planejador e Gerador de Conteudo")
    st.caption("Gere plano semanal ou publicacao especifica com PDF dedicado.")

    with st.sidebar:
        if st.button("Sair", use_container_width=True):
            st.session_state["auth_ok"] = False
            st.rerun()

    api_key = obter_api_key()
    contas_disponiveis = list(CONTAS.keys())
    nome_para_id = {CONTAS[cid]["nome"]: cid for cid in contas_disponiveis}
    opcoes_cliente = list(nome_para_id.keys()) + ["Todos"]
    aba_semanal, aba_especifico = st.tabs(["Plano Semanal", "Conteudo Especifico"])

    with aba_semanal:
        with st.form("form_planejamento", clear_on_submit=False):
            escolha_cliente = st.selectbox(
                "Cliente",
                options=opcoes_cliente,
                index=len(opcoes_cliente) - 1,
                key="cliente_semanal",
            )
            data_inicio = st.date_input(
                "Data de inicio",
                value=date.today(),
                format="YYYY-MM-DD",
                key="data_inicio_semanal",
            )
            dias = st.number_input(
                "Para quantos dias? (1 a 7)",
                min_value=1,
                max_value=7,
                value=7,
                step=1,
                key="dias_semanal",
            )
            gerar_semanal = st.form_submit_button(
                "Gerar Plano + PDF",
                type="primary",
                use_container_width=True,
            )

        if gerar_semanal:
            contas_selecionadas = _resolver_contas(escolha_cliente, nome_para_id, contas_disponiveis)

            if not api_key:
                st.error("GROQ_API_KEY nao encontrada no .env.")
                st.code("GROQ_API_KEY=gsk_...", language="bash")
                return
            if not contas_selecionadas:
                st.error("Selecione pelo menos um cliente.")
                return

            generator = InstagramContentGenerator(api_key)
            passos_totais = len(contas_selecionadas) * 4
            progresso_estado = {"done": 0}
            barra = st.progress(0.0, text="Iniciando...")
            status_box = st.empty()

            def status_cb(msg: str):
                progresso_estado["done"] += 1
                fracao = min(progresso_estado["done"] / max(passos_totais, 1), 1.0)
                barra.progress(fracao, text=msg)
                status_box.info(msg)

            with st.spinner("Gerando conteudo semanal..."):
                plano = gerar_plano_semanal(
                    generator=generator,
                    conta_ids=contas_selecionadas,
                    data_inicio=data_inicio,
                    dias=dias,
                    status_cb=status_cb,
                )
                pasta_semana = salvar_plano_em_markdown(plano, CONFIGURACOES["pasta_output"])
                caminho_pdf = os.path.join(pasta_semana, "plano_semanal.pdf")
                try:
                    exportar_plano_pdf(plano, caminho_pdf)
                except ModuleNotFoundError as exc:
                    st.error(str(exc))
                    st.info("Instale dependencias com: pip install -r requirements.txt")
                    return

            barra.progress(1.0, text="Concluido")
            status_box.success(f"Arquivos gerados em: {pasta_semana}")
            st.success("Plano semanal gerado com sucesso.")

            st.write("### Resumo")
            for conta in plano["contas"]:
                total_posts = sum(len(d["posts"]) for d in conta["dias"])
                total_reels = sum(len(d["reels"]) for d in conta["dias"])
                total_carrosseis = sum(len(d["carrosseis"]) for d in conta["dias"])
                total_stories = sum(d["stories_quantidade"] for d in conta["dias"])
                st.write(
                    f"- {conta['nome']}: posts={total_posts}, reels={total_reels}, "
                    f"carrosseis={total_carrosseis}, stories={total_stories}"
                )

            with open(caminho_pdf, "rb") as f:
                st.download_button(
                    label="Baixar PDF Semanal",
                    data=f.read(),
                    file_name=os.path.basename(caminho_pdf),
                    mime="application/pdf",
                    use_container_width=True,
                    key="download_pdf_semanal",
                )

    with aba_especifico:
        st.write("Geracao de uma publicacao focada em tema definido por você Camila.")
        tipos = {
            "Post": "post",
            "Reel": "reel",
            "Carrossel": "carrossel",
            "Stories": "stories",
        }
        with st.form("form_especifico", clear_on_submit=False):
            escolha_cliente_esp = st.selectbox(
                "Cliente",
                options=opcoes_cliente,
                index=0,
                key="cliente_especifico",
            )
            tipo_label = st.selectbox(
                "Tipo de conteudo",
                options=list(tipos.keys()),
                key="tipo_especifico",
            )
            prompt_usuario = st.text_area(
                "Tema central da publicacao (faça seu prompt completo aqui Camila)",
                placeholder="Ex.: Ensaios de irmaos com recem-nascido sem perder protagonismo do primogenito.",
                height=110,
                key="prompt_especifico",
            )
            stories_quantidade = 6
            stories_dias = 1
            if tipos[tipo_label] == "stories":
                stories_dias = st.number_input(
                    "Para quantos dias de stories? (1 a 7)",
                    min_value=1,
                    max_value=7,
                    value=1,
                    step=1,
                    key="stories_dias_especifico",
                )
                stories_quantidade = st.number_input(
                    "Quantos stories por dia? (1 a 12)",
                    min_value=1,
                    max_value=12,
                    value=6,
                    step=1,
                    key="stories_qtd_especifico",
                )
            gerar_especifico = st.form_submit_button(
                "Gerar Conteudo Especifico + PDF",
                type="primary",
                use_container_width=True,
            )

        if "resultado_especifico" not in st.session_state:
            st.session_state["resultado_especifico"] = None
            st.session_state["pasta_especifico"] = None
            st.session_state["caminho_pdf_especifico"] = None
            st.session_state["validacao_especifico"] = None
            st.session_state["download_liberado_especifico"] = False

        if gerar_especifico:
            contas_especifico = _resolver_contas(escolha_cliente_esp, nome_para_id, contas_disponiveis)
            tipo = tipos[tipo_label]

            if not api_key:
                st.error("GROQ_API_KEY nao encontrada no .env.")
                st.code("GROQ_API_KEY=gsk_...", language="bash")
                return
            if not prompt_usuario.strip():
                st.error("Informe o tema central para orientar a geracao.")
                return

            generator = InstagramContentGenerator(api_key)
            barra_esp = st.progress(0.0, text="Iniciando...")
            itens = []
            total = len(contas_especifico)

            with st.spinner("Gerando conteudo especifico..."):
                for i, conta_id in enumerate(contas_especifico, 1):
                    barra_esp.progress(
                        min((i - 1) / max(total, 1), 1.0),
                        text=f"Gerando para {CONTAS[conta_id]['nome']}...",
                    )
                    item = generator.gerar_conteudo_especifico(
                        conta_id=conta_id,
                        tipo=tipo,
                        prompt_usuario=prompt_usuario.strip(),
                        stories_quantidade=int(stories_quantidade),
                        stories_dias=int(stories_dias),
                    )
                    itens.append(item)

                resultado = {
                    "tipo": tipo,
                    "prompt_usuario": prompt_usuario.strip(),
                    "itens": itens,
                }
                pasta_especifico = _salvar_markdown_conteudo_especifico(
                    resultado,
                    CONFIGURACOES["pasta_output"],
                )

            barra_esp.progress(1.0, text="Concluido")
            st.success(f"Conteudo especifico gerado em: {pasta_especifico}")

            st.session_state["resultado_especifico"] = resultado
            st.session_state["pasta_especifico"] = pasta_especifico
            st.session_state["caminho_pdf_especifico"] = os.path.join(
                pasta_especifico,
                "conteudo_especifico.pdf",
            )
            st.session_state["validacao_especifico"] = None
            st.session_state["download_liberado_especifico"] = False

        resultado_salvo = st.session_state.get("resultado_especifico")
        if resultado_salvo:
            st.write("### Etapa 1: Conteudo gerado")
            for item in resultado_salvo["itens"]:
                with st.expander(
                    f"{item['conta_nome']} - {resultado_salvo['tipo'].title()}",
                    expanded=False,
                ):
                    if not item.get("tema_detectado", True):
                        st.warning(
                            "Tema central com baixa aderencia detectada automaticamente. "
                            "Considere regenerar com prompt mais especifico."
                        )
                    st.caption(
                        f"Tentativas: {item.get('tentativa', 1)} | "
                        f"Tema detectado: {'sim' if item.get('tema_detectado', False) else 'nao'}"
                    )
                    st.write(item["conteudo"])

            st.write("### Etapa 2: Validacao do tema")
            if st.button("Validar Conteudo Especifico", use_container_width=True):
                validacao = _validar_resultado_especifico(resultado_salvo)
                st.session_state["validacao_especifico"] = validacao

                if validacao["aprovado"]:
                    caminho_pdf_especifico = st.session_state["caminho_pdf_especifico"]
                    try:
                        exportar_conteudo_especifico_pdf(resultado_salvo, caminho_pdf_especifico)
                    except ModuleNotFoundError as exc:
                        st.error(str(exc))
                        st.info("Instale dependencias com: pip install -r requirements.txt")
                        return
                    st.session_state["download_liberado_especifico"] = True
                else:
                    st.session_state["download_liberado_especifico"] = False

            validacao_salva = st.session_state.get("validacao_especifico")
            if validacao_salva:
                if validacao_salva["aprovado"]:
                    st.success("Validacao aprovada: tema encontrado em todos os conteudos.")
                else:
                    st.error(
                        "Validacao reprovada: pelo menos um conteudo nao apresentou aderencia "
                        "suficiente ao tema."
                    )
                for item_val in validacao_salva["itens"]:
                    status = "OK" if item_val["valido"] else "FALHOU"
                    termos = ", ".join(item_val["termos_encontrados"]) or "nenhum"
                    st.write(f"- {item_val['conta_nome']}: {status} (termos encontrados: {termos})")

            if st.session_state.get("download_liberado_especifico"):
                caminho_pdf_especifico = st.session_state["caminho_pdf_especifico"]
                with open(caminho_pdf_especifico, "rb") as f:
                    st.download_button(
                        label="Baixar PDF do Conteudo Especifico",
                        data=f.read(),
                        file_name=os.path.basename(caminho_pdf_especifico),
                        mime="application/pdf",
                        use_container_width=True,
                        key="download_pdf_especifico",
                    )


if __name__ == "__main__":
    main()
