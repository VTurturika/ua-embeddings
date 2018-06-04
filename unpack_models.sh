#!/bin/sh

printf "Clearing log folders ... "
rm -rf log/wiki/
rm -rf log/potter/
printf "Done\n"

printf "Extract models from archives ... "
tar -xzf log/wiki.tar.gz
tar -xzf log/potter.tar.gz
printf "Done\n"