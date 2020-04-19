#!/bin/bash

echo -e "\e[34mEnter the fortigate address (e.g.: 192.168.102.32):\e[0m"
read FGT_ADDRESS
echo -e "\e[34mEnter the username:\e[0m"
read USER_NAME
echo -e "\e[34mEnter the password:\e[0m"
read PASSWORD

SHOULD_DOWNLOAD=yes
SCHEMA_PATH=./fgt_schema.json

if test -f $SCHEMA_PATH; then
    version=`cat fgt_schema.json |grep '^  \"version\"'`
    echo "Existing file found with version:", $version
    echo -n -e "\e[34mReplace the existing file or not [yes/no]?\e[0m"
    read SHOULD_DOWNLOAD
fi

if [ "${SHOULD_DOWNLOAD}" != "yes" ]; then
    echo "Using the existing file."
    exit 0
fi

curl -k -i -X POST https://${FGT_ADDRESS}/logincheck -d "username=${USER_NAME}&secretkey=${PASSWORD}" --dump-header /tmp/headers.txt

curl -k -s --output ${SCHEMA_PATH} -X GET https://${FGT_ADDRESS}/api/v2/cmdb?action=schema -b /tmp/headers.txt

echo "Downloaded schema to ${SCHEMA_PATH}"
