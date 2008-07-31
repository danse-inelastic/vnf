#!/usr/bin/env sh

cgi='/usr/lib/cgi-bin'

cp -r ../html/* /var/www/apache2-default

cp -r ../content $cgi
cp -r ../config $cgi
cp -r ../sampleassemblies $cgi
cp -r ../cgi $cgi

#cp ../cgi/main.py $cgi
#cp ../cgi/main.sh $cgi
#cp ../cgi/dottools $cgi
