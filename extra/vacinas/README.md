
# Vacinas Continente Diário
- Pasta: `diário`
- Formato: `YYYY-mm-dd_vacinas.json`
- Resultado raw da API no dia correspondente
- Cópia de segurança diária, pois a API não tem dados históricos como por exemplo a API de amostras.


# Vacinas Ilhas
- Pasta: `ilhas`
- Formato: `vacinas_X.csv`
- Dados oficiais das ilhas
- Madeira: https://covidmadeira.pt/vacinacao/
- Açores: https://vacinacao-covid19.azores.gov.pt/
- Açores com dados totais `vacinas_acores.csv` e por ilhas `vacinas_acores_ilhas.csv`


# Vacinas Relatório
- Pasta: `relatório`
- Relatório PDF: `YYYY-mm-dd_Relatório_Vacinação_X.pdf`
- Dataset CSV: `YYYY-mm-dd_Dataset_Vacinação_X.csv`
- Relatório número `X` publicado na data `YYYY-mm-dd`, geralmente quarta-feira.
- PDF refere-se ao domingo anterior como último dia de dados.
- CSV refere-se à segunda-feira da semana anterior, o que corresponde ao primeiro dia de dados dessa semana.
- Dados reais correspondem tipicamente a meio do dia seguinte à data do relatório.
- Fonte: https://covid19.min-saude.pt/relatorio-de-vacinacao/


### Relatório 2021-02-15
- `2021-02-15_Dataset_Vacinação_1.csv`
- `Dataset vacinação (16/02/2021)`
- CSV publicado a `2021-02-16` com data `2021-02-08` e dados aparentemente entre 15 e 16
- `2021-02-15_Relatório_Vacinação_1.pdf`
- `Relatório de Vacinação nº 1 (27/12/2020 a 14/02/2021)`
- PDF publicado a `2021-02-16` com data `2021-02-14` e dados aparentemente entre 15 e 16

### Relatório 2021-02-22
- `2021-02-22_Dataset_Vacinação_2.csv`
- `Dataset vacinação (21/02/2021)`
- CSV publicado a `2021-02-24` com data `2021-02-15` e dados aparentemente entre 22 e 23
- `2021-02-22_Relatório_Vacinação_2.pdf`
- `Relatório de Vacinação nº 2 (27/01/2020 a 21/02/2021)`
- PDF publicado a `2021-02-24` com data `2021-02-21` e dados aparentemente entre 22 e 23

### Relatório 2021-03-01
- `2021-03-01_Dataset_Vacinação_3.csv`
- `Dataset vacinação (3)`
- CSV publicado a `2021-03-03` com data `2021-02-22` e dados aparentemente entre 01 e 02
- `2021-03-01_Relatório_Vacinação_3.pdf`
- `Relatório de Vacinação nº 3 (27/01/2020 a 28/02/2021)`
- PDF publicado a `2021-03-03` com data `2021-02-28` e dados aparentemente entre 01 e 02

### Relatório 2021-03-08
- `2021-03-08_Dataset_Vacinação_4.csv`
- `Dataset vacinação (4)`
- CSV publicado a `2021-03-10` com data `2021-03-01` e dados aparentemente entre 07 e 08
- `2021-03-08_Relatório_Vacinação_4.pdf`
- `Relatório de Vacinação nº 4 (27/01/2020 a 07/03/2021)`
- PDF publicado a `2021-03-03` com data `2021-03-07` e dados aparentemente entre 07 e 08

### Relatório 2021-03-15
- `2021-03-15_Dataset_Vacinação_5.csv`
- `Dataset vacinação (5)`
- CSV publicado a `2021-03-17` com data `2021-03-08` e dados aparentemente entre 15 e 16
- `2021-03-15_Relatório_Vacinação_5.pdf`
- `Relatório de Vacinação nº 5 (27/01/2020 a 14/03/2021)`
- PDF publicado a `2021-03-17` com data `2021-03-14` e dados aparentemente entre 15 e 16
- `Relatório dia 14 dose1 = 827 902 dose2 = 341 034`
- `Diário___ dia 15 dose1 = 827 508 dose2 = 340 707`
- `Diário___ dia 16 dose1 = 849 464 dose2 = 343 722`

### Relatório 2021-03-22
- Inclusão das Ilhas
- `2021-03-22_Dataset_Vacinação_6.csv`
- `Dataset vacinação (6)`
- CSV publicado a `2021-03-24` com data `2021-03-15` e dados desconhecidos
- (1,4M é mais que 1,3M a 23, provavelmente por agora incluir as ilhas)
- RA Açores em `mac-roman` - `iconv -f macroman -t utf8` !
- `2021-03-22_Relatório_Vacinação_6.pdf`
- `Relatório de Vacinação nº 6 (27/01/2020 a 21/03/2021)`
- PDF publicado a `2021-03-24` com data `2021-03-21` e dados desconhecidos
- `Relatório dia 21 dose1 = 942 825 dose2 = 471 204`
- `Diário___ dia 22 dose1 = 903 964 dose2 = 447 552`
- `Diário___ dia 23 dose1 = 914 058 dose2 = 455 184`
- `Diário___ dia 24 dose1 = 934 295 dose2 = 457 256`

### Relatório 2021-03-29
- `2021-03-29_Dataset_Vacinação_7.csv`
- `Dataset vacinação (7)`
- CSV publicado a `2021-03-31` com data `2021-03-22` e dados desconhecidos
- `"RA Açores"` passou a `"RA_Acores"` para evitar `mac-roman`
- `2021-03-29_Relatório_Vacinação_7.pdf`
- `Relatório de Vacinação nº 7 (27/01/2020 a 28/03/2021)`
- PDF publicado a `2021-03-31` com data `2021-03-28` e dados desconhecidos
- `Relatório dia 28 dose1 = 1 196 971 dose2 = 494 521`
- `Diário___ dia 29 dose1 = 1 148 757 dose2 = 469 642`
- `Diário___ dia 30 dose1 = 1 169 676 dose2 = 472 270`
- `Diário___ dia 31 dose1 = 1 197 027 dose2 = 475 866`

### Relatório 2021-04-05
- `2021-04-05_Dataset_Vacinação_8.csv`
- `Dataset vacinação (8)`
- CSV publicado a `2021-04-07` com data `2021-03-29` e dados desconhecidos
- `2021-04-05_Relatório_Vacinação_8.pdf`
- `Relatório de Vacinação nº 8 (27/01/2020 a 04/04/2021)`
- PDF publicado a `2021-04-07` com data `2021-04-04` e dados desconhecidos
- `Relatório dia 04 dose1 = 1 334 338 dose2 = 579 069`

### Relatório 2021-04-12
- `2021-04-12_Dataset_Vacinação_9.csv`
- `Dataset vacinação (9)`
- CSV publicado a `2021-04-14` com data `2021-04-11` e dados desconhecidos
- `2021-04-12_Relatório_Vacinação_9.pdf`
- `Relatório de Vacinação nº 9 (27/01/2020 a 11/04/2021)`
- PDF publicado a `2021-04-14` com data `2021-04-11` e dados desconhecidos

### Relatório 2021-04-19
- `2021-04-19_Dataset_Vacinação_10.csv`
- `Dataset vacinação (10)`
- CSV publicado a `2021-04-20` com data `2021-04-18` e dados desconhecidos
- `2021-04-19_Relatório_Vacinação_10.pdf`
- `Relatório de Vacinação nº 10 (27/01/2020 a 18/04/2021)`
- PDF publicado a `2021-04-20` com data `2021-04-18` e dados desconhecidos

### Relatório 2021-04-26
- `2021-04-26_Dataset_Vacinação_11.csv`
- `Dataset vacinação (11)`
- CSV publicado a `2021-04-27` com data `2021-04-25` e dados desconhecidos
- `2021-04-26_Relatório_Vacinação_11.pdf`
- `Relatório de Vacinação nº 11 (27/01/2020 a 25/04/2021)`
- PDF publicado a `2021-04-27` com data `2021-04-25` e dados desconhecidos

### Relatório 2021-05-03
- `2021-05-03_Dataset_Vacinação_12.csv`
- `Dataset vacinação (12)`
- CSV publicado a `2021-05-04` com data `2021-05-02` e dados desconhecidos
- `2021-05-03_Relatório_Vacinação_12.pdf`
- `Relatório de Vacinação nº 12 (27/01/2020 a 02/05/2021)`
- PDF publicado a `2021-05-04` com data `2021-05-02` e dados desconhecidos

### Relatório 2021-05-10
- `2021-05-10_Dataset_Vacinação_13.csv`
- `Dataset vacinação (13)`
- CSV publicado a `2021-05-11` com data `2021-05-09` e dados desconhecidos
- `2021-05-10_Relatório_Vacinação_13.pdf`
- `Relatório de Vacinação nº 13 (27/01/2020 a 09/05/2021)`
- PDF publicado a `2021-05-11` com data `2021-05-09` e dados desconhecidos

### Relatório 2021-05-17
- `2021-05-17_Dataset_Vacinação_14.csv`
- `Dataset vacinação (14)`
- CSV publicado a `2021-05-18` com data `2021-05-16` e dados desconhecidos
- `2021-05-17_Relatório_Vacinação_14.pdf`
- `Relatório de Vacinação nº 14 (27/01/2020 a 16/05/2021)`
- PDF publicado a `2021-05-18` com data `2021-05-16` e dados desconhecidos

### Relatório 2021-05-24
- `2021-05-24_Dataset_Vacinação_15.csv`
- `Dataset vacinação (15)`
- CSV publicado a `2021-05-25` com data `2021-05-23` e dados desconhecidos
- `2021-05-24_Relatório_Vacinação_15.pdf`
- `Relatório de Vacinação nº 15 (27/01/2020 a 23/05/2021)`
- PDF publicado a `2021-05-25` com data `2021-05-23` e dados desconhecidos
