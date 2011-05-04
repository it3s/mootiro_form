#! /bin/sh
# http://babel.edgewall.org/wiki/Documentation/0.9/cmdline.html

OUTDIR=mootiro_form/locale
POTFILE=$OUTDIR/js_mf.pot

# Regenerate the .pot file
pybabel extract -F $OUTDIR/js_mapping.conf -k "tr" --omit-header -w 100 --sort-by-file -o $POTFILE mootiro_form/static

# Update the .po files
#pybabel update -D js_mf -i $POTFILE -d $OUTDIR -N

# Edit the pt_BR file
# sudo apt-get install poedit
#echo Running poedit...
#poedit $OUTDIR/en/LC_MESSAGES/js_mf.po

# Compile the .mo
# ./setup.py compile_catalog # makes translations available to the app
