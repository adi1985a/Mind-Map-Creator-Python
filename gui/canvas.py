from PyQt5.QtWidgets import QWidget, QVBoxLayout, QInputDialog, QMenu, QColorDialog, QMessageBox
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush, QFont, QLinearGradient, QPainterPath
from mind_map_creator.models.node import Node

class MindMapCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.nodes = []
        self.connections = []
        self.setMinimumSize(800, 600)
        self.setMouseTracking(True)
        
        self.selected_nodes = []
        self.connection_mode = False
        self.connecting_node = None
        self.last_position = QPoint(50, 50)  # Starting position for new nodes
        self.dragging = False
        self.drag_node = None
        self.drag_offset = QPoint()
        self.hover_node = None
        self.hover_connection = None
        self.grid_size = 20
        self.show_grid = True
        self.selected_connection = None  # Add this line
        
    def clear(self):
        self.nodes = []
        self.connections = []
        self.update()

    def create_new_node(self):
        text, ok = QInputDialog.getText(self, 'New Node', 'Enter node text:')
        if ok and text:
            node = Node(text)
            node.position = (self.last_position.x(), self.last_position.y())
            self.nodes.append(node)
            # Update position for next node
            self.last_position = QPoint(self.last_position.x() + 150, self.last_position.y())
            if self.last_position.x() > self.width() - 100:
                self.last_position = QPoint(50, self.last_position.y() + 100)
            self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            clicked_node = self.get_node_at_position(event.pos())
            clicked_connection = self.get_connection_at_position(event.pos())
            
            if clicked_node:
                if self.connection_mode and self.connecting_node:
                    if clicked_node == self.connecting_node:
                        QMessageBox.warning(self, "Warning", "Cannot connect node to itself!")
                    else:
                        self.create_connection(self.connecting_node, clicked_node)
                    self.connection_mode = False
                    self.connecting_node = None
                    self.setCursor(Qt.ArrowCursor)
                else:
                    self.select_node(clicked_node)
                    self.dragging = True
                    self.drag_node = clicked_node
                    self.drag_offset = QPoint(
                        event.pos().x() - clicked_node.position[0],
                        event.pos().y() - clicked_node.position[1]
                    )
            elif clicked_connection:
                self.select_connection(clicked_connection)
                self.selected_nodes.clear()
            else:
                self.selected_nodes.clear()
                self.selected_connection = None
            self.update()
        elif event.button() == Qt.RightButton:
            self.show_context_menu(event.pos())

    def mouseMoveEvent(self, event):
        if self.dragging and self.drag_node:
            # Calculate new position using the stored offset
            new_x = event.pos().x() - self.drag_offset.x()
            new_y = event.pos().y() - self.drag_offset.y()
            
            # Optional: Snap to grid
            if self.show_grid:
                new_x = round(new_x / self.grid_size) * self.grid_size
                new_y = round(new_y / self.grid_size) * self.grid_size
            
            # Update node position
            self.drag_node.position = (new_x, new_y)
            self.update()
        
        # Update hover states
        self.hover_node = self.get_node_at_position(event.pos())
        self.hover_connection = self.get_connection_at_position(event.pos())
        if self.hover_node or self.hover_connection:
            self.setCursor(Qt.PointingHandCursor)
        else:
            self.setCursor(Qt.ArrowCursor)
        self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.dragging:
            self.dragging = False
            self.drag_node = None
            self.drag_offset = QPoint()
        self.update()

    def show_context_menu(self, pos):
        if not self.selected_nodes:
            return
            
        menu = QMenu(self)
        
        # Add shape submenu
        shape_menu = menu.addMenu("Shape")
        
        for shape_name in Node.SHAPES.values():
            shape_action = shape_menu.addAction(shape_name.capitalize())
            shape_action.triggered.connect(lambda checked, s=shape_name: self.change_node_shape(self.selected_nodes[0], s))
        
        # Add color submenu
        color_menu = menu.addMenu("Colors")
        
        bg_color = color_menu.addAction("Background Color")
        bg_color.triggered.connect(lambda: self.change_node_color(self.selected_nodes[0], "background"))
        
        border_color = color_menu.addAction("Border Color")
        border_color.triggered.connect(lambda: self.change_node_color(self.selected_nodes[0], "border"))
        
        text_color = color_menu.addAction("Text Color")
        text_color.triggered.connect(lambda: self.change_node_color(self.selected_nodes[0], "text"))
        
        duplicate = menu.addAction("Duplicate Node")
        duplicate.triggered.connect(lambda: self.duplicate_node(self.selected_nodes[0]))
        
        menu.exec_(self.mapToGlobal(pos))

    def change_node_color(self, node, color_type="background"):
        color = QColorDialog.getColor()
        if color.isValid():
            if color_type == "background":
                node.set_color(color.name())
            elif color_type == "border":
                node.set_border_color(color.name())
            elif color_type == "text":
                node.set_text_color(color.name())
            self.update()

    def change_node_shape(self, node, shape):
        """Change the shape of the node"""
        node.set_shape(shape)
        self.update()

    def duplicate_node(self, node):
        new_node = Node(node.title + " (copy)")
        new_node.style = node.style.copy()
        new_node.position = (node.position[0] + 20, node.position[1] + 20)
        self.nodes.append(new_node)
        self.update()

    def get_node_at_position(self, pos):
        for node in self.nodes:
            node_rect = QRect(node.position[0], node.position[1], 
                            node.style['size'][0], node.style['size'][1])
            if node_rect.contains(pos):
                return node
        return None

    def select_node(self, node):
        if node not in self.selected_nodes:
            self.selected_nodes = [node]
        else:
            self.selected_nodes.remove(node)

    def create_connection(self, node1, node2):
        """Create a connection between two nodes with improved error handling."""
        try:
            if not node1 or not node2:
                return False
                
            if node1 == node2:
                return False
                
            # Check if connection already exists (in either direction)
            for existing_conn in self.connections:
                n1, n2 = existing_conn
                if (n1 == node1 and n2 == node2) or (n1 == node2 and n2 == node1):
                    return False
            
            # Create new connection
            self.connections.append((node1, node2))
            self.update()
            return True
            
        except Exception as e:
            print(f"Error creating connection: {e}")
            return False

    def select_connection(self, connection):
        """Handle connection selection."""
        try:
            if self.selected_connection == connection:
                self.selected_connection = None
            else:
                self.selected_connection = connection
                self.selected_nodes.clear()
            self.update()
        except Exception as e:
            print(f"Error selecting connection: {e}")

    def start_connection_mode(self):
        try:
            if not self.selected_nodes:
                return
                
            if len(self.selected_nodes) > 1:
                return

            self.connection_mode = True
            self.connecting_node = self.selected_nodes[0]
            self.setCursor(Qt.CrossCursor)
            
        except Exception as e:
            print(f"Error starting connection mode: {e}")
            self.connection_mode = False
            self.connecting_node = None
            self.setCursor(Qt.ArrowCursor)

    def delete_selected_nodes(self):
        if self.selected_connection:
            self.delete_connection(self.selected_connection)
            self.selected_connection = None
        else:
            for node in self.selected_nodes:
                self.nodes.remove(node)
                # Remove connections involving this node
                self.connections = [c for c in self.connections 
                                  if node not in (c[0], c[1])]
            self.selected_nodes.clear()
        self.update()

    def get_connection_at_position(self, pos):
        """Get connection near the given position with improved error handling."""
        try:
            for conn in self.connections:
                if self._is_point_on_line(pos, conn):
                    return conn
            return None
        except Exception as e:
            print(f"Error in get_connection_at_position: {e}")
            return None

    def _is_point_on_line(self, point, connection):
        """Check if point is near the connection line."""
        try:
            node1, node2 = connection
            # Get center points of nodes
            p1 = QPoint(node1.position[0] + node1.style['size'][0]//2,
                       node1.position[1] + node1.style['size'][1]//2)
            p2 = QPoint(node2.position[0] + node2.style['size'][0]//2,
                       node2.position[1] + node2.style['size'][1]//2)
            
            # Calculate distance and check against tolerance
            distance = self._point_line_distance(point, p1, p2)
            return distance is not None and distance < 5.0  # 5.0 pixels tolerance
            
        except Exception as e:
            print(f"Error in _is_point_on_line: {e}")
            return False

    def _point_line_distance(self, point, line_start, line_end):
        """Calculate the distance from a point to a line segment."""
        try:
            # Convert points to float coordinates
            px, py = float(point.x()), float(point.y())
            x1, y1 = float(line_start.x()), float(line_start.y())
            x2, y2 = float(line_end.x()), float(line_end.y())
            
            # Calculate squared length of line segment
            length_sq = (x2 - x1) ** 2 + (y2 - y1) ** 2
            
            # If segment is actually a point, return distance to the point
            if length_sq == 0:
                return ((px - x1) ** 2 + (py - y1) ** 2) ** 0.5
            
            # Calculate projection parameter
            t = max(0, min(1, ((px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)) / length_sq))
            
            # Calculate closest point on line segment
            closest_x = x1 + t * (x2 - x1)
            closest_y = y1 + t * (y2 - y1)
            
            # Return distance to closest point
            return ((px - closest_x) ** 2 + (py - closest_y) ** 2) ** 0.5
            
        except (TypeError, ValueError) as e:
            print(f"Error in point_line_distance calculation: {e}")
            return None

    def delete_connection(self, connection):
        if connection in self.connections:
            self.connections.remove(connection)
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        if self.show_grid:
            self._draw_grid(painter)
        
        # Draw connections first (under nodes)
        for connection in self.connections:
            try:
                if connection == self.hover_connection:
                    pen = QPen(Qt.red, 2, Qt.DashLine)
                else:
                    pen = QPen(Qt.black, 2)
                painter.setPen(pen)
                self._draw_connection(painter, connection)
            except Exception as e:
                print(f"Error drawing connection: {e}")
        
        # Draw nodes on top
        for node in self.nodes:
            try:
                self._draw_node(painter, node)
            except Exception as e:
                print(f"Error drawing node: {e}")

    def _draw_node(self, painter, node):
        # Create gradient background
        gradient = QLinearGradient(
            node.position[0], node.position[1],
            node.position[0], node.position[1] + node.style['size'][1]
        )
        
        base_color = QColor(node.style['background'])
        gradient.setColorAt(0, base_color.lighter(120))
        gradient.setColorAt(1, base_color)
        
        # Draw shadow
        shadow_rect = QRect(
            node.position[0] + 3, node.position[1] + 3,
            node.style['size'][0], node.style['size'][1]
        )
        painter.setBrush(QColor(0, 0, 0, 30))
        painter.setPen(Qt.NoPen)
        painter.drawRect(shadow_rect)
        
        # Draw node with selected shape
        node_rect = QRect(
            node.position[0], node.position[1],
            node.style['size'][0], node.style['size'][1]
        )
        
        # Set pen based on selection state
        if node in self.selected_nodes:
            painter.setPen(QPen(QColor("#3399FF"), 2))
        elif node == self.hover_node:
            painter.setPen(QPen(QColor("#66CCFF"), 2))
        else:
            painter.setPen(QPen(QColor(node.style['border_color']), node.style['border_width']))
        
        painter.setBrush(QBrush(gradient))
        
        # Draw different shapes
        if node.style['shape'] == Node.SHAPES["rectangle"]:
            painter.drawRect(node_rect)
        elif node.style['shape'] == Node.SHAPES["ellipse"]:
            painter.drawEllipse(node_rect)
        elif node.style['shape'] == Node.SHAPES["rounded"]:
            painter.drawRoundedRect(node_rect, 15, 15)
        elif node.style['shape'] == Node.SHAPES["diamond"]:
            self._draw_diamond(painter, node_rect)
        elif node.style['shape'] == Node.SHAPES["hexagon"]:
            self._draw_hexagon(painter, node_rect)
        
        # Draw text with shadow
        painter.setPen(QColor(0, 0, 0, 127))
        painter.setFont(QFont('Arial', 10))
        painter.drawText(node_rect.adjusted(1, 1, 1, 1), Qt.AlignCenter, node.title)
        
        painter.setPen(QColor(node.style['color']))
        painter.drawText(node_rect, Qt.AlignCenter, node.title)

    def _draw_grid(self, painter):
        painter.setPen(QPen(QColor(200, 200, 200, 100), 1, Qt.DotLine))
        for x in range(0, self.width(), self.grid_size):
            painter.drawLine(x, 0, x, self.height())
        for y in range(0, self.height(), self.grid_size):
            painter.drawLine(0, y, self.width(), y)

    def _draw_connection(self, painter, connection):
        """Draw connection with arrow and improved visual feedback."""
        try:
            node1, node2 = connection
            # Calculate center points
            start = QPoint(
                node1.position[0] + node1.style['size'][0] // 2,
                node1.position[1] + node1.style['size'][1] // 2
            )
            end = QPoint(
                node2.position[0] + node2.style['size'][0] // 2,
                node2.position[1] + node2.style['size'][1] // 2
            )
            
            # Set line style based on selection state
            if connection == self.selected_connection:
                painter.setPen(QPen(Qt.red, 3))
            elif connection == self.hover_connection:
                painter.setPen(QPen(Qt.blue, 2, Qt.DashLine))
            else:
                painter.setPen(QPen(Qt.black, 2))
            
            # Draw main line
            painter.drawLine(start, end)
            
            # Draw arrow at end
            arrow_size = 10
            angle = 30  # degrees
            
            # Calculate arrow points
            dx = end.x() - start.x()
            dy = end.y() - start.y()
            length = (dx * dx + dy * dy) ** 0.5
            
            if length > 0:
                dx, dy = dx / length, dy / length
                
                # Calculate arrow points
                x1 = end.x() - arrow_size * (dx * 0.866 + dy * 0.5)
                y1 = end.y() - arrow_size * (dy * 0.866 - dx * 0.5)
                x2 = end.x() - arrow_size * (dx * 0.866 - dy * 0.5)
                y2 = end.y() - arrow_size * (dy * 0.866 + dx * 0.5)
                
                # Draw arrow
                painter.drawLine(end, QPoint(int(x1), int(y1)))
                painter.drawLine(end, QPoint(int(x2), int(y2)))

        except Exception as e:
            print(f"Error drawing connection: {e}")

    def _draw_diamond(self, painter, rect):
        """Draw a diamond shape"""
        path = QPainterPath()
        path.moveTo(rect.left() + rect.width()/2, rect.top())
        path.lineTo(rect.right(), rect.top() + rect.height()/2)
        path.lineTo(rect.left() + rect.width()/2, rect.bottom())
        path.lineTo(rect.left(), rect.top() + rect.height()/2)
        path.closeSubpath()
        painter.drawPath(path)

    def _draw_hexagon(self, painter, rect):
        """Draw a hexagon shape"""
        path = QPainterPath()
        w = rect.width()
        h = rect.height()
        x = rect.left()
        y = rect.top()
        
        path.moveTo(x + w/4, y)
        path.lineTo(x + 3*w/4, y)
        path.lineTo(x + w, y + h/2)
        path.lineTo(x + 3*w/4, y + h)
        path.lineTo(x + w/4, y + h)
        path.lineTo(x, y + h/2)
        path.closeSubpath()
        painter.drawPath(path)
