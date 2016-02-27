"""Puts the active project into 'hiero.activeProject'"""

import os
import hiero


def selectionChanged(event):
    selection = event.sender.selection()
    binSelection = selection
    if (len(binSelection) > 0
            and hasattr(binSelection[0], 'project')):
        hiero.activeProject = binSelection[0].project()

hiero.core.events.registerInterest('kSelectionChanged', selectionChanged)


def projectCreated(event):
    hiero.activeProject = event.sender

hiero.core.events.registerInterest('kAfterNewProjectCreated', projectCreated)


def projectLoad(event):
    basename = os.path.basename(event.sender.path())
    if basename != 'HieroPresets.hrox':
        hiero.activeProject = event.sender

hiero.core.events.registerInterest('kAfterProjectLoad', projectLoad)
