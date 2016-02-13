# coding: utf-8

"""
Addon to add Heisig translation from another Deck to specified fields

License: The MIT License (MIT)
"""

searchString = u"deck:@Nihongo::Heisig　-tag:HeisigPrimitive kanji:*{0}*"
heisigfieldname = 'KeyDE'
heisigOutputFormatString = u".{0}."

Vocab_SrcField = 'Japanese'
#Vocab_SrcField2 = 'Kana'
dstField = 'Heisig'

OVERWRITE_DST_FIELD=False



# Anki
# import the main window object (mw) from ankiqt
from aqt import mw
import aqt
from anki.hooks import addHook
from aqt.utils import showInfo, showWarning
import re


# Qt
from PyQt4.QtGui import *
from PyQt4.QtCore import *


# class BrowserLookup:

# def get_selected(self, view):
#   """Copy selected text"""
#   return view.page().selectedText()
#
# def lookup_action(self, view):
#   browser = aqt.dialogs.open("Browser", aqt.mw)
#   browser.form.searchEdit.lineEdit().setText(self.get_selected(view))
#   browser.onSearch()
#
# def add_action(self, view, menu, action):
#   """Add 'lookup' action to context menu"""
#   if self.get_selected(view):
#     action = menu.addAction(action)
#     action.connect(action, SIGNAL('triggered()'),
#       lambda view=view: self.lookup_action(view))

# def context_lookup_action(self, view, menu):
#   """Browser Lookup action"""
#   self.add_action(view, menu,
#     u'Search Browser for %s...' % self.get_selected(view)[:20])

def showTooltip(text, timeOut=3000):
    aqt.utils.tooltip("<b>Heisig:</b><br />" + text, timeOut)
    return


def setupMenu(browser):
    a = QAction("Bulk-Generate Heisig", browser)
    browser.connect(a, SIGNAL("triggered()"), lambda e=browser: onBulkGenerateHeisig(e))
    browser.form.menuEdit.addSeparator()
    browser.form.menuEdit.addAction(a)


def onFocusLost(flag, n, fidx):
    # message = "Flag1 '{0}', N: '{1}', fidx '{2}'".format(str(type(flag)), n.model()['name'], str(type(fidx)))
    # "Flag %s, N: %s, fidx %s" #% ("a", "b", "c")
    # message = "Flag %s, N: %s, fidx %s" % (type(flag), type(n), type(fidx))
    # message += " for: deck '%s', model '%s'" % (deck['name'], model['name'])
    # showTooltip(message, 5000);

    #    showTooltip("Focus lost", 5000);

    return True


def comment():
    ## event coming from src field?
    # if fidx != srcIdx:
    # return flag
    # if n[dst]:
    # return flag
    ## grab source text
    # srcTxt = mw.col.media.strip(n[src])
    # if not srcTxt:
    # return flag
    ## update field
    # try:
    # n[dst] = mecab.splitHeisig()
    # except Exception, e:
    # raise
    return True


# Interface function for Heisig search
def getHeisigFromDeck(char):
    from aqt import mw
    ids = mw.col.findNotes(searchString.format(char))
    #showTooltip("Heisig: {0}".format(len(ids)), 5000);
    if len(ids) == 1:
        note = mw.col.getNote(ids[0])
        heisigKey = note[heisigfieldname]
        return heisigKey
    else:
        return None


def translateToHeisig(text, heisigLookupFunction, heisigFormatString=u"{0}"):
    result = u""
    for c in text:
        value = heisigLookupFunction(c)
        if value != None:
            result += heisigFormatString.format(value)
        else:
            result += c
    return result

def stripFormatting(txt):
    return re.sub("<.*?>", "", txt)


def onBulkGenerateHeisig(browser):
    mw.checkpoint("bulk-generate Heisig")
    mw.progress.start()

    nids = browser.selectedNotes()
    #showTooltip(u"Count: {0}".format(len(nids)), 2000)
    for nid in nids:
        note = mw.col.getNote(nid)
        src = None
        if Vocab_SrcField in note:
            src = stripFormatting(note[Vocab_SrcField])
        if dstField not in note:
            #showInfo ("--> Field %s not found!" % (dstField))
            continue
        if note[dstField] and not OVERWRITE_DST_FIELD:
            #showInfo ("--> %s not empty. Skipping!" % (Vocab_SrcField))
            continue
        heisig = translateToHeisig(src, getHeisigFromDeck, heisigOutputFormatString)
        #showInfo ("Heisig: %s " % heisig)
        note[dstField] = heisig
        note.flush()
    
    mw.progress.finish()
    mw.reset()
    return True
    # bulkGenerateHeisig(browser.selectedNotes())


addHook("browser.setupMenus", setupMenu)
# addHook('editFocusLost', onFocusLost)

