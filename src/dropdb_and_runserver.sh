#! /bin/sh

COMMAND="rm -r data/"
COMMAND2="paster serve --reload development.ini"
echo "   " $COMMAND
$COMMAND
echo "   " $COMMAND2
$COMMAND2
