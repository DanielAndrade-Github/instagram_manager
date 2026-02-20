"""
App Streamlit para gerar plano semanal e exportar PDF.
"""

from __future__ import annotations

import os
from datetime import date

import streamlit as st
from dotenv import load_dotenv

from config import CONTAS, CONFIGURACOES
from generator import InstagramContentGenerator
from pdf_exporter import exportar_plano_pdf
from weekly_planner import gerar_plano_semanal, salvar_plano_em_markdown


def main():
    load_dotenv()
    st.set_page_config(page_title="Planejador Instagram", layout="wide")
    st.title("Planejador Semanal de Conteudo")
    st.caption("Gera de 1 a 7 dias de conteudo por cliente e exporta um PDF unico.")

    with st.sidebar:
        st.header("Configuracao")
        api_key = st.text_input(
            "GROQ_API_KEY",
            value=os.getenv("GROQ_API_KEY", ""),
            type="password",
            help="Chave da Groq (free tier disponivel).",
        )
        contas_disponiveis = list(CONTAS.keys())
        opcoes_cliente = []
        if len(contas_disponiveis) >= 1:
            opcoes_cliente.append("1")
        if len(contas_disponiveis) >= 2:
            opcoes_cliente.append("2")
        if len(contas_disponiveis) >= 1:
            opcoes_cliente.append("todos")

        escolha_cliente = st.selectbox(
            "Qual cliente quer? (1, 2 ou todos)",
            options=opcoes_cliente,
            index=opcoes_cliente.index("todos") if "todos" in opcoes_cliente else 0,
            help=(
                f"1 = {CONTAS[contas_disponiveis[0]]['nome']}"
                + (
                    f" | 2 = {CONTAS[contas_disponiveis[1]]['nome']}"
                    if len(contas_disponiveis) >= 2
                    else ""
                )
            ),
        )
        if escolha_cliente == "1":
            contas_selecionadas = [contas_disponiveis[0]]
        elif escolha_cliente == "2":
            contas_selecionadas = [contas_disponiveis[1]]
        else:
            contas_selecionadas = contas_disponiveis

        data_inicio = st.date_input(
            "Data de inicio (incluida no plano)",
            value=date.today(),
            format="YYYY-MM-DD",
            help="Se executar no sabado, mantenha a data de hoje para incluir o sabado.",
        )
        dias = st.number_input("Para quantos dias? (1 a 7)", min_value=1, max_value=7, value=7, step=1)
        gerar = st.button("Gerar Plano + PDF", type="primary", use_container_width=True)

    st.write("### Volumes semanais configurados")
    for conta_id in contas_selecionadas:
        volume = CONTAS[conta_id]["volume"]
        st.write(
            f"- {CONTAS[conta_id]['nome']}: "
            f"{volume['posts']} posts, {volume['reels']} reels, "
            f"{volume['carrosseis']} carrosseis, {volume['stories']} stories"
        )

    if not gerar:
        return

    if not api_key:
        st.error("Informe a GROQ_API_KEY no campo lateral ou no arquivo .env.")
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

    with st.spinner("Gerando conteudo, aguarde..."):
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
        st.write(f"**{conta['nome']}**")
        for dia in conta["dias"]:
            st.write(
                f"- {dia['dia_semana']} ({dia['data']}): "
                f"posts={len(dia['posts'])}, reels={len(dia['reels'])}, "
                f"carrosseis={len(dia['carrosseis'])}, stories={dia['stories_quantidade']}"
            )

    with open(caminho_pdf, "rb") as f:
        st.download_button(
            label="Baixar PDF",
            data=f.read(),
            file_name=os.path.basename(caminho_pdf),
            mime="application/pdf",
            use_container_width=True,
        )


if __name__ == "__main__":
    main()
