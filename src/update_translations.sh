#! /bin/sh

# 1. Server i18n
echo
./setup.py extract_messages
echo
./setup.py update_catalog
echo
./setup.py compile_catalog

# 2. Client i18n
echo
./translate_js.sh start
echo
./translate_js.sh finish
