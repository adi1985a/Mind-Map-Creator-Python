from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QAction, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt
from .canvas import MindMapCanvas
from .toolbar import Toolbar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mind Map Creator")
        self.resize(1200, 800)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create canvas first
        self.canvas = MindMapCanvas(self)
        layout.addWidget(self.canvas)
        
        # Create toolbar after canvas
        self.toolbar = Toolbar(self)
        self.addToolBar(self.toolbar)
        
        self.setup_menu()

    def get_canvas(self):
        return self.canvas

    def setup_menu(self):
        menubar = self.menuBar()
        
        # File Menu
        file_menu = menubar.addMenu("File")
        new_action = QAction("New", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_mind_map)
        file_menu.addAction(new_action)
        
        save_action = QAction("Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_mind_map)
        file_menu.addAction(save_action)
        
        # Edit Menu
        edit_menu = menubar.addMenu("Edit")
        add_node_action = QAction("Add Node", self)
        add_node_action.triggered.connect(self.add_node)
        edit_menu.addAction(add_node_action)
        
        delete_action = QAction("Delete", self)
        delete_action.setShortcut("Del")
        delete_action.triggered.connect(self.delete_selected)
        edit_menu.addAction(delete_action)
        
        # Export Menu
        export_menu = menubar.addMenu("Export")
        export_pdf_action = QAction("Export as PDF", self)
        export_pdf_action.triggered.connect(self.export_pdf)
        export_menu.addAction(export_pdf_action)

        # Help Menu
        help_menu = menubar.addMenu("Help")
        instructions_action = QAction("Instructions", self)
        instructions_action.triggered.connect(self.show_instructions)
        help_menu.addAction(instructions_action)

        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def new_mind_map(self):
        reply = QMessageBox.question(self, 'New Mind Map', 
                                   'Are you sure you want to create a new mind map?',
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.canvas.clear()

    def save_mind_map(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Mind Map", "", 
                                                 "Mind Map Files (*.mm);;All Files (*)")
        if file_name:
            # TODO: Implement actual save functionality
            QMessageBox.information(self, "Save", "Mind map saved successfully!")

    def add_node(self):
        self.canvas.create_new_node()

    def delete_selected(self):
        self.canvas.delete_selected_nodes()

    def export_pdf(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Export PDF", "", 
                                                 "PDF Files (*.pdf);;All Files (*)")
        if file_name:
            # TODO: Implement PDF export
            QMessageBox.information(self, "Export", "Export to PDF completed!")

    def show_about(self):
        QMessageBox.about(self, "About Mind Map Creator",
            """Mind Map Creator v1.0
            
Created by: Adrian Leśniak
Year: 2023

A powerful tool for creating and managing mind maps 
with an intuitive graphical interface.""")

    def show_instructions(self):
        QMessageBox.information(self, "Instructions",
            """How to use Mind Map Creator:

1. Creating Nodes:
   - Click 'Add Node' button or use Edit menu
   - Enter node text in the dialog

2. Managing Nodes:
   - Drag nodes to move them
   - Double-click to edit text
   - Right-click for shape and color options

3. Connecting Nodes:
   - Select a node and click 'Connect'
   - Click another node to create connection

4. Other Features:
   - Use 'Save' to preserve your work
   - Export to PDF available
   - Delete nodes using Delete key""")
