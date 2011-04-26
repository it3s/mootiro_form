#! /bin/sh
echo
./setup.py extract_messages
echo
./setup.py update_catalog
echo
./setup.py compile_catalog
