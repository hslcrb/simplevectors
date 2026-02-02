import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QToolBar, QFileDialog, 
                               QMessageBox, QListWidget, QDockWidget, QVBoxLayout, 
                               QWidget, QPushButton, QColorDialog, QLabel, QSplitter)
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtCore import Qt, QByteArray
from ..assets.i18n import i18n
from ..core.file_io import FileIO
from ..core.svg_manager import SvgManager
import uuid

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.svg_manager = SvgManager()
        self.current_file_path = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"{i18n.get('app_title')} - Rheehose")
        self.resize(1000, 700)

        # Central Widget (SVG Viewer)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        # Splitter to hold view and maybe side panel
        self.splitter = QSplitter(Qt.Horizontal)
        self.layout.addWidget(self.splitter)

        self.svg_widget = QSvgWidget()
        self.svg_widget.setStyleSheet("background-color: white;")
        self.splitter.addWidget(self.svg_widget)

        # Sidebar for layer/element list (Primitive representation)
        self.sidebar = QWidget()
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.element_list = QListWidget()
        self.element_list.clicked.connect(self.on_element_selected)
        self.sidebar_layout.addWidget(QLabel("Elements (IDs)"))
        self.sidebar_layout.addWidget(self.element_list)
        self.splitter.addWidget(self.sidebar)
        
        # Set splitter sizes
        self.splitter.setSizes([800, 200])

        self.create_actions()
        self.create_menus()
        self.create_toolbar()
        self.update_ui_text()

    def create_actions(self):
        # File Actions
        self.act_open = QAction(i18n.get('open'), self)
        self.act_open.triggered.connect(self.open_file)
        
        self.act_save = QAction(i18n.get('save'), self)
        self.act_save.triggered.connect(self.save_file)
        
        self.act_convert = QAction(i18n.get('convert'), self)
        self.act_convert.triggered.connect(self.convert_file)

        self.act_export_selected = QAction(i18n.get('export_selected'), self)
        self.act_export_selected.triggered.connect(self.export_selected)

        # Edit Actions
        self.act_color = QAction(i18n.get('change_color'), self)
        self.act_color.triggered.connect(self.change_item_color)
        
        self.act_group = QAction(i18n.get('group'), self)
        self.act_group.triggered.connect(self.group_items)

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

    def toggle_language(self):
        i18n.toggle_language()
        self.update_ui_text()

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, i18n.get('open'), "", "Vector Files (*.svg *.eps);;All Files (*)")
        if path:
            try:
                # Basic handling: if SVG, load directly. If EPS, convert first?
                # For this prototype, we focus on SVG primarily as the internal format.
                if path.lower().endswith('.eps'):
                    # TODO: Implement EPS to SVG conversion or intermediate load
                    QMessageBox.warning(self, i18n.get('warning'), "EPS loading is experimental. Please rely on SVG.")
                    return

                content = FileIO.open_svg(path)
                self.svg_manager.load_content(content)
                self.current_file_path = path
                self.refresh_view()
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
                # Save current state to temp if needed, or just use current file
                # If we have modified the SVG in memory, we should save it first or convert the in-memory string.
                # svglib works on files. Note: For a robust app, we'd pipe the string.
                # Here, we save to a temporary location or just overwrite current if saved.
                if self.current_file_path:
                    # Save current state to ensure conversions reflects edits
                    FileIO.save_svg(self.current_file_path, self.svg_manager.get_string())
                    FileIO.convert(self.current_file_path, path, ext)
                    QMessageBox.information(self, i18n.get('success'), i18n.get('conversion_complete'))
            except Exception as e:
                QMessageBox.critical(self, i18n.get('error'), str(e))

    def refresh_view(self):
        # QSvgWidget reads from file or bytes.
        svg_bytes = self.svg_manager.get_string().encode('utf-8')
        self.svg_widget.load(QByteArray(svg_bytes))

    def populate_element_list(self):
        self.element_list.clear()
        if not self.svg_manager.root:
            return
        
        # Naive traversal for items with IDs.
        # In a real app, we'd walk the tree.
        for elem in self.svg_manager.root.xpath("//*[@id]"):
            self.element_list.addItem(elem.attrib['id'])

    def on_element_selected(self):
        # Highlight logic could go here (e.g. adding a stroke)
        pass

    def get_selected_id(self):
        items = self.element_list.selectedItems()
        if items:
            return items[0].text()
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
                self.refresh_view()
                self.statusBar().showMessage(i18n.get('color_changed'))
            else:
                 QMessageBox.warning(self, i18n.get('error'), "Failed to change color.")

    def group_items(self):
        items = self.element_list.selectedItems()
        if not items:
            return
        ids = [item.text() for item in items]
        if len(ids) < 2:
            return 
        
        group_id = f"group_{uuid.uuid4().hex[:8]}"
        if self.svg_manager.group_elements(ids, group_id):
            self.refresh_view()
            self.populate_element_list()
            self.statusBar().showMessage(i18n.get('grouped'))

    def export_selected(self):
        eid = self.get_selected_id()
        if not eid:
             QMessageBox.warning(self, i18n.get('warning'), i18n.get('no_selection'))
             return
        
        # Get element string
        element = self.svg_manager.root.xpath(f"//*[@id='{eid}']")[0]
        xml_str = etree.tostring(element).decode('utf-8')
        
        path, _ = QFileDialog.getSaveFileName(self, i18n.get('export_selected'), f"{eid}.svg", "SVG Files (*.svg)")
        if path:
             try:
                 FileIO.export_element(xml_str, path)
                 self.statusBar().showMessage(i18n.get('success'))
             except Exception as e:
                 QMessageBox.critical(self, i18n.get('error'), str(e))

    def show_about(self):
        QMessageBox.about(self, i18n.get('about'), i18n.get('about_text'))

    def closeEvent(self, event):
        # Could ask for confirmation
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
