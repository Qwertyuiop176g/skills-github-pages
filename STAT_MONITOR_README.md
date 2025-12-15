# StatMonitor Image Processing Module

A Python module for adding stat monitoring headers to images with customizable text and logo overlays.

## Features

- Add stat headers to images with a single function call
- Cross-platform font support (Windows, macOS, Linux)
- Customizable positioning, colors, and sizing
- Optional logo overlay support
- Automatic text scaling to fit bounding box
- Debug mode for visualization

## Installation

Requires Python 3.6+ and Pillow:

```bash
pip install Pillow
```

## Quick Start

### Basic Usage

```python
from stat_monitor import process_image

# Process an image file
result = process_image("input.png", logo_path="logo.png")
result.save("output.png")
```

### Using PIL Image Object

```python
from PIL import Image
from stat_monitor import process_image

# Load image
img = Image.open("input.png")

# Process it
result = process_image(img, logo_path="logo.png")
result.save("output.png")
```

### Custom Positioning and Colors

```python
result = process_image(
    "input.png",
    x=100,              # X position of overlay
    y=100,              # Y position of overlay
    width=800,          # Width of overlay area
    height=400,         # Height of overlay area
    fill_color=(50, 50, 50, 255),  # RGBA background color
    logo_path="logo.png",
    debug=True          # Show debug rectangles
)
result.save("output.png")
```

### Custom Fonts

```python
result = process_image(
    "input.png",
    logo_path="logo.png",
    font_regular="/path/to/regular.ttf",
    font_bold="/path/to/bold.ttf"
)
result.save("output.png")
```

## API Reference

### `process_image()`

Main function to process an image with stat header overlay.

**Parameters:**
- `input_image` (str or PIL.Image): Either a PIL Image object or path to an image file
- `x` (int, optional): X coordinate of overlay area. Default: 4510
- `y` (int, optional): Y coordinate of overlay area. Default: 5050
- `width` (int, optional): Width of overlay area. Default: 1200
- `height` (int, optional): Height of overlay area. Default: 520
- `fill_color` (tuple, optional): RGBA tuple for background. Default: (44, 42, 44, 255)
- `logo_path` (str, optional): Path to logo image file. Default: None
- `debug` (bool, optional): Enable debug visualization. Default: False
- `font_regular` (str, optional): Path to regular font file. Default: System font
- `font_bold` (str, optional): Path to bold font file. Default: System font

**Returns:**
- PIL.Image: Processed image with stat header overlay

### `replace_area()`

Replace a rectangular area with solid color.

**Parameters:**
- `img` (PIL.Image): Image to modify
- `x` (int): X coordinate of top-left corner
- `y` (int): Y coordinate of top-left corner
- `width` (int): Width of area
- `height` (int): Height of area
- `fill_color` (tuple, optional): RGBA color. Default: (32, 32, 32, 255)

**Returns:**
- tuple: (x1, y1, x2, y2) actual coordinates used

### `draw_stat_header()`

Draw a scalable stat header on an image.

**Parameters:**
- `img` (PIL.Image): Image to draw on
- `box_x1`, `box_y1`, `box_x2`, `box_y2` (int): Bounding box coordinates
- `logo_path` (str, optional): Path to logo image
- `logo_scale` (float, optional): Logo scale factor. Default: 0.85
- `line_spacing_ratio` (float, optional): Line spacing ratio. Default: 0.18
- `min_font_size` (int, optional): Minimum font size. Default: 10
- `fill_box` (bool, optional): Scale text to fill box. Default: True
- `debug` (bool, optional): Show debug rectangles. Default: False
- `font_regular` (str, optional): Regular font path
- `font_bold` (str, optional): Bold font path

### `draw_bbox()`

Draw a red bounding box for debugging.

**Parameters:**
- `img` (PIL.Image): Image to draw on
- `x1`, `y1`, `x2`, `y2` (int): Box coordinates
- `width` (int, optional): Line width. Default: 2

## Platform Support

The module automatically detects the operating system and uses appropriate default fonts:

- **Windows**: Segoe UI (Regular and Bold)
- **macOS**: Helvetica
- **Linux**: DejaVu Sans or Liberation Sans (whichever is available)

You can override the default fonts by providing custom font paths.

## Examples

### Example 1: Simple Processing

```python
from stat_monitor import process_image

# Process with default settings
result = process_image("screenshot.png", logo_path="icon.png")
result.save("output.png")
```

### Example 2: Large Image Processing

```python
# For very large images (e.g., 4K or higher resolution)
result = process_image(
    "large_screenshot.png",
    x=4510,
    y=5050,
    width=1200,
    height=520,
    logo_path="icon.png"
)
result.save("output.png")
```

### Example 3: Debug Mode

```python
# Enable debug mode to see bounding boxes
result = process_image(
    "input.png",
    x=100,
    y=100,
    width=600,
    height=300,
    debug=True  # Shows red box around replacement area and green box around text
)
result.save("debug_output.png")
```

### Example 4: Batch Processing

```python
import os
from stat_monitor import process_image

# Process multiple images
input_dir = "screenshots"
output_dir = "processed"
logo = "logo.png"

for filename in os.listdir(input_dir):
    if filename.endswith((".png", ".jpg", ".jpeg")):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)
        
        result = process_image(input_path, logo_path=logo)
        result.save(output_path)
        print(f"Processed {filename}")
```

## Notes

- The module automatically converts images to RGBA mode for processing
- Logo images are resized to fit inline with text
- Text scaling automatically adjusts to fit within the specified bounding box
- The stat header includes:
  - Title: "StatMonitor v2.3 by SP#0305"
  - Current time range and date
  - OCR status
  - OS information
  - Discord link with logo
  - Version information

## License

This module is provided as-is for use in the skills-github-pages repository.
