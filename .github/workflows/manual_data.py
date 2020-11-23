import requests
import datetime
import pandas as pd
from pathlib import Path


if __name__ == "__main__":

    today = "21-11-2020"

    # boletim
    ativos = 82767
    recuperados = 169379
    obitos = 3824
    vigilancia = 80521
    confirmados = 255970
    confirmados_novos = 6472

    internados = 3025
    internados_uci = 485

    confirmados_m = 112961
    confirmados_f = 138276
    confirmados_desconhecido = 4733

    obitos_m = 1967
    obitos_f = 1857

    confirmados_arsnorte = 0
    confirmados_arscentro = 0
    confirmados_arslvt = 0
    confirmados_arsalentejo = 0
    confirmados_arsalgarve = 0
    confirmados_acores = 0
    confirmados_madeira = 0
    obitos_arsnorte = 0
    obitos_arscentro = 0
    obitos_arslvt = 0
    obitos_arsalentejo = 0
    obitos_arsalgarve = 0
    obitos_acores = 0
    obitos_madeira = 0

    # derivaveis
    internados_enfermaria = internados - internados_uci

    # only on API
    confirmados_estrangeiro = 0
    confirmados_0_9_f = 0
    confirmados_0_9_m = 0
    confirmados_10_19_f = 0
    confirmados_10_19_m = 0
    confirmados_20_29_f = 0
    confirmados_20_29_m = 0
    confirmados_30_39_f = 0
    confirmados_30_39_m = 0
    confirmados_40_49_f = 0
    confirmados_40_49_m = 0
    confirmados_50_59_f = 0
    confirmados_50_59_m = 0
    confirmados_60_69_f = 0
    confirmados_60_69_m = 0
    confirmados_70_79_f = 0
    confirmados_70_79_m = 0
    confirmados_80_plus_f = 0
    confirmados_80_plus_m = 0
    obitos_estrangeiro = 0
    obitos_0_9_f = 0
    obitos_0_9_m = 0
    obitos_10_19_f = 0
    obitos_10_19_m = 0
    obitos_20_29_f = 0
    obitos_20_29_m = 0
    obitos_30_39_f = 0
    obitos_30_39_m = 0
    obitos_40_49_f = 0
    obitos_40_49_m = 0
    obitos_50_59_f = 0
    obitos_50_59_m = 0
    obitos_60_69_f = 0
    obitos_60_69_m = 0
    obitos_70_79_f = 0
    obitos_70_79_m = 0
    obitos_80_plus_f = 0
    obitos_80_plus_m = 0
    recuperados_arsnorte = 0
    recuperados_arscentro = 0
    recuperados_arslvt = 0
    recuperados_arsalentejo = 0
    recuperados_arsalgarve = 0
    recuperados_acores = 0
    recuperados_madeira = 0
    recuperados_estrangeiro = 0

    # unknowns
    lab = 0
    suspeitos = 0
    n_confirmados = 0
    cadeias_transmissao = 0
    transmissao_importada = 0
    sintomas_tosse = 0
    sintomas_febre = 0
    sintomas_dificuldade_respiratoria = 0
    sintomas_cefaleia = 0
    sintomas_dores_musculares = 0
    sintomas_fraqueza_generalizada = 0
    confirmados_desconhecidos_m = 0
    confirmados_desconhecidos_f = 0

    # ORDENAR DADOS
    new_row = pd.DataFrame(
        [
            [
                today,
                "{} 00:00".format(today),
                confirmados,
                confirmados_arsnorte,
                confirmados_arscentro,
                confirmados_arslvt,
                confirmados_arsalentejo,
                confirmados_arsalgarve,
                confirmados_acores,
                confirmados_madeira,
                confirmados_estrangeiro,
                confirmados_novos,
                recuperados,
                obitos,
                internados,
                internados_uci,
                lab,
                suspeitos,
                vigilancia,
                n_confirmados,
                cadeias_transmissao,
                transmissao_importada,
                confirmados_0_9_f,
                confirmados_0_9_m,
                confirmados_10_19_f,
                confirmados_10_19_m,
                confirmados_20_29_f,
                confirmados_20_29_m,
                confirmados_30_39_f,
                confirmados_30_39_m,
                confirmados_40_49_f,
                confirmados_40_49_m,
                confirmados_50_59_f,
                confirmados_50_59_m,
                confirmados_60_69_f,
                confirmados_60_69_m,
                confirmados_70_79_f,
                confirmados_70_79_m,
                confirmados_80_plus_f,
                confirmados_80_plus_m,
                sintomas_tosse,
                sintomas_febre,
                sintomas_dificuldade_respiratoria,
                sintomas_cefaleia,
                sintomas_dores_musculares,
                sintomas_fraqueza_generalizada,
                confirmados_f,
                confirmados_m,
                obitos_arsnorte,
                obitos_arscentro,
                obitos_arslvt,
                obitos_arsalentejo,
                obitos_arsalgarve,
                obitos_acores,
                obitos_madeira,
                obitos_estrangeiro,
                recuperados_arsnorte,
                recuperados_arscentro,
                recuperados_arslvt,
                recuperados_arsalentejo,
                recuperados_arsalgarve,
                recuperados_acores,
                recuperados_madeira,
                recuperados_estrangeiro,
                obitos_0_9_f,
                obitos_0_9_m,
                obitos_10_19_f,
                obitos_10_19_m,
                obitos_20_29_f,
                obitos_20_29_m,
                obitos_30_39_f,
                obitos_30_39_m,
                obitos_40_49_f,
                obitos_40_49_m,
                obitos_50_59_f,
                obitos_50_59_m,
                obitos_60_69_f,
                obitos_60_69_m,
                obitos_70_79_f,
                obitos_70_79_m,
                obitos_80_plus_f,
                obitos_80_plus_m,
                obitos_f,
                obitos_m,
                confirmados_desconhecidos_m,
                confirmados_desconhecidos_f,
                ativos,
                internados_enfermaria,
                confirmados_desconhecido,
            ]
        ]
    )

    # write to csv
    csv_path = str(Path(__file__).resolve().parents[2] / "data.csv")
    new_row.to_csv(csv_path, mode="a", header=False, index=False, sep=",")
