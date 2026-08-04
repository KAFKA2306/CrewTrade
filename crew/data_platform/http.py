from __future__ import annotations

import time
from datetime import timezone
from email.utils import parsedate_to_datetime
from typing import Mapping

import requests

from crew.data_platform.contracts import HttpPayload, utc_now


class HttpClient:
    """Small governed HTTP client with declared identity, retries, and rate limiting."""

    def __init__(
        self,
        *,
        user_agent: str,
        min_interval_seconds: float = 0.15,
        timeout_seconds: float = 30.0,
        max_attempts: int = 4,
    ) -> None:
        if not user_agent.strip():
            raise ValueError("A declared user agent is required for automated ingestion.")
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": user_agent,
                "Accept-Encoding": "gzip, deflate",
                "Accept": "application/json, application/xml, text/xml, text/csv, */*",
            }
        )
        self.min_interval_seconds = max(0.0, min_interval_seconds)
        self.timeout_seconds = timeout_seconds
        self.max_attempts = max_attempts
        self._last_request_at = 0.0

    def get(
        self,
        url: str,
        *,
        params: Mapping[str, object] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> HttpPayload:
        last_error: Exception | None = None
        for attempt in range(1, self.max_attempts + 1):
            self._throttle()
            try:
                response = self.session.get(
                    url,
                    params=params,
                    headers=dict(headers or {}),
                    timeout=self.timeout_seconds,
                )
                if response.status_code in {429, 500, 502, 503, 504}:
                    if attempt == self.max_attempts:
                        response.raise_for_status()
                    time.sleep(self._retry_delay(response.headers, attempt))
                    continue
                response.raise_for_status()
                retrieved_at = utc_now()
                date_header = response.headers.get("Date")
                if date_header:
                    try:
                        retrieved_at = parsedate_to_datetime(date_header).astimezone(
                            timezone.utc
                        )
                    except (TypeError, ValueError, OverflowError):
                        pass
                return HttpPayload(
                    body=response.content,
                    url=response.url,
                    status_code=response.status_code,
                    content_type=response.headers.get(
                        "Content-Type", "application/octet-stream"
                    ),
                    retrieved_at=retrieved_at,
                    headers=dict(response.headers),
                )
            except requests.RequestException as error:
                last_error = error
                if attempt == self.max_attempts:
                    raise
                time.sleep(min(2**attempt, 20))
        raise RuntimeError("HTTP request failed") from last_error

    def _throttle(self) -> None:
        elapsed = time.monotonic() - self._last_request_at
        if elapsed < self.min_interval_seconds:
            time.sleep(self.min_interval_seconds - elapsed)
        self._last_request_at = time.monotonic()

    @staticmethod
    def _retry_delay(headers: Mapping[str, str], attempt: int) -> float:
        retry_after = headers.get("Retry-After")
        if retry_after:
            try:
                return min(float(retry_after), 60.0)
            except ValueError:
                pass
        return min(2**attempt, 20)
