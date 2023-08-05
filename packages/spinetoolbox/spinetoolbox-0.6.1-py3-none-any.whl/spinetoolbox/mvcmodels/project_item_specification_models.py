######################################################################################################################
# Copyright (C) 2017-2021 Spine project consortium
# This file is part of Spine Toolbox.
# Spine Toolbox is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option)
# any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General
# Public License for more details. You should have received a copy of the GNU Lesser General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
######################################################################################################################

"""
Contains a class for storing Tool specifications.

:authors: P. Savolainen (VTT)
:date:   23.1.2018
"""

from PySide2.QtCore import Qt, QModelIndex, QAbstractListModel, QSortFilterProxyModel, Slot


class ProjectItemSpecificationModel(QAbstractListModel):
    """Class to store specs that are available in a project e.g. GAMS or Julia models."""

    def __init__(self, icons):
        super().__init__()
        self._specs = list()
        self._icons = icons
        self._project = None

    @Slot(str)
    def add_specification(self, name):
        """Adds a specification to the model.

        Args:
            name (str): specification's name
        """
        self.insertRow(self._project.get_specification(name))

    @Slot(str)
    def remove_specification(self, name):
        """Removes a specification from the model

        Args:
            name (str): specification's name
        """
        for i, spec in enumerate(self._specs):
            if spec.name == name:
                self.removeRow(i)
                return

    @Slot(str, str)
    def replace_specification(self, old_name, new_name):
        """Replaces a specification.

        Args:
            old_name (str): previous name
            new_name (str): new name
        """
        for i, spec in enumerate(self._specs):
            if spec.name == old_name:
                self._specs[i] = self._project.get_specification(new_name)
                index = self.index(i, 0)
                self.dataChanged.emit(index, index, [Qt.DisplayRole, Qt.ToolTipRole])
                return

    def connect_to_project(self, project):
        """Connects the model to a project.

        Args:
            project (SpineToolboxProject): project to connect to
        """
        self.clear()
        self._project = project
        for spec in self._project.specifications():
            self.insertRow(spec)
        self._project.specification_added.connect(self.add_specification)
        self._project.specification_removed.connect(self.remove_specification)
        self._project.specification_replaced.connect(self.replace_specification)

    def clear(self):
        self.beginResetModel()
        self._specs = list()
        self.endResetModel()

    def rowCount(self, parent=None):
        """Returns the number of specs in the model.

        Args:
            parent (QModelIndex): Not used (because this is a list)

        Returns:
            Number of rows (available specs) in the model
        """
        return len(self._specs)

    def data(self, index, role=None):
        """Must be reimplemented when subclassing.

        Args:
            index (QModelIndex): Requested index
            role (int): Data role

        Returns:
            Data according to requested role
        """
        if not index.isValid() or self.rowCount() == 0:
            return None
        row = index.row()
        if role == Qt.DisplayRole:
            specname = self._specs[row].name
            return specname
        if role == Qt.ToolTipRole:
            if row >= self.rowCount():
                return ""
            return (
                "<p>Drag-and-drop this onto the Design View "
                f"to create a new <b>{self._specs[row].name}</b> item.</p>"
            )
        if role == Qt.DecorationRole:
            return self._icons[self._specs[row].item_type]

    def flags(self, index):
        """Returns enabled flags for the given index.

        Args:
            index (QModelIndex): Index of spec
        """
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def insertRow(self, spec, row=None, parent=QModelIndex()):
        """Insert row (specification) into model.

        Args:
            spec (ProjectItemSpecification): spec added to the model
            row (int, optional): Row to insert spec to
            parent (QModelIndex): Parent of child (not used)

        Returns:
            Void
        """
        if row is None:
            row = self.rowCount()
        self.beginInsertRows(parent, row, row)
        self._specs.insert(row, spec)
        self.endInsertRows()

    def removeRow(self, row, parent=QModelIndex()):
        """Remove row (spec) from model.

        Args:
            row (int): Row to remove the spec from
            parent (QModelIndex): Parent of spec on row (not used)

        Returns:
            Boolean variable
        """
        if row < 0 or row > self.rowCount():
            # logging.error("Invalid row number")
            return False
        self.beginRemoveRows(parent, row, row)
        self._specs.pop(row)
        self.endRemoveRows()
        return True

    def specification(self, row):
        """Returns spec specification on given row.

        Args:
            row (int): Row of spec specification

        Returns:
            ProjectItemSpecification from specification list or None if given row is zero
        """
        return self._specs[row]

    def specifications(self):
        """Yields all specs."""
        yield from self._specs

    def specification_row(self, name):
        """Returns the row on which the given specification is located or -1 if it is not found."""
        for i in range(len(self._specs)):
            if name.lower() == self._specs[i].name.lower():
                return i
        return -1

    def specification_index(self, name):
        """Returns the QModelIndex on which a specification with
        the given name is located or invalid index if it is not found."""
        row = self.specification_row(name)
        if row == -1:
            return QModelIndex()
        return self.createIndex(row, 0)


class FilteredSpecificationModel(QSortFilterProxyModel):
    def __init__(self, item_type):
        super().__init__()
        self.item_type = item_type

    def filterAcceptsRow(self, source_row, source_parent):
        spec = self.sourceModel().specification(source_row)
        return spec.item_type == self.item_type

    def get_mime_data_text(self, index):
        row = self.mapToSource(index).row()
        return ",".join([self.item_type, self.sourceModel().specification(row).name])

    def specifications(self):
        """Yields all specs."""
        for row in range(self.rowCount()):
            source_row = self.mapToSource(self.index(row, 0)).row()
            yield self.sourceModel().specification(source_row)
