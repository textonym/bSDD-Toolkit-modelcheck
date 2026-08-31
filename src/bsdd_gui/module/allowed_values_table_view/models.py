from __future__ import annotations

from bsdd_json.models import BsddClassProperty, BsddProperty
from bsdd_json.utils import property_utils
from PySide6.QtCore import (
    QModelIndex,
    QSortFilterProxyModel,
    Qt,
)

from bsdd_gui import tool
from bsdd_gui.presets.models_presets import ItemModel


class AllowedValuesModel(ItemModel):
    def __init__(
        self, tl=None, bsdd_data: BsddClassProperty | BsddProperty = None, *args, **kwargs
    ):
        super().__init__(tool.AllowedValuesTableView, bsdd_data, *args, **kwargs)
        self.bsdd_data: BsddClassProperty | BsddProperty

    @property
    def parent_property(self) -> BsddProperty | None:
        if isinstance(self.bsdd_data, BsddClassProperty):
            return property_utils.get_property_by_class_property(
                self.bsdd_data, self.bsdd_dictionary
            )
        return None

    @property
    def bsdd_dictionary(self):
        return tool.Project.get()

    @property
    def active_class(self):
        return tool.MainWindowWidget.get_active_class()

    @property
    def active_pset(self):
        return tool.MainWindowWidget.get_active_pset()

    def columnCount(self, /, parent=...):
        res = super().columnCount(parent)
        return res

    def get_allowed_values(self):
        """
        returns all Allowed Values.
        If there are no allowed values in the ClassProperty it returns the allowed Values of its parent
        """
        own_values = self.bsdd_data.AllowedValues
        if not own_values:
            parent_values = self.parent_property.AllowedValues if self.parent_property else []
            return parent_values
        return own_values

    def rowCount(self, parent=None):
        if parent is None:
            parent = QModelIndex()
        if not self.bsdd_data:
            return 0
        if parent.isValid():
            return 0

        return len(self.get_allowed_values())

    def index(self, row: int, column: int, parent=None):
        if parent is None:
            parent = QModelIndex()
        if parent.isValid():
            return QModelIndex()

        if 0 > row >= len(self.rowCount()):
            return QModelIndex()
        allowed_value = self.get_allowed_values()[row]
        index = self.createIndex(row, column, allowed_value)
        return index

    def flags(self, index):
        parent_av = self.parent_property.AllowedValues if self.parent_property else []
        if index.internalPointer() in parent_av:
            return super().flags(index) & ~Qt.ItemFlag.ItemIsEnabled
        return super().flags(index) | Qt.ItemFlag.ItemIsEditable


# typing
class SortModel(QSortFilterProxyModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def sourceModel(self) -> AllowedValuesModel:
        return super().sourceModel()
