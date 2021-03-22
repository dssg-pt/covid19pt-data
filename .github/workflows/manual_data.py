import numpy as np
import pandas as pd
from pathlib import Path


if __name__ == "__main__":

    today = "21-03-2021"

    # boletim
    ativos = 33443
    recuperados = 767319
    obitos = 16768
    vigilancia = 14986
    confirmados = 817530
    confirmados_novos = 450

    confirmados_arsnorte = 329484
    obitos_arsnorte = 5289
    confirmados_arscentro = 116661
    obitos_arscentro = 2986
    confirmados_arslvt = 309757
    obitos_arslvt = 7083
    confirmados_arsalentejo = 28897
    obitos_arsalentejo = 966
    confirmados_arsalgarve = 20425
    obitos_arsalgarve = 351
    confirmados_acores = 3954
    obitos_acores = 28
    confirmados_madeira = 8352
    obitos_madeira = 65

    internados = 765
    internados_uci = 170

    confirmados_m = 370138
    confirmados_f = 447102
    confirmados_desconhecido = 290

    obitos_m = 8803
    obitos_f = 7965

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
            ]
        ]
    )

    # write to csv
    csv_path = str(Path(__file__).resolve().parents[2] / "data.csv")
    new_row.to_csv(csv_path, mode="a", header=False, index=False, sep=",")
