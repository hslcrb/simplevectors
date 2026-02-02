import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QToolBar, QFileDialog, 
                               QMessageBox, QListWidget, QDockWidget, QVBoxLayout, 
                               QWidget, QPushButton, QColorDialog, QLabel, QSplitter,
                               QGraphicsView, QGraphicsScene, QGraphicsRectItem,
                               QComboBox, QHBoxLayout, QGroupBox, QGraphicsItem, QMenu)
from PySide6.QtSvgWidgets import QGraphicsSvgItem
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtGui import QAction, QIcon, QKeySequence, QPainter, QPalette, QWheelEvent, QColor, QPen, QTransform
from PySide6.QtCore import Qt, QByteArray, QSize
from ..assets.i18n import i18n
from ..core.file_io import FileIO
from ..core.svg_manager import SvgManager
from ..core.image_tracer import ImageTracer
import uuid
from lxml import etree

class InteractiveSvgItem(QGraphicsSvgItem):
    def __init__(self, renderer, element_id):
        super().__init__()
        self.setSharedRenderer(renderer)
        self.setElementId(element_id)
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable)

    def paint(self, painter, option, widget=None):
        # We need to remove the State_Selected flag before calling super().paint
        # so that the built-in selection (dotted line) is not drawn if we want custom one.
        # But QGraphicsSvgItem doesn't have built-in selection style usually.
        super().paint(painter, option, widget)
        
        if self.isSelected():
            painter.save()
            # Mint color borders
            mint_color = QColor("#00FFbf") 
            pen = QPen(mint_color, 2, Qt.DashLine)
            pen.setCosmetic(True) # Width stays same on zoom
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(self.boundingRect())
            painter.restore()

class GraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.SmoothPixmapTransform)
        self.setDragMode(QGraphicsView.RubberBandDrag) # Enable Area Selection
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setOptimizationFlags(QGraphicsView.DontAdjustForAntialiasing | QGraphicsView.IndirectPainting)

    def wheelEvent(self, event: QWheelEvent):
        if event.modifiers() & Qt.ControlModifier:
            zoomInFactor = 1.25
            zoomOutFactor = 1 / zoomInFactor
            if event.angleDelta().y() > 0:
                zoomFactor = zoomInFactor
            else:
                zoomFactor = zoomOutFactor
            self.scale(zoomFactor, zoomFactor)
        else:
            super().wheelEvent(event)
            
    def mousePressEvent(self, event):
        # Prevent Right Click from clearing selection
        if event.button() == Qt.RightButton:
            return

        # Allow panning with Middle Mouse or Alt+Click if RubberBand is default
        if event.button() == Qt.MiddleButton:
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            original_event = event
            super().mousePressEvent(event)
            # We might need to fake a release to switch mode back properly later? 
            # Or just set it and reset on release.
        else:
            self.setDragMode(QGraphicsView.RubberBandDrag)
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.setDragMode(QGraphicsView.RubberBandDrag) 

    def keyPressEvent(self, event):
        # WASD and Arrow Keys for panning
        step = 20
        hbar = self.horizontalScrollBar()
        vbar = self.verticalScrollBar()
        
        if event.key() == Qt.Key_Left or event.key() == Qt.Key_A:
            hbar.setValue(hbar.value() - step)
        elif event.key() == Qt.Key_Right or event.key() == Qt.Key_D:
            hbar.setValue(hbar.value() + step)
        elif event.key() == Qt.Key_Up or event.key() == Qt.Key_W:
            vbar.setValue(vbar.value() - step)
        elif event.key() == Qt.Key_Down or event.key() == Qt.Key_S:
            vbar.setValue(vbar.value() + step)
        # Zoom Keys (Ctrl +, Ctrl -)
        elif event.modifiers() & Qt.ControlModifier:
            if event.key() == Qt.Key_Plus or event.key() == Qt.Key_Equal:
                self.scale(1.25, 1.25)
            elif event.key() == Qt.Key_Minus:
                self.scale(0.8, 0.8)
            else:
                super().keyPressEvent(event)
        else:
            super().keyPressEvent(event)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.svg_manager = SvgManager()
        self.current_file_path = None
        self.scene = QGraphicsScene()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"{i18n.get('app_title')} - Rheehose")
        self.resize(1200, 800)

        # Central Widget Layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        self.splitter = QSplitter(Qt.Horizontal)
        self.layout.addWidget(self.splitter)

        # Graphics View (The Canvas)
        self.view = GraphicsView()
        self.view.setContextMenuPolicy(Qt.CustomContextMenu) # Enable custom context menu
        self.view.customContextMenuRequested.connect(self.on_context_menu)
        self.scene.selectionChanged.connect(self.on_scene_selection_changed) 
        self.view.setScene(self.scene)
        self.splitter.addWidget(self.view)

        # Sidebar (Elements + Trace)
        self.sidebar = QWidget()
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        
        # Element List
        self.element_list = QListWidget()
        self.element_list.setSelectionMode(QListWidget.ExtendedSelection)
        self.element_list.itemSelectionChanged.connect(self.on_element_selected)
        self.sidebar_layout.addWidget(QLabel(i18n.get('view'))) # Placeholder title
        self.sidebar_layout.addWidget(self.element_list)
        
        # Image Trace Panel
        self.trace_group = QGroupBox(i18n.get('image_trace'))
        self.trace_layout = QVBoxLayout()
        
        self.btn_select_img = QPushButton(i18n.get('select_image'))
        self.btn_select_img.clicked.connect(self.select_image_to_trace)
        self.trace_layout.addWidget(self.btn_select_img)
        
        self.trace_layout.addWidget(QLabel(i18n.get('preset')))
        self.combo_preset = QComboBox()
        self.combo_preset.addItems(list(ImageTracer.PRESETS.keys()))
        self.trace_layout.addWidget(self.combo_preset)
        
        self.btn_trace = QPushButton(i18n.get('trace'))
        self.btn_trace.clicked.connect(self.perform_trace)
        self.btn_trace.setEnabled(False) 
        self.trace_layout.addWidget(self.btn_trace)
        
        self.trace_group.setLayout(self.trace_layout)
        self.sidebar_layout.addWidget(self.trace_group)
        
        self.splitter.addWidget(self.sidebar)
        self.splitter.setSizes([900, 300])

        self.create_actions()
        self.create_menus()
        self.create_toolbar()
        self.update_ui_text()
        
        # Trace state
        self.trace_img_path = None

    def create_actions(self):
        # File Actions
        self.act_open = QAction(i18n.get('open'), self)
        self.act_open.triggered.connect(self.open_file)
        self.act_open.setShortcut(QKeySequence.Open)
        
        self.act_save = QAction(i18n.get('save'), self)
        self.act_save.triggered.connect(self.save_file)
        self.act_save.setShortcut(QKeySequence.Save)
        
        self.act_convert = QAction(i18n.get('convert'), self)
        self.act_convert.triggered.connect(self.convert_file)

        self.act_export_selected = QAction(i18n.get('export_selected'), self)
        self.act_export_selected.triggered.connect(self.export_selected)

        # Edit Actions
        self.act_color = QAction(i18n.get('change_color'), self)
        self.act_color.triggered.connect(self.change_item_color)
        
        self.act_group = QAction(i18n.get('group'), self)
        self.act_group.triggered.connect(self.group_items)

        self.act_ungroup = QAction(i18n.get('ungroup'), self)
        self.act_ungroup.triggered.connect(self.ungroup_items)
        
        self.act_delete = QAction(i18n.get('delete'), self)
        self.act_delete.triggered.connect(self.delete_item)
        self.act_delete.setShortcut(QKeySequence.Delete)

        self.act_undo = QAction(i18n.get('undo'), self)
        self.act_undo.triggered.connect(self.undo)
        self.act_undo.setShortcut(QKeySequence.Undo)

        self.act_redo = QAction(i18n.get('redo'), self)
        self.act_redo.triggered.connect(self.redo)
        self.act_redo.setShortcut(QKeySequence.Redo)

        # Zoom Actions
        self.act_zoom_in = QAction("Zoom In", self)
        self.act_zoom_in.setShortcut(QKeySequence.ZoomIn)
        self.act_zoom_in.triggered.connect(lambda: self.view.scale(1.25, 1.25))
        
        self.act_zoom_out = QAction("Zoom Out", self)
        self.act_zoom_out.setShortcut(QKeySequence.ZoomOut)
        self.act_zoom_out.triggered.connect(lambda: self.view.scale(0.8, 0.8))

        # View/Lang Actions
        self.act_toggle_lang = QAction(i18n.get('toggle_language'), self)
        self.act_toggle_lang.triggered.connect(self.toggle_language)

        self.act_about = QAction(i18n.get('about'), self)
        self.act_about.triggered.connect(self.show_about)

    def create_menus(self):
        menubar = self.menuBar()
        self.menu_file = menubar.addMenu(i18n.get('file'))
        self.menu_file.addAction(self.act_open)
        self.menu_file.addAction(self.act_save)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.act_convert)
        self.menu_file.addAction(self.act_export_selected)

        self.menu_edit = menubar.addMenu(i18n.get('edit'))
        self.menu_edit.addAction(self.act_color)
        self.menu_edit.addAction(self.act_group)

        self.menu_view = menubar.addMenu(i18n.get('view'))
        self.menu_view.addAction(self.act_zoom_in)
        self.menu_view.addAction(self.act_zoom_out)
        self.menu_view.addSeparator()
        self.menu_view.addAction(self.act_toggle_lang)
        
        self.menu_help = menubar.addMenu("Help")
        self.menu_help.addAction(self.act_about)

    def create_toolbar(self):
        self.toolbar = QToolBar("Main Toolbar")
        self.addToolBar(self.toolbar)
        self.toolbar.addAction(self.act_open)
        self.toolbar.addAction(self.act_save)
        self.toolbar.addAction(self.act_color)
        self.toolbar.addAction(self.act_group)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.act_toggle_lang)

    def update_ui_text(self):
        """Updates text elements based on current language."""
        self.setWindowTitle(f"{i18n.get('app_title')} - Rheehose")
        self.menu_file.setTitle(i18n.get('file'))
        self.menu_edit.setTitle(i18n.get('edit'))
        self.menu_view.setTitle(i18n.get('view'))
        
        self.act_open.setText(i18n.get('open'))
        self.act_save.setText(i18n.get('save'))
        self.act_convert.setText(i18n.get('convert'))
        self.act_export_selected.setText(i18n.get('export_selected'))
        self.act_color.setText(i18n.get('change_color'))
        self.act_group.setText(i18n.get('group'))
        self.act_toggle_lang.setText(i18n.get('toggle_language'))
        self.act_about.setText(i18n.get('about'))
        
        self.trace_group.setTitle(i18n.get('image_trace'))
        self.btn_select_img.setText(i18n.get('select_image'))
        self.btn_trace.setText(i18n.get('trace'))

    def toggle_language(self):
        i18n.toggle_language()
        self.update_ui_text()

    def load_svg_to_scene(self, svg_content):
        self.scene.clear()
        
        # Keep reference to renderer
        self.renderer = QSvgRenderer(QByteArray(svg_content.encode('utf-8')))
        
        # 1. Background (The actual render)
        # Locked so it cannot be selected directly, we use overlay for that.
        svg_item = QGraphicsSvgItem()
        svg_item.setSharedRenderer(self.renderer)
        svg_item.setFlags(QGraphicsItem.ItemClipsToShape) # Disable default selection
        self.scene.addItem(svg_item)
        self.scene.setSceneRect(svg_item.boundingRect())
        self.main_svg_item = svg_item
        
        if self.svg_manager.root is None:
            return

        # 2. Transparent Interactive Overlays
        # Iterate over all elements to create hitboxes
        for elem in self.svg_manager.root.iter():
            tag = etree.QName(elem).localname
            if tag in ['path', 'rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon', 'text', 'image']:
                if 'id' in elem.attrib:
                    eid = elem.attrib['id']
                    if self.renderer.elementExists(eid):
                         # Get bounds in local coordinates
                         bounds = self.renderer.boundsOnElement(eid)
                         
                         # Create an invisible interactive item matching the bounds
                         hitbox = QGraphicsRectItem(bounds)
                         
                         # Note: matrixForElement is missing in some PySide6 bindings, 
                         # so we skip explicit transform application to avoid crashes.
                         # This might cause misalignment for transformed elements, 
                         # but ensures stability.
                         
                         # Branding & Flags
                         hitbox.setBrush(QColor(0, 0, 0, 1)) # Almost transparent but hit-testable.
                         hitbox.setPen(Qt.NoPen)             # No border by default
                         hitbox.setFlags(QGraphicsItem.ItemIsSelectable)
                         hitbox.setData(0, "interactive")
                         hitbox.setData(1, eid)
                         
                         self.scene.addItem(hitbox)

    def on_scene_selection_changed(self):
        """Sync scene selection to list widget."""
        selected_items = self.scene.selectedItems()
        # If nothing selected, just clear list
        if not selected_items:
            self.element_list.blockSignals(True)
            self.element_list.clearSelection()
            self.element_list.blockSignals(False)
            return

        # Temporarily block signals to avoid loop
        self.element_list.blockSignals(True)
        self.element_list.clearSelection()
        
        ids_to_select = []
        for item in selected_items:
             eid = item.data(1)
             if eid:
                 ids_to_select.append(eid)
        
        # Find in list
        for i in range(self.element_list.count()):
            item = self.element_list.item(i)
            if item.text() in ids_to_select:
                item.setSelected(True)
        
        self.element_list.blockSignals(False)

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, i18n.get('open'), "", "Vector Files (*.svg *.eps);;All Files (*)")
        if path:
            try:
                if path.lower().endswith('.eps'):
                    QMessageBox.warning(self, i18n.get('warning'), "EPS loading is experimental.")
                    return

                content = FileIO.open_svg(path)
                self.svg_manager.load_content(content)
                self.current_file_path = path
                self.load_svg_to_scene(self.svg_manager.get_string())
                self.populate_element_list()
                self.statusBar().showMessage(i18n.get('file_opened').format(path))
            except Exception as e:
                QMessageBox.critical(self, i18n.get('error'), str(e))

    def save_file(self):
        if self.current_file_path:
            try:
                FileIO.save_svg(self.current_file_path, self.svg_manager.get_string())
                self.statusBar().showMessage(i18n.get('file_saved').format(self.current_file_path))
            except Exception as e:
                QMessageBox.critical(self, i18n.get('error'), str(e))
        else:
            self.save_as_file()

    def save_as_file(self):
        path, _ = QFileDialog.getSaveFileName(self, i18n.get('save_as'), "", "SVG Files (*.svg)")
        if path:
            try:
                FileIO.save_svg(path, self.svg_manager.get_string())
                self.current_file_path = path
                self.statusBar().showMessage(i18n.get('file_saved').format(path))
            except Exception as e:
                 QMessageBox.critical(self, i18n.get('error'), str(e))

    def convert_file(self):
        if not self.current_file_path:
            return
        
        path, _ = QFileDialog.getSaveFileName(self, i18n.get('convert'), "", "PDF (*.pdf);;EPS (*.eps);;PNG (*.png)")
        if path:
            ext = path.split('.')[-1]
            try:
                if self.current_file_path:
                    # Save first
                    FileIO.save_svg(self.current_file_path, self.svg_manager.get_string())
                    FileIO.convert(self.current_file_path, path, ext)
                    QMessageBox.information(self, i18n.get('success'), i18n.get('conversion_complete'))
            except Exception as e:
                QMessageBox.critical(self, i18n.get('error'), str(e))

    def populate_element_list(self):
        self.element_list.clear()
        if self.svg_manager.root is None:
            return
        for elem in self.svg_manager.root.xpath("//*[@id]"):
            self.element_list.addItem(elem.attrib['id'])

    def on_element_selected(self):
        """Handle element selection in the list widget."""
        # Highlight selection
        # Remove previous highlights
        for item in self.scene.items():
            if item.data(0) == "highlight":
               self.scene.removeItem(item)

        items = self.element_list.selectedItems()
        for item in items:
            eid = item.text()
            if self.renderer.elementExists(eid):
                rect = self.renderer.boundsOnElement(eid)
                # No matrix, just overlay
                
                highlight = QGraphicsRectItem(rect)
                highlight.setData(0, "highlight") 
                
                pen = QPen(QColor("#00FFbf"), 2, Qt.DashLine)
                pen.setCosmetic(True)
                highlight.setPen(pen)
                highlight.setBrush(Qt.NoBrush)
                self.scene.addItem(highlight)

    def get_selected_id(self):
        # Backward compatibility helper for single item actions like color change
        items = self.get_selected_ids()
        if items:
            return items[0]
        return None
    def change_item_color(self):
        eid = self.get_selected_id()
        if not eid:
            QMessageBox.warning(self, i18n.get('warning'), i18n.get('no_selection'))
            return

        color = QColorDialog.getColor()
        if color.isValid():
            new_color = color.name()
            if self.svg_manager.change_color(eid, new_color):
                self.load_svg_to_scene(self.svg_manager.get_string())
                self.statusBar().showMessage(i18n.get('color_changed'))

    def group_items(self):
        items = self.element_list.selectedItems()
        if not items:
            return
        ids = [item.text() for item in items]
        if len(ids) < 2:
            return 
        
        group_id = f"group_{uuid.uuid4().hex[:8]}"
        if self.svg_manager.group_elements(ids, group_id):
            self.load_svg_to_scene(self.svg_manager.get_string())
            self.populate_element_list()
            self.statusBar().showMessage(i18n.get('grouped'))

    def export_selected(self):
        eid = self.get_selected_id()
        if not eid:
             QMessageBox.warning(self, i18n.get('warning'), i18n.get('no_selection'))
             return
        
        element = self.svg_manager.root.xpath(f"//*[@id='{eid}']")[0]
        xml_str = etree.tostring(element).decode('utf-8')
        
        path, _ = QFileDialog.getSaveFileName(self, i18n.get('export_selected'), f"{eid}.svg", "SVG Files (*.svg)")
        if path:
             try:
                 FileIO.export_element(xml_str, path)
                 self.statusBar().showMessage(i18n.get('success'))
             except Exception as e:
                 QMessageBox.critical(self, i18n.get('error'), str(e))

    # --- Image Trace Features ---
    def select_image_to_trace(self):
        path, _ = QFileDialog.getOpenFileName(self, i18n.get('select_image'), "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if path:
            self.trace_img_path = path
            self.btn_trace.setEnabled(True)
            self.statusBar().showMessage(f"Selected: {path}")

    def perform_trace(self):
        if not self.trace_img_path:
            return
        
        preset = self.combo_preset.currentText()
        try:
            svg_content = ImageTracer.trace_image(self.trace_img_path, preset)
            
            # Load into manager
            self.svg_manager.load_content(svg_content)
            self.load_svg_to_scene(svg_content)
            self.populate_element_list()
            
            # Ask to save?
            self.current_file_path = None # New file
            self.statusBar().showMessage("Trace complete.")
        except Exception as e:
             QMessageBox.critical(self, i18n.get('error'), str(e))

    def undo(self):
        if self.svg_manager.undo():
            self.refresh_scene_and_list()
        else:
            print("Nothing to undo")

    def redo(self):
        if self.svg_manager.redo():
             self.refresh_scene_and_list()
        else:
             print("Nothing to redo")

    def get_selected_ids(self):
        """Returns a list of all selected item IDs."""
        items = self.element_list.selectedItems()
        return [item.text() for item in items]

    def group_items(self):
        eids = self.get_selected_ids()
        if len(eids) < 2:
            QMessageBox.warning(self, i18n.get('warning'), "Select at least 2 items to group.")
            return

        group_id = f"group_{uuid.uuid4().hex[:8]}"
        if self.svg_manager.group_elements(eids, group_id):
            self.refresh_scene_and_list()
        else:
            QMessageBox.warning(self, i18n.get('error'), "Failed to group items.")

    def ungroup_items(self):
        eids = self.get_selected_ids()
        if not eids:
            return
            
        if self.svg_manager.ungroup_elements(eids):
            self.refresh_scene_and_list()

    def delete_item(self):
        # Supports multi-delete now
        eids = self.get_selected_ids()
        if not eids:
            return
        
        reply = QMessageBox.question(self, i18n.get('delete'), f"{i18n.get('delete')} {len(eids)} items?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            if self.svg_manager.delete_elements(eids):
                self.refresh_scene_and_list()

    def refresh_scene_and_list(self):
         content = self.svg_manager.get_string()
         self.load_svg_to_scene(content)
         self.populate_element_list()

    def show_about(self):
        QMessageBox.about(self, i18n.get('about'), i18n.get('about_text'))

    def on_context_menu(self, pos):
        # Always show all options, but disable/enable based on context
        menu = QMenu(self)
        
        # 1. Edit History
        menu.addAction(self.act_undo)
        menu.addAction(self.act_redo)
        menu.addSeparator()
        
        # Check if anything is selected
        selected_id = self.get_selected_id()
        has_selection = selected_id is not None
        
        # 2. Manipulation Options
        # Color
        self.act_color.setEnabled(has_selection)
        menu.addAction(self.act_color)
        
        menu.addSeparator()
        
        # Group/Ungroup
        self.act_group.setEnabled(has_selection)
        menu.addAction(self.act_group)
        
        self.act_ungroup.setEnabled(has_selection)
        menu.addAction(self.act_ungroup)
        
        menu.addSeparator()
        
        # Delete/Export
        self.act_delete.setEnabled(has_selection)
        menu.addAction(self.act_delete)
        
        self.act_export_selected.setEnabled(has_selection)
        menu.addAction(self.act_export_selected)
        
        menu.exec(self.view.mapToGlobal(pos))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
