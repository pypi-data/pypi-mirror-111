import logging

from gi.repository import Gdk, Gtk

from gaphor import UML
from gaphor.core import gettext, transactional
from gaphor.core.format import format, parse
from gaphor.diagram.propertypages import (
    ComboModel,
    EditableTreeModel,
    PropertyPageBase,
    PropertyPages,
    new_resource_builder,
    on_bool_cell_edited,
    on_text_cell_edited,
)
from gaphor.UML.classes.association import AssociationItem
from gaphor.UML.classes.datatype import DataTypeItem
from gaphor.UML.classes.dependency import DependencyItem
from gaphor.UML.classes.enumeration import EnumerationItem
from gaphor.UML.classes.interface import Folded, InterfaceItem
from gaphor.UML.classes.klass import ClassItem
from gaphor.UML.components.connector import ConnectorItem
from gaphor.UML.profiles.stereotypepropertypages import stereotype_model

log = logging.getLogger(__name__)


new_builder = new_resource_builder("gaphor.UML.classes")


@transactional
def on_keypress_event(ctrl, keyval, keycode, state, tree):
    k = Gdk.keyval_name(keyval).lower()
    if k in ("backspace", "delete"):
        model, iter = tree.get_selection().get_selected()
        if iter:
            model.remove(iter)
    elif k in ("equal", "plus"):
        model, iter = tree.get_selection().get_selected()
        model.swap(iter, model.iter_next(iter))
        return True
    elif k in ("minus", "underscore"):
        model, iter = tree.get_selection().get_selected()
        model.swap(iter, model.iter_previous(iter))
        return True


class ClassAttributes(EditableTreeModel):
    """GTK tree model to edit class attributes."""

    def __init__(self, item):
        super().__init__(item, cols=(str, bool, object))

    def get_rows(self):
        for attr in self._item.subject.ownedAttribute:
            if not attr.association:
                yield [format(attr, note=True), attr.isStatic, attr]

    def create_object(self):
        attr = self._item.model.create(UML.Property)
        self._item.subject.ownedAttribute = attr
        return attr

    @transactional
    def set_object_value(self, row, col, value):
        attr = row[-1]
        if col == 0:
            parse(attr, value)
            row[0] = format(attr, note=True)
        elif col == 1:
            attr.isStatic = not attr.isStatic
            row[1] = attr.isStatic
        elif col == 2:
            # Value in attribute object changed:
            row[0] = format(attr, note=True)
            row[1] = attr.isStatic

    def swap_objects(self, o1, o2):
        return self._item.subject.ownedAttribute.swap(o1, o2)

    def sync_model(self, new_order):
        self._item.subject.ownedAttribute.order(new_order.index)


class ClassOperations(EditableTreeModel):
    """GTK tree model to edit class operations."""

    def __init__(self, item):
        super().__init__(item, cols=(str, bool, bool, object))

    def get_rows(self):
        for operation in self._item.subject.ownedOperation:
            yield [
                format(operation, note=True),
                operation.isAbstract,
                operation.isStatic,
                operation,
            ]

    def create_object(self):
        operation = self._item.model.create(UML.Operation)
        self._item.subject.ownedOperation = operation
        return operation

    @transactional
    def set_object_value(self, row, col, value):
        operation = row[-1]
        if col == 0:
            parse(operation, value)
            row[0] = format(operation, note=True)
        elif col == 1:
            operation.isAbstract = not operation.isAbstract
            row[1] = operation.isAbstract
        elif col == 2:
            operation.isStatic = not operation.isStatic
            row[2] = operation.isStatic
        elif col == 3:
            row[0] = format(operation, note=True)
            row[1] = operation.isAbstract
            row[2] = operation.isStatic

    def swap_objects(self, o1, o2):
        return self._item.subject.ownedOperation.swap(o1, o2)

    def sync_model(self, new_order):
        self._item.subject.ownedOperation.order(new_order.index)


class ClassEnumerationLiterals(EditableTreeModel):
    """GTK tree model to edit enumeration literals."""

    def __init__(self, item):
        super().__init__(item, cols=(str, object))

    def get_rows(self):
        for literal in self._item.subject.ownedLiteral:
            yield [format(literal), literal]

    def create_object(self):
        literal = self._item.model.create(UML.EnumerationLiteral)
        self._item.subject.ownedLiteral = literal
        literal.enumeration = self._item.subject
        return literal

    @transactional
    def set_object_value(self, row, col, value):
        literal = row[-1]
        if col == 0:
            parse(literal, value)
            row[0] = format(literal)
        elif col == 1:
            # Value in attribute object changed:
            row[0] = format(literal)

    def swap_objects(self, o1, o2):
        return self._item.subject.ownedLiteral.swap(o1, o2)

    def sync_model(self, new_order):
        self._item.subject.ownedLiteral.order(new_order.index)


def tree_view_column_tooltips(tree_view, tooltips):
    assert tree_view.get_n_columns() == len(tooltips)

    def on_query_tooltip(widget, x, y, keyboard_mode, tooltip):
        path_and_more = widget.get_path_at_pos(x, y)
        if path_and_more:
            path, column, cx, cy = path_and_more
            n = widget.get_columns().index(column)
            if tooltips[n]:
                tooltip.set_text(tooltips[n])
                return True
        return False

    tree_view.connect("query-tooltip", on_query_tooltip)


@PropertyPages.register(UML.NamedElement)
class NamedElementPropertyPage(PropertyPageBase):
    """An adapter which works for any named item view.

    It also sets up a table view which can be extended.
    """

    order = 10

    def __init__(self, subject: UML.NamedElement):
        super().__init__()
        assert subject is None or isinstance(subject, UML.NamedElement), "%s" % type(
            subject
        )
        self.subject = subject
        self.watcher = subject.watcher() if subject else None

    def construct(self):
        if not self.subject or UML.model.is_metaclass(self.subject):
            return

        assert self.watcher
        builder = new_builder(
            "named-element-editor",
            signals={
                "name-changed": (self._on_name_changed,),
                "name-entry-destroyed": (self.watcher.unsubscribe_all,),
            },
        )

        subject = self.subject

        entry = builder.get_object("name-entry")
        entry.set_text(subject and subject.name or "")

        def handler(event):
            if event.element is subject and event.new_value != entry.get_text():
                entry.set_text(event.new_value or "")

        self.watcher.watch("name", handler)

        return builder.get_object("named-element-editor")

    @transactional
    def _on_name_changed(self, entry):
        self.subject.name = entry.get_text()


@PropertyPages.register(UML.Classifier)
class ClassifierPropertyPage(PropertyPageBase):

    order = 15

    def __init__(self, subject):
        self.subject = subject

    def construct(self):
        if UML.model.is_metaclass(self.subject):
            return

        builder = new_builder(
            "classifier-editor",
            signals={"abstract-changed": (self._on_abstract_change,)},
        )

        abstract = builder.get_object("abstract")
        abstract.set_active(self.subject.isAbstract)

        return builder.get_object("classifier-editor")

    @transactional
    def _on_abstract_change(self, button, gparam):
        self.subject.isAbstract = button.get_active()


@PropertyPages.register(InterfaceItem)
class InterfacePropertyPage(PropertyPageBase):
    """Adapter which shows a property page for an interface view."""

    order = 15

    def __init__(self, item):
        self.item = item

    def construct(self):
        builder = new_builder(
            "interface-editor", signals={"folded-changed": (self._on_fold_change,)}
        )

        item = self.item

        connected_items = [
            c.item for c in item.diagram.connections.get_connections(connected=item)
        ]
        disallowed = (ConnectorItem,)
        can_fold = not any(map(lambda i: isinstance(i, disallowed), connected_items))

        folded = builder.get_object("folded")
        folded.set_active(item.folded != Folded.NONE)
        folded.set_sensitive(can_fold)

        return builder.get_object("interface-editor")

    @transactional
    def _on_fold_change(self, button, gparam):
        item = self.item

        fold = button.get_active()

        item.folded = Folded.PROVIDED if fold else Folded.NONE


@PropertyPages.register(DataTypeItem)
@PropertyPages.register(ClassItem)
@PropertyPages.register(InterfaceItem)
class AttributesPage(PropertyPageBase):
    """An editor for attributes associated with classes and interfaces."""

    order = 20

    def __init__(self, item):
        super().__init__()
        self.item = item
        self.watcher = item.subject and item.subject.watcher()

    def construct(self):
        if not self.item.subject:
            return

        self.model = ClassAttributes(self.item)

        builder = new_builder(
            "attributes-editor",
            signals={
                "show-attributes-changed": (self._on_show_attributes_change,),
                "attributes-name-edited": (on_text_cell_edited, self.model, 0),
                "attributes-static-edited": (on_bool_cell_edited, self.model, 1),
                "tree-view-destroy": (self.watcher.unsubscribe_all,),
            },
        )
        page = builder.get_object("attributes-editor")

        show_attributes = builder.get_object("show-attributes")
        show_attributes.set_active(self.item.show_attributes)

        tree_view: Gtk.TreeView = builder.get_object("attributes-list")
        tree_view.set_model(self.model)
        tree_view_column_tooltips(tree_view, ["", gettext("Static")])
        if Gtk.get_major_version() == 3:
            controller = self.key_controller = Gtk.EventControllerKey.new(tree_view)
        else:
            controller = Gtk.EventControllerKey.new()
            tree_view.add_controller(controller)
        controller.connect("key-pressed", on_keypress_event, tree_view)

        def handler(event):
            attribute = event.element
            for row in self.model:
                if row[-1] is attribute:
                    row[:] = [
                        format(attribute, note=True),
                        attribute.isStatic,
                        attribute,
                    ]

        self.watcher.watch("ownedAttribute.name", handler).watch(
            "ownedAttribute.isDerived", handler
        ).watch("ownedAttribute.visibility", handler).watch(
            "ownedAttribute.isStatic", handler
        ).watch(
            "ownedAttribute.lowerValue", handler
        ).watch(
            "ownedAttribute.upperValue", handler
        ).watch(
            "ownedAttribute.defaultValue", handler
        ).watch(
            "ownedAttribute.typeValue", handler
        )

        return page

    @transactional
    def _on_show_attributes_change(self, button, gparam):
        self.item.show_attributes = button.get_active()
        self.item.request_update()


@PropertyPages.register(DataTypeItem)
@PropertyPages.register(ClassItem)
@PropertyPages.register(InterfaceItem)
class OperationsPage(PropertyPageBase):
    """An editor for operations associated with classes and interfaces."""

    order = 30

    def __init__(self, item):
        super().__init__()
        self.item = item
        self.watcher = item.subject and item.subject.watcher()

    def construct(self):
        if not self.item.subject:
            return

        self.model = ClassOperations(self.item)

        builder = new_builder(
            "operations-editor",
            signals={
                "show-operations-changed": (self._on_show_operations_change,),
                "operations-name-edited": (on_text_cell_edited, self.model, 0),
                "operations-abstract-edited": (on_bool_cell_edited, self.model, 1),
                "operations-static-edited": (on_bool_cell_edited, self.model, 2),
                "tree-view-destroy": (self.watcher.unsubscribe_all,),
            },
        )

        show_operations = builder.get_object("show-operations")
        show_operations.set_active(self.item.show_operations)

        tree_view: Gtk.TreeView = builder.get_object("operations-list")
        tree_view.set_model(self.model)
        tree_view_column_tooltips(
            tree_view, ["", gettext("Abstract"), gettext("Static")]
        )
        if Gtk.get_major_version() == 3:
            controller = self.key_controller = Gtk.EventControllerKey.new(tree_view)
        else:
            controller = Gtk.EventControllerKey.new()
            tree_view.add_controller(controller)
        controller.connect("key-pressed", on_keypress_event, tree_view)

        def handler(event):
            operation = event.element
            for row in self.model:
                if row[-1] is operation:
                    row[:] = [
                        format(operation, note=True),
                        operation.isAbstract,
                        operation.isStatic,
                        operation,
                    ]

        self.watcher.watch("ownedOperation.name", handler).watch(
            "ownedOperation.isAbstract", handler
        ).watch("ownedOperation.visibility", handler).watch(
            "ownedOperation.ownedParameter.lowerValue", handler
        ).watch(
            "ownedOperation.ownedParameter.upperValue", handler
        ).watch(
            "ownedOperation.ownedParameter.typeValue", handler
        ).watch(
            "ownedOperation.ownedParameter.defaultValue", handler
        )

        return builder.get_object("operations-editor")

    @transactional
    def _on_show_operations_change(self, button, gparam):
        self.item.show_operations = button.get_active()
        self.item.request_update()


@PropertyPages.register(EnumerationItem)
class EnumerationPage(PropertyPageBase):
    """An editor for enumeration literals for an enumeration."""

    order = 20

    def __init__(self, item):
        super().__init__()
        self.item = item
        self.watcher = item.subject and item.subject.watcher()

    def construct(self):
        if not isinstance(self.item.subject, UML.Enumeration):
            return

        builder = new_builder("enumerations-editor")
        page = builder.get_object("enumerations-editor")

        show_enumerations = builder.get_object("show-enumerations")
        show_enumerations.set_active(self.item.show_enumerations)

        self.model = ClassEnumerationLiterals(self.item)

        tree_view: Gtk.TreeView = builder.get_object("enumerations-list")
        tree_view.set_model(self.model)

        def handler(event):
            enumeration = event.element
            for row in self.model:
                if row[-1] is enumeration:
                    row[:] = [format(enumeration), enumeration]

        self.watcher.watch("ownedLiteral.name", handler)

        builder.connect_signals(
            {
                "show-enumerations-changed": (self._on_show_enumerations_change,),
                "enumerations-name-edited": (on_text_cell_edited, self.model, 0),
                "tree-view-destroy": (self.watcher.unsubscribe_all,),
                "enumerations-keypress": (on_keypress_event,),
            }
        )
        return page

    @transactional
    def _on_show_enumerations_change(self, button, gparam):
        self.item.show_attributes = button.get_active()
        self.item.request_update()


PropertyPages.register(EnumerationItem)(AttributesPage)
PropertyPages.register(EnumerationItem)(OperationsPage)


@PropertyPages.register(DependencyItem)
class DependencyPropertyPage(PropertyPageBase):
    """Dependency item editor."""

    order = 20

    DEPENDENCY_TYPES = (
        (gettext("Dependency"), UML.Dependency),
        (gettext("Usage"), UML.Usage),
        (gettext("Realization"), UML.Realization),
        (gettext("Implementation"), UML.InterfaceRealization),
    )

    def __init__(self, item):
        super().__init__()
        self.item = item
        self.watcher = self.item.watcher()
        self.builder = new_builder(
            "dependency-editor",
            signals={
                "dependency-type-changed": (self._on_dependency_type_change,),
                "automatic-changed": (self._on_auto_dependency_change,),
                "dependency-type-destroy": (self.watcher.unsubscribe_all,),
            },
        )

    def construct(self):
        dependency_combo = self.builder.get_object("dependency-combo")
        model = ComboModel(self.DEPENDENCY_TYPES)
        dependency_combo.set_model(model)

        automatic = self.builder.get_object("automatic")
        automatic.set_active(self.item.auto_dependency)

        self.update()

        self.watcher.watch("subject", self._on_subject_change)

        return self.builder.get_object("dependency-editor")

    def _on_subject_change(self, event):
        self.update()

    def update(self):
        """Update dependency type combo box.

        Disallow dependency type when dependency is established.
        """
        combo = self.builder.get_object("dependency-combo")
        if combo.get_model():
            item = self.item
            index = combo.get_model().get_index(item.dependency_type)
            combo.props.sensitive = not item.auto_dependency
            combo.set_active(index)

    @transactional
    def _on_dependency_type_change(self, combo):
        cls = combo.get_model().get_value(combo.get_active())
        self.item.dependency_type = cls
        subject = self.item.subject
        if subject:
            UML.model.swap_element(subject, cls)
            self.item.request_update()

    @transactional
    def _on_auto_dependency_change(self, switch, gparam):
        self.item.auto_dependency = switch.get_active()
        self.update()


def _dummy_handler(*args):
    pass


@PropertyPages.register(AssociationItem)
class AssociationPropertyPage(PropertyPageBase):

    NAVIGABILITY = (None, False, True)
    AGGREGATION = ("none", "shared", "composite")

    order = 20

    def __init__(self, item):
        self.item = item
        self.subject = item.subject
        self.watcher = item.subject and self.subject.watcher()
        self.semaphore = 0

    def handlers_end(self, end_name, end):
        subject = end.subject

        stereotypes = UML.model.get_stereotypes(subject)
        if stereotypes:
            model, toggle_handler, set_value_handler = stereotype_model(subject)
            return model, {
                f"{end_name}-toggle-stereotype": toggle_handler,
                f"{end_name}-set-slot-value": set_value_handler,
            }
        else:
            return None, {
                f"{end_name}-toggle-stereotype": (_dummy_handler,),
                f"{end_name}-set-slot-value": (_dummy_handler,),
            }

    def construct_end(self, builder, end_name, end, stereotypes_model):
        subject = end.subject
        title = builder.get_object(f"{end_name}-title")
        if subject.type:
            title.set_text(f"{end_name.title()} (: {subject.type.name})")

        self.update_end_name(builder, end_name, subject)

        navigation = builder.get_object(f"{end_name}-navigation")
        navigation.set_active(self.NAVIGABILITY.index(subject.navigability))

        aggregation = builder.get_object(f"{end_name}-aggregation")
        aggregation.set_active(self.AGGREGATION.index(subject.aggregation))

        if stereotypes_model:
            stereotype_list = builder.get_object(f"{end_name}-stereotype-list")
            stereotype_list.set_model(stereotypes_model)
        else:
            stereotype_frame = builder.get_object(f"{end_name}-stereotype-frame")
            stereotype_frame.hide()

    def update_end_name(self, builder, end_name, subject):
        name = builder.get_object(f"{end_name}-name")
        new_name = (
            format(
                subject,
                visibility=True,
                is_derived=True,
                multiplicity=True,
            )
            or ""
        )
        if not (name.is_focus() or self.semaphore):
            self.semaphore += 1
            name.set_text(new_name)
            self.semaphore -= 1
        return name

    def construct(self):
        if not self.subject:
            return None

        head = self.item.head_end
        tail = self.item.tail_end

        head_model, head_signal_handlers = self.handlers_end("head", head)
        tail_model, tail_signal_handlers = self.handlers_end("tail", tail)

        builder = new_builder(
            "association-editor",
            signals={
                "show-direction-changed": (self._on_show_direction_change,),
                "invert-direction-changed": (self._on_invert_direction_change,),
                "head-name-changed": (self._on_end_name_change, head),
                "head-navigation-changed": (self._on_end_navigability_change, head),
                "head-aggregation-changed": (self._on_end_aggregation_change, head),
                "tail-name-changed": (self._on_end_name_change, tail),
                "tail-navigation-changed": (self._on_end_navigability_change, tail),
                "tail-aggregation-changed": (self._on_end_aggregation_change, tail),
                "association-editor-destroy": (self.watcher.unsubscribe_all,),
                **head_signal_handlers,
                **tail_signal_handlers,
            },
        )

        show_direction = builder.get_object("show-direction")
        show_direction.set_active(self.item.show_direction)

        self.construct_end(builder, "head", head, head_model)
        self.construct_end(builder, "tail", tail, tail_model)

        def name_handler(event):
            end_name = "head" if event.element is head.subject else "tail"
            self.update_end_name(builder, end_name, event.element)

        def restore_nav_handler(event):
            for end_name, end in (("head", head), ("tail", tail)):
                combo = builder.get_object(f"{end_name}-navigation")
                self._on_end_navigability_change(combo, end)

        # Watch on association end:
        self.watcher.watch("memberEnd[Property].name", name_handler).watch(
            "memberEnd[Property].visibility", name_handler
        ).watch("memberEnd[Property].lowerValue", name_handler).watch(
            "memberEnd[Property].upperValue", name_handler
        ).watch(
            "memberEnd[Property].type",
            restore_nav_handler,
        )

        return builder.get_object("association-editor")

    @transactional
    def _on_show_direction_change(self, button, gparam):
        self.item.show_direction = button.get_active()

    @transactional
    def _on_invert_direction_change(self, button):
        self.item.invert_direction()

    @transactional
    def _on_end_name_change(self, entry, end):
        if not self.semaphore:
            self.semaphore += 1
            parse(end.subject, entry.get_text())
            self.semaphore -= 1

    @transactional
    def _on_end_navigability_change(self, combo, end):
        if end.subject and end.subject.opposite and end.subject.opposite.type:
            UML.model.set_navigability(
                end.subject.association,
                end.subject,
                self.NAVIGABILITY[combo.get_active()],
            )
            # Call this again, or non-navigability will not be displayed
            self.item.update_ends()

    @transactional
    def _on_end_aggregation_change(self, combo, end):
        end.subject.aggregation = self.AGGREGATION[combo.get_active()]
