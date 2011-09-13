# Created By: Virgil Dupras
# Created On: 2011-09-06
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from collections import Sequence, MutableSequence

from ..util import minmax
from .base import NoopGUI

class Selectable(Sequence):
    def __init__(self):
        self._selected_indexes = []
    
    #--- Private
    def _check_selection_range(self):
        if not self:
            self._selected_indexes = []
        if not self._selected_indexes:
            return
        self._selected_indexes = [index for index in self._selected_indexes if index < len(self)]
        if not self._selected_indexes:
            self._selected_indexes = [len(self) - 1]
    
    #--- Virtual
    def _update_selection(self):
        # Takes the table's selection and does appropriates updates on the Document's side.
        pass
    
    #--- Public
    def select(self, indexes):
        if isinstance(indexes, int):
            indexes = [indexes]
        self.selected_indexes = indexes
        self._update_selection()
    
    #--- Properties
    @property
    def selected_index(self):
        return self._selected_indexes[0] if self._selected_indexes else None
    
    @selected_index.setter
    def selected_index(self, value):
        self.selected_indexes = [value]
    
    @property
    def selected_indexes(self):
        return self._selected_indexes
    
    @selected_indexes.setter
    def selected_indexes(self, value):
        self._selected_indexes = value
        self._selected_indexes.sort()
        self._check_selection_range()


class SelectableList(MutableSequence, Selectable):
    def __init__(self, items=None):
        Selectable.__init__(self)
        if items:
            self._items = list(items)
        else:
            self._items = []
    
    def __delitem__(self, key):
        self._items.__delitem__(key)
        self._check_selection_range()
        self._on_change()
    
    def __getitem__(self, key):
        return self._items.__getitem__(key)
    
    def __len__(self):
        return len(self._items)
    
    def __setitem__(self, key, value):
        self._items.__setitem__(key, value)
        self._on_change()
    
    #--- Override
    def append(self, item):
        self._items.append(item)
        self._on_change()
    
    def insert(self, index, item):
        self._items.insert(index, item)
        self._on_change()
    
    def remove(self, row):
        self._items.remove(row)
        self._check_selection_range()
        self._on_change()
    
    #--- Virtual
    def _on_change(self):
        pass
    

class GUISelectableList(SelectableList):
    def __init__(self, items=None, view=None):
        SelectableList.__init__(self, items)
        if view is None:
            view = NoopGUI()
        self.view = view
    
    def _on_change(self):
        self.view.refresh()