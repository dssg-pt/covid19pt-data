Correr o ficheiro: python3 extract_dataset.py

OR

cd ..
docker build -t python-barcode .
docker run python-barcode

Este programa confirma se os valores extraidos sao iguais aos valores presentes no data.csv (desde 20-03 ate 22-03)
Todos os testes passam com excecao das colunas "confirmados_novos" e "cadeias_transmissao", cuja informacao ja nao dada

Se o formato do ficheiro de mantiver o program gera tambem as linhas do novo csv. Deve-se substituir "FILL" por um valor correto.