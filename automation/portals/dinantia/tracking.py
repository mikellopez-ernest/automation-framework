from __future__ import annotations

from collections.abc import Callable
from typing import Any

from playwright.sync_api import Locator, Response

from automation.core.elements import Elements
from automation.core.page import BasePage

from .constants import (
    DEFAULT_TIMEOUT_MS,
    TRACKING_PAGE_URL_FRAGMENT,
)

TRACKING_MENU_TEXT = "Seguiment"

DATE_RANGE_BUTTON_SELECTOR = (
    'button[aria-haspopup="listbox"]:has(svg[data-icon="calendar"])'
)

SELECTED_RANGE_SELECTOR = 'span[id$="-selected"]'
VISIBLE_LISTBOX_SELECTOR = 'ul[role="listbox"]:visible'

CHART_DATA_ENDPOINT = "/web/attitude/get_chart_data"
NETWORK_TIMEOUT_MS = 60_000


class DinantiaTrackingPage(BasePage):
    """Dinantia tracking page."""

    def open(self) -> None:
        """Open the tracking section."""
        self.logger.info("Opening tracking page")

        tracking_menu = Elements.role(
            self.page,
            "treeitem",
            TRACKING_MENU_TEXT,
        )

        tracking_menu.wait_for(
            state="visible",
            timeout=DEFAULT_TIMEOUT_MS,
        )

        tracking_menu.click()

        self.page.wait_for_url(
            lambda url: TRACKING_PAGE_URL_FRAGMENT in url,
            timeout=DEFAULT_TIMEOUT_MS,
        )

        self.logger.info(
            "Tracking page opened: %s",
            self.page.url,
        )

    def select_school_year(self, school_year: str) -> None:
        """Select a school year and wait for its chart data."""
        date_range_button = self._get_date_range_button()
        selected_range = self._get_selected_range(
            date_range_button,
        )

        self.logger.info(
            "Current tracking date range: %s",
            selected_range,
        )

        if selected_range == school_year:
            self.logger.info(
                "School year %s is already selected",
                school_year,
            )
            return

        self._open_date_range_selector(
            date_range_button,
        )

        school_year_option = self._get_school_year_option(
            school_year,
        )

        responses: list[dict[str, Any]] = []
        response_listener = self._create_response_listener(
            responses,
        )

        self.page.on(
            "response",
            response_listener,
        )

        try:
            self.logger.info(
                "Selecting school year %s",
                school_year,
            )

            with self.page.expect_response(
                self._is_chart_data_response,
                timeout=NETWORK_TIMEOUT_MS,
            ):
                school_year_option.click()

            self.page.wait_for_load_state(
                "networkidle",
                timeout=NETWORK_TIMEOUT_MS,
            )
        finally:
            self.page.remove_listener(
                "response",
                response_listener,
            )

        self._log_chart_responses(
            responses,
        )

        final_response = self._select_final_chart_response(
            responses,
        )

        self.logger.info(
            "School year %s loaded successfully with %d records",
            school_year,
            final_response["record_count"],
        )

    def _get_date_range_button(self) -> Locator:
        date_range_button = Elements.locator(
            self.page,
            DATE_RANGE_BUTTON_SELECTOR,
        ).first

        date_range_button.wait_for(
            state="visible",
            timeout=DEFAULT_TIMEOUT_MS,
        )

        return date_range_button

    @staticmethod
    def _get_selected_range(
        date_range_button: Locator,
    ) -> str:
        selected_text = date_range_button.locator(
            SELECTED_RANGE_SELECTOR,
        ).inner_text()

        return str(selected_text).strip()

    def _open_date_range_selector(
        self,
        date_range_button: Locator,
    ) -> None:
        self.logger.info(
            "Opening tracking date range selector",
        )

        date_range_button.scroll_into_view_if_needed()
        date_range_button.click()

    def _get_school_year_option(
        self,
        school_year: str,
    ) -> Locator:
        listbox = Elements.locator(
            self.page,
            VISIBLE_LISTBOX_SELECTOR,
        ).first

        listbox.wait_for(
            state="visible",
            timeout=DEFAULT_TIMEOUT_MS,
        )

        school_year_option = listbox.get_by_role(
            "option",
            name=school_year,
            exact=True,
        )

        school_year_option.wait_for(
            state="visible",
            timeout=DEFAULT_TIMEOUT_MS,
        )

        return school_year_option

    def _create_response_listener(
        self,
        responses: list[dict[str, Any]],
    ) -> Callable[[Response], None]:
        def collect_response(response: Response) -> None:
            if not self._is_chart_data_response(response):
                return

            response_data = self._read_chart_response(
                response,
            )

            responses.append(response_data)

        return collect_response

    @staticmethod
    def _is_chart_data_response(
        response: Response,
    ) -> bool:
        return response.request.method == "POST" and response.url.endswith(
            CHART_DATA_ENDPOINT,
        )

    @staticmethod
    def _read_chart_response(
        response: Response,
    ) -> dict[str, Any]:
        result: dict[str, Any] = {
            "status": response.status,
            "ok": response.ok,
            "url": response.url,
            "valid_json": False,
            "record_count": -1,
            "payload": None,
        }

        try:
            payload = response.json()
        except Exception:
            return result

        result["valid_json"] = True
        result["payload"] = payload

        if not isinstance(payload, dict):
            return result

        records = payload.get("data")

        if isinstance(records, list):
            result["record_count"] = len(records)

        return result

    def _log_chart_responses(
        self,
        responses: list[dict[str, Any]],
    ) -> None:
        if not responses:
            raise RuntimeError("Dinantia did not return any chart data response")

        self.logger.info(
            "Chart data responses received: %d",
            len(responses),
        )

        for index, response_data in enumerate(
            responses,
            start=1,
        ):
            self.logger.info(
                "Chart response %d: status=%s ok=%s valid_json=%s records=%s",
                index,
                response_data["status"],
                response_data["ok"],
                response_data["valid_json"],
                response_data["record_count"],
            )

    @staticmethod
    def _select_final_chart_response(
        responses: list[dict[str, Any]],
    ) -> dict[str, Any]:
        valid_responses = [
            response_data
            for response_data in responses
            if response_data["ok"]
            and response_data["valid_json"]
            and response_data["record_count"] >= 0
        ]

        if not valid_responses:
            raise RuntimeError("Dinantia chart data responses were not valid")

        return max(
            valid_responses,
            key=lambda response_data: response_data["record_count"],
        )
