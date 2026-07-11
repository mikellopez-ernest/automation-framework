from __future__ import annotations

from typing import Literal, TypeAlias

from playwright.sync_api import Locator, Page

AriaRole: TypeAlias = Literal[
    "button",
    "checkbox",
    "combobox",
    "dialog",
    "form",
    "heading",
    "link",
    "list",
    "listbox",
    "listitem",
    "menu",
    "menuitem",
    "navigation",
    "option",
    "radio",
    "row",
    "searchbox",
    "tab",
    "table",
    "textbox",
    "tree",
    "treeitem",
]


class Elements:
    """Factory for creating semantic Playwright locators."""

    @staticmethod
    def role(
        page: Page,
        role: AriaRole,
        name: str | None = None,
        *,
        exact: bool = True,
    ) -> Locator:
        """Locate an element by its accessibility role."""
        return page.get_by_role(
            role,
            name=name,
            exact=exact,
        )

    @staticmethod
    def button(
        page: Page,
        name: str,
        *,
        exact: bool = True,
    ) -> Locator:
        """Locate a button by its accessible name."""
        return Elements.role(
            page,
            "button",
            name,
            exact=exact,
        )

    @staticmethod
    def link(
        page: Page,
        name: str,
        *,
        exact: bool = True,
    ) -> Locator:
        """Locate a link by its accessible name."""
        return Elements.role(
            page,
            "link",
            name,
            exact=exact,
        )

    @staticmethod
    def textbox(
        page: Page,
        name: str,
        *,
        exact: bool = True,
    ) -> Locator:
        """Locate a textbox by its accessible name."""
        return Elements.role(
            page,
            "textbox",
            name,
            exact=exact,
        )

    @staticmethod
    def placeholder(
        page: Page,
        placeholder: str,
        *,
        exact: bool = True,
    ) -> Locator:
        """Locate an input by its placeholder."""
        return page.get_by_placeholder(
            placeholder,
            exact=exact,
        )

    @staticmethod
    def text(
        page: Page,
        text: str,
        *,
        exact: bool = True,
    ) -> Locator:
        """Locate an element by its visible text."""
        return page.get_by_text(
            text,
            exact=exact,
        )

    @staticmethod
    def locator(
        page: Page,
        selector: str,
    ) -> Locator:
        """Create a raw locator when no semantic locator is available."""
        return page.locator(selector)
