# Mind Map Creator

## Overview
Mind Map Creator is a desktop application built with PyQt5, designed by Adrian Leśniak in 2023. It provides an intuitive interface for creating, editing, and organizing mind maps. Users can add nodes, connect them, customize appearances, save projects, and export to PDF.

## Features
- **Node Management**: Add, edit, move, and delete nodes with drag-and-drop support.
- **Customization**: Change node shapes, colors, and text via right-click options.
- **Connections**: Create links between nodes for structured mind maps.
- **File Operations**: Save mind maps and export them as PDF files.
- **User Interface**: Includes a toolbar, menu (File, Edit, Export, Help), and detailed instructions.

## Requirements
- Python 3.6+
- Libraries:
  - `PyQt5`

Install the required library using:
```bash
pip install PyQt5
```

## Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```
2. Install the required library (see Requirements).
3. Run the application:
   ```bash
   python main.py
   ```

## Usage
1. Launch the application to start creating a mind map.
2. **Controls**:
   - **Add Node**: Use the toolbar or Edit > Add Node to create nodes.
   - **Edit Node**: Double-click to edit text; right-click for shape/color options.
   - **Connect Nodes**: Select a node, click "Connect," then select another node.
   - **Move Nodes**: Drag nodes to reposition.
   - **Delete**: Select nodes and press Delete or use Edit > Delete.
   - **Save/Export**: Use File > Save or Export > Export as PDF.
   - **Help**: Access instructions via Help > Instructions.
3. Save your work or export to PDF for sharing.

## File Structure
- `main.py`: Main script containing the application logic and UI setup.
- `canvas.py`: (Assumed) Handles the mind map canvas and node rendering.
- `toolbar.py`: (Assumed) Defines the toolbar for quick access to tools.
- `README.md`: This file, providing project documentation.

## Notes
- The save and PDF export functionalities are placeholders (marked as TODO) and require implementation.
- Ensure `canvas.py` and `toolbar.py` are in the same directory as `main.py` or adjust import paths accordingly.
- The application assumes a basic structure for the canvas and toolbar modules, which are not provided in the code snippet.

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make changes and commit (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
For questions