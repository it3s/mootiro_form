#! /bin/sh
echo "    You may call this script with -v for verbose output."
echo "    ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨\n"
PYTHONWARNINGS=
# http://docs.python.org/library/unittest.html#test-discovery
python -m unittest discover -s mootiro_form/tests $*
