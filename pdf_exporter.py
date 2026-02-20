"""
Exporta plano semanal para PDF organizado por cliente e dia.
"""

from __future__ import annotations

import re
from html import escape


def _normalizar_linha_markdown(linha: str) -> str:
    linha = linha.strip()
    if not linha:
        return ""
    linha = re.sub(r"^#{1,6}\s*", "", linha)
    linha = escape(linha)
    linha = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", linha)
    return linha


def _adicionar_bloco_texto(story, texto: str, estilo, paragraph_cls, spacer_cls):
    linhas = (texto or "").splitlines()
    if not linhas:
        story.append(paragraph_cls("Sem conteudo.", estilo))
        return

    for linha in linhas:
        html_linha = _normalizar_linha_markdown(linha)
        if not html_linha:
            story.append(spacer_cls(1, 4))
            continue
        story.append(paragraph_cls(html_linha, estilo))
        story.append(spacer_cls(1, 2))


def _carregar_reportlab():
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.platypus import (
            PageBreak,
            Paragraph,
            SimpleDocTemplate,
            Spacer,
        )
    except ModuleNotFoundError as exc:
        raise ModuleNotFoundError(
            "Biblioteca 'reportlab' nao instalada. Execute: pip install reportlab"
        ) from exc
    return A4, ParagraphStyle, getSampleStyleSheet, PageBreak, Paragraph, SimpleDocTemplate, Spacer


def exportar_plano_pdf(plano: dict, caminho_pdf: str) -> str:
    (
        A4,
        ParagraphStyle,
        getSampleStyleSheet,
        PageBreak,
        Paragraph,
        SimpleDocTemplate,
        Spacer,
    ) = _carregar_reportlab()

    doc = SimpleDocTemplate(
        caminho_pdf,
        pagesize=A4,
        leftMargin=32,
        rightMargin=32,
        topMargin=36,
        bottomMargin=36,
        title="Plano Semanal de Conteudo",
    )
    styles = getSampleStyleSheet()
    titulo = styles["Title"]
    h2 = styles["Heading2"]
    h3 = styles["Heading3"]
    secao = ParagraphStyle(
        "Secao",
        parent=styles["Heading4"],
        spaceBefore=6,
        spaceAfter=6,
    )
    normal = ParagraphStyle(
        "NormalCustom",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        spaceBefore=0,
        spaceAfter=0,
    )
    h2.spaceAfter = 8
    h3.spaceAfter = 6

    story = []
    story.append(Paragraph("Plano Semanal de Conteudo", titulo))
    story.append(
        Paragraph(
            f"Periodo: {plano['data_inicio']} ate {plano['data_fim']}",
            normal,
        )
    )
    story.append(Spacer(1, 12))

    for conta_index, conta in enumerate(plano["contas"]):
        story.append(Paragraph(f"Cliente: {escape(conta['nome'])}", h2))
        story.append(Spacer(1, 6))

        for dia in conta["dias"]:
            story.append(
                Paragraph(
                    f"{escape(dia['dia_semana']).title()} - {dia['data']}",
                    h3,
                )
            )
            resumo = (
                f"Posts: {len(dia['posts'])} | Reels: {len(dia['reels'])} | "
                f"Carrosseis: {len(dia['carrosseis'])} | Stories: {dia['stories_quantidade']}"
            )
            story.append(Paragraph(resumo, normal))
            story.append(Spacer(1, 6))

            if dia["posts"]:
                for i, conteudo in enumerate(dia["posts"], 1):
                    story.append(Paragraph(f"Post {i}", secao))
                    _adicionar_bloco_texto(story, conteudo, normal, Paragraph, Spacer)
                    story.append(Spacer(1, 8))

            if dia["reels"]:
                for i, conteudo in enumerate(dia["reels"], 1):
                    story.append(Paragraph(f"Reel {i}", secao))
                    _adicionar_bloco_texto(story, conteudo, normal, Paragraph, Spacer)
                    story.append(Spacer(1, 8))

            if dia["carrosseis"]:
                for i, conteudo in enumerate(dia["carrosseis"], 1):
                    story.append(Paragraph(f"Carrossel {i}", secao))
                    _adicionar_bloco_texto(story, conteudo, normal, Paragraph, Spacer)
                    story.append(Spacer(1, 8))

            story.append(Paragraph("Stories", secao))
            _adicionar_bloco_texto(story, dia["stories"], normal, Paragraph, Spacer)
            story.append(Spacer(1, 12))

        if conta_index < len(plano["contas"]) - 1:
            story.append(PageBreak())

    doc.build(story)
    return caminho_pdf


def exportar_conteudo_especifico_pdf(resultado: dict, caminho_pdf: str) -> str:
    (
        A4,
        ParagraphStyle,
        getSampleStyleSheet,
        PageBreak,
        Paragraph,
        SimpleDocTemplate,
        Spacer,
    ) = _carregar_reportlab()

    doc = SimpleDocTemplate(
        caminho_pdf,
        pagesize=A4,
        leftMargin=32,
        rightMargin=32,
        topMargin=36,
        bottomMargin=36,
        title="Conteudo Especifico",
    )

    styles = getSampleStyleSheet()
    titulo = styles["Title"]
    h2 = styles["Heading2"]
    h3 = styles["Heading3"]
    normal = ParagraphStyle(
        "NormalCustomEspecifico",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        spaceBefore=0,
        spaceAfter=0,
    )
    h2.spaceAfter = 8
    h3.spaceAfter = 6

    story = []
    story.append(Paragraph("Conteudo Especifico", titulo))
    story.append(Paragraph(f"Tipo: {escape(resultado['tipo']).title()}", normal))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Tema central escolhido:</b>", normal))
    _adicionar_bloco_texto(story, resultado["prompt_usuario"], normal, Paragraph, Spacer)
    story.append(Spacer(1, 12))

    for idx, item in enumerate(resultado["itens"]):
        story.append(Paragraph(f"Cliente: {escape(item['conta_nome'])}", h2))
        if item.get("stories_quantidade"):
            dias = item.get("stories_dias", 1)
            total = dias * item["stories_quantidade"]
            story.append(
                Paragraph(
                    f"Stories solicitados: {item['stories_quantidade']} por dia, "
                    f"durante {dias} dia(s) (total {total})",
                    normal,
                )
            )
            story.append(Spacer(1, 4))
        story.append(Paragraph("Conteudo gerado", h3))
        _adicionar_bloco_texto(story, item["conteudo"], normal, Paragraph, Spacer)
        story.append(Spacer(1, 12))
        if idx < len(resultado["itens"]) - 1:
            story.append(PageBreak())

    doc.build(story)
    return caminho_pdf
