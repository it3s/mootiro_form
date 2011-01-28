#! /bin/sh

git pull

# Regenerate the .pot file
# ./setup.py update_catalog
./setup.py extract_messages

# Compile the .mo
./setup.py compile_catalog # makes translations available to the app
