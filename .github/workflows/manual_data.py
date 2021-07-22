import numpy as np
import pandas as pd
from pathlib import Path


if __name__ == "__main__":

    today = "22-07-2021"

    # boletim
    ativos = 52988
    recuperados = 873008
    obitos = 17248
    vigilancia = 81377
    confirmados = 943244
    confirmados_novos = 3622

    confirmados_arsnorte = 365899
    obitos_arsnorte = 5387
    confirmados_arscentro = 127427
    obitos_arscentro = 3036
    confirmados_arslvt = 369161
    obitos_arslvt = 7362
    confirmados_arsalentejo = 32742
    obitos_arsalentejo = 977
    confirmados_arsalgarve = 30696
    obitos_arsalgarve = 381
    confirmados_acores = 6977
    obitos_acores = 35
    confirmados_madeira = 10342
    obitos_madeira = 70

    internados, internados_uci = 860, 178

    confirmados_m, confirmados_f = 432287, 510337
    confirmados_desconhecido = 620

    obitos_m, obitos_f = 9056, 8192

    incidencia_nacional, incidencia_continente = 409.0, 421.3
    rt_nacional, rt_continente = 1.09, 1.09


    # derivaveis
    internados_enfermaria = internados - internados_uci

    # only on API
    confirmados_estrangeiro = np.nan
    confirmados_0_9_f = np.nan
    confirmados_0_9_m = np.nan
    confirmados_10_19_f = np.nan
    confirmados_10_19_m = np.nan
    confirmados_20_29_f = np.nan
    confirmados_20_29_m = np.nan
    confirmados_30_39_f = np.nan
    confirmados_30_39_m = np.nan
    confirmados_40_49_f = np.nan
    confirmados_40_49_m = np.nan
    confirmados_50_59_f = np.nan
    confirmados_50_59_m = np.nan
    confirmados_60_69_f = np.nan
    confirmados_60_69_m = np.nan
    confirmados_70_79_f = np.nan
    confirmados_70_79_m = np.nan
    confirmados_80_plus_f = np.nan
    confirmados_80_plus_m = np.nan
    obitos_estrangeiro = np.nan
    obitos_0_9_f = np.nan
    obitos_0_9_m = np.nan
    obitos_10_19_f = np.nan
    obitos_10_19_m = np.nan
    obitos_20_29_f = np.nan
    obitos_20_29_m = np.nan
    obitos_30_39_f = np.nan
    obitos_30_39_m = np.nan
    obitos_40_49_f = np.nan
    obitos_40_49_m = np.nan
    obitos_50_59_f = np.nan
    obitos_50_59_m = np.nan
    obitos_60_69_f = np.nan
    obitos_60_69_m = np.nan
    obitos_70_79_f = np.nan
    obitos_70_79_m = np.nan
    obitos_80_plus_f = np.nan
    obitos_80_plus_m = np.nan
    recuperados_arsnorte = np.nan
    recuperados_arscentro = np.nan
    recuperados_arslvt = np.nan
    recuperados_arsalentejo = np.nan
    recuperados_arsalgarve = np.nan
    recuperados_acores = np.nan
    recuperados_madeira = np.nan
    recuperados_estrangeiro = np.nan

    # unknowns
    lab = np.nan
    suspeitos = np.nan
    n_confirmados = np.nan
    cadeias_transmissao = np.nan
    transmissao_importada = np.nan
    sintomas_tosse = np.nan
    sintomas_febre = np.nan
    sintomas_dificuldade_respiratoria = np.nan
    sintomas_cefaleia = np.nan
    sintomas_dores_musculares = np.nan
    sintomas_fraqueza_generalizada = np.nan
    confirmados_desconhecidos_m = np.nan
    confirmados_desconhecidos_f = np.nan

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
                incidencia_nacional,
                incidencia_continente,
                rt_nacional,
                rt_continente,
            ]
        ]
    )

    # write to csv
    csv_path = str(Path(__file__).resolve().parents[2] / "data.csv")
    new_row.to_csv(csv_path, mode="a", header=False, index=False, sep=",")
