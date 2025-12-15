#!/usr/bin/env python3
"""
Simple test to verify the stat_monitor module functionality.
"""

from stat_monitor import process_image, replace_area, draw_bbox, draw_stat_header
from PIL import Image


def test_module_imports():
    """Test that all functions can be imported"""
    print("✓ Module imports successful")


def test_create_test_image():
    """Test creating a simple test image"""
    # Create a test image (800x600 RGBA)
    img = Image.new('RGBA', (800, 600), color=(100, 100, 100, 255))
    assert img.size == (800, 600)
    print("✓ Test image creation successful")
    return img


def test_replace_area_function():
    """Test the replace_area function"""
    img = Image.new('RGBA', (800, 600), color=(100, 100, 100, 255))
    
    # Test basic replacement
    x1, y1, x2, y2 = replace_area(img, 10, 10, 100, 100, fill_color=(50, 50, 50, 255))
    assert x1 == 10
    assert y1 == 10
    assert x2 == 110
    assert y2 == 110
    print("✓ replace_area function works correctly")


def test_draw_bbox_function():
    """Test the draw_bbox function"""
    img = Image.new('RGBA', (800, 600), color=(100, 100, 100, 255))
    
    # Should not raise an error
    draw_bbox(img, 10, 10, 100, 100)
    print("✓ draw_bbox function works correctly")


def test_draw_stat_header_function():
    """Test the draw_stat_header function"""
    img = Image.new('RGBA', (800, 600), color=(100, 100, 100, 255))
    
    # Should not raise an error
    draw_stat_header(img, 10, 10, 400, 300)
    print("✓ draw_stat_header function works correctly")


def test_process_image_with_pil_image():
    """Test process_image with a PIL Image object"""
    img = Image.new('RGBA', (1000, 1000), color=(100, 100, 100, 255))
    
    # Process with default small area to fit in test image
    result = process_image(
        img,
        x=10,
        y=10,
        width=400,
        height=300
    )
    
    assert result.size == (1000, 1000)
    assert result.mode == 'RGBA'
    print("✓ process_image with PIL Image works correctly")


def test_process_image_with_custom_params():
    """Test process_image with custom parameters"""
    img = Image.new('RGBA', (1000, 1000), color=(100, 100, 100, 255))
    
    result = process_image(
        img,
        x=50,
        y=50,
        width=300,
        height=200,
        fill_color=(44, 42, 44, 255),
        debug=False
    )
    
    assert result.size == (1000, 1000)
    print("✓ process_image with custom parameters works correctly")


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("Running StatMonitor Module Tests")
    print("=" * 60)
    print()
    
    try:
        test_module_imports()
        test_create_test_image()
        test_replace_area_function()
        test_draw_bbox_function()
        test_draw_stat_header_function()
        test_process_image_with_pil_image()
        test_process_image_with_custom_params()
        
        print()
        print("=" * 60)
        print("All tests passed! ✓")
        print("=" * 60)
        return True
        
    except Exception as e:
        print()
        print("=" * 60)
        print(f"Test failed with error: {e}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
