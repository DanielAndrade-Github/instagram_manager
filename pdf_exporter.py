"""
Exporta plano semanal para PDF organizado por cliente e dia.
"""

from __future__ import annotations

from html import escape


def _texto_para_paragrafo(texto: str) -> str:
    texto = texto or ""
    return escape(texto).replace("\n", "<br/>")


def exportar_plano_pdf(plano: dict, caminho_pdf: str) -> str:
    try:
        from reportlab.lib import colors
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
    normal = ParagraphStyle(
        "NormalCustom",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
    )
    bloco = ParagraphStyle(
        "Bloco",
        parent=normal,
        backColor=colors.whitesmoke,
        borderColor=colors.lightgrey,
        borderWidth=0.5,
        borderPadding=8,
    )

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
                    story.append(Paragraph(f"<b>Post {i}</b>", normal))
                    story.append(Paragraph(_texto_para_paragrafo(conteudo), bloco))
                    story.append(Spacer(1, 6))

            if dia["reels"]:
                for i, conteudo in enumerate(dia["reels"], 1):
                    story.append(Paragraph(f"<b>Reel {i}</b>", normal))
                    story.append(Paragraph(_texto_para_paragrafo(conteudo), bloco))
                    story.append(Spacer(1, 6))

            if dia["carrosseis"]:
                for i, conteudo in enumerate(dia["carrosseis"], 1):
                    story.append(Paragraph(f"<b>Carrossel {i}</b>", normal))
                    story.append(Paragraph(_texto_para_paragrafo(conteudo), bloco))
                    story.append(Spacer(1, 6))

            story.append(Paragraph("<b>Stories</b>", normal))
            story.append(Paragraph(_texto_para_paragrafo(dia["stories"]), bloco))
            story.append(Spacer(1, 12))

        if conta_index < len(plano["contas"]) - 1:
            story.append(PageBreak())

    doc.build(story)
    return caminho_pdf
