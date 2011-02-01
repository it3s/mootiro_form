#! /bin/sh

git pull
echo === Press Enter to translate...
read -r USER_INPUT
echo $USER_INPUT

# Regenerate the .pot file
# ./setup.py update_catalog
./setup.py extract_messages

# Compile the .mo
./setup.py compile_catalog # makes translations available to the app
