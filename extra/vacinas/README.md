
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
- `Dataset vacinação (16/02/2021)`
- `Relatório de Vacinação nº 1 (27/12/2020 a 14/02/2021)`
- publicado a `2021-02-16` com data `2021-02-08` a `2021-02-14`
- dados entre 15 e 16

### Relatório 2021-02-22
- `Dataset vacinação (21/02/2021)`
- `Relatório de Vacinação nº 2 (27/12/2020 a 21/02/2021)`
- publicado a `2021-02-24` com data `2021-02-15` a `2021-02-21`
- dados entre 22 e 23

### Relatório 2021-03-01
- `Dataset vacinação (3)`
- `Relatório de Vacinação nº 3 (27/12/2020 a 28/02/2021)`
- publicado a `2021-03-03` com data `2021-02-22` a `2021-02-28`
- dados entre 01 e 02

### Relatório 2021-03-08
- `Dataset vacinação (4)`
- `Relatório de Vacinação nº 4 (27/12/2020 a 07/03/2021)`
- publicado a `2021-03-03` com data `2021-03-01` a `2021-03-07`
- dados entre 07 e 08

### Relatório 2021-03-15
- `Dataset vacinação (5)`
- `Relatório de Vacinação nº 5 (27/12/2020 a 14/03/2021)`
- publicado a `2021-03-17` com data `2021-03-08` a `2021-03-14`
- dados aparentemente entre 15 e 16
- `Relatório dia 14 dose1 = 827 902 dose2 = 341 034`
- `Diário___ dia 15 dose1 = 827 508 dose2 = 340 707`
- `Diário___ dia 16 dose1 = 849 464 dose2 = 343 722`

### Relatório 2021-03-22
- Inclusão das Ilhas
- `Dataset vacinação (6)`
- (1,4M é mais que 1,3M a 23, provavelmente por agora incluir as ilhas)
- RA Açores em `mac-roman` - `iconv -f macroman -t utf8` !
- `Relatório de Vacinação nº 6 (27/12/2020 a 21/03/2021)`
- PDF publicado a `2021-03-24` com data `2021-03-21`
- `Relatório dia 21 dose1 = 942 825 dose2 = 471 204`
- `Diário___ dia 22 dose1 = 903 964 dose2 = 447 552`
- `Diário___ dia 23 dose1 = 914 058 dose2 = 455 184`
- `Diário___ dia 24 dose1 = 934 295 dose2 = 457 256`

### Relatório 2021-03-29
- `Dataset vacinação (7)`
- `"RA Açores"` passou a `"RA_Acores"` para evitar `mac-roman`
- `Relatório de Vacinação nº 7 (27/12/2020 a 28/03/2021)`
- publicado a `2021-03-31` com data `2021-03-28`
- `Relatório dia 28 dose1 = 1 196 971 dose2 = 494 521`
- `Diário___ dia 29 dose1 = 1 148 757 dose2 = 469 642`
- `Diário___ dia 30 dose1 = 1 169 676 dose2 = 472 270`
- `Diário___ dia 31 dose1 = 1 197 027 dose2 = 475 866`

### Relatório 2021-04-05
- `Dataset vacinação (8)`
- `Relatório de Vacinação nº 8 (27/12/2020 a 04/04/2021)`
- publicado a `2021-04-07` com data `2021-04-04`
- `Relatório dia 04 dose1 = 1 334 338 dose2 = 579 069`

### Relatório 2021-04-12
- `Dataset vacinação (9)`
- `Relatório de Vacinação nº 9 (27/12/2020 a 11/04/2021)`
- publicado a `2021-04-14` com data `2021-04-11`

### Relatório 2021-04-19
- `Dataset vacinação (10)`
- `Relatório de Vacinação nº 10 (27/12/2020 a 18/04/2021)`
- publicado a `2021-04-20` com data `2021-04-18`

### Relatório 2021-04-26
- `Dataset vacinação (11)`
- `Relatório de Vacinação nº 11 (27/12/2020 a 25/04/2021)`
- publicado a `2021-04-27` com data `2021-04-25`

### Relatório 2021-05-03
- `Dataset vacinação (12)`
- `Relatório de Vacinação nº 12 (27/12/2020 a 02/05/2021)`
- publicado a `2021-05-04` com data `2021-05-02`

### Relatório 2021-05-10
- `Dataset vacinação (13)`
- `Relatório de Vacinação nº 13 (27/12/2020 a 09/05/2021)`
- publicado a `2021-05-11` com data `2021-05-09`

### Relatório 2021-05-17
- `Dataset vacinação (14)`
- `Relatório de Vacinação nº 14 (27/12/2020 a 16/05/2021)`
- publicado a `2021-05-18` com data `2021-05-16`

### Relatório 2021-05-24
- `Dataset vacinação (15)`
- `Relatório de Vacinação nº 15 (27/12/2020 a 23/05/2021)`
- publicado a `2021-05-25` com data `2021-05-23`

### Relatório 2021-05-31
- `Dataset vacinação (16)`
- `Relatório de Vacinação nº 16 (27/12/2020 a 30/05/2021)`
- publicado a `2021-06-02` com data `2021-05-30`

### Relatório 2021-06-07
- `Dataset vacinação (17)`
- `Relatório de Vacinação nº 17 (27/12/2020 a 06/06/2021)`
- publicado a `2021-06-09` com data `2021-06-06`

### Relatório 2021-06-14
- `Dataset vacinação (18)`
- `Relatório de Vacinação nº 18 (27/12/2020 a 13/06/2021)`
- publicado a `2021-06-16` com data `2021-06-13`

### Relatório 2021-06-21
- `Dataset vacinação (19)`
- `Relatório de Vacinação nº 19 (27/12/2020 a 20/06/2021)`
- publicado a `2021-06-23` com data `2021-06-20`

### Relatório 2021-06-28
- `Dataset vacinação (20)`
- `Relatório de Vacinação nº 19 (27/12/2020 a 27/06/2021)`
- publicado a `2021-06-30` com data `2021-06-27`

### Relatório 2021-07-05
- `Dataset vacinação (21)`
- `Relatório de Vacinação nº 21 (27/12/2020 a 04/07/2021)`
- publicado a `2021-07-07` com data `2021-07-04`
- Relatório mostra que valores diários durante a semana de
  2021-06-28 a 2021-07-04 estão inflacionados, talvez com
  inclusão forçada do histórico de vacinação de ilhas.
  Valores diários de 2021-06-05 parecem semelhantes aos
  valores semanais nacionais, enquanto nas semanas anteriores
  correspondiam apenas ao continente.

### Relatório 2021-07-12
- `Dataset vacinação (22)`
- `Relatório de Vacinação nº 22 (27/12/2020 a 11/07/2021)`
- publicado a `2021-07-14` com data `2021-07-11` (domingo)

### Relatório 2021-07-19
- `Dataset vacinação (23)` EM FALTA
- `Relatório de Vacinação nº 23 (27/12/2020 a 18/07/2021)`
- publicado a `2021-07-21` (quarta) com data `2021-07-18` (domingo)

### Relatório 2021-07-26
- `Dataset vacinação (24)`
- `Relatório de Vacinação nº 24 (27/12/2020 a 25/07/2021)`
- publicado a `2021-07-27` (terça noite) com data `2021-07-25` (domingo)

### Relatório 2021-08-02
- `Dataset vacinação (25)`
- `Relatório de Vacinação nº 25 (27/12/2020 a 01/08/2021)`
- publicado a `2021-08-03` (terça noite) com data `2021-08-01` (domingo)

### Relatório 2021-08-09
- `Dataset vacinação (26)`
- `Relatório de Vacinação nº 26 (27/12/2020 a 08/08/2021)`
- publicado a `2021-08-10` (terça noite) com data `2021-08-08` (domingo)

### Relatório 2021-08-16
- `Dataset vacinação (27)`
- `Relatório de Vacinação nº 27 (27/12/2020 a 15/08/2021)`
- publicado a `2021-08-17` (terça noite) com data `2021-08-15` (domingo)

### Relatório 2021-08-23
- `Dataset vacinação (28)`
- `Relatório de Vacinação nº 28 (27/12/2020 a 22/08/2021)`
- publicado a `2021-08-25` (quarta noite) com data `2021-08-22` (domingo)

### Relatório 2021-08-30
- `Dataset vacinação (29)`
- `Relatório de Vacinação nº 29 (27/12/2020 a 29/08/2021)`
- publicado a `2021-09-01` (quarta noite) com data `2021-08-29` (domingo)

### Relatório 2021-09-06
- `Dataset vacinação (30)`
- `Relatório de Vacinação nº 30 (27/12/2020 a 05/09/2021)`
- publicado a `2021-09-07` (terça noite) com data `2021-09-05` (domingo)

### Relatório 2021-09-13
- `Dataset vacinação (31)`
- `Relatório de Vacinação nº 31 (27/12/2020 a 12/09/2021)`
- publicado a `2021-09-14` (terça noite) com data `2021-09-12` (domingo)

### Relatório 2021-09-20
- `Dataset vacinação (32)`
- `Relatório de Vacinação nº 32 (27/12/2020 a 19/09/2021)`
- publicado a `2021-09-21` (terça noite) com data `2021-09-19` (domingo)

### Relatório 2021-09-27
- `Dataset vacinação (33)`
- `Relatório de Vacinação nº 33 (27/12/2020 a 26/09/2021)`
- publicado a `2021-09-28` (terça noite) com data `2021-09-26` (domingo)

### Relatório 2021-10-04
- `Dataset vacinação (34)`
- `Relatório de Vacinação nº 34 (27/12/2020 a 03/10/2021)`
- publicado a `2021-10-05` (terça noite) com data `2021-10-03` (domingo)

### Relatório 2021-10-11
- `Dataset vacinação (35)`
- `Relatório de Vacinação nº 35 (27/12/2020 a 10/10/2021)`
- publicado a `2021-10-12` (terça noite) com data `2021-10-10` (domingo)

### Relatório 2021-10-18
- `Dataset vacinação (36)`
- `Relatório de Vacinação nº 36 (27/12/2020 a 17/10/2021)`
- publicado a `2021-10-19` (terça noite) com data `2021-10-17` (domingo)

### Relatório 2021-10-25
- `Dataset vacinação (37)`
- `Relatório de Vacinação nº 37 (27/12/2020 a 24/10/2021)`
- publicado a `2021-10-25` (terça noite) com data `2021-10-24` (domingo)

### Relatório 2021-11-01
- `Dataset vacinação (38)`
- `Relatório de Vacinação nº 38 (27/12/2020 a 31/10/2021)`
- publicado a `2021-11-02` (terça noite) com data `2021-10-31` (domingo)
