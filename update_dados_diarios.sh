#!/bin/bash

git pull

curl --connect-timeout 3 -gsN 'https://covid19.min-saude.pt/numero-de-novos-casos-e-obitos-por-dia/' | perl -ne 's/http/\nhttp/g;print' | perl -ne '/(http[^"]+\.xls[^"]*)/&&print"$1\n"' | sort -n | uniq | while read a ; do b=${a:0:78};c=$(basename $b); [ -r "dados_diarios/$c.xlsx" ] && continue ; echo $a ;  curl --connect-timeout 3 -o "dados_diarios/$c.xlsx" "$a" ; done 

python3 .github/workflows/update_dados_diarios.py $(ls dados_diarios/*.xls* | sort -n | tail -1)

git add dados_diarios/*.xls*
git add dados_diarios.csv
git add update_dados_diarios.sh
git add .github/workflows/update_dados_diarios.py

if [ "x$(git status | grep -E "modified|new file)")" != "x" ] ; then
	git status
	python3 .github/workflows/update_readme.py 
	git add README*

	git commit -m "dados diarios"
	git push && git push dssg
fi

