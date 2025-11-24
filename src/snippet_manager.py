"""Snippet manager with built-in library and custom snippet support."""

import json
import os
from typing import List, Optional, Dict, Tuple
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path


@dataclass
class Snippet:
    """Represents a code snippet."""

    name: str  # Unique identifier
    title: str  # Display name
    content: str  # Snippet content
    language: str = "text"  # Programming language
    description: str = ""  # Human-readable description
    shortcut: Optional[str] = None  # Keyboard shortcut (e.g., "tab" or "Ctrl+Shift+P")
    tags: List[str] = field(default_factory=list)  # Tags for categorization
    created_at: datetime = field(default_factory=datetime.now)  # Creation timestamp
    updated_at: datetime = field(default_factory=datetime.now)  # Last update timestamp
    usage_count: int = 0  # How many times used
    custom: bool = False  # Whether this is a custom snippet

    def has_placeholder(self) -> bool:
        """Check if snippet contains placeholders.

        Returns:
            True if snippet has ${n} or similar placeholders
        """
        return "${" in self.content

    def get_placeholders(self) -> List[str]:
        """Get list of placeholder names in snippet.

        Returns:
            List of placeholder names
        """
        import re

        matches = re.findall(r"\$\{(\w+)\}", self.content)
        return matches

    def expand(self, replacements: Optional[Dict[str, str]] = None) -> str:
        """Expand snippet with placeholder replacements.

        Args:
            replacements: Dictionary of placeholder names to replacement values

        Returns:
            Expanded snippet content
        """
        expanded = self.content

        if replacements:
            import re

            for placeholder, value in replacements.items():
                pattern = r"\$\{" + re.escape(placeholder) + r"\}"
                expanded = re.sub(pattern, value, expanded)

        return expanded


class SnippetManager:
    """Manages code snippets with built-in library and custom storage."""

    BUILTIN_SNIPPETS = {
        # Python snippets
        "py_if": Snippet(
            name="py_if",
            title="Python if statement",
            content="if ${condition}:\n    ${body}",
            language="python",
            description="Python if statement with placeholder",
            tags=["python", "control-flow"],
        ),
        "py_for": Snippet(
            name="py_for",
            title="Python for loop",
            content="for ${item} in ${iterable}:\n    ${body}",
            language="python",
            description="Python for loop with placeholder",
            tags=["python", "control-flow", "loop"],
        ),
        "py_while": Snippet(
            name="py_while",
            title="Python while loop",
            content="while ${condition}:\n    ${body}",
            language="python",
            description="Python while loop with placeholder",
            tags=["python", "control-flow", "loop"],
        ),
        "py_try": Snippet(
            name="py_try",
            title="Python try-except",
            content="try:\n    ${code}\nexcept ${exception} as ${var}:\n    ${handler}",
            language="python",
            description="Python try-except block",
            tags=["python", "error-handling"],
        ),
        "py_func": Snippet(
            name="py_func",
            title="Python function",
            content='def ${function_name}(${params}):\n    """${docstring}"""\n    ${body}',
            language="python",
            description="Python function definition",
            tags=["python", "function"],
        ),
        "py_class": Snippet(
            name="py_class",
            title="Python class",
            content='class ${ClassName}:\n    """${docstring}"""\n    def __init__(self):\n        ${body}',
            language="python",
            description="Python class definition",
            tags=["python", "class"],
        ),
        "py_docstring": Snippet(
            name="py_docstring",
            title="Python docstring",
            content='"""\n${description}\n\nArgs:\n    ${args}: ${arg_desc}\n\nReturns:\n    ${return_desc}\n"""',
            language="python",
            description="Python docstring template",
            tags=["python", "documentation"],
        ),
        "py_main": Snippet(
            name="py_main",
            title="Python main block",
            content='if __name__ == "__main__":\n    ${body}',
            language="python",
            description="Python main entry point",
            tags=["python", "entry-point"],
        ),
        # JavaScript snippets
        "js_if": Snippet(
            name="js_if",
            title="JavaScript if statement",
            content="if (${condition}) {\n    ${body}\n}",
            language="javascript",
            description="JavaScript if statement",
            tags=["javascript", "control-flow"],
        ),
        "js_for": Snippet(
            name="js_for",
            title="JavaScript for loop",
            content="for (let ${i} = 0; ${i} < ${length}; ${i}++) {\n    ${body}\n}",
            language="javascript",
            description="JavaScript for loop",
            tags=["javascript", "control-flow", "loop"],
        ),
        "js_func": Snippet(
            name="js_func",
            title="JavaScript function",
            content="function ${functionName}(${params}) {\n    ${body}\n}",
            language="javascript",
            description="JavaScript function definition",
            tags=["javascript", "function"],
        ),
        "js_arrow": Snippet(
            name="js_arrow",
            title="JavaScript arrow function",
            content="const ${name} = (${params}) => {\n    ${body}\n};",
            language="javascript",
            description="JavaScript arrow function",
            tags=["javascript", "function", "es6"],
        ),
        # General snippets
        "comment": Snippet(
            name="comment",
            title="Comment",
            content="# ${comment}",
            language="text",
            description="Simple comment",
            tags=["comment"],
        ),
        "todo": Snippet(
            name="todo",
            title="TODO comment",
            content="# TODO: ${task}",
            language="text",
            description="TODO comment",
            tags=["comment", "todo"],
        ),
    }

    def __init__(self, config_dir: Optional[str] = None):
        """Initialize snippet manager.

        Args:
            config_dir: Directory for storing custom snippets (default: ~/.config/jtext)
        """
        if config_dir is None:
            config_dir = os.path.expanduser("~/.config/jtext")

        self.config_dir = Path(config_dir)
        self.snippets_file = self.config_dir / "snippets.json"
        self.snippets: Dict[str, Snippet] = {}

        # Load built-in snippets
        for snippet in self.BUILTIN_SNIPPETS.values():
            self.snippets[snippet.name] = snippet

        # Load custom snippets
        self._load_custom_snippets()

    def _load_custom_snippets(self) -> None:
        """Load custom snippets from config file."""
        if not self.snippets_file.exists():
            return

        try:
            with open(self.snippets_file, "r") as f:
                data = json.load(f)

            for snippet_data in data.get("snippets", []):
                snippet = self._dict_to_snippet(snippet_data)
                self.snippets[snippet.name] = snippet

        except (json.JSONDecodeError, KeyError):
            pass

    def _dict_to_snippet(self, data: Dict) -> Snippet:
        """Convert dictionary to Snippet object.

        Args:
            data: Dictionary with snippet data

        Returns:
            Snippet object
        """
        # Convert timestamp strings back to datetime
        if isinstance(data.get("created_at"), str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        if isinstance(data.get("updated_at"), str):
            data["updated_at"] = datetime.fromisoformat(data["updated_at"])

        return Snippet(**data)

    def _snippet_to_dict(self, snippet: Snippet) -> Dict:
        """Convert Snippet to dictionary for JSON serialization.

        Args:
            snippet: Snippet object

        Returns:
            Dictionary representation
        """
        data = asdict(snippet)
        # Convert datetime to ISO format strings
        data["created_at"] = snippet.created_at.isoformat()
        data["updated_at"] = snippet.updated_at.isoformat()
        return data

    def add_snippet(self, snippet: Snippet) -> None:
        """Add or update a snippet.

        Args:
            snippet: The snippet to add
        """
        snippet.custom = True
        snippet.updated_at = datetime.now()
        self.snippets[snippet.name] = snippet
        self._save_custom_snippets()

    def remove_snippet(self, name: str) -> bool:
        """Remove a custom snippet.

        Args:
            name: Name of snippet to remove

        Returns:
            True if removed, False if not found or built-in
        """
        if name not in self.snippets:
            return False

        snippet = self.snippets[name]
        if not snippet.custom:
            return False

        del self.snippets[name]
        self._save_custom_snippets()
        return True

    def get_snippet(self, name: str) -> Optional[Snippet]:
        """Get a snippet by name.

        Args:
            name: Name of snippet

        Returns:
            Snippet object or None
        """
        return self.snippets.get(name)

    def get_all_snippets(self) -> List[Snippet]:
        """Get all snippets.

        Returns:
            List of all snippets
        """
        return list(self.snippets.values())

    def get_snippets_by_language(self, language: str) -> List[Snippet]:
        """Get snippets for a specific language.

        Args:
            language: Programming language

        Returns:
            List of snippets for language
        """
        return [s for s in self.snippets.values() if s.language == language or s.language == "text"]

    def get_snippets_by_tag(self, tag: str) -> List[Snippet]:
        """Get snippets with a specific tag.

        Args:
            tag: Tag name

        Returns:
            List of snippets with tag
        """
        return [s for s in self.snippets.values() if tag in s.tags]

    def search_snippets(self, query: str) -> List[Snippet]:
        """Search snippets by name, title, or description.

        Args:
            query: Search query

        Returns:
            List of matching snippets
        """
        query_lower = query.lower()
        results = []

        for snippet in self.snippets.values():
            if (
                query_lower in snippet.name.lower()
                or query_lower in snippet.title.lower()
                or query_lower in snippet.description.lower()
            ):
                results.append(snippet)

        return results

    def use_snippet(self, name: str, replacements: Optional[Dict[str, str]] = None) -> Optional[str]:
        """Use a snippet and expand it.

        Args:
            name: Name of snippet
            replacements: Dictionary of placeholder replacements

        Returns:
            Expanded snippet content or None
        """
        snippet = self.get_snippet(name)
        if not snippet:
            return None

        snippet.usage_count += 1
        snippet.updated_at = datetime.now()

        if snippet.custom:
            self._save_custom_snippets()

        return snippet.expand(replacements)

    def get_top_used_snippets(self, limit: int = 10) -> List[Tuple[Snippet, int]]:
        """Get most used snippets.

        Args:
            limit: Maximum number to return

        Returns:
            List of (snippet, usage_count) tuples
        """
        sorted_snippets = sorted(self.snippets.values(), key=lambda s: s.usage_count, reverse=True)
        return [(s, s.usage_count) for s in sorted_snippets[:limit]]

    def get_recent_snippets(self, limit: int = 10) -> List[Snippet]:
        """Get recently updated snippets.

        Args:
            limit: Maximum number to return

        Returns:
            List of recently updated snippets
        """
        sorted_snippets = sorted(self.snippets.values(), key=lambda s: s.updated_at, reverse=True)
        return sorted_snippets[:limit]

    def get_languages(self) -> List[str]:
        """Get list of available languages.

        Returns:
            List of language names
        """
        languages = set()
        for snippet in self.snippets.values():
            if snippet.language != "text":
                languages.add(snippet.language)
        return sorted(languages)

    def get_tags(self) -> List[str]:
        """Get list of all tags used.

        Returns:
            List of tag names
        """
        tags = set()
        for snippet in self.snippets.values():
            tags.update(snippet.tags)
        return sorted(tags)

    def _save_custom_snippets(self) -> None:
        """Save custom snippets to file."""
        self.config_dir.mkdir(parents=True, exist_ok=True)

        custom_snippets = [
            self._snippet_to_dict(s) for s in self.snippets.values() if s.custom
        ]

        data = {"snippets": custom_snippets, "version": "1.0"}

        with open(self.snippets_file, "w") as f:
            json.dump(data, f, indent=2)

    def export_snippets(self, filepath: str, custom_only: bool = True) -> bool:
        """Export snippets to a file.

        Args:
            filepath: Path to export to
            custom_only: Only export custom snippets

        Returns:
            True if successful
        """
        try:
            snippets_to_export = [
                self._snippet_to_dict(s)
                for s in self.snippets.values()
                if not custom_only or s.custom
            ]

            data = {"snippets": snippets_to_export, "version": "1.0"}

            with open(filepath, "w") as f:
                json.dump(data, f, indent=2)

            return True

        except (IOError, OSError):
            return False

    def import_snippets(self, filepath: str, overwrite: bool = False) -> Tuple[int, int]:
        """Import snippets from a file.

        Args:
            filepath: Path to import from
            overwrite: Overwrite existing snippets with same name

        Returns:
            Tuple of (imported_count, skipped_count)
        """
        imported = 0
        skipped = 0

        try:
            with open(filepath, "r") as f:
                data = json.load(f)

            for snippet_data in data.get("snippets", []):
                snippet = self._dict_to_snippet(snippet_data)

                if snippet.name in self.snippets and not overwrite:
                    skipped += 1
                    continue

                self.add_snippet(snippet)
                imported += 1

            return imported, skipped

        except (IOError, OSError, json.JSONDecodeError, KeyError):
            return imported, skipped

    def clear_usage_stats(self) -> None:
        """Clear usage statistics for all snippets."""
        for snippet in self.snippets.values():
            snippet.usage_count = 0

    def get_statistics(self) -> Dict:
        """Get statistics about snippets.

        Returns:
            Dictionary with statistics
        """
        total_snippets = len(self.snippets)
        custom_count = sum(1 for s in self.snippets.values() if s.custom)
        builtin_count = total_snippets - custom_count
        total_uses = sum(s.usage_count for s in self.snippets.values())
        languages = len(self.get_languages())
        tags = len(self.get_tags())

        return {
            "total_snippets": total_snippets,
            "custom_snippets": custom_count,
            "builtin_snippets": builtin_count,
            "total_uses": total_uses,
            "languages": languages,
            "tags": tags,
        }
