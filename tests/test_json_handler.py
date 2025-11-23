"""Unit tests for JsonHandler."""

import pytest
from src.json_handler import JsonHandler


class TestJsonValidation:
    """Test JSON validation."""

    def test_is_valid_json_simple(self):
        """Test simple valid JSON."""
        assert JsonHandler.is_json('{"key": "value"}')
        assert JsonHandler.is_json('[]')
        assert JsonHandler.is_json('[1, 2, 3]')

    def test_is_valid_json_complex(self):
        """Test complex valid JSON."""
        json_str = '{"name": "John", "age": 30, "items": [1, 2, 3]}'
        assert JsonHandler.is_json(json_str)

    def test_is_valid_json_nested(self):
        """Test nested JSON."""
        json_str = '{"user": {"name": "John", "address": {"city": "NYC"}}}'
        assert JsonHandler.is_json(json_str)

    def test_is_invalid_json(self):
        """Test invalid JSON."""
        assert not JsonHandler.is_json('{invalid}')
        assert not JsonHandler.is_json('{"key": value}')
        assert not JsonHandler.is_json('[1, 2, ]')

    def test_is_json_empty_string(self):
        """Test empty string is not JSON."""
        assert not JsonHandler.is_json('')
        assert not JsonHandler.is_json('   ')

    def test_is_json_with_unicode(self):
        """Test JSON with unicode characters."""
        assert JsonHandler.is_json('{"emoji": "😀"}')
        assert JsonHandler.is_json('{"french": "café"}')

    def test_is_json_with_escape_sequences(self):
        """Test JSON with escape sequences."""
        assert JsonHandler.is_json('{"newline": "line1\\nline2"}')
        assert JsonHandler.is_json('{"tab": "col1\\tcol2"}')


class TestJsonFormatting:
    """Test JSON formatting."""

    def test_format_simple_json(self):
        """Test formatting simple JSON."""
        input_json = '{"key":"value","number":42}'
        formatted, success = JsonHandler.format_json(input_json)

        assert success
        assert '"key"' in formatted
        assert '"value"' in formatted
        assert formatted.count('\n') > 0  # Should have newlines

    def test_format_json_indentation(self):
        """Test JSON formatting with custom indentation."""
        input_json = '{"key":"value"}'
        formatted_2, success_2 = JsonHandler.format_json(input_json, indent=2)
        formatted_4, success_4 = JsonHandler.format_json(input_json, indent=4)

        assert success_2
        assert success_4
        # 4-space indentation should have more spaces
        assert formatted_4.count(' ') > formatted_2.count(' ')

    def test_format_array(self):
        """Test formatting array."""
        input_json = '[1,2,3,4,5]'
        formatted, success = JsonHandler.format_json(input_json)

        assert success
        assert formatted.count('\n') > 0

    def test_format_complex_json(self):
        """Test formatting complex nested JSON."""
        input_json = '{"users":[{"name":"John","age":30},{"name":"Jane","age":25}]}'
        formatted, success = JsonHandler.format_json(input_json)

        assert success
        assert '"users"' in formatted
        assert '"name"' in formatted

    def test_format_invalid_json(self):
        """Test formatting invalid JSON returns original."""
        input_json = '{invalid}'
        formatted, success = JsonHandler.format_json(input_json)

        assert not success
        assert formatted == input_json

    def test_format_empty_json(self):
        """Test formatting empty content."""
        formatted, success = JsonHandler.format_json('')
        assert not success
        assert formatted == ''

    def test_format_preserves_content(self):
        """Test that formatting preserves all content."""
        input_json = '{"key":"value","nested":{"inner":"data"}}'
        formatted, success = JsonHandler.format_json(input_json)

        assert success
        # Parse both to ensure they're equivalent
        import json
        assert json.loads(input_json) == json.loads(formatted)


class TestJsonMinification:
    """Test JSON minification."""

    def test_minify_simple_json(self):
        """Test minifying simple JSON."""
        input_json = '{\n  "key": "value"\n}'
        minified, success = JsonHandler.minify_json(input_json)

        assert success
        assert '\n' not in minified
        assert minified.count(' ') == 0

    def test_minify_preserves_content(self):
        """Test that minification preserves content."""
        input_json = '{"key": "value", "number": 42}'
        minified, success = JsonHandler.minify_json(input_json)

        assert success
        import json
        assert json.loads(input_json) == json.loads(minified)

    def test_minify_complex_json(self):
        """Test minifying complex JSON."""
        formatted = '''{
  "users": [
    {
      "name": "John",
      "age": 30
    }
  ]
}'''
        minified, success = JsonHandler.minify_json(formatted)

        assert success
        assert minified == '{"users":[{"name":"John","age":30}]}'

    def test_minify_invalid_json(self):
        """Test minifying invalid JSON."""
        input_json = '{invalid}'
        minified, success = JsonHandler.minify_json(input_json)

        assert not success
        assert minified == input_json

    def test_minify_empty(self):
        """Test minifying empty content."""
        minified, success = JsonHandler.minify_json('')
        assert not success
        assert minified == ''


class TestJsonError:
    """Test JSON error detection."""

    def test_get_json_error_valid(self):
        """Test getting error for valid JSON."""
        error = JsonHandler.get_json_error('{"key": "value"}')
        assert error is None

    def test_get_json_error_invalid(self):
        """Test getting error for invalid JSON."""
        error = JsonHandler.get_json_error('{invalid}')
        assert error is not None
        assert 'JSON Error' in error

    def test_get_json_error_empty(self):
        """Test getting error for empty content."""
        error = JsonHandler.get_json_error('')
        assert error is not None
        assert 'Empty' in error

    def test_get_json_error_with_line_info(self):
        """Test error includes line information."""
        json_str = '{\n"key": "value"\ninvalid\n}'
        error = JsonHandler.get_json_error(json_str)
        assert error is not None
        assert 'line' in error.lower()

    def test_get_json_error_unclosed_brace(self):
        """Test error for unclosed brace."""
        error = JsonHandler.get_json_error('{"key": "value"')
        assert error is not None

    def test_get_json_error_trailing_comma(self):
        """Test error for trailing comma."""
        error = JsonHandler.get_json_error('[1, 2, 3,]')
        assert error is not None


class TestJsonValidateFunction:
    """Test validate_json function."""

    def test_validate_valid_json(self):
        """Test validating valid JSON."""
        is_valid, error = JsonHandler.validate_json('{"key": "value"}')
        assert is_valid
        assert error is None

    def test_validate_invalid_json(self):
        """Test validating invalid JSON."""
        is_valid, error = JsonHandler.validate_json('{invalid}')
        assert not is_valid
        assert error is not None

    def test_validate_returns_error_message(self):
        """Test that validate returns helpful error message."""
        is_valid, error = JsonHandler.validate_json('["unclosed array"')
        assert not is_valid
        assert error is not None
        assert len(error) > 0

    def test_validate_empty(self):
        """Test validating empty content."""
        is_valid, error = JsonHandler.validate_json('')
        assert not is_valid
        assert error is not None


class TestJsonRoundTrip:
    """Test JSON round-trip operations."""

    def test_format_minify_roundtrip(self):
        """Test formatting then minifying preserves content."""
        original = '{"user": {"name": "John", "age": 30}}'

        formatted, format_success = JsonHandler.format_json(original)
        assert format_success

        minified, minify_success = JsonHandler.minify_json(formatted)
        assert minify_success

        import json
        assert json.loads(original) == json.loads(minified)

    def test_minify_format_roundtrip(self):
        """Test minifying then formatting preserves content."""
        original = '''
        {
            "users": [
                {"name": "John", "age": 30},
                {"name": "Jane", "age": 25}
            ]
        }
        '''

        minified, minify_success = JsonHandler.minify_json(original)
        assert minify_success

        formatted, format_success = JsonHandler.format_json(minified)
        assert format_success

        import json
        assert json.loads(original) == json.loads(formatted)


class TestJsonEdgeCases:
    """Test edge cases for JSON handling."""

    def test_empty_object(self):
        """Test handling empty object."""
        assert JsonHandler.is_json('{}')
        formatted, success = JsonHandler.format_json('{}')
        assert success

    def test_empty_array(self):
        """Test handling empty array."""
        assert JsonHandler.is_json('[]')
        formatted, success = JsonHandler.format_json('[]')
        assert success

    def test_null_value(self):
        """Test handling null value."""
        assert JsonHandler.is_json('{"key": null}')
        formatted, success = JsonHandler.format_json('{"key": null}')
        assert success

    def test_boolean_values(self):
        """Test handling boolean values."""
        assert JsonHandler.is_json('{"enabled": true, "disabled": false}')
        formatted, success = JsonHandler.format_json('{"enabled": true, "disabled": false}')
        assert success

    def test_negative_numbers(self):
        """Test handling negative numbers."""
        assert JsonHandler.is_json('{"temperature": -10, "balance": -99.99}')
        formatted, success = JsonHandler.format_json('{"temperature": -10}')
        assert success

    def test_scientific_notation(self):
        """Test handling scientific notation."""
        assert JsonHandler.is_json('{"value": 1.23e-4}')
        formatted, success = JsonHandler.format_json('{"value": 1.23e-4}')
        assert success

    def test_unicode_escape_sequences(self):
        """Test handling unicode escape sequences."""
        json_str = '{"emoji": "\\u0048\\u0065\\u006c\\u006c\\u006f"}'
        assert JsonHandler.is_json(json_str)
        formatted, success = JsonHandler.format_json(json_str)
        assert success
