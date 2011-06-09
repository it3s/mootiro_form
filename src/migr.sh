#! /bin/sh

CONNECTION="postgresql+psycopg2://mootiro_form:1234@127.0.0.1:5433/mootiro_form"
PRECIOUS="./mootiro_form/precious/"

case "$1" in
'start')
    echo "migrate version_control CONNECTION PRECIOUS $2"
    migrate version_control $CONNECTION $PRECIOUS $2
;;
'up')
    echo "migrate upgrade CONNECTION PRECIOUS $2"
    migrate upgrade $CONNECTION $PRECIOUS $2
;;
'down')
    echo "migrate downgrade CONNECTION PRECIOUS $2"
    migrate downgrade $CONNECTION $PRECIOUS $2
;;
*)
    echo "You must have the migrate command accessible."
    echo "Possible commands:"
    echo "    migr.sh start <version>"
    echo "    migr.sh up <version>"
    echo "    migr.sh down <version>"
;;
esac

