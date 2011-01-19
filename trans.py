# Created By: Virgil Dupras
# Created On: 2010-06-23
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

# Doing i18n with GNU gettext for the core text gets complicated, so what I do is that I make the
# GUI layer responsible for supplying a tr() function.

import sys
import locale
import logging

_trfunc = None

def tr(s, context=None):
    if _trfunc is None:
        return s
    else:
        if context:
            return _trfunc(s, context)
        else:
            return _trfunc(s)

def set_tr(new_tr):
    global _trfunc
    _trfunc = new_tr

def install_cocoa_trans():
    from .cocoa.objcmin import NSBundle
    mainBundle = NSBundle.mainBundle()
    def cocoa_tr(s, context='core'):
        return mainBundle.localizedStringForKey_value_table_(s, s, context)
    set_tr(cocoa_tr)
    currentLang = NSBundle.preferredLocalizationsFromArray_(mainBundle.localizations())[0]
    LANG2LOCALENAME = {'fr': 'fr_FR', 'de': 'de_DE'}
    if currentLang in LANG2LOCALENAME:
        locale.setlocale(locale.LC_ALL, LANG2LOCALENAME[currentLang])

def install_qt_trans(lang=None):
    from PyQt4.QtCore import QCoreApplication, QTranslator, QLocale
    if sys.platform == 'win32':
        LANG2LOCALENAME = {'fr': 'fra_fra', 'de': 'deu_deu'}
    elif sys.platform == 'darwin':
        LANG2LOCALENAME = {'fr': 'fr_FR', 'de': 'de_DE'}
    else:
        LANG2LOCALENAME = {'fr': 'fr_FR.UTF-8', 'de': 'de_DE.UTF-8'}
    if not lang:
        lang = str(QLocale.system().name())[:2]
    if lang in LANG2LOCALENAME:
        localeName = LANG2LOCALENAME[lang]
        try:
            locale.setlocale(locale.LC_ALL, str(localeName))
        except locale.Error:
            logging.warning("Couldn't set locale %s", localeName)
    else:
        lang = 'en'
    qtr1 = QTranslator(QCoreApplication.instance())
    qtr1.load(':/qt_%s' % lang)
    QCoreApplication.installTranslator(qtr1)
    qtr2 = QTranslator(QCoreApplication.instance())
    qtr2.load(':/%s' % lang)
    QCoreApplication.installTranslator(qtr2)
    def qt_tr(s, context='core'):
        return str(QCoreApplication.translate(context, s, None))
    set_tr(qt_tr)
