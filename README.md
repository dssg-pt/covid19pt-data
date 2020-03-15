# 😷️🇵🇹 Dados relativos à pandemia COVID-19 em Portugal 

📅️ **Última actualização**: 14 de Março de 2020, 12h

ℹ️ **Fonte dos dados**: [Direcção Geral de Saúde](https://www.dgs.pt/) - Ministério da Saúde Português, através do _dashboard_ do COVID-19 ([aqui](https://covid19.min-saude.pt/ponto-de-situacao-atual-em-portugal/)  e dos [relatórios de situação publicados diariamente](https://covid19.min-saude.pt/relatorio-de-situacao/) desde 03/03/2020.

# 🤔 Contexto

Embora a comunicação e partilha de dados por parte do Ministério de Saúde Português tenha melhorado consideravelmente ao longo da crise do COVID-19, ainda está longe de ideal (havendo a destacar o exemplo do [repositório da Protecção Civil Italiana no GitHub](https://github.com/pcm-dpc/COVID-19)).

A informação disponibilizada pela Direcção Geral de Saúde (DGS), para além de não ter o nível de granularidade da das autoridades italianas, também não é disponibilizada em formatos abertos e facilmente inspeccionáveis/manipuláveis. Ficam assim dificultadas tarefas de análise, modelação e visualização por parte da comunidade (quer mais informal, quer mais académica/industrial) disposta a colaborar no combate à pandemia com as ferramentas que conhece: as de análise de dados.

❗ O compromisso deste repositório é justamente esse: **todos os dias enquanto esta pandemia durar, o ficheiro `data.csv` será actualizado com a informação mais recente disponibilizada pela Direcção Geral de Saúde**. Esta informação será extraída do relatório de situação o mais rapidamente possível após a sua disponibilização (que costuma ser ~12h00 GMT+00:00). 

A estrutura base deste ficheiro, desenhada para fácil manipulação em Excel/Python/R não mudará, podendo a comunidade analítica considerá-lo um alvo imutável (em termos de localização e estrutura) para, por exemplo, alimentar plataformas de visualização/modelação. De notar que, mediante a evolução do formato dos relatórios de situação, poderão ser adicionadas novas colunas, mantendo-se claro a retrocompatibilidade.

_Porque tudo começa com bons dados._

# 🧱 Estrutura

O repositório está organizado da seguinte forma:
+ `data.csv`: o Pastel de Nata. 
+ `archive/`: arquivo de todos os relatórios de situação disponibilizados pela DGS, em formato `.pdf`. Os relatórios são disponibilizados diariamente, desde o dia 03-03-2020.
+ `notebooks/`: contém um pequeno _notebook_ Python com um pequeno exemplo de como abrir, interagir e navegar pelos dados. **A análise aí efectuada tem zero valor científico/clínico**.

# 📔 Dicionário dos dados

Uma explicação do conteúdo em `data.csv`. 

📝 _ARS_: Administração Regional de Saúde 

| Nome da coluna        | Significado           | Possíveis valores  |
| ------------- |:-------------:| -----:|
| `data` | Data de publicação dos dados (nem sempre os dados reflectem a realidade desse dia, podendo nalguns casos estar desfasados) | Data no formato DD-MM-YYYY |
| `confirmados` | Casos confirmados      | Inteiro >= 0 |
| `confirmados_arsnorte` | Casos confirmados na ARS Norte      | Inteiro >= 0 |
| `confirmados_arscentro` | Casos confirmados na ARS Centro      | Inteiro >= 0 |
| `confirmados_arslvt` | Casos confirmados na ARS Lisboa e Vale do Tejo      | Inteiro >= 0 |
| `confirmados_alentejo` | Casos confirmados na ARS Alentejo     | Inteiro >= 0 |
| `confirmados_arsalgarve` | Casos confirmados na ARS Algarve    | Inteiro >= 0 |
| `confirmados_acores` | Casos confirmados na Região Autónoma dos Açores | Inteiro >= 0 |
| `confirmados_madeira` | Casos confirmados na Região Autónoma da Madeira  |  Inteiro >= 0 |
| `confirmados_estrangeiro` | Casos confirmados no estrangeiro | Inteiro >= 0 ou `NaN` para os dias em que a DGS não reportava este indicador |
| `confirmados_novos` | Total de novos casos confirmados comparativamente ao dia anterior | Inteiro >= 0 |
| `recuperados` | Total de casos recuperados | Inteiro >= 0 |
| `obitos` | Total de óbitos | Inteiro >= 0 |
| `internados` | Total de pacientes COVID-19 internados | Inteiro >= 0 ou `NaN` para os dias em que a DGS não reportava este indicador |
| `internados_uci` | Pacientes COVID-19 internados em Unidades de Cuidado Intensivos | Inteiro >= 0 ou `NaN` para os dias em que a DGS não reportava este indicador |
| `lab` | Total de casos suspeitos a aguardar resultados laboratoriais | Inteiro >= 0 ou `NaN` para os dias em que a DGS não reportava este indicador |
| `suspeitos` | Total de casos suspeitos (tendo a [definição sido actualizada](https://www.dgs.pt/directrizes-da-dgs/orientacoes-e-circulares-informativas/orientacao-n-002a2020-de-25012020-atualizada-a-250220201.aspx) a 29/03/2020)   | Inteiro >= 0 |
| `vigilancia` | Total de casos sob vigilância pelas autoridades de saúde | Inteiro >= 0 ou `NaN` para os dias em que a DGS não reportava este indicador |
| `cadeias_transmissao` | Número de cadeias de transmissão do SARS-CoV-2 activas | Inteiro >= 0 ou `NaN` para os dias em que a DGS não reportava este indicador |
| `transmissao_importada` | Número de casos confirmados com transmissão por via de infectados de outros países | Inteiro >= 0 ou `NaN` para os dias em que a DGS não reportava este indicador |
| `transmissao_comunitaria` | Número de casos confirmados com transmissão por via da respectiva comunidade local | Inteiro >= 0 ou `NaN` para os dias em que a DGS não reportava este indicador |

Relativamente à coluna `data`, esta corresponde à data em que a DGS disponibilizou esta informação, que nem sempre corresponde à data de recolha. A partir de 03-03-2020, é possível verificar nalguns relatórios de situação (disponíveis na pasta `archive/`) a data efectiva de recolha da informação apresentada. 

Nos seus relatórios de situação, a DGS reporta alguma informação epidemiológica extra, como género e grupo etário dos infectados, que poderá vir a ser adicionada caso haja interesse para tal. 

Uma outra métrica com potencial interesse científico, o número de casos com base na data de início de sintomas, é também reportada pela DGS. No entanto, é apenas disponibilizado um gráfico de eixos esparsos, o que pode introduzir erros de aproximação na transcrição e comprometer a factualidade dos dados. Por essa razão, esta informação é propositadamente excluída. 

# 💡 Problemas, inconsistências e melhorias

Quaisquer sugestões de dados complementares (provindos de fontes oficiais), inconsistências nos dados ou melhorias, à vontade ➡️ _Issues_ ou _Pull Requests_.
