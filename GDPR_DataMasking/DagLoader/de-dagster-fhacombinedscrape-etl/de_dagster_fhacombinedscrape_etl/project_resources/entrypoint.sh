#!/bin/bash
declare -r KERBEROS_KEYTAB_FILE=${KERBEROS_KEYTAB_FILE:-/tmp/krb5.keytab}
declare -r REFRESH_PERIOD_SECONDS=${REFRESH_PERIOD_SECONDS:-3600}



printf "%b" "addent -password -p $SVC_ACCT_USERNAME -k 1 -e aes256-cts\n`echo $SVC_ACCT_PASSWORD`\nwrite_kt $KERBEROS_KEYTAB_FILE\nexit\n" | ktutil

touch $KERBEROS_CACHE_FILE




kinit $SVC_ACCT_USERNAME -k -t $KERBEROS_KEYTAB_FILE
chmod 666 $KERBEROS_CACHE_FILE
klist

exit 0