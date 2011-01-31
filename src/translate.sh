#! /bin/sh

# Regenerate the .pot file
# ./setup.py update_catalog
./setup.py extract_messages

# Edit the pt_BR file
# sudo apt-get install poedit
echo Running poedit...
poedit mootiro_form/locale/pt_BR/LC_MESSAGES/mootiro_form.po

# Compile the .mo
./setup.py compile_catalog # makes translations available to the app