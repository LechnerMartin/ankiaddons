# coding: utf-8

"""
Addon to add Heisig translation from another Deck to specified fields

License: The MIT License (MIT)
"""

searchString = u"deck:@Nihongo::Heisig　-tag:HeisigPrimitive kanji:*{0}*"
heisigfieldname = 'KeyDE'

# Anki
import aqt
from anki.hooks import addHook

# Qt
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class BrowserLookup:

  def get_selected(self, view):
    """Copy selected text"""
    return view.page().selectedText()

  def lookup_action(self, view):
    browser = aqt.dialogs.open("Browser", aqt.mw)
    browser.form.searchEdit.lineEdit().setText(self.get_selected(view))
    browser.onSearch()

  def add_action(self, view, menu, action):
    """Add 'lookup' action to context menu"""
    if self.get_selected(view):
      action = menu.addAction(action)
      action.connect(action, SIGNAL('triggered()'),
        lambda view=view: self.lookup_action(view))

  def context_lookup_action(self, view, menu):
    """Browser Lookup action"""
    self.add_action(view, menu,
      u'Search Browser for %s...' % self.get_selected(view)[:20])

def showTooltip(text, timeOut=3000):
    aqt.utils.tooltip("<b>Heisig:</b><br />" + text, timeOut)
    return

def setupMenu(browser):
    a = QAction("Bulk-Generate Heisig", browser)
    browser.connect(a, SIGNAL("triggered()"), lambda e=browser: onBulkGenerateHeisig(e))
    browser.form.menuEdit.addSeparator()
    browser.form.menuEdit.addAction(a)

def onFocusLost(flag, n, fidx):
    #message = "Flag1 '{0}', N: '{1}', fidx '{2}'".format(str(type(flag)), n.model()['name'], str(type(fidx)))
    #"Flag %s, N: %s, fidx %s" #% ("a", "b", "c") 
    #message = "Flag %s, N: %s, fidx %s" % (type(flag), type(n), type(fidx)) 
    #message += " for: deck '%s', model '%s'" % (deck['name'], model['name'])
   # showTooltip(message, 5000);
    
#    showTooltip("Focus lost", 5000);
    
    return True


def comment():
    ## event coming from src field?
    #if fidx != srcIdx:
        #return flag
    #if n[dst]:
        #return flag
    ## grab source text
    #srcTxt = mw.col.media.strip(n[src])
    #if not srcTxt:
        #return flag
    ## update field
    #try:
        #n[dst] = mecab.splitHeisig()
    #except Exception, e:
        #raise
    return True

# Interface function for Heisig search
def getHeisigFromDeck(char):
    from aqt import mw
    ids = mw.col.findNotes(searchString.format(char))
    showTooltip("Heisig: {0}".format(len(ids)), 5000);
    if len(ids) == 1 :
        note = mw.col.getNote(ids[0])
        return note[heisigfieldname]
    else:
        return char


def onBulkGenerateHeisig(browser):
    a = getHeisigFromDeck(u"丨")
    b = getHeisigFromDeck(u"朝")
    showTooltip(u"Heisig: {0} {1}".format(a, b), 5000);

    #expr = u"彼二千三百六十円も使った。"
    #print mecab.reading(expr).encode("utf-8")
    #def findNotes(self, query):
    #   return anki.find.Finder(self).findNotes(query)
    #showTooltip("Hello again!", 5000);
    return True
    #bulkGenerateHeisig(browser.selectedNotes())

addHook("browser.setupMenus", setupMenu)
#addHook('editFocusLost', onFocusLost)


############################
# tests
############################
