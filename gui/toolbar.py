from PyQt5.QtWidgets import QToolBar, QAction, QMessageBox
from PyQt5.QtGui import QIcon

class Toolbar(QToolBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.init_toolbar()
    
    def init_toolbar(self):
        # Add Node action
        add_node_action = QAction("Add Node", self)
        add_node_action.setStatusTip("Add a new node")
        add_node_action.triggered.connect(self.handle_add_node)
        self.addAction(add_node_action)
        
        # Connect action
        connect_action = QAction("Connect", self)
        connect_action.setStatusTip("Connect nodes")
        connect_action.triggered.connect(self.handle_connect)
        self.addAction(connect_action)
        
        self.addSeparator()
        
        # Delete action
        delete_action = QAction("Delete", self)
        delete_action.setStatusTip("Delete selected")
        delete_action.triggered.connect(self.handle_delete)
        self.addAction(delete_action)

    def handle_add_node(self):
        if hasattr(self.main_window, 'add_node'):
            self.main_window.add_node()
        else:
            QMessageBox.warning(self, "Error", "Add node functionality not available")

    def handle_connect(self):
        canvas = self.main_window.get_canvas()
        if canvas:
            canvas.start_connection_mode()
        else:
            QMessageBox.warning(self, "Error", "Canvas not available")

    def handle_delete(self):
        if hasattr(self.main_window, 'delete_selected'):
            self.main_window.delete_selected()
        else:
            QMessageBox.warning(self, "Error", "Delete functionality not available")
