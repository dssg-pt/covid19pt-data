# Extracção de número de casos confirmados por concelho

A partir de 24 Março de 2020, a DGS passou a disponibilizar o número de casos confirmados por concelho.
O script `extract_concelhos.py` extrai estes dados em batch dos relatórios existentes, uniformiza o nome dos concelhos usando códigos distrito e códigos de município e exporta os resultados em formato .csv

O script re-analiza todos os relatórios disponívies em _dgs-reports-archive_ e cria o ficheiro `casos_concelho.csv` com casos confirmados por concelho desde o dia 24 Março 2020.

## Execução

Para a execução do script pode ser usado o conda environment definido em `requirements.yml`, p.ex.:

```bash
conda env create -f requirements.yml
conda activate covid_concelhos
python extract_concelhos.py
```

Se algum relatorio futuro referir o nome de um concelhos que nao esteja na lista DICO ou nos sinónimos, o relatório nao será salvo. Uma correspondência com o nome correcto terá de ser adicionada ao ficheiro _fix_names.yml_

## Notas

- Os nomes dos concelhos são normalizados usando os sinónimos em `fix_names.yml` (com estrutura nome oficial: variantes encontradas nos relatórios)
- A fonte dos nomes oficiais, códigos de concelho e distrito (DICO) foram recolhidos de https://github.com/centraldedados/codigos_postais
- Alguns relatórios do fim de Março têm um formato estranho e não são lidos.
- Os Relatórios de Situação da DGS fornecem algumas notas metodológicas potencialmente relevantes:
    - Em cada dia a informação corresponde a cerca de 80% do total de casos confirmados
    - Quando os casos confirmados são inferiores a 3, os dados nao sao apresentados por motivos de confidencialidade
    - Até ao dia 30 Março dados para alguns concelhos foram fornecidos pelas ARS






