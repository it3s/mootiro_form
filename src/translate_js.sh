#! /bin/sh
# http://babel.edgewall.org/wiki/Documentation/0.9/cmdline.html

DOMAIN=js_mf
OUTDIR=mootiro_form/locale
POTFILE=$OUTDIR/$DOMAIN.pot
EN_POFILE=$OUTDIR/en/LC_MESSAGES/$DOMAIN.po
JS_DIR=mootiro_form/static/js/i18n

if [ $1 = 'start' ]; then
    if [ -f $EN_POFILE ]; then
        echo "English javascript PO file found, so updating them."
    else
        echo "Creating the javascript PO files."
        pybabel init -D $DOMAIN -i $POTFILE -d $OUTDIR -l en
        pybabel init -D $DOMAIN -i $POTFILE -d $OUTDIR -l pt_BR
    fi

    # Regenerate the .pot file
    pybabel extract -F $OUTDIR/js_mapping.conf -k "tr" --omit-header -w 100 \
        --sort-by-file -o $POTFILE mootiro_form/static && \
    # Update the .po files
    pybabel update -D $DOMAIN -i $POTFILE -d $OUTDIR -N -l en && \
    pybabel update -D $DOMAIN -i $POTFILE -d $OUTDIR -N -l pt_BR

    echo "\nSuccess: POT and PO files updated. You may now run poedit."
    echo "After that, type this:  $0 finish\n"
elif [ $1 = 'finish' ]; then
    echo "Compiling javascript translations to JSON.\n"
    po2json -D $DOMAIN -d $OUTDIR -o $JS_DIR -n mfTranslations -i
    echo "All javascript translations compiled.\n"
else
    echo "\nCall $0 with either 'start' or 'finish' as an argument."
    echo "Example:  $0 start\n"
    # sudo apt-get install poedit
    #echo Running poedit...
    #poedit $OUTDIR/en/LC_MESSAGES/$DOMAIN.po
fi
