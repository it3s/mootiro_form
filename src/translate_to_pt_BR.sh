#! /bin/sh

# KLUDGE: We remove the deform-compiled templates because they end in .pt.py
rm -r mootiro_form/fieldtypes/templates/*.pt.py

# Regenerate the .pot file
./setup.py extract_messages

# Update the .po files
./setup.py update_catalog

# Edit the pt_BR file
# sudo apt-get install poedit
echo Running poedit...
poedit mootiro_form/locale/pt_BR/LC_MESSAGES/mootiro_form.po

# Compile the .mo
./setup.py compile_catalog # makes translations available to the app
