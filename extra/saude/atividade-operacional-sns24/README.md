O dataset disponibilizado nesta pasta é o seguinte:

- [Atividade Operacional SNS24](https://transparencia.sns.gov.pt/explore/dataset/atividade-operacional-sns-24/table/?sort=periodo)

Normalmente, é atualizado diariamente, mas não estão disponíveis dados desde 9 de março de 2020.

# 🧱 Estrutura

A pasta está organizada da seguinte forma
+ `atividade-operacional-sns-24-cleaned.csv`: Dataset limpo por nós, com uma única linha por dia, e as restantes métricas calculadas em colunas. 
+ `atividade-operacional-sns-24-orig.csv`: Dataset original, fornecido na fonte.
+ `clean_notebook.ipynb`: Código usado para gerar o ficheiro `atividade-operacional-sns-24-cleaned.csv`

# 📔 Dicionário dos dados

Uma explicação do conteúdo em `atendimento-nos-csp-gripe-cleaned.csv`. 

📝 _ARS_: Administração Regional de Saúde 

📝 _CSP_: Cuidados de Saúde Primários

| Nome da coluna        | Significado           | Possíveis valores  |
| ------------- |:-------------:| -----:|
| `periodo` | Data de medição | Data no formato DD-MM-YYYY |
| `valor_absoluto_ch_aband_apos_15s` | Valor absoluto das chamadas abandonadas após 15 segundos | Inteiro, >= 0 |
| `valor_absoluto_ch_aband_até_15s` | Valor absoluto das chamadas abandonadas até 15 segundos | Inteiro, >= 0 |
| `valor_absoluto_ch_atendidas` | Valor absoluto das chamadas atendidas | Inteiro, >= 0 |
| `valor_absoluto_ch_oferecidas` | Valor absoluto das chamadas oferecidas | Inteiro, >= 0 |
| `valor_absoluto_ch_seguimento` | Valor absoluto das chamadas de seguimento | Inteiro, >= 0 |
| `taxa_ch_aband_apos_15s` | Taxa das chamadas abandonadas após 15 segundos | Inteiro, >= 0 |
| `taxa_ch_aband_ate_15s` | Taxa das chamadas abandonadas até 15 segundos | Inteiro, >= 0 |
| `taxa_ch_atendidas` | Taxa das chamadas atendidas | Inteiro, >= 0 |
| `taxa_ch_oferecidas` | Taxa das chamadas atendidas | Inteiro, >= 0 |
| `taxa_ch_seguimento` | Taxa das chamadas de seguimento | Inteiro, >= 0 
