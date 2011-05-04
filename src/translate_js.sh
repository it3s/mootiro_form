#! /bin/sh
# http://babel.edgewall.org/wiki/Documentation/0.9/cmdline.html

DOMAIN=js_mf
OUTDIR=mootiro_form/locale
POTFILE=$OUTDIR/$DOMAIN.pot

# This creates the catalogues, based on the POTFILE -- but this should run only once:
# pybabel init -D $DOMAIN -i $POTFILE -d $OUTDIR -l en
# pybabel init -D $DOMAIN -i $POTFILE -d $OUTDIR -l pt_BR

# Regenerate the .pot file
pybabel extract -F $OUTDIR/js_mapping.conf -k "tr" --omit-header -w 100 \
    --sort-by-file -o $POTFILE mootiro_form/static && \
# Update the .po files
pybabel update -D $DOMAIN -i $POTFILE -d $OUTDIR -N -l en && \
pybabel update -D $DOMAIN -i $POTFILE -d $OUTDIR -N -l pt_BR

# Edit the pt_BR file
# sudo apt-get install poedit
#echo Running poedit...
#poedit $OUTDIR/en/LC_MESSAGES/$DOMAIN.po

# TODO: Compile to JSON
