"""
Planejamento semanal de conteúdo por cliente e por dia.
"""

from __future__ import annotations

import os
import re
import unicodedata
from datetime import date, timedelta

from config import CONTAS, CONFIGURACOES


WEEKDAY_PT = [
    "segunda-feira",
    "terca-feira",
    "quarta-feira",
    "quinta-feira",
    "sexta-feira",
    "sabado",
    "domingo",
]


def _slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


def distribuir_total(total: int, buckets: int) -> list[int]:
    if buckets <= 0:
        return []
    base = total // buckets
    resto = total % buckets
    return [base + (1 if i < resto else 0) for i in range(buckets)]


def distribuir_itens(itens: list[str], buckets: int) -> list[list[str]]:
    distribuicao = [[] for _ in range(buckets)]
    for i, item in enumerate(itens):
        distribuicao[i % buckets].append(item)
    return distribuicao


def gerar_plano_semanal(
    generator,
    conta_ids: list[str],
    data_inicio: date,
    dias: int = 7,
    status_cb=None,
):
    datas = [data_inicio + timedelta(days=i) for i in range(dias)]
    contas_output = []

    for conta_id in conta_ids:
        conta = CONTAS[conta_id]
        volume = conta["volume"]

        if status_cb:
            status_cb(f"{conta['nome']}: gerando posts...")
        posts = generator.gerar_posts(conta_id, volume["posts"])

        if status_cb:
            status_cb(f"{conta['nome']}: gerando reels...")
        reels = generator.gerar_reels(conta_id, volume["reels"])

        if status_cb:
            status_cb(f"{conta['nome']}: gerando carrosseis...")
        carrosseis = generator.gerar_carrosseis(conta_id, volume["carrosseis"])

        stories_por_dia = distribuir_total(volume["stories"], dias)
        if status_cb:
            status_cb(f"{conta['nome']}: gerando stories por dia...")
        stories_dia = generator.gerar_stories_por_dia(conta_id, stories_por_dia)

        posts_dia = distribuir_itens(posts, dias)
        reels_dia = distribuir_itens(reels, dias)
        carrosseis_dia = distribuir_itens(carrosseis, dias)

        dias_output = []
        for i, dia_data in enumerate(datas):
            stories_item = next((s for s in stories_dia if s["dia"] == i + 1), None)
            dias_output.append(
                {
                    "data": dia_data.isoformat(),
                    "dia_semana": WEEKDAY_PT[dia_data.weekday()],
                    "posts": posts_dia[i],
                    "reels": reels_dia[i],
                    "carrosseis": carrosseis_dia[i],
                    "stories": stories_item["conteudo"] if stories_item else "",
                    "stories_quantidade": stories_item["quantidade"] if stories_item else 0,
                }
            )

        contas_output.append(
            {
                "conta_id": conta_id,
                "nome": conta["nome"],
                "dias": dias_output,
                "volume": volume,
            }
        )

    return {
        "data_inicio": datas[0].isoformat(),
        "data_fim": datas[-1].isoformat(),
        "dias": dias,
        "contas": contas_output,
    }


def salvar_plano_em_markdown(plano: dict, pasta_output: str | None = None) -> str:
    pasta_base = pasta_output or CONFIGURACOES["pasta_output"]
    pasta_semana = os.path.join(
        pasta_base,
        f"plano_{plano['data_inicio']}_a_{plano['data_fim']}",
    )
    os.makedirs(pasta_semana, exist_ok=True)

    for conta in plano["contas"]:
        pasta_conta = os.path.join(pasta_semana, _slugify(conta["nome"]))
        os.makedirs(pasta_conta, exist_ok=True)

        for dia in conta["dias"]:
            arquivo = os.path.join(
                pasta_conta,
                f"{dia['data']}_{_slugify(dia['dia_semana'])}.md",
            )
            with open(arquivo, "w", encoding="utf-8") as f:
                f.write(f"# {conta['nome']} - {dia['dia_semana']} ({dia['data']})\n\n")

                f.write("## Posts\n\n")
                if dia["posts"]:
                    for i, post in enumerate(dia["posts"], 1):
                        f.write(f"### Post {i}\n\n{post}\n\n")
                else:
                    f.write("Sem post planejado.\n\n")

                f.write("## Reels\n\n")
                if dia["reels"]:
                    for i, reel in enumerate(dia["reels"], 1):
                        f.write(f"### Reel {i}\n\n{reel}\n\n")
                else:
                    f.write("Sem reel planejado.\n\n")

                f.write("## Carrosseis\n\n")
                if dia["carrosseis"]:
                    for i, carrossel in enumerate(dia["carrosseis"], 1):
                        f.write(f"### Carrossel {i}\n\n{carrossel}\n\n")
                else:
                    f.write("Sem carrossel planejado.\n\n")

                f.write(f"## Stories ({dia['stories_quantidade']})\n\n")
                f.write((dia["stories"] or "Sem stories planejados.") + "\n")

    return pasta_semana
