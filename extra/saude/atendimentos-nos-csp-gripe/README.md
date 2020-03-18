O dataset disponibilizado nesta pasta é o seguinte:

- [Atividade do Síndrome Gripal nos Cuidados de Saúde Primários](https://transparencia.sns.gov.pt/explore/dataset/atendimentos-nos-csp-gripe/export/?disjunctive.ars&sort=dia)

Normalmente, é atualizado diariamente, mas não estão disponíveis dados desde 9 de março de 2020.

# 🧱 Estrutura

A pasta está organizada da seguinte forma
+ `atendimento-nos-csp-gripe-cleaned.csv`: Dataset limpo por nós, com uma única linha por dia, e as restantes métricas calculadas em colunas. 
+ `atendimento-nos-csp-gripe.csv`: Dataset original, fornecido na fonte.
+ `clean_notebook.ipynb`: Código usado para gerar o ficheiro `atendimento-nos-csp-gripe-cleaned.csv`

# 📔 Dicionário dos dados

Uma explicação do conteúdo em `atendimento-nos-csp-gripe-cleaned.csv`. 

📝 _ARS_: Administração Regional de Saúde 

📝 _CSP_: Cuidados de Saúde Primários

| Nome da coluna        | Significado           | Possíveis valores  |
| ------------- |:-------------:| -----:|
| `periodo` | Data de medição | Data no formato DD-MM-YYYY |
| `ARS` | Data de medição | String |
| `n_cons_csp` | Nº Consultas nos CSP | Inteiro, >= 0 |
| `n_cons_csp_np` | Nº Consultas CSP (Não Programadas) | Inteiro, >= 0 |
| `n_cons_csp_p` | Nº Consultas CSP (Programadas) | Inteiro, >= 0 |
| `n_cons_csp_gripe` | Nº Consultas Gripe nos CSP | Inteiro, >= 0 |

