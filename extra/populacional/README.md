
## 🧑 Populacional

- [Densidade populacional](https://www.pordata.pt/Municipios/Densidade+populacional-452)
- [População residente](https://www.pordata.pt/Municipios/População+residente++estimativas+a+31+de+Dezembro-120)
- [Índice de dependência de idosos](https://www.pordata.pt/Municipios/%C3%8Dndice+de+depend%C3%AAncia+de+idosos-461)

São fornecidos os ficheiros acima, para 2019, e versão simplificadas em CSV, contendo as contagens para as regiões NUTS II e para Concelhos, usadas pela DGS para reportar os casos.

### Densidade populacional
- *Onde há mais e menos pessoas, em média, por km2?*
- 2019
- https://www.pordata.pt/Municipios/Densidade+populacional-452


### População residente, estimativas a 31 de Dezembro
- *Onde há mais e menos pessoas no final de cada ano?*
- 2019
- https://www.pordata.pt/Municipios/População+residente++estimativas+a+31+de+Dezembro-120

### Índice de dependência de idosos
- *Onde há mais e menos idosos por 100 pessoas em idade activa?*
- 2019
- https://www.pordata.pt/Municipios/Índice+de+dependência+de+idosos-461


### CSV Conversion

Download the xsls files, open in some app that can read them, and export as CSV.

The relevant sheet is the "Quadros", which contains the needed data, plus some headers and footers

Note: be careful with the "Í" accent - it may be a single character (I acute) or may be two characters (I plus acute modifier) 

If CSV is exported with commas as decimal separator and semicolons as columns separator (e.g. in Portugal), run:
```
for i in PORDATA_Densidade-populacional PORDATA_Estimativas-a-31-12 PORDATA_Índice-de-dependência-de-idosos ; do
  perl -p -i -e 's/,/./g;s/;/,/g;' "$i.csv"
done
```

Keep only the rows for the header ("Âmbito…"), "NUTS" and "Município", and only the first 4 columns:
```
for i in PORDATA_Densidade-populacional PORDATA_Estimativas-a-31-12 PORDATA_Índice-de-dependência-de-idosos ; do
  # remove headers and footers and extra columns
  cat "${i}.csv" | grep -E "^(.*mbito|NUTS|Munic)" | cut -d, -f1-4 > foo ; mv foo "${i}.csv"
done
```

Split the full CSV into the "simplificado" with the NUTS II entries, and the "concelhos" with the "municípios".
This also renames some "concelhos" to be aligned with the "data_concelhos.csv" names.
```
for i in PORDATA_Densidade-populacional PORDATA_Estimativas-a-31-12 PORDATA_Índice-de-dependência-de-idosos ; do
  cat "${i}.csv" | grep -E "^(.*mbito|NUTS II,)" \
    | perl -lne '/^([^,]+?,[^,]+?),(.+)$/; ($m,$v)=($1,$2); $v=~s/[^0-9,.]//g; print "$m,$v"' \
    | sort > "${i}_simplificado.csv"
  cat "${i}.csv" | grep -E "^(.*mbito|Munic.*?)" \
    | perl -lne '/^([^,]+?,[^,]+?),(.+)$/; ($m,$v)=($1,$2); $v=~s/[^0-9,.]//g; print "$m,$v"' \
    | perl -lne 's/,Lagoa,/,Lagoa (Faro),/; s/,Lagoa \[R.A.A.],/,Lagoa,/; s/,Calheta \[R.A.A.],/,Calheta (Açores),/; s/,Calheta \[R.A.M.],/,Calheta,/;print' \
    | sort > "${i}_concelhos.csv"
done
```


This is a quick check to ensure all concelhos are an exact match with data_concelhos.csv, with none more and none less than the other file. At the end the 'foo' file must be empty:
```
# create a 'foo' without the header
cat PORDATA_Estimativas-a-31-12_concelhos.csv \
  | grep -v ",Anos," > foo
# for each column on the data_concelhos.csv, except "data", look for it on the 'foo' file. If missing, say FAIL. If present, take it out of the file.
cat ../../data_concelhos.csv | head -1 | perl -lne 's/,/\n/g;print' | grep -v data | while read a ; do grep -q -i ",$a," foo || echo "FAIL $a" ; cat foo | grep -v -i ",$a," > foo2 ; mv foo2 foo ; done
ls -la foo
```
