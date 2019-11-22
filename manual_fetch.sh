#!/bin/bash

echo -n "Enter Your ACCESS_TOKEN: "
read -s access_token
read -e -p "Enter Your DB_PATH: " db_path
read -e -p "Enter Your REPORT_PATH: " report_path
read -e -p "Download database from Dropbox? (y/N): " download
read -e -p "Upload database from Dropbox? (y/N): " upload
read -e -p "Fetch start index: " si
read -e -p "Fetch max index: " mi
echo ""

#ACCESS_TOKEN
if [ -z $access_token ]
then
    echo "Require ACCESS_TOKEN"
    exit 1
else
    export ACCESS_TOKEN=$access_token
fi

#DB_PATH
if [ -z $db_path ]
then
    echo "Require DB_PATH"
    exit 1
else
    export DB_PATH=$db_path
fi

# REPORT_PATH
if [ -z $report_path ]
then
    echo "Require REPORT_PATH"
    exit 1
else
    export REPORT_PATH=$report_path
fi

# exist prarxivate
if [ ! -d ./prarxivate ]
then 
    echo "Clone prarxivate"
    git clone https://github.com/GzuPark/prarxivate.git
    cp automation.py prarxivate/automation.py
fi

cd prarxivate

# download db
if [[ $download == "y" || $download == "Y" ]]
then
    echo "Download database from Dropbox"
    python -c 'from automation import download_db; download_db();'
elif [ ! -f "./data/db.p" ]
then
    echo "Download database from Dropbox"
    python -c 'from automation import download_db; download_db();'
fi

# fetch
python fetch_papers.py -si $si -mi $mi -sq cat:cs.CV+OR+cat:cs.RO+OR+cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.CL+OR+cat:cs.NE+OR+cat:stat.ML

# upload db
if [[ $upload == "y" || $upload == "Y" ]]
then
    echo "Upload database from Dropbox"
    python -c 'from automation import upload_db; upload_db();'
fi
