#!/bin/sh

printf "Removing old archives ... "
rm -f log/wiki.tar.gz
rm -f log/potter.tar.gz
printf "Done\n"

printf "Creating new archives from models ... "
tar -czf wiki.tar.gz log/wiki
tar -czf potter.tar.gz log/potter
printf "Done\n"

printf "Moving archives to log directory ... "
mv wiki.tar.gz log
mv potter.tar.gz log
printf "Done\n"
