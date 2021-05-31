# 😷️🇵🇹 Dados relativos à pandemia COVID-19 em Portugal

📅️ **Última actualização**: 31 de Maio de 2021, 15:18

ℹ️ **Fonte dos dados**: [Direcção Geral de Saúde](https://www.dgs.pt/) - Ministério da Saúde Português, através do _dashboard_ do COVID-19 ([aqui](https://covid19.min-saude.pt/ponto-de-situacao-atual-em-portugal/)) e da base de dados da ESRI Portugal [aqui](https://esriportugal.maps.arcgis.com/home/item.html?id=803d4c90bbb04c03999e65e5ce411cf8#data), desde 03/03/2020.

👁️ **Utilizaste estes dados para análises/plataformas/notícias?**: Deixa-nos detalhes [aqui](https://github.com/dssg-pt/covid19pt-data/discussions/), na categoria 🙌 _Montra de Projectos_.

✉️ **Carta Aberta à Direcção Geral de Saúde:** Escrevemos um relatório em formato de [Carta Aberta](https://docs.google.com/document/d/1Ce_CTcIZhDB2tzBV4jK8SkZYYpNF6wg3JtqaJlOZ43Q/edit) que contém tudo o que aprendemos acerca da estratégia de dados da DGS a respeito do COVID-19. Nesta carta fazemos várias sugestões no sentido de criar uma verdadeira cultura de dados abertos no seio desta organização. Se fazes parte de uma organização que partilha estes valores, a carta pode ser assinada [aqui](https://docs.google.com/forms/d/e/1FAIpQLScgHvFFrtjZG2sYK2NqmzxZDfyo_LabUSaCZdX-hkKdpOb8ZQ/viewform)

# 🤔 Contexto

Embora a comunicação e partilha de dados por parte do Ministério de Saúde Português tenha melhorado consideravelmente ao longo da crise do COVID-19, ainda está longe de ideal (havendo a destacar o exemplo do [repositório da Protecção Civil Italiana no GitHub](https://github.com/pcm-dpc/COVID-19)).

A informação disponibilizada pela Direcção Geral de Saúde (DGS), para além de não ter o nível de granularidade da das autoridades italianas, também não é disponibilizada em formatos abertos e facilmente inspeccionáveis/manipuláveis. Ficam assim dificultadas tarefas de análise, modelação e visualização por parte da comunidade (quer mais informal, quer mais académica/industrial) disposta a colaborar no combate à pandemia com as ferramentas que conhece: as de análise de dados.

❗ O compromisso deste repositório é justamente esse: **todos os dias enquanto esta pandemia durar, o ficheiro `data.csv` será actualizado com a informação mais recente disponibilizada pela Direcção Geral de Saúde**. Esta informação será extraída das fontes de dados da [dashboard](https://github.com/dssg-pt/covid19pt-data/pull/330) assim que disponbilizada (por vezes algumas horas depois do lançamento do relatório).

A estrutura base deste ficheiro, desenhada para fácil manipulação em Excel/Python/R não mudará, podendo a comunidade analítica considerá-lo um alvo imutável (em termos de localização e estrutura) para, por exemplo, alimentar plataformas de visualização/modelação. De notar que, mediante a evolução do formato dos relatórios de situação, poderão ser adicionadas novas colunas, mantendo-se claro a retrocompatibilidade. Fontes adicionais de dados poderão também ser adicionadas.

_Porque tudo começa com bons dados._

# 👁️ Aplicações deste repositório
+ [Como achatar a curva? O que revelam as experiências dos países](https://www.publico.pt/interactivo/coronavirus-como-achatar-curva-que-revelam-experiencias-paises), por Rui Barros e Dinis Correia (Público)
+ [Ainda há Covid-19 amanhã?](https://aquelemiguel.github.io/ainda-ha-covid-19-amanha/), por [Miguel Mano](https://github.com/aquelemiguel)
+ [COVID-19 Portugal Data](https://ruicalheno133.github.io/covid-19-dashboard/), por [Rui Calheno](https://github.com/ruicalheno133)
+ [Resumo COVID-19](https://covid19pt.github.io/covid-19-pt/covid-resumo/), por [Pedro Lima](https://github.com/pvl)
+ [COVID-19 Cases](https://app.powerbi.com/view?r=eyJrIjoiYzcyYTg1ZDYtZjI2Zi00NWNhLWJhYzUtZTM1NjliZjlkOGExIiwidCI6ImIwMzNhNWMyLTFhNGUtNDIwMS1iNGZiLWIwZDkzYjlhMGIxOSIsImMiOjl9), por [@hrmartins](https://github.com/hrmartins)
+ [Novos casos diários do vírus de corona COVID-19 por região](http://lundici.it/covid19-portugal/), por [@giuppo](https://github.com/giuppo)
+ [Dashboard tech4COVID19](https://app.powerbi.com/view?r=eyJrIjoiYTVjOTk1OGEtYWEyZi00NTU4LWJhYmYtZTYwYzVlNzAwNjMyIiwidCI6ImE3NjA2YjE0LWJhY2EtNGZjMS04Nzc3LTkyZDIzNzc2YjIzNiIsImMiOjl9), por [Manuel Banza](https://github.com/ManuelBanza)
+ [COVID-19 Portugal](https://covid19portugal.herokuapp.com/), por [Frederico Pimpão](https://github.com/fredericopimpao)
+ [Estatisticas COVID-19](https://jrab.herokuapp.com/), por [@jrabasilio](https://github.com/jrabasilio)
+ [COVID-19 em Portugal](https://dnunessandro.github.io/covid19/), por [@dnunessandro](https://github.com/dnunessandro)
+ [Measuring Icebergs: Using Different Methods to Estimate the Number of COVID-19 Cases in Portugal and Spain](https://github.com/GCGImdea/coronasurveys/blob/master/reports/2020-03-29-CaseEstimation.pdf), por [CoronaSurveys Research Team](https://coronasurveys.com/)
+ [Covid-19](https://covid-19pt.herokuapp.com/), por [Artur Mendes](https://github.com/mornaistar)
+ [Análise sobre o COVID-19](https://www.analise.pt/covid-19), por [Fabiano Rodrigues](https://github.com/jfabiano)
+ [COVID 19 - Portugal e um olhar sobre o mundo](https://covid19.crossroads.pt/), por [José Correia da Silva](https://github.com/zemanels)
+ [COVID-19 Portugal](https://covid-19-proj.vascosilva.site/), por [Vasco Silva](https://github.com/vascocsilva)
+ [Pandemia COVID-19 em Portugal](https://paulojmoreira.outsystemscloud.com/Covid19PT/), por [Paulo Moreira](https://github.com/moreirapjb)
+ [COVID-19 Time varying reproduction numbers estimation for Portugal](https://perone.github.io/covid19analysis/portugal_r0.html), por [Christian S. Perone](https://github.com/perone)
+ [COVID19 Portugal data](https://covid19.anteropires.com/), por [Antero Pires](https://anteropires.com/)
+ [COVID-19 Portugal Dashboard](https://covid19dashboardpt.herokuapp.com/), por [@dvpinho](https://github.com/dvpinho)
+ [Como está a evoluir a pandemia covid-19 onde vivo?](https://www.publico.pt/interactivo/como-esta-evoluir-pandemia-covid19-onde-vivo#/), por Rui Barros, Dinis Correia e Hélio Carvalho (Público)
+ [COVID-19 Insights](https://insights.cotec.pt/), por [COTEC e Nova IMS](https://insights.cotec.pt/index.php/equipa)
+ [EyeData|COVID-19](https://analytics.socialdatalab.pt/EyeData/EyeData-COVID19.html), por [Agência Lusa](https://www.lusa.pt/) e [Social Data Lab](https://socialdatalab.pt/index.php/pt/)
+ [COVID-19](https://filipeataide.shinyapps.io/COVID19/), por [@filipeataide](https://github.com/filipeataide)
+ [Daily Portuguese COVID-19 Data](https://github.com/CEAUL/Dados_COVID-19_PT), por [@saghirb](https://github.com/saghirb)
+ [Epidemiologia Covid Interativa](https://barometro-covid-19.ensp.unl.pt/epidemiologia-da-covid-19/epidemiologia-covid-interativa/), por [Escola Nacional de Saúde Pública](https://www.ensp.unl.pt/home/)
+ [COVID-19 Rt estimator](https://alfredob.shinyapps.io/estR0/), por [@AlfredoBB](https://github.com/AlfredoBB)
+ E muitas mais [aqui](https://github.com/dssg-pt/covid19pt-data/discussions/categories/montra-de-projectos), no fórum do repositório

# 🧱 Estrutura

O repositório está organizado da seguinte forma:
+ `data.csv`: o Pastel de Nata. Dados extraídos da [dashboard](https://covid19.min-saude.pt/ponto-de-situacao-atual-em-portugal/) e do [relatório diário](https://covid19.min-saude.pt/relatorio-de-situacao/) da DGS.
+ `amostras.csv`: contém dados diários relativos às amostras, extraídos da [dashboard](https://covid19.min-saude.pt/ponto-de-situacao-atual-em-portugal/) da DGS.
+ `vacinas.csv`: contém dados diários relativos à vacinação, extraídos da [dashboard](https://covid19.min-saude.pt/ponto-de-situacao-atual-em-portugal/) da DGS. Nota: estes valores, tal como a dashboard e as imagens publicadas nas redes sociais, correspondem apenas à população residente no continente, excluindo as ilhas. O mesmo se aplica nos [relatórios de vacinação](https://covid19.min-saude.pt/relatorio-de-vacinacao/) até 17-03-2021, com o relatório #6 de 24-03-2021 passando a incluir as ilhas.
+ `vacinas_detalhe.csv`: contém dados detalhados semanais relativos à vacinação, extraídos do [dataset do relatório de vacinação](https://covid19.min-saude.pt/relatorio-de-vacinacao/) da DGS. Nota: até 17-03-2021 incluia apenas população residente no continente, vide nota de `vacinas.csv`. Nota: tal como todos os outros `csv`, a coluna `data` corresponde ao dia seguinte aos dados reportados (7 dias neste caso), enquanto o `Relatório PDF` refere o último dia desses 7 dias, e o `Dataset CSV` refere o primeiro dia desses 7 dias.
+ `data_concelhos.csv`: contém dados acumulados relativos aos confirmados por concelho, extraídos do [dashboard da DGS](https://covid19.min-saude.pt/ponto-de-situacao-atual-em-portugal/) (e por isso sujeito às mesmas limitações relativamente a abrangência e protecção de dados, nomeadamente concelhos com menos de 3 confirmados não são reportados). Esta série de dados tem início a 24-03-2020 e tem cadência diária até 04-07-2020, passando a cadência semanal a 14-07-2020, e terminando a 26-10-2020. Vide os próximos dados para o novo formato.
+ `data_concelhos_14dias.csv` e `data_concelhos_incidencia.csv` contém dados de confirmados do acumulado dos 14 dias anteriores à data do reporte, no primeiro ficheiro, e proporcional a 100k habitantes no segundo ficheiro. Inclui os dados calculados do `data_concelhos.csv` desde que os daddos são semanais, nomeadamente entre 27-07-2020 (correspondendo ao periodo de 13-07-2020 a 26-07-2020) até 26-10-2020, e será actualizado conforme seja disponibilizado pela DGS (semanalmente à segunda-feira).
+ `archive/`: arquivo de todos os relatórios de situação disponibilizados pela DGS, em formato `.pdf`. Os relatórios são disponibilizados diariamente, desde o dia 03-03-2020.
+ `notebooks/`: contém um _notebook_ Python com um exemplo simples de como carregar e visualizar os dados.
+ `extra/`: contém fontes de dados extras que podem ser usadas para complementar as análises dos restantes dados. As descrições dessas fontes de dados encontram-se dentro de um README nessa pasta.

# 📡 API Rest para os dados portugueses e mundiais

Em conjunto com a [VOST Portugal](https://www.vost.pt), desenvolvemos uma API disponível a todos com os dados disponibilizados deste repositório, numa tentativa de dar uma ferramenta mais acessível a todos os que querem analisar os dados. Podem aceder e consultar a documentação aqui: https://covid19-api.vost.pt

> (Versão anterior, desatualizada)
> Autor: Carlos Matos | [Grupo IFT](https://grupoift.pt)

> Dados em versão API com resposta JSON, atualização diária conforme esta base de dados e dados da OMS para o endpoint dos dados mundiais por país. [Acesso via RapidApi](https://rapidapi.com/gitgrupoift/api/covid-19-dados-abertos), com exemplos de requisição e resposta, exemplos de clients e SDK.

# 📔 Dicionário dos dados

Uma explicação do conteúdo em `data.csv`.

📝 _ARS_: Administração Regional de Saúde

| Nome da coluna        | Significado           | Possíveis valores  |
| ------------- |:-------------:| -----:|
| `data` | Data da publicação dos dados | DD-MM-YYYY |
| `data_dados` | Data e hora da recolha dos dados apresentados (quando omitida nos relatórios, assume-se como sendo a data da publicação dos dados). **Geralmente, os dados são reportados até às 24h do dia anterior à `data` (equivalentes às 00h do dia de `data`, sendo este último o formato utilizado).** | DD-MM-YYYY HH:MM|
| `confirmados` | Casos confirmados      | Inteiro >= 0 |
| `confirmados_arsnorte` | Casos confirmados na ARS Norte      | Inteiro >= 0 |
| `confirmados_arscentro` | Casos confirmados na ARS Centro      | Inteiro >= 0 |
| `confirmados_arslvt` | Casos confirmados na ARS Lisboa e Vale do Tejo      | Inteiro >= 0 |
| `confirmados_arsalentejo` | Casos confirmados na ARS Alentejo     | Inteiro >= 0 |
| `confirmados_arsalgarve` | Casos confirmados na ARS Algarve    | Inteiro >= 0 |
| `confirmados_acores` | Casos confirmados na Região Autónoma dos Açores | Inteiro >= 0 |
| `confirmados_madeira` | Casos confirmados na Região Autónoma da Madeira  |  Inteiro >= 0 |
| `confirmados_estrangeiro` | Casos confirmados no estrangeiro | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador. **A partir de 28-03-2020, este indicador deixou de ser reportados e os respectivos casos imputados às ARS/Regiões de origem.** |
| `confirmados_novos` | Número de novos casos confirmados comparativamente ao dia anterior. É uma coluna calculada a partir da diferença nos casos `confirmados` entre dias consecutivos | Inteiro >= 0 |
| `recuperados` | Total de casos recuperados | Inteiro >= 0 |
| `obitos` | Total de óbitos | Inteiro >= 0 |
| `internados` | Número de pacientes COVID-19 internados | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `internados_uci` | Número de pacientes COVID-19 internados em Unidades de Cuidados Intensivos | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `lab` | Número de casos suspeitos a aguardar resultados laboratoriais | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `suspeitos` | Total de casos suspeitos (tendo a [definição sido actualizada](https://www.dgs.pt/directrizes-da-dgs/orientacoes-e-circulares-informativas/orientacao-n-002a2020-de-25012020-atualizada-a-250220201.aspx) a 29/02/2020) desde 01/01/2020  | Inteiro >= 0 |
| `vigilancia` | Número de casos sob vigilância pelas autoridades de saúde | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `n_confirmados` | Número de casos cuja suspeita de infecção não se confirmou | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `cadeias_transmissao` | Número de cadeias de transmissão do SARS-CoV-2 activas | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `transmissao_importada` | Número de casos confirmados com transmissão por via de infectados de outros países | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `confirmados_0_9_f` | Número de casos confirmados do sexo feminino na faixa etária 0-9 anos | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `confirmados_0_9_m` | Número de casos confirmados do sexo masculino na faixa etária 0-9 anos | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `confirmados_10_19_f` | Número de casos confirmados do sexo feminino na faixa etária 10-19 anos | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `confirmados_10_19_m` | Número de casos confirmados do sexo masculino na faixa etária 10-19 anos | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `confirmados_20_29_f` | Número de casos confirmados do sexo feminino na faixa etária 20-29 anos | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `confirmados_20_29_m` | Número de casos confirmados do sexo masculino na faixa etária 20-29 anos | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `confirmados_30_39_f` | Número de casos confirmados do sexo feminino na faixa etária 30-39 anos | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `confirmados_30_39_m` | Número de casos confirmados do sexo masculino na faixa etária 30-39 anos | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `confirmados_40_49_f` | Número de casos confirmados do sexo feminino na faixa etária 40-49 anos | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `confirmados_40_49_m` | Número de casos confirmados do sexo masculino na faixa etária 40-49 anos | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `confirmados_50_59_f` | Número de casos confirmados do sexo feminino na faixa etária 50-59 anos | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `confirmados_50_59_m` | Número de casos confirmados do sexo masculino na faixa etária 50-59 anos | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `confirmados_60_69_f` | Número de casos confirmados do sexo feminino na faixa etária 60-69 anos | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `confirmados_60_69_m` | Número de casos confirmados do sexo masculino na faixa etária 60-69 anos | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `confirmados_70_79_f` | Número de casos confirmados do sexo feminino na faixa etária 70-79 anos | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `confirmados_70_79_m` | Número de casos confirmados do sexo masculino na faixa etária 70-79 anos | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `confirmados_80_plus_f` | Número de casos confirmados do sexo feminino na faixa etária 80+ anos | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `confirmados_80_plus_m` | Número de casos confirmados do sexo masculino na faixa etária 80+ anos | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `sintomas_tosse` | Percentagem de casos infetados que reportaram o sintoma de tosse. Conforme informa a DGS, estes dados são relativos apenas a uma %, não-especificada e variável, dos infectados | fracção entre [0, 1] ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `sintomas_febre` | Percentagem de casos infetados que reportaram o sintoma de febre. Conforme informa a DGS, estes dados são relativos apenas a uma %, não-especificada e variável, dos infectados | fracção entre [0, 1] ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `sintomas_dificuldade_respiratoria` | Percentagem de casos infetados que reportaram o sintoma de dificuldades respiratórias. Conforme informa a DGS, estes dados são relativos apenas a uma %, não-especificada e variável, dos infectados | fracção entre [0, 1] ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `sintomas_cefaleia` | Percentagem de casos infetados que reportaram o sintoma de cefaleias. Conforme informa a DGS, estes dados são relativos apenas a uma %, não-especificada e variável, dos infectados | fracção entre [0, 1] ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `sintomas_dores_musculares` | Percentagem de casos infetados que reportaram o sintoma de dores musculares. Conforme informa a DGS, estes dados são relativos apenas a uma %, não-especificada e variável, dos infectados | fracção entre [0, 1] ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `sintomas_fraqueza_generalizada` | Percentagem de casos infetados que reportaram o sintoma de fraqueza generalizada. Conforme informa a DGS, estes dados são relativos apenas a uma %, não-especificada e variável, dos infectados | fracção entre [0, 1] ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `confirmados_f` | Número total de confirmados do sexo feminino | Inteiro >= 0 ou _vazio_ para os dias em falta |
| `confirmados_m` | Número total de confirmados do sexo masculino | Inteiro >= 0 ou _vazio_ para os dias em falta |
| `obitos_arsnorte` | Total de óbitos na ARS Norte      | Inteiro >= 0 |
| `obitos_arscentro` | Total de óbitos na ARS Centro      | Inteiro >= 0 |
| `obitos_arslvt` | Total de óbitos na ARS Lisboa e Vale do Tejo      | Inteiro >= 0 |
| `obitos_arsalentejo` | Total de óbitos na ARS Alentejo     | Inteiro >= 0 |
| `obitos_arsalgarve` | Total de óbitos na ARS Algarve    | Inteiro >= 0 |
| `obitos_acores` | Total de óbitos na Região Autónoma dos Açores | Inteiro >= 0 |
| `obitos_madeira` | Total de óbitos na Região Autónoma da Madeira  |  Inteiro >= 0 |
| `obitos_estrangeiro` | Total de óbitos no estrangeiro | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador. **A partir de 28-03-2020, este indicador deixou de ser reportados e os respectivos casos imputados às ARS/Regiões de origem.** |
| `recuperados_arsnorte` | Total de pacientes recuperados na ARS Norte      | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `recuperados_arscentro` | Total de pacientes recuperados na ARS Centro      | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `recuperados_arslvt` | Total de pacientes recuperados na ARS Lisboa e Vale do Tejo      | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `recuperados_arsalentejo` | Total de pacientes recuperados na ARS Alentejo | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `recuperados_arsalgarve` | Total de pacientes recuperados na ARS Algarve | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `recuperados_acores` | Total de pacientes recuperados na Região Autónoma dos Açores | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `recuperados_madeira` | Total de pacientes recuperados na Região Autónoma da Madeira  |  Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `recuperados_estrangeiro` | Total de pacientes recuperados no estrangeiro | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador. **A partir de 28-03-2020, este indicador deixou de ser reportados e os respectivos casos imputados às ARS/Regiões de origem.** |
| `obitos_0_9_f` | Número total de óbitos de pacientes do sexo feminino na faixa etária 0-9 anos | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `obitos_0_9_m` | Número total de óbitos de pacientes do sexo masculino na faixa etária 0-9 anos | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `obitos_10_19_f` | Número total de óbitos de pacientes do sexo feminino na faixa etária 10-19 anos | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `obitos_10_19_m` | Número total de óbitos de pacientes do sexo masculino na faixa etária 10-19 anos | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `obitos_20_29_f` | Número total de óbitos de pacientes do sexo feminino na faixa etária 20-29 anos | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `obitos_20_29_m` | Número total de óbitos de pacientes do sexo masculino na faixa etária 20-29 anos | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `obitos_30_39_f` | Número total de óbitos de pacientes do sexo feminino na faixa etária 30-39 anos | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `obitos_30_39_m` | Número total de óbitos de pacientes do sexo masculino na faixa etária 30-39 anos | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `obitos_40_49_f` | Número total de óbitos de pacientes do sexo feminino na faixa etária 40-49 anos | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `obitos_40_49_m` | Número total de óbitos de pacientes do sexo masculino na faixa etária 40-49 anos | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `obitos_50_59_f` | Número total de óbitos de pacientes do sexo feminino na faixa etária 50-59 anos | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `obitos_50_59_m` | Número total de óbitos de pacientes do sexo masculino na faixa etária 50-59 anos | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `obitos_60_69_f` | Número total de óbitos de pacientes do sexo feminino na faixa etária 60-69 anos | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `obitos_60_69_m` | Número total de óbitos de pacientes do sexo masculino na faixa etária 60-69 anos | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `obitos_70_79_f` | Número total de óbitos de pacientes do sexo feminino na faixa etária 70-79 anos | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `obitos_70_79_m` | Número total de óbitos de pacientes do sexo masculino na faixa etária 70-79 anos | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `obitos_80_plus_f` | Número total de óbitos de pacientes do sexo feminino na faixa etária 80+ anos | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `obitos_80_plus_m` | Número total de óbitos de pacientes do sexo masculino na faixa etária 80+ anos | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `obitos_f` | Número total de óbitos de pacientes do sexo feminino | Inteiro >= 0 ou _vazio_ para os dias em falta |
| `obitos_m` | Número total de óbitos de pacientes do sexo masculino | Inteiro >= 0 ou _vazio_ para os dias em falta
| `confirmados_desconhecidos_m` | Número de casos confirmados do sexo masculino com idade desconhecida | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador
| `confirmados_desconhecidos_f` | Número de casos confirmados do sexo masculino com idade desconhecida | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador
| `ativos` | Número de casos ativos | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador
| `internados_enfermaria` | Número de pacientes COVID-19 internados em Enfermaria (não Unidades de Cuidados Intensivos) | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador |
| `confirmados_desconhecidos` | Número de casos confirmados com sexo desconhecido | Inteiro >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador
| `incidencia_nacional` | Número de casos confirmados nos 14 dias anteriores e por 100 mil habitantes, nacional, desde 15-03-2021 | Fração >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador
| `incidencia_continente` | Número de casos confirmados nos 14 dias anteriores e por 100 mil habitantes, continente, excluindo ilhas, desde 15-03-2021 | Fração >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador
| `rt_nacional` | R(t) nacional, desde 15-03-2021 | Fração >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador
| `rt_continente` | R(t) continente, excluindo ilhas, desde 15-03-2021 | Fração >= 0 ou _vazio_ para os dias em que a DGS não reportava este indicador

> Definições exactas de alguns destes termos constam do glossário do [Plano Nacional de Preparação e Resposta à Doença por novo coronavírus (COVID-19)](https://covid19.min-saude.pt/wp-content/uploads/2020/03/Plano-de-Conting%C3%AAncia-Novo-Coronavirus_Covid-19.pdf) (página 65 em diante).
> A 26/03/2020, a soma do número de pacientes recuperados por ARS/Região Autónoma nem sempre é igual ao número total de recuperados. A DGS reportou os dados desta forma, indicando que o diferencial correspondia a "_21 casos recuperados laboratorialmente_" e a "_aguardar mais informação._"

Uma outra métrica com potencial interesse científico, o número de casos com base na data de início de sintomas, é também reportada pela DGS. No entanto, é apenas disponibilizado um gráfico de eixos esparsos, o que pode introduzir erros de aproximação na transcrição e comprometer a factualidade dos dados. Por essa razão, esta informação é propositadamente excluída.

Relativamente ao conteúdo em `amostras.csv`:

| Nome da coluna        | Significado           | Possíveis valores  |
| ------------- |:-------------:| -----:|
| `data` | Data a que se referem os dados | DD-MM-YYYY |
| `amostras` | Número total de amostras processadas | Inteiro >= 0 ou _vazio_ |
| `amostras_novas` | Número diário de novas amostras processadas | Inteiro >= 0 ou _vazio_ |
| `amostras_pcr` | Número total de amostras PCR processadas | Inteiro >= 0 ou _vazio_ |
| `amostras_pcr_novas` | Número diário de novas amostras PCR processadas | Inteiro >= 0 ou _vazio_ |
| `amostras_antigenio` | Número total de amostras Antigénio processadas | Inteiro >= 0 ou _vazio_ |
| `amostras_antigenio_novas` | Número diário de novas amostras Antigénio processadas | Inteiro >= 0 ou _vazio_ |

> Relativamente a estes dados, o [dashboard da DGS](https://covid19.min-saude.pt/ponto-de-situacao-atual-em-portugal/) dá conta de que _"correspondem ao número de amostras processadas para diagnóstico de SARS-CoV-2 em laboratórios públicos e privados desde o dia 1 de março."_ Dizem ainda que _"Os dados diários após 2 de abril de 2020 ainda estão a ser recolhidos, pelo que os valores no gráfico poderão sofrer alterações."_ De facto, há a possibilidade de, a cada dia, dados referentes a dias anteriores serem alterados, provavelmente pelo facto de a informação relativa ao processamento de amostras ser recebida pela DGS com alguns dias de desfasamento.

Relativamente ao conteúdo em `vacinas.csv`:

| Nome da coluna        | Significado           | Possíveis valores  |
| ------------- |:-------------:| -----:|
| `data` | Data a que se referem os dados | DD-MM-YYYY |
| `doses` | Número total de doses de vacinas administradas | Inteiro >= 0 ou _vazio_ |
| `doses_novas` | Número diário de doses de vacinas administradas | Inteiro >= 0 ou _vazio_ |
| `doses1` | Número total de primeiras doses de vacinas administradas | Inteiro >= 0 ou _vazio_ |
| `doses1_novas` | Número diário de primeiras doses de vacinas administradas | Inteiro >= 0 ou _vazio_ |
| `doses2` | Número total de segundas doses de vacinas administradas | Inteiro >= 0 ou _vazio_ |
| `doses2_novas` | Número diário de segundas doses de vacinas administradas | Inteiro >= 0 ou _vazio_ |
| `pessoas_vacinadas_completamente` | Número total de pessoas com vacinação completa - com vacina unidose ou com a segunda dose. Tenderá para o total da população. | Inteiro >= 0 ou _vazio_ |
| `pessoas_vacinadas_completamente_novas` | Número diário de pessoas com vacinaçao completa | Inteiro >= 0 ou _vazio_ |
| `pessoas_vacinadas_parcialmente` | Número total de pessoas com vacinaçao parcial - com apeas a primeira dose de vacinas com duas doses. Tenderá para zero conforme a população receba a segunda dose.  | Inteiro >= 0 ou _vazio_ |
| `pessoas_vacinadas_parcialmente_novas` | Número diário de pessoas com vacinaçao parcial | Inteiro >= 0 ou _vazio_ |

Relativamente ao conteúdo em `vacinas_detalhe.csv`:

| Nome da coluna        | Significado           | Possíveis valores  |
| ------------- |:-------------:| -----:|
| `data` | Data a que se referem os dados | DD-MM-YYYY |
| `recebidas` | Número total de doses de vacinas recebidas | Inteiro >= 0 ou _vazio_ |
| `distribuidas` | Número total de doses de vacinas distribuidas | Inteiro >= 0 ou _vazio_ |
| `[*]` | As colunas seguintes referem-se aos valores para Portugal continental, sem sufixo, e repetindo depois com cada sufixo por idade [0_17, 18_24, 25_49, 50_64, 65_79, 80+, desconhecido], e por ARS [arsnorte, arscentro, arslvt, arsalentejo, arsalgarve, madeira, açores, outro] |
| `doses` | Número total de doses de vacinas administradas | Inteiro >= 0 ou _vazio_ |
| `doses_novas` | Número diário de doses de vacinas administradas | Inteiro >= 0 ou _vazio_ |
| `doses1` | Número total de primeiras doses de vacinas administradas | Inteiro >= 0 ou _vazio_ |
| `doses1_novas` | Número diário de primeiras doses de vacinas administradas | Inteiro >= 0 ou _vazio_ |
| `doses2` | Número total de segundas doses de vacinas administradas | Inteiro >= 0 ou _vazio_ |
| `doses2_novas` | Número diário de segundas doses de vacinas administradas | Inteiro >= 0 ou _vazio_ |
| `dosesunk` | Número total de doses desconhecidas de vacinas administradas | Inteiro >= 0 ou _vazio_ |
| `dosesunk_novas` | Número diário de doses desconhecidas de vacinas administradas | Inteiro >= 0 ou _vazio_ |
| `doses1_perc` | Percentagem de população vacinada com a primeira dose | fracção entre [0, 1] ou _vazio_ |
| `doses2_perc` | Percentagem de população vacinada com a segunda dose | fracção entre [0, 1] ou _vazio_ |
| `populacao1` | População a que se referem os dados (doses1 ÷ doses1_perc), a que deverá corresponder ao respectivo valor de população de acordo com INE/PORDATA 2019 | Inteiro >= 0 ou _vazio_ |
| `populacao2` | População a que se referem os dados (doses2 ÷ doses2_perc), a que deverá corresponder ao respectivo valor de população de acordo com INE/PORDATA 2019 | Inteiro >= 0 ou _vazio_ |

Relativamente ao ficheiro `data_concelhos.csv`:

| Nome da coluna        | Significado           | Possíveis valores  |
| ------------- |:-------------:| -----:|
| `data` | Data a que se referem os dados | DD-MM-YYYY |
| `[nome_concelho]` | Número total de casos acumulados | Inteiro >= 0 ou _vazio_ para os dias em que este indicador não é reportado neste concelho caso seja inferior a 3. |

> Estes dados são extraídos do serviço da [ESRI de ArcGIS](https://services.arcgis.com/CCZiGSEQbAxxFVh3/arcgis/rest/services/COVID19_ConcelhosDiarios/FeatureServer/0/) e podem ter algumas diferenças em relação ao boletim oficial (isto é, concelhos que deixam de aparecer no boletim continuam a aparecer no serviço).
A partir de 31/03, estes casos passaram a ser reportados pelas Administrações Regionais de Saúde e Regiões Autónomas, sendo que qualquer conclusão com base nos dias anteriores deve ser tomada com cuidado.

Relativamente ao ficheiro `rt.csv`:

| Nome da coluna        | Significado           | Possíveis valores  |
| ------------- |:-------------:| -----:|
| `data` | Data a que se referem os dados | DD-MM-YYYY |
| `rt_[região]` | Rt para a respectiva região | Fração >= 0 ou _vazio_ |
| `rt_95_inferior_[região]` | Limite inferior Índice Confiança 95% do Rt para a respectiva região | Fração >= 0 ou _vazio_ |
| `rt_95_superior_[região]` | Limite superior Índice Confiança 95% do Rt para a respectiva região | Fração >= 0 ou _vazio_ |

> Estes dados são extraídos do [Instituto Nacional de Saúde Doutor Ricardo Jorge (INSA)](http://www.insa.min-saude.pt/category/areas-de-atuacao/epidemiologia/covid-19-curva-epidemica-e-parametros-de-transmissibilidade/)

# 💡 Problemas, inconsistências e melhorias

Quaisquer sugestões de dados complementares (provenientes de fontes oficiais), inconsistências nos dados ou melhorias genéricas, à vontade ➡️ _Issues_ ou _Pull Requests_.

# 🌍 Sobre a Data Science for Social Good Portugal

A [Data Science for Social Good Portugal](https://www.dssg.pt) é uma comunidade aberta de cientistas de dados, amantes de dados e entusiastas de dados que querem atacar problemas que importam verdadeiramente. Acreditamos no poder dos dados para transformar a nossa sociedade para o melhor e para todos.

[@dssgPT](https://twitter.com/dssgpt) | [fb.com/DSSGPortugal](https://facebook.com/DSSGPortugal/) | [Instagram @dssg_pt](https://instagram.com/dssg_pt/) | [LinkedIn](https://linkedin.com/company/dssg-portugal)
