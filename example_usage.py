#!/usr/bin/env python3
"""
Example script demonstrating how to use the stat_monitor module.

This script shows various ways to use the process_image function to add
stat headers to images.
"""

from stat_monitor import process_image
from PIL import Image


def example_1_basic():
    """Example 1: Basic usage with file path"""
    print("Example 1: Basic usage")
    print("-" * 50)
    print("# Process an image file directly")
    print("result = process_image('input.png', logo_path='logo.png')")
    print("result.save('output.png')")
    print()


def example_2_pil_image():
    """Example 2: Using PIL Image object"""
    print("Example 2: Using PIL Image object")
    print("-" * 50)
    print("from PIL import Image")
    print("img = Image.open('input.png')")
    print("result = process_image(img, logo_path='logo.png')")
    print("result.save('output.png')")
    print()


def example_3_custom_positioning():
    """Example 3: Custom positioning and colors"""
    print("Example 3: Custom positioning and colors")
    print("-" * 50)
    print("result = process_image(")
    print("    'input.png',")
    print("    x=100,              # X position of overlay")
    print("    y=100,              # Y position of overlay")
    print("    width=800,          # Width of overlay area")
    print("    height=400,         # Height of overlay area")
    print("    fill_color=(50, 50, 50, 255),  # RGBA background color")
    print("    logo_path='logo.png',")
    print("    debug=True          # Show debug rectangles")
    print(")")
    print("result.save('output.png')")
    print()


def example_4_custom_fonts():
    """Example 4: Custom fonts"""
    print("Example 4: Custom fonts")
    print("-" * 50)
    print("result = process_image(")
    print("    'input.png',")
    print("    logo_path='logo.png',")
    print("    font_regular='/path/to/regular.ttf',")
    print("    font_bold='/path/to/bold.ttf'")
    print(")")
    print("result.save('output.png')")
    print()


def example_5_batch_processing():
    """Example 5: Batch processing multiple images"""
    print("Example 5: Batch processing")
    print("-" * 50)
    print("import os")
    print("from stat_monitor import process_image")
    print()
    print("input_dir = 'screenshots'")
    print("output_dir = 'processed'")
    print("logo = 'logo.png'")
    print()
    print("for filename in os.listdir(input_dir):")
    print("    if filename.endswith(('.png', '.jpg', '.jpeg')):")
    print("        input_path = os.path.join(input_dir, filename)")
    print("        output_path = os.path.join(output_dir, filename)")
    print("        ")
    print("        result = process_image(input_path, logo_path=logo)")
    print("        result.save(output_path)")
    print("        print(f'Processed {filename}')")
    print()


def main():
    """Display all examples"""
    print("=" * 70)
    print("StatMonitor Image Processing - Usage Examples")
    print("=" * 70)
    print()
    
    example_1_basic()
    example_2_pil_image()
    example_3_custom_positioning()
    example_4_custom_fonts()
    example_5_batch_processing()
    
    print("=" * 70)
    print("For more information, see STAT_MONITOR_README.md")
    print("=" * 70)


if __name__ == "__main__":
    main()
