"""
StatMonitor Image Processing Module

This module provides functions to add stat headers to images with customizable
text and logo overlays. Originally designed for game stat monitoring.
"""

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import os
import platform


def replace_area(
    img,
    x,
    y,
    width,
    height,
    fill_color=(32, 32, 32, 255)
):
    """
    Replace a rectangular area of an image with a solid color.
    
    Args:
        img: PIL Image object to modify
        x: X coordinate of top-left corner
        y: Y coordinate of top-left corner
        width: Width of the area to replace
        height: Height of the area to replace
        fill_color: RGBA tuple for the fill color (default: dark gray)
    
    Returns:
        Tuple of (x1, y1, x2, y2) representing the actual coordinates used
    
    Raises:
        ValueError: If the resulting box is invalid
    """
    W, H = img.size

    # Ensure all values are integers
    x = int(x)
    y = int(y)
    width = int(width)
    height = int(height)

    x1 = max(0, x)
    y1 = max(0, y)
    x2 = min(W, x + width)
    y2 = min(H, y + height)

    if x2 <= x1 or y2 <= y1:
        raise ValueError(f"Invalid replacement box: x1={x1}, y1={y1}, x2={x2}, y2={y2}, image size={W}x{H}")

    draw = ImageDraw.Draw(img)
    draw.rectangle([x1, y1, x2, y2], fill=fill_color)

    return x1, y1, x2, y2


def draw_bbox(img, x1, y1, x2, y2, width=2):
    """
    Draw a red bounding box on the image (for debugging).
    
    Args:
        img: PIL Image object to draw on
        x1: Left X coordinate
        y1: Top Y coordinate
        x2: Right X coordinate
        y2: Bottom Y coordinate
        width: Line width in pixels (default: 2)
    """
    draw = ImageDraw.Draw(img)
    draw.rectangle(
        [x1, y1, x2, y2],
        outline=(255, 0, 0, 255),
        width=width
    )


def _get_default_fonts():
    """
    Get platform-appropriate default font paths.
    
    Returns:
        Tuple of (regular_font_path, bold_font_path)
    """
    system = platform.system()
    
    if system == "Windows":
        return (
            r"C:\Windows\Fonts\segoeui.ttf",
            r"C:\Windows\Fonts\segoeuib.ttf"
        )
    elif system == "Darwin":  # macOS
        return (
            "/System/Library/Fonts/Helvetica.ttc",
            "/System/Library/Fonts/Helvetica.ttc"
        )
    else:  # Linux
        # Common paths for Linux systems
        possible_fonts = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/TTF/DejaVuSans.ttf",
        ]
        for font_path in possible_fonts:
            if os.path.exists(font_path):
                return (font_path, font_path)
        # Fallback to default PIL font
        return (None, None)


def draw_stat_header(
    img,
    box_x1,
    box_y1,
    box_x2,
    box_y2,
    logo_path=None,
    logo_scale=0.85,
    line_spacing_ratio=0.18,
    min_font_size=10,
    fill_box=True,
    debug=False,
    font_regular=None,
    font_bold=None,
):
    """
    Draw a scalable stat header with inline logo on an image.
    
    Args:
        img: PIL Image object to draw on
        box_x1: Left X coordinate of bounding box
        box_y1: Top Y coordinate of bounding box
        box_x2: Right X coordinate of bounding box
        box_y2: Bottom Y coordinate of bounding box
        logo_path: Path to logo image file (optional)
        logo_scale: Scale factor for logo relative to text height (default: 0.85)
        line_spacing_ratio: Ratio of line spacing to font size (default: 0.18)
        min_font_size: Minimum font size in pixels (default: 10)
        fill_box: Whether to scale text to fill the box (default: True)
        debug: Draw debug rectangles showing bounds (default: False)
        font_regular: Path to regular font file (optional, uses system default if None)
        font_bold: Path to bold font file (optional, uses system default if None)
    """
    draw = ImageDraw.Draw(img)

    # Ensure all coordinates are integers
    box_x1 = int(box_x1)
    box_y1 = int(box_y1)
    box_x2 = int(box_x2)
    box_y2 = int(box_y2)

    box_w = box_x2 - box_x1
    box_h = box_y2 - box_y1

    # Debug: replacement box
    if debug: 
        draw.rectangle(
            [box_x1, box_y1, box_x2, box_y2],
            outline=(255, 0, 0, 200),
            width=2
        )

    # Get font paths
    if font_regular is None or font_bold is None:
        default_regular, default_bold = _get_default_fonts()
        font_regular = font_regular or default_regular
        font_bold = font_bold or default_bold

    FONT_REG = font_regular
    FONT_BOLD = font_bold

    BASE_TITLE = 23
    BASE_SUB   = 22
    BASE_BODY  = 19

    # Colors
    C_TITLE = (180, 179, 180, 255)
    C_SP    = (234, 90, 32, 255)
    C_TIME  = (249, 213, 61, 255)
    C_OCR_L = (210, 210, 210, 255)
    C_OCR_V = (75, 202, 38, 255)
    C_OS    = (9, 164, 206, 255)
    C_LINK  = (50, 97, 191, 255)
    C_VER   = (164, 113, 190, 255)

    base_spacing = int(BASE_BODY * line_spacing_ratio)

    # Get current date and time
    now = datetime.now()
    current_hour = now.hour
    next_hour = (current_hour + 1) % 24
    time_range = f"{current_hour:02d}:00 - {next_hour:02d}:00"
    date_str = now.strftime("%B %d, %Y")
    datetime_text = f"{time_range} • {date_str}"

    # Load logo
    logo_img = None
    if logo_path and os.path.exists(logo_path): 
        logo_img = Image.open(logo_path).convert("RGBA")

    # Font builder
    def build_fonts(scale):
        fonts = {}
        if FONT_BOLD:
            try:
                fonts["title"] = ImageFont.truetype(FONT_BOLD, max(min_font_size, int(BASE_TITLE * scale)))
                fonts["sub"] = ImageFont.truetype(FONT_BOLD, max(min_font_size, int(BASE_SUB * scale)))
                fonts["body"] = ImageFont.truetype(FONT_BOLD, max(min_font_size, int(BASE_BODY * scale)))
            except Exception as e:
                # Fallback to default font
                default_font = ImageFont.load_default()
                fonts["title"] = default_font
                fonts["sub"] = default_font
                fonts["body"] = default_font
        else:
            default_font = ImageFont.load_default()
            fonts["title"] = default_font
            fonts["sub"] = default_font
            fonts["body"] = default_font
        return fonts

    # Text lines (logo inline on last line)
    def lines_def(fonts, scale):
        body = fonts["body"]
        logo_w = logo_h = 0

        if logo_img:
            logo_h = int(body.size * logo_scale) if hasattr(body, 'size') else int(10 * logo_scale)
            ratio = logo_h / logo_img.height
            logo_w = int(logo_img.width * ratio)

        return [
            [("StatMonitor v2.3 ", fonts["body"], C_TITLE),
             ("by SP#0305", fonts["body"], C_SP)],

            [(datetime_text, fonts["body"], C_TIME)],

            [("OCR:  ", body, C_OCR_L),
             ("Enabled (en-US)", body, C_OCR_V)],

            [("Windows 11 Enterprise", body, C_OS)],

            [
                ("discord.gg/natromacro  ", body, C_LINK),
                ("<LOGO>", (logo_w, logo_h), None),
                ("  Natro v1.0.1", body, C_VER),
            ],
        ]

    # Measure block
    def measure(scale):
        fonts = build_fonts(scale)
        max_w = 0
        total_h = 0

        for line in lines_def(fonts, scale):
            line_w = 0
            line_h = 0

            for item in line:
                if item[0] == "<LOGO>":
                    w, h = item[1]
                else:
                    text, font, _ = item
                    w = draw.textlength(text, font=font)
                    h = font.size if hasattr(font, 'size') else 10

                line_w += w
                line_h = max(line_h, h)

            max_w = max(max_w, line_w)
            total_h += line_h + int(base_spacing * scale)

        total_h -= int(base_spacing * scale)
        return max_w, total_h

    # Scaling
    scale = 1.0
    for _ in range(40):
        tw, th = measure(scale)
        if tw <= box_w and th <= box_h:
            scale *= 1.04 if fill_box else 1.0
        else:
            scale /= 1.04
            break

    fonts = build_fonts(scale)
    spacing = int(base_spacing * scale)
    text_w, text_h = measure(scale)

    # Center block
    x0 = box_x1 + (box_w - text_w) // 2
    y0 = box_y1 + (box_h - text_h) // 2

    # Debug: text bounds
    if debug:
        draw.rectangle(
            [x0, y0, x0 + text_w, y0 + text_h],
            outline=(0, 255, 0, 200),
            width=2
        )

    # Draw text & logo
    cy = y0
    for line_idx, line in enumerate(lines_def(fonts, scale)):
        line_w = sum(
            (item[1][0] if item[0] == "<LOGO>" else draw.textlength(item[0], font=item[1]))
            for item in line
        )
        cx = x0 + (text_w - line_w) // 2

        # Get the tallest font in this line for baseline calculation
        max_font_size = max(
            (item[1][1] if item[0] == "<LOGO>" else (item[1].size if hasattr(item[1], 'size') else 10))
            for item in line
        )
        
        # Get the dominant font for this line
        if line_idx == 0:
            # First line - use tallest font
            tallest_font = max((item[1] for item in line if item[0] != "<LOGO>"), key=lambda f: f.size if hasattr(f, 'size') else 10)
            if hasattr(tallest_font, 'getmetrics'):
                ascent, descent = tallest_font.getmetrics()
            else:
                ascent, descent = 8, 2
        else:
            # Other lines - use body font
            if hasattr(fonts["body"], 'getmetrics'):
                ascent, descent = fonts["body"].getmetrics()
            else:
                ascent, descent = 8, 2
        
        baseline_y = cy + ascent
        
        # Draw all items in the line
        for item in line:
            if item[0] == "<LOGO>":
                # Skip logo if no logo_img is provided
                if logo_img:
                    # Get the current line's font for proper sizing
                    line_font = fonts["body"]
                    line_font_size = line_font.size if hasattr(line_font, 'size') else 10
                    
                    # Make logo same height as the font on this line
                    lh = line_font_size
                    ratio = lh / logo_img.height
                    lw = int(logo_img.width * ratio)
                    
                    # Align bottom of logo with baseline + custom shift
                    logo_shift = +9  # Negative = shift up, Positive = shift down
                    ly = int(baseline_y - lh + logo_shift)
                    
                    logo_resized = logo_img.resize((lw, lh), Image.LANCZOS)
                    img.alpha_composite(logo_resized, (int(cx), int(ly)))
                    cx += lw
                # If no logo, just skip this item (don't add width)
            else:  
                text, font, color = item
                # Align text to baseline
                if hasattr(font, 'getmetrics'):
                    text_ascent, text_descent = font.getmetrics()
                else:
                    text_ascent, text_descent = 8, 2
                text_y = baseline_y - text_ascent
                draw.text((cx, text_y), text, font=font, fill=color)
                cx += draw.textlength(text, font=font)

        cy += max_font_size + spacing


def process_image(
    input_image,
    x=4510,
    y=5050,
    width=1200,
    height=520,
    fill_color=(44, 42, 44, 255),
    logo_path=None,
    debug=False,
    font_regular=None,
    font_bold=None,
):
    """
    Process an image by adding a stat header overlay.
    
    This is the main function that combines replace_area and draw_stat_header
    to create a complete stat monitoring overlay on an image.
    
    Args:
        input_image: Either a PIL Image object or a path to an image file
        x: X coordinate of the overlay area (default: 4510)
        y: Y coordinate of the overlay area (default: 5050)
        width: Width of the overlay area (default: 1200)
        height: Height of the overlay area (default: 520)
        fill_color: RGBA tuple for background fill (default: dark gray)
        logo_path: Path to logo image file (optional)
        debug: Enable debug visualization (default: False)
        font_regular: Path to regular font file (optional)
        font_bold: Path to bold font file (optional)
    
    Returns:
        PIL Image object with the stat header applied
    
    Example:
        >>> from PIL import Image
        >>> img = Image.open("input.png")
        >>> result = process_image(img, logo_path="logo.png")
        >>> result.save("output.png")
        
        Or with a file path:
        >>> result = process_image("input.png", logo_path="logo.png")
        >>> result.save("output.png")
    """
    # Load image if a path is provided
    if isinstance(input_image, str):
        img = Image.open(input_image).convert("RGBA")
    else:
        img = input_image.convert("RGBA")
    
    # Replace the area with solid color
    x1, y1, x2, y2 = replace_area(
        img,
        x, y,
        width, height,
        fill_color=fill_color
    )
    
    # Draw the stat header
    draw_stat_header(
        img,
        x1, y1, x2, y2,
        logo_path=logo_path,
        debug=debug,
        font_regular=font_regular,
        font_bold=font_bold,
    )
    
    return img


# Example usage (commented out - uncomment and modify paths to test)
if __name__ == "__main__":
    # Example 1: Using file paths
    # result = process_image(
    #     r"C:\Users\Qwerty\Downloads\test.png",
    #     logo_path=r"C:\Users\Qwerty\Downloads\icon.png"
    # )
    # result.save(r"C:\Users\Qwerty\Downloads\output.png")
    
    # Example 2: Using PIL Image object
    # from PIL import Image
    # img = Image.open(r"C:\Users\Qwerty\Downloads\test.png")
    # result = process_image(img, logo_path=r"C:\Users\Qwerty\Downloads\icon.png")
    # result.save(r"C:\Users\Qwerty\Downloads\output.png")
    
    # Example 3: Custom positioning and colors
    # result = process_image(
    #     "input.png",
    #     x=100,
    #     y=100,
    #     width=800,
    #     height=400,
    #     fill_color=(50, 50, 50, 255),
    #     logo_path="logo.png",
    #     debug=True
    # )
    # result.save("output.png")
    
    print("StatMonitor module loaded. Import and use process_image() to process images.")
