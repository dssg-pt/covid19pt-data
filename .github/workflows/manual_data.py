import numpy as np
import pandas as pd
from pathlib import Path


if __name__ == "__main__":

    today = "08-07-2021"

    # boletim
    ativos = 41863
    recuperados = 840297
    obitos = 17135
    vigilancia = 68867
    confirmados = 899295
    confirmados_novos = 3269

    confirmados_arsnorte = 350771
    obitos_arsnorte = 5371
    confirmados_arscentro = 123792
    obitos_arscentro = 3029
    confirmados_arslvt = 350282
    obitos_arslvt = 7292
    confirmados_arsalentejo = 31543
    obitos_arsalentejo = 973
    confirmados_arsalgarve = 26457
    obitos_arsalgarve = 366
    confirmados_acores = 6418
    obitos_acores = 34
    confirmados_madeira = 10032
    obitos_madeira = 70

    internados, internados_uci = 599, 136

    confirmados_m, confirmados_f = 410663, 488127
    confirmados_desconhecido = 505

    obitos_m, obitos_f = 8996, 8139

    incidencia_nacional, incidencia_continente = 247.3, 254.8
    rt_nacional, rt_continente = 1.20, 1.20


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
