#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR

source db.secrets
QUERY='SELECT * FROM trueMatches WHERE trueMatches.paidApp IS NOT NULL'
mysql --skip-column-names --host=$HOST --user=$USER --password="$PASSWORD" $DB --execute="$QUERY" 2> /dev/null | tr '\t' ','
