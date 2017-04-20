#!/bin/bash
curd=`pwd`;
CERTDIR=`grep CERTDIR caops.conf |cut -d '=' -f2|tr -d "'\""`
echo -n >newcertlist.txt
cd "$CERTDIR"; for i in `ls`; do subj=`openssl x509 -in $i -noout -subject|cut -d '=' -f2-`; echo "$subj:$i"|cut -d ' ' -f2- >>$curd/newcertlist.txt; done; cd ..
