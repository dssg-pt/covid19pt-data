O dataset disponibilizado nesta pasta é o seguinte:

- [Atividade Prestação SNS 24 para a Síndrome Gripal](https://transparencia.sns.gov.pt/explore/dataset/atividade-prestacao-sns-24-para-a-sindrome-gripal/table/?sort=periodo)

Normalmente, é atualizado diariamente, mas não estão disponíveis dados desde 9 de março de 2020.

# 🧱 Estrutura

A pasta está organizada da seguinte forma
+ `atividade-prestacao-sns-24-para-a-sindrome-gripal-cleaned.csv`: Dataset limpo por nós, com uma única linha por dia, e as restantes métricas calculadas em colunas. 
+ `atividade-prestacao-sns-24-para-a-sindrome-gripal-orig.csv`: Dataset original, fornecido na fonte.
+ `clean_notebook.ipynb`: Código usado para gerar o ficheiro `atividade-prestacao-sns-24-para-a-sindrome-gripal-cleaned.csv`

# 📔 Dicionário dos dados

Uma explicação do conteúdo em `atividade-prestacao-sns-24-para-a-sindrome-gripal-cleaned.csv`. 

📝 _ARS_: Administração Regional de Saúde 

📝 _CSP_: Cuidados de Saúde Primários 

📝 _CIAV_ : Centro de Informação Antivenenos

| Nome da coluna        | Significado           | Possíveis valores  |
| ------------- |:-------------:| -----:|
| `periodo` | Data de medição | Data no formato DD-MM-YYYY |
| `valor_absoluto_encam_CIAV` | Valor absoluto encaminhamentos para CIAV | Inteiro, >= 0 |
| `valor_absoluto_encam_CSP` | Valor absoluto encaminhamentos para CSP | Inteiro, >= 0 |
| `valor_absoluto_encam_INEM` | Valor absoluto encaminhamentos para INEM | Inteiro, >= 0 |
| `valor_absoluto_encam_autocuidados` | Valor absoluto encaminhamentos para Autocuidados | Inteiro, >= 0 |
| `valor_absoluto_encam_outros` | Valor absoluto encaminhamentos para Outros | Inteiro, >= 0 |
| `valor_absoluto_encam_urgencia` | Valor absoluto encaminhamentos para Urgência | Inteiro, >= 0 |
| `taxa_encam_CIAV` | Taxa encaminhamentos para CIAV | Inteiro, >= 0 |
| `taxa_encam_CSP` | Taxa encaminhamentos para CSP | Inteiro, >= 0 |
| `taxa_encam_INEM` | Taxa encaminhamentos para INEM | Inteiro, >= 0 |
| `taxa_encam_autocuidados` | Taxa encaminhamentos para Autocuidados | Inteiro, >= 0 |
| `taxa_encam_outros` | Taxa encaminhamentos para Outros | Inteiro, >= 0 |
| `taxa_encam_urgencia` | Taxa encaminhamentos para Urgência | Inteiro, >= 0 |



