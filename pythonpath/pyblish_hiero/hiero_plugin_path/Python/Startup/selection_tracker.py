"""Puts the active project into 'hiero.activeProject'"""

import hiero


def selectionChanged(event):
    hiero.selection = event.sender.selection()

hiero.core.events.registerInterest('kSelectionChanged', selectionChanged)
