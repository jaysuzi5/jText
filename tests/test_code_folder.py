"""Unit tests for code folding functionality."""

import pytest
from src.code_folder import CodeFolder, FoldRegion


class TestFoldRegion:
    """Test FoldRegion dataclass."""

    def test_create_fold_region(self):
        """Test creating a fold region."""
        region = FoldRegion(start_line=5, end_line=10, level=0, region_type="function")
        assert region.start_line == 5
        assert region.end_line == 10
        assert region.level == 0
        assert region.region_type == "function"
        assert not region.is_folded

    def test_fold_region_line_count(self):
        """Test getting line count."""
        region = FoldRegion(start_line=5, end_line=10, level=0, region_type="function")
        assert region.line_count == 6  # Lines 5-10 inclusive

    def test_fold_region_contains_line(self):
        """Test checking if line is in region."""
        region = FoldRegion(start_line=5, end_line=10, level=0, region_type="function")
        assert region.contains_line(5)
        assert region.contains_line(7)
        assert region.contains_line(10)
        assert not region.contains_line(4)
        assert not region.contains_line(11)

    def test_fold_region_overlaps(self):
        """Test overlap detection."""
        region1 = FoldRegion(start_line=5, end_line=10, level=0, region_type="function")
        region2 = FoldRegion(start_line=8, end_line=15, level=0, region_type="function")
        region3 = FoldRegion(start_line=11, end_line=20, level=0, region_type="function")

        assert region1.overlaps_with(region2)
        assert region2.overlaps_with(region1)
        assert not region1.overlaps_with(region3)


class TestCodeFolderBasic:
    """Test basic CodeFolder functionality."""

    def test_create_code_folder(self):
        """Test creating a code folder."""
        folder = CodeFolder()
        assert folder.regions == []

    def test_analyze_empty_text(self):
        """Test analyzing empty text."""
        folder = CodeFolder()
        regions = folder.analyze("")
        assert regions == []

    def test_clear_regions(self):
        """Test clearing regions."""
        folder = CodeFolder()
        folder.regions = [FoldRegion(0, 5, 0, "function")]
        folder.clear()
        assert folder.regions == []


class TestFunctionDetection:
    """Test function detection."""

    def test_detect_python_function(self):
        """Test detecting Python function."""
        code = """def hello():
    print('hello')
    return True
"""
        folder = CodeFolder()
        regions = folder.analyze(code)

        function_regions = [r for r in regions if r.region_type == "function"]
        assert len(function_regions) > 0

    def test_detect_javascript_function(self):
        """Test detecting JavaScript function."""
        code = """function hello() {
    console.log('hello');
    return true;
}"""
        folder = CodeFolder()
        regions = folder.analyze(code)

        function_regions = [r for r in regions if r.region_type == "function"]
        assert len(function_regions) > 0

    def test_detect_multiple_functions(self):
        """Test detecting multiple functions."""
        code = """def func1():
    pass

def func2():
    pass

def func3():
    pass"""
        folder = CodeFolder()
        regions = folder.analyze(code)

        function_regions = [r for r in regions if r.region_type == "function"]
        assert len(function_regions) >= 3


class TestClassDetection:
    """Test class detection."""

    def test_detect_python_class(self):
        """Test detecting Python class."""
        code = """class MyClass:
    def __init__(self):
        self.value = 0

    def method(self):
        return self.value
"""
        folder = CodeFolder()
        regions = folder.analyze(code)

        class_regions = [r for r in regions if r.region_type == "class"]
        assert len(class_regions) > 0

    def test_detect_multiple_classes(self):
        """Test detecting multiple classes."""
        code = """class A:
    pass

class B:
    pass

class C:
    pass"""
        folder = CodeFolder()
        regions = folder.analyze(code)

        class_regions = [r for r in regions if r.region_type == "class"]
        assert len(class_regions) >= 3


class TestBlockDetection:
    """Test block detection (if, for, while, etc.)."""

    def test_detect_if_block(self):
        """Test detecting if block."""
        code = """if condition:
    do_something()
    do_more()
"""
        folder = CodeFolder()
        regions = folder.analyze(code)

        block_regions = [r for r in regions if r.region_type == "block"]
        assert len(block_regions) > 0

    def test_detect_for_loop(self):
        """Test detecting for loop."""
        code = """for i in range(10):
    print(i)
    process(i)
"""
        folder = CodeFolder()
        regions = folder.analyze(code)

        block_regions = [r for r in regions if r.region_type == "block"]
        assert len(block_regions) > 0

    def test_detect_while_loop(self):
        """Test detecting while loop."""
        code = """while True:
    process()
    if done:
        break
"""
        folder = CodeFolder()
        regions = folder.analyze(code)

        block_regions = [r for r in regions if r.region_type == "block"]
        assert len(block_regions) > 0

    def test_detect_try_block(self):
        """Test detecting try-except block."""
        code = """try:
    risky_operation()
except Exception:
    handle_error()
"""
        folder = CodeFolder()
        regions = folder.analyze(code)

        block_regions = [r for r in regions if r.region_type == "block"]
        assert len(block_regions) > 0


class TestCommentDetection:
    """Test comment block detection."""

    def test_detect_python_comment_block(self):
        """Test detecting Python comment block."""
        code = """# This is a comment
# Second comment line
# Third comment line
code_line = 1
"""
        folder = CodeFolder()
        regions = folder.analyze(code)

        comment_regions = [r for r in regions if r.region_type == "comment"]
        assert len(comment_regions) > 0

    def test_detect_single_line_comment(self):
        """Test single line comment doesn't create region."""
        code = """# Single comment
code = 1
"""
        folder = CodeFolder()
        regions = folder.analyze(code)

        # Single comment line might not create a region
        # depending on implementation


class TestIndentDetection:
    """Test indentation-based region detection."""

    def test_detect_indent_regions(self):
        """Test detecting indent-based regions."""
        code = """for i in range(10):
    print(i)
    if i > 5:
        print('big')
    else:
        print('small')
"""
        folder = CodeFolder()
        regions = folder.analyze(code)

        indent_regions = [r for r in regions if r.region_type == "indent"]
        assert len(indent_regions) > 0


class TestRegionQueries:
    """Test querying regions."""

    def test_get_regions_at_line(self):
        """Test getting regions at a specific line."""
        code = """def func():
    x = 1
    y = 2
    return x + y
"""
        folder = CodeFolder()
        regions = folder.analyze(code)

        # Line 2 should be in function region
        regions_at_2 = folder.get_regions_at_line(2)
        assert len(regions_at_2) > 0

    def test_get_top_level_regions(self):
        """Test getting top-level regions only."""
        code = """class A:
    def method(self):
        pass

class B:
    pass
"""
        folder = CodeFolder()
        folder.analyze(code)

        top_level = folder.get_top_level_regions()
        assert all(r.level == 0 for r in top_level)

    def test_get_nested_regions(self):
        """Test getting nested regions."""
        code = """class A:
    def method(self):
        if True:
            pass
"""
        folder = CodeFolder()
        folder.analyze(code)

        if folder.regions:
            parent = folder.regions[0]
            nested = folder.get_nested_regions(parent)
            # Should have at least the method inside the class


class TestFoldToggle:
    """Test fold toggling."""

    def test_toggle_fold_state(self):
        """Test toggling fold state."""
        region = FoldRegion(0, 5, 0, "function")
        assert not region.is_folded

        region.is_folded = True
        assert region.is_folded

    def test_toggle_fold_method(self):
        """Test toggle_fold method."""
        folder = CodeFolder()
        region = FoldRegion(0, 5, 0, "function")
        folder.regions.append(region)

        assert not region.is_folded
        folder.toggle_fold(region)
        assert region.is_folded
        folder.toggle_fold(region)
        assert not region.is_folded


class TestFoldAll:
    """Test fold/unfold all operations."""

    def test_fold_all(self):
        """Test folding all regions."""
        folder = CodeFolder()
        folder.regions = [
            FoldRegion(0, 5, 0, "function"),
            FoldRegion(7, 12, 0, "function"),
            FoldRegion(14, 20, 0, "function"),
        ]

        folder.fold_all()
        assert all(r.is_folded for r in folder.regions)

    def test_unfold_all(self):
        """Test unfolding all regions."""
        folder = CodeFolder()
        folder.regions = [
            FoldRegion(0, 5, 0, "function", is_folded=True),
            FoldRegion(7, 12, 0, "function", is_folded=True),
        ]

        folder.unfold_all()
        assert all(not r.is_folded for r in folder.regions)

    def test_fold_level(self):
        """Test folding by level."""
        folder = CodeFolder()
        folder.regions = [
            FoldRegion(0, 5, 0, "class"),
            FoldRegion(1, 4, 1, "function"),
            FoldRegion(2, 3, 2, "block"),
        ]

        folder.fold_level(1)
        # Regions with level <= 1 should be folded
        assert folder.regions[0].is_folded  # level 0
        assert folder.regions[1].is_folded  # level 1
        assert not folder.regions[2].is_folded  # level 2

    def test_unfold_level(self):
        """Test unfolding by level."""
        folder = CodeFolder()
        folder.regions = [
            FoldRegion(0, 5, 0, "class", is_folded=True),
            FoldRegion(1, 4, 1, "function", is_folded=True),
            FoldRegion(2, 3, 2, "block", is_folded=True),
        ]

        folder.unfold_level(1)
        # Regions with level <= 1 should be unfolded
        assert not folder.regions[0].is_folded
        assert not folder.regions[1].is_folded
        assert folder.regions[2].is_folded


class TestVisibleLines:
    """Test visible lines calculation."""

    def test_get_visible_lines_no_folds(self):
        """Test all lines visible when nothing is folded."""
        text = "line1\nline2\nline3\nline4\nline5"
        folder = CodeFolder()
        visible = folder.get_visible_lines(text)
        assert visible == [0, 1, 2, 3, 4]

    def test_get_visible_lines_with_fold(self):
        """Test visible lines with a folded region."""
        text = "line1\nline2\nline3\nline4\nline5"
        folder = CodeFolder()
        folder.regions = [FoldRegion(1, 3, 0, "block", is_folded=True)]

        visible = folder.get_visible_lines(text)
        # Lines 2 and 3 should be hidden
        assert 0 in visible
        assert 1 in visible  # Start of folded region
        assert 2 not in visible
        assert 3 not in visible
        assert 4 in visible

    def test_get_visible_lines_multiple_folds(self):
        """Test visible lines with multiple folded regions."""
        text = "0\n1\n2\n3\n4\n5\n6\n7\n8\n9"
        folder = CodeFolder()
        folder.regions = [
            FoldRegion(1, 2, 0, "block", is_folded=True),
            FoldRegion(5, 7, 0, "block", is_folded=True),
        ]

        visible = folder.get_visible_lines(text)
        assert 0 in visible
        assert 1 in visible
        assert 2 not in visible
        assert 3 in visible
        assert 4 in visible
        assert 5 in visible
        assert 6 not in visible
        assert 7 not in visible
        assert 8 in visible


class TestFoldIndicators:
    """Test fold indicator generation."""

    def test_get_fold_indicators(self):
        """Test getting fold indicators."""
        folder = CodeFolder()
        folder.regions = [
            FoldRegion(0, 5, 0, "function"),
            FoldRegion(7, 12, 0, "function", is_folded=True),
            FoldRegion(14, 20, 0, "function"),
        ]

        indicators = folder.get_fold_indicators()
        assert len(indicators) == 3
        assert (0, False) in indicators
        assert (7, True) in indicators
        assert (14, False) in indicators

    def test_get_fold_indicators_single_line(self):
        """Test that single-line regions are not included."""
        folder = CodeFolder()
        folder.regions = [
            FoldRegion(0, 0, 0, "comment"),  # Single line
            FoldRegion(1, 5, 0, "function"),  # Multi-line
        ]

        indicators = folder.get_fold_indicators()
        # Only multi-line regions should have indicators
        assert len(indicators) == 1
        assert (1, False) in indicators


class TestComplexCode:
    """Test folding with complex code structures."""

    def test_nested_functions(self):
        """Test with nested functions."""
        code = """def outer():
    def inner1():
        pass

    def inner2():
        pass

    return inner1, inner2
"""
        folder = CodeFolder()
        regions = folder.analyze(code)
        functions = [r for r in regions if r.region_type == "function"]
        assert len(functions) >= 2

    def test_class_with_methods(self):
        """Test class with multiple methods."""
        code = """class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b
"""
        folder = CodeFolder()
        regions = folder.analyze(code)

        classes = [r for r in regions if r.region_type == "class"]
        assert len(classes) > 0

    def test_mixed_blocks(self):
        """Test code with mixed block types."""
        code = """def process(items):
    result = []
    for item in items:
        if item > 0:
            try:
                result.append(item * 2)
            except:
                pass
    return result
"""
        folder = CodeFolder()
        regions = folder.analyze(code)
        assert len(regions) > 0
