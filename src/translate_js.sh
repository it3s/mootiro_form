#! /bin/sh
# http://babel.edgewall.org/wiki/Documentation/0.9/cmdline.html

DOMAIN=js_mf
OUTDIR=mootiro_form/locale
POTFILE=$OUTDIR/$DOMAIN.pot
EN_POFILE=$OUTDIR/en/LC_MESSAGES/$DOMAIN.po
JS_DIR=mootiro_form/static/js/i18n


if [ $1 = 'start' ]; then
    # Regenerate the .pot file
    pybabel extract -F $OUTDIR/js_mapping.conf -k "tr" --omit-header -w 100 \
        --sort-by-file -o $POTFILE mootiro_form/static
    if [ $? -ne 0 ]; then
        echo ERROR
        exit 1
    fi

    if [ -f $EN_POFILE ]; then
        echo "\nEnglish javascript PO file found, so updating them.\n"
        pybabel update -D $DOMAIN -i $POTFILE -d $OUTDIR -N -l en && \
        pybabel update -D $DOMAIN -i $POTFILE -d $OUTDIR -N -l pt_BR
    else
        echo "\nCreating the javascript PO files. This might erase existing "
        echo "translations, if any. Press CTRL-C to cancel or ENTER to proceed"
        read anenter
        pybabel init -D $DOMAIN -i $POTFILE -d $OUTDIR -l en && \
        pybabel init -D $DOMAIN -i $POTFILE -d $OUTDIR -l pt_BR
    fi

    echo "\nSuccess: POT and PO files updated. You may now run poedit."
    echo "After that, type this:  $0 finish\n"

elif [ $1 = 'finish' ]; then
    echo "Compiling javascript translations to JSON.\n"
    po2json -D $DOMAIN -d $OUTDIR -o $JS_DIR -n mfTranslations -i
    if [ $? = 0 ]; then
        echo "All javascript translations compiled.\n"
    else
        echo ERROR
        exit 1
    fi
else
    echo "\nCall $0 with either 'start' or 'finish' as an argument."
    echo "Example:  $0 start\n"
    # sudo apt-get install poedit
    #echo Running poedit...
    #poedit $OUTDIR/en/LC_MESSAGES/$DOMAIN.po
fi
