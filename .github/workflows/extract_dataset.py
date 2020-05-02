from os import listdir
from os.path import isfile, join
from pathlib import Path
import pandas as pd
import numpy as np
import textract
import re
import datetime

def get_report(file_path):
    
    # Date of report
    date = file_path.split("-")[-1].split('.pdf')[0][-10:].replace("_", "-")

    text_raw = textract.process(file_path).decode("utf-8")
    text = process_raw_text(text_raw)
    file = {
        "file_path": file_path,
        "date": date,
        "text_raw": text_raw,
        "text": text
    }
    
    return file


def process_raw_text(report_text_raw):
    lines = report_text_raw.split("\n")
    lines = [l for l in lines if l]
    return "\n".join(lines)


def extract_data(reports, original_dataframe):
    # Dates
    dates = []

    # Valores Iniciais
    confirmados = []
    n_confirmados = []
    lab = []
    recuperados = []
    vigilancia = []
    suspeitos = []

    # Confirmados
    confirmados_acores = []
    confirmados_madeira = []
    confirmados_arsnorte = []
    confirmados_arscentro = []
    confirmados_arslvt = []
    confirmados_arsalentejo = []
    confirmados_arsalgarve = []
    confirmados_estrangeiro = []

    # Obitos
    obitos = []
    obitos_acores = []
    obitos_madeira = []
    obitos_arsnorte = []
    obitos_arscentro = []
    obitos_arslvt = []
    obitos_arsalentejo = []
    obitos_arsalgarve = []
    obitos_estrangeiro = []

    # Recuperados
    #recuperados_arsnorte = []
    #recuperados_arscentro = []
    #recuperados_arslvt = []
    recuperados_arsalentejo = []
    recuperados_arsalgarve = []
    recuperados_estrangeiro = []

    # Confirmados Faixa Etaria
    confirmados_f = []
    confirmados_m = []
    confirmados_0_9_f = []
    confirmados_0_9_m = []
    confirmados_10_19_f = []
    confirmados_10_19_m = []
    confirmados_20_29_f = []
    confirmados_20_29_m =[ ]
    confirmados_30_39_f = []
    confirmados_30_39_m = []
    confirmados_40_49_f = []
    confirmados_40_49_m = []
    confirmados_50_59_f = []
    confirmados_50_59_m = []
    confirmados_60_69_f = []
    confirmados_60_69_m = []
    confirmados_70_79_f = []
    confirmados_70_79_m = []
    confirmados_80_plus_f = []
    confirmados_80_plus_m = []

    # Obitos Faixa Etaria
    obitos_f = []
    obitos_m = []
    obitos_0_9_f = []
    obitos_0_9_m = []
    obitos_10_19_f = []
    obitos_10_19_m = []
    obitos_20_29_f = []
    obitos_20_29_m =[ ]
    obitos_30_39_f = []
    obitos_30_39_m = []
    obitos_40_49_f = []
    obitos_40_49_m = []
    obitos_50_59_f = []
    obitos_50_59_m = []
    obitos_60_69_f = []
    obitos_60_69_m = []
    obitos_70_79_f = []
    obitos_70_79_m = []
    obitos_80_plus_f = []
    obitos_80_plus_m = []

    # Internados
    internados = []
    internados_uci = []

    # Sintomas
    sintomas_tosse = []
    sintomas_febre = []
    sintomas_dificuldade_respiratoria = []
    sintomas_cefaleia = []
    sintomas_dores_musculares = []
    sintomas_fraqueza_generalizada = []
    transmissao_importada = []
    confirmados_novos = []


    for report in reports:
        text = report["text"]
        lines = text.split("\n")

        print(lines)

        try:
            print("Running first script")

            [suspeitos_value, confirmados_value, n_confirmados_value, lab_value, recuperados_value,
            obitos_value, vigilancia_value,
            confirmados_acores_value, obitos_acores_value, confirmados_madeira_value, obitos_madeira_value,
            confirmados_arsnorte_value, obitos_arsnorte_value,  # recuperados_arsnorte_value,
            confirmados_arscentro_value, obitos_arscentro_value,  # recuperados_arscentro_value,
            confirmados_arslvt_value, obitos_arslvt_value,  #recuperados_arslvt_value,
            confirmados_arsalentejo_value, obitos_arsalentejo_value, confirmados_arsalgarve_value, obitos_arsalgarve_value
            ] = get_all_numbers_from_list(lines, "Total de casos", "Região de residência")
            
        except ValueError:

            print("Running second script")

            [confirmados_acores_value, obitos_acores_value, confirmados_madeira_value, obitos_madeira_value,
            confirmados_arsnorte_value, obitos_arsnorte_value,  # recuperados_arsnorte_value,
            confirmados_arscentro_value, obitos_arscentro_value,  # recuperados_arscentro_value,
            ] = get_all_numbers_from_list(lines, "Açores", "Total de casos")

            [suspeitos_value, confirmados_value, n_confirmados_value, lab_value, recuperados_value,
            obitos_value, confirmados_arslvt_value, obitos_arslvt_value,  #recuperados_arslvt_value,
            confirmados_arsalentejo_value, obitos_arsalentejo_value, confirmados_arsalgarve_value, obitos_arsalgarve_value
            ] = get_all_numbers_from_list(lines, "Total de casos", "Região de residência")

            vigilancia_value = get_all_numbers_from_list(lines, "pelas Autoridades de Saúde", "Legenda")


        """ INITIAL VALUES ON LEFT """

        dates.append(report["date"])
        confirmados.append(confirmados_value)
        n_confirmados.append(n_confirmados_value)
        lab.append(lab_value)
        recuperados.append(recuperados_value)
        vigilancia.append(vigilancia_value)
        suspeitos.append(suspeitos_value)
        obitos.append(obitos_value)


        """ CONFIMADOS, OBITOS E RECUPERADOS POR REGIAO """
        # Acores
        confirmados_acores.append(confirmados_acores_value)
        obitos_acores.append(obitos_acores_value)

        # Madeira
        confirmados_madeira.append(confirmados_madeira_value)
        obitos_madeira.append(obitos_madeira_value)

        # Norte
        confirmados_arsnorte.append(confirmados_arsnorte_value)
        obitos_arsnorte.append(obitos_arsnorte_value)
        #recuperados_arsnorte.append(recuperados_arsnorte_value)

        # Centro
        confirmados_arscentro.append(confirmados_arscentro_value)
        obitos_arscentro.append(obitos_arscentro_value)
        #recuperados_arscentro.append(recuperados_arscentro_value)

        # Lisboa
        confirmados_arslvt.append(confirmados_arslvt_value)
        obitos_arslvt.append(obitos_arslvt_value)
        #recuperados_arslvt.append(recuperados_arslvt_value)

        # Alentejo
        confirmados_arsalentejo.append(confirmados_arsalentejo_value)
        obitos_arsalentejo.append(obitos_arsalentejo_value)

        # Algarve
        confirmados_arsalgarve.append(confirmados_arsalgarve_value)
        obitos_arsalgarve.append(obitos_arsalgarve_value)


        """ CONFIRMADOS NOVOS"""

#        index_last_row = original_dataframe.index[original_dataframe['data'] == report["date"]].tolist()[0] - 1
        confirmados_old = original_dataframe.iloc[-1]["confirmados"]
        confirmados_novos_value = int(confirmados_value - confirmados_old)
        confirmados_novos.append(confirmados_novos_value)


        """ CONFIMADOS POR FAIXA ETARIA """

        print("Numbers:", get_all_numbers_from_list(lines, "80+", "CARACTERIZAÇÃO DEMOGRÁFICA DOS CASOS CONFIRMADOS"))

        [confirmados_0_9_m_value, confirmados_10_19_m_value, confirmados_20_29_m_value,
         confirmados_30_39_m_value, confirmados_40_49_m_value, confirmados_50_59_m_value,
         confirmados_60_69_m_value, confirmados_70_79_m_value, confirmados_80_plus_m_value,
         confirmados_0_9_f_value, confirmados_10_19_f_value, confirmados_20_29_f_value,
         confirmados_30_39_f_value, confirmados_40_49_f_value, confirmados_50_59_f_value,
         confirmados_60_69_f_value, confirmados_70_79_f_value, confirmados_80_plus_f_value, total, total2,
        ] = get_all_numbers_from_list(lines, "80+", "CARACTERIZAÇÃO DEMOGRÁFICA DOS CASOS CONFIRMADOS")


        confirmados_m_value = sum([confirmados_0_9_m_value, confirmados_10_19_m_value, confirmados_20_29_m_value,
                                     confirmados_30_39_m_value, confirmados_40_49_m_value, confirmados_50_59_m_value,
                                     confirmados_60_69_m_value, confirmados_70_79_m_value, confirmados_80_plus_m_value])

        confirmados_f_value = sum([confirmados_0_9_f_value, confirmados_10_19_f_value, confirmados_20_29_f_value,
                                   confirmados_30_39_f_value, confirmados_40_49_f_value, confirmados_50_59_f_value,
                                   confirmados_60_69_f_value, confirmados_70_79_f_value, confirmados_80_plus_f_value,
                                   ])

        # Append Confirmados Values
        confirmados_f.append(confirmados_f_value)
        confirmados_m.append(confirmados_m_value)
        confirmados_0_9_f.append(confirmados_0_9_f_value)
        confirmados_0_9_m.append(confirmados_0_9_m_value)
        confirmados_10_19_f.append(confirmados_10_19_f_value)
        confirmados_10_19_m.append(confirmados_10_19_m_value)
        confirmados_20_29_f.append(confirmados_20_29_f_value)
        confirmados_20_29_m.append(confirmados_20_29_m_value)
        confirmados_30_39_f.append(confirmados_30_39_f_value)
        confirmados_30_39_m.append(confirmados_30_39_m_value)
        confirmados_40_49_f.append(confirmados_40_49_f_value)
        confirmados_40_49_m.append(confirmados_40_49_m_value)
        confirmados_50_59_f.append(confirmados_50_59_f_value)
        confirmados_50_59_m.append(confirmados_50_59_m_value)
        confirmados_60_69_f.append(confirmados_60_69_f_value)
        confirmados_60_69_m.append(confirmados_60_69_m_value)
        confirmados_70_79_f.append(confirmados_70_79_f_value)
        confirmados_70_79_m.append(confirmados_70_79_m_value)
        confirmados_80_plus_f.append(confirmados_80_plus_f_value)
        confirmados_80_plus_m.append(confirmados_80_plus_m_value)


        """ OBITOS POR FAIXA ETARIA """

        [obitos_0_9_m_value, obitos_10_19_m_value, obitos_20_29_m_value,
         obitos_30_39_m_value, obitos_40_49_m_value, obitos_50_59_m_value,
         obitos_60_69_m_value, obitos_70_79_m_value, obitos_80_plus_m_value, total,
         obitos_0_9_f_value, obitos_10_19_f_value, obitos_20_29_f_value,
         obitos_30_39_f_value, obitos_40_49_f_value, obitos_50_59_f_value,
         obitos_60_69_f_value, obitos_70_79_f_value, obitos_80_plus_f_value, total2,
        ] = get_all_numbers_from_list(lines, "CARACTERIZAÇÃO DOS ÓBITOS OCORRIDOS", "Saiba mais em https://covid19.min-saude.pt/")

        obitos_m_value = sum([obitos_0_9_m_value, obitos_10_19_m_value, obitos_20_29_m_value,
                                     obitos_30_39_m_value, obitos_40_49_m_value, obitos_50_59_m_value,
                                     obitos_60_69_m_value, obitos_70_79_m_value, obitos_80_plus_m_value])

        obitos_f_value = sum([obitos_0_9_f_value, obitos_10_19_f_value, obitos_20_29_f_value,
                                   obitos_30_39_f_value, obitos_40_49_f_value, obitos_50_59_f_value,
                                   obitos_60_69_f_value, obitos_70_79_f_value, obitos_80_plus_f_value,
                                   ])

        # Append Obitos Values
        obitos_f.append(obitos_f_value)
        obitos_m.append(obitos_m_value)
        obitos_0_9_f.append(obitos_0_9_f_value)
        obitos_0_9_m.append(obitos_0_9_m_value)
        obitos_10_19_f.append(obitos_10_19_f_value)
        obitos_10_19_m.append(obitos_10_19_m_value)
        obitos_20_29_f.append(obitos_20_29_f_value)
        obitos_20_29_m.append(obitos_20_29_m_value)
        obitos_30_39_f.append(obitos_30_39_f_value)
        obitos_30_39_m.append(obitos_30_39_m_value)
        obitos_40_49_f.append(obitos_40_49_f_value)
        obitos_40_49_m.append(obitos_40_49_m_value)
        obitos_50_59_f.append(obitos_50_59_f_value)
        obitos_50_59_m.append(obitos_50_59_m_value)
        obitos_60_69_f.append(obitos_60_69_f_value)
        obitos_60_69_m.append(obitos_60_69_m_value)
        obitos_70_79_f.append(obitos_70_79_f_value)
        obitos_70_79_m.append(obitos_70_79_m_value)
        obitos_80_plus_f.append(obitos_80_plus_f_value)
        obitos_80_plus_m.append(obitos_80_plus_m_value)


        """ INTERNADOS """

        [internados_value, internados_uci_value] = get_all_numbers_from_list(lines, "INTERNADOS", "FEBRE")

        internados.append(internados_value)
        internados_uci.append(internados_uci_value)


        """ SINTOMAS """

        # collect all percentages
        percentages = get_all_percentages_from_list(lines)

        sintomas_febre.append(percentages[-6])
        sintomas_tosse.append(percentages[-5])
        sintomas_dificuldade_respiratoria.append(percentages[-4])
        sintomas_cefaleia.append(percentages[-3])
        sintomas_dores_musculares.append(percentages[-2])
        sintomas_fraqueza_generalizada.append(percentages[-1])


        """ TRANSMISSAO IMPORTADA """

        transmissao_importada_value = get_transmissao_importada_value(lines)
        transmissao_importada.append(transmissao_importada_value)


    data = {
        "data": dates,
        "confirmados": confirmados,
        "n_confirmados": n_confirmados,
        "lab": lab,
        "recuperados": recuperados,
        "vigilancia": vigilancia,
        "suspeitos": suspeitos,
        "confirmados_acores": confirmados_acores,
        "confirmados_madeira": confirmados_madeira,
        "confirmados_arsnorte": confirmados_arsnorte,
        "confirmados_arscentro": confirmados_arscentro,
        "confirmados_arslvt": confirmados_arslvt,
        "confirmados_arsalentejo": confirmados_arsalentejo,
        "confirmados_arsalgarve": confirmados_arsalgarve,
        "obitos_arsnorte": obitos_arsnorte,
        "obitos_arscentro": obitos_arscentro,
        "obitos_arslvt": obitos_arslvt,
        "obitos_arsalentejo": obitos_arsalentejo,
        "obitos_arsalgarve": obitos_arsalgarve,
        "obitos_acores": obitos_acores,
        "obitos_madeira": obitos_madeira,
        #"recuperados_arsnorte": recuperados_arsnorte,
        #"recuperados_arscentro": recuperados_arscentro,
        #"recuperados_arslvt": recuperados_arslvt,
        "confirmados_f": confirmados_f,
        "confirmados_m": confirmados_m,
        "confirmados_0_9_f": confirmados_0_9_f,
        "confirmados_0_9_m": confirmados_0_9_m,
        "confirmados_10_19_f": confirmados_10_19_f,
        "confirmados_10_19_m": confirmados_10_19_m,
        "confirmados_20_29_f": confirmados_20_29_f,
        "confirmados_20_29_m": confirmados_20_29_m,
        "confirmados_30_39_f": confirmados_30_39_f,
        "confirmados_30_39_m": confirmados_30_39_m,
        "confirmados_40_49_f": confirmados_40_49_f,
        "confirmados_40_49_m": confirmados_40_49_m,
        "confirmados_50_59_f": confirmados_50_59_f,
        "confirmados_50_59_m": confirmados_50_59_m,
        "confirmados_60_69_f": confirmados_60_69_f,
        "confirmados_60_69_m": confirmados_60_69_m,
        "confirmados_70_79_f": confirmados_70_79_f,
        "confirmados_70_79_m": confirmados_70_79_m,
        "confirmados_80_plus_f": confirmados_80_plus_f,
        "confirmados_80_plus_m": confirmados_80_plus_m,
        "obitos_f": obitos_f,
        "obitos_m": obitos_m,
        "obitos_0_9_f": obitos_0_9_f,
        "obitos_0_9_m": obitos_0_9_m,
        "obitos_10_19_f": obitos_10_19_f,
        "obitos_10_19_m": obitos_10_19_m,
        "obitos_20_29_f": obitos_20_29_f,
        "obitos_20_29_m": obitos_20_29_m,
        "obitos_30_39_f": obitos_30_39_f,
        "obitos_30_39_m": obitos_30_39_m,
        "obitos_40_49_f": obitos_40_49_f,
        "obitos_40_49_m": obitos_40_49_m,
        "obitos_50_59_f": obitos_50_59_f,
        "obitos_50_59_m": obitos_50_59_m,
        "obitos_60_69_f": obitos_60_69_f,
        "obitos_60_69_m": obitos_60_69_m,
        "obitos_70_79_f": obitos_70_79_f,
        "obitos_70_79_m": obitos_70_79_m,
        "obitos_80_plus_f": obitos_80_plus_f,
        "obitos_80_plus_m": obitos_80_plus_m,
        "obitos": obitos,
        "internados": internados,
        "internados_uci": internados_uci,
        "sintomas_tosse": sintomas_tosse,
        "sintomas_febre": sintomas_febre,
        "sintomas_dificuldade_respiratoria": sintomas_dificuldade_respiratoria,
        "sintomas_cefaleia": sintomas_cefaleia,
        "sintomas_dores_musculares": sintomas_dores_musculares,
        "sintomas_fraqueza_generalizada": sintomas_fraqueza_generalizada,
        "transmissao_importada": transmissao_importada,
        "confirmados_novos": confirmados_novos
    }

    df = pd.DataFrame(data)

    return df

def get_all_numbers_from_list(lines, string_bottom, string_upper):
    numbers = []

    index_bottom = lines.index(string_bottom)
    index_upper = lines.index(string_upper)

    for i in range(index_bottom, index_upper):
        line = lines[i]

        if is_int(line):
            numbers.append(int(line))

        if "*" in line:
            line = line.replace("*", "")
            if is_int(line):
                numbers.append(int(line))

    return numbers


def get_all_percentages_from_list(lines):
    percentages = []

    for line in lines:

        if "%" in line:
            line = line.replace("%", "")
            if is_int(line):
                percentages.append(int(line) / 100)

    return percentages


def get_transmissao_importada_value(lines):
    index_bottom = lines.index("CASOS IMPORTADOS")
    index_upper = lines.index("00-09 anos")
    counter = 0

    for i in range(index_bottom, index_upper):
        number = re.findall(r'[0-9]+', lines[i])
        if number:
            counter += int(number[0])

    return counter


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def save_new_data(r, path_to_csv):

    row = [[
        r["data"],
        "{} 00:00".format(r["data"]), # DATA DADOS -> substituir por hora
        r["confirmados"],
        r["confirmados_arsnorte"],
        r["confirmados_arscentro"],
        r["confirmados_arslvt"],
        r["confirmados_arsalentejo"],
        r["confirmados_arsalgarve"],
        r["confirmados_acores"],
        r["confirmados_madeira"],
        "", #r["confirmados_estrangeiro"],
        r["confirmados_novos"],
        r["recuperados"],
        r["obitos"],
        r["internados"],
        r["internados_uci"],
        r["lab"],
        r["suspeitos"],
        r["vigilancia"],
        r["n_confirmados"],
        "", # cadeias transmissao -> vazio
        r["transmissao_importada"],
        r["confirmados_0_9_f"],
        r["confirmados_0_9_m"],
        r["confirmados_10_19_f"],
        r["confirmados_10_19_m"],
        r["confirmados_20_29_f"],
        r["confirmados_20_29_m"],
        r["confirmados_30_39_f"],
        r["confirmados_30_39_m"],
        r["confirmados_40_49_f"],
        r["confirmados_40_49_m"],
        r["confirmados_50_59_f"],
        r["confirmados_50_59_m"],
        r["confirmados_60_69_f"],
        r["confirmados_60_69_m"],
        r["confirmados_70_79_f"],
        r["confirmados_70_79_m"],
        r["confirmados_80_plus_f"],
        r["confirmados_80_plus_m"],
        r["sintomas_tosse"],
        r["sintomas_febre"],
        r["sintomas_dificuldade_respiratoria"],
        r["sintomas_cefaleia"],
        r["sintomas_dores_musculares"],
        r["sintomas_fraqueza_generalizada"],
        r["confirmados_f"],
        r["confirmados_m"],
        r["obitos_arsnorte"],
        r["obitos_arscentro"],
        r["obitos_arslvt"],
        r["obitos_arsalentejo"],
        r["obitos_arsalgarve"],
        r["obitos_acores"],
        r["obitos_madeira"],
        "", #r["obitos_estrangeiro"],
        "", #["recuperados_arsnorte"],
        "", #["recuperados_arscentro"],
        "", #["recuperados_arslvt"],
        "", #r["recuperados_arsalentejo"],
        "", #r["recuperados_arsalgarve"],
        "", #r["recuperados_acores"],
        "", #r["recuperados_madeira"],
        "", #r["recuperados_estrangeiro"],
        r["obitos_0_9_f"],
        r["obitos_0_9_m"],
        r["obitos_10_19_f"],
        r["obitos_10_19_m"],
        r["obitos_20_29_f"],
        r["obitos_20_29_m"],
        r["obitos_30_39_f"],
        r["obitos_30_39_m"],
        r["obitos_40_49_f"],
        r["obitos_40_49_m"],
        r["obitos_50_59_f"],
        r["obitos_50_59_m"],
        r["obitos_60_69_f"],
        r["obitos_60_69_m"],
        r["obitos_70_79_f"],
        r["obitos_70_79_m"],
        r["obitos_80_plus_f"],
        r["obitos_80_plus_m"],
        r["obitos_f"],
        r["obitos_m"]
    ]]

    df = pd.DataFrame(row)

    df.to_csv(path_to_csv, header=False, index=False, mode='a', line_terminator='\n')

def _extract_report_id(r):
    r_file = r[r.rfind('/'):]
    r_id = int(r_file[r_file.rfind('-') + 1:r_file.find('_')])
    return r_id

if __name__ == '__main__':

    # Constants
    PATH_TO_DATA_CSV = str(Path(__file__).resolve().parents[2] / 'data.csv')
    
    # Get the latest report 
    reports_path = reports_folder = Path(__file__).resolve().parents[2] / 'dgs-reports-archive'
    reports_list = [str(f) for f in list(reports_path.iterdir()) if str(f).endswith('.pdf')]
    reports_list.sort(key=_extract_report_id)

    # Run data extraction on the report
    report = get_report(reports_list[-1])
    new_dataframe = extract_data([report], pd.read_csv(PATH_TO_DATA_CSV))
    
    # Save new line into data.csv file
    save_new_data(new_dataframe.iloc[-1], PATH_TO_DATA_CSV)

    # Done
    print("Done!")