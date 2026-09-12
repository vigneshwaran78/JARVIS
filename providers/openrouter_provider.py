from __future__ import annotations

import json
import ssl
import urllib.error
import urllib.request
from typing import Any

from logging_utils.request_logger import RequestLogger
from providers.llm_provider import LLMProvider


class OpenRouterProvider(LLMProvider):
    def __init__(
        self,
        api_key: str,
        model: str,
        site_url: str | None = None,
        app_name: str | None = None,
        request_logger: RequestLogger | None = None,
    ) -> None:
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY is required.")
        if not model:
            raise ValueError("OPENROUTER_MODEL is required.")

        self.api_key = api_key
        self.model = model
        self.site_url = site_url
        self.app_name = app_name
        self.url = "https://openrouter.ai/api/v1/chat/completions"
        self.request_logger = request_logger or RequestLogger()

    def chat(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
        }

        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        if self.site_url:
            headers["HTTP-Referer"] = self.site_url
        if self.app_name:
            headers["X-Title"] = self.app_name

        request = urllib.request.Request(
            self.url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        ssl_context = _create_ssl_context()
        log_path = self.request_logger.create_log("POST", self.url, headers, payload)

        try:
            with urllib.request.urlopen(request, timeout=60, context=ssl_context) as response:
                data = json.loads(response.read().decode("utf-8"))
                self.request_logger.save_response(log_path, response.status, data)
        except urllib.error.HTTPError as error:
            body = error.read().decode("utf-8")
            self.request_logger.save_error(log_path, error.code, body)
            raise RuntimeError(f"OpenRouter HTTP {error.code}: {body}") from error
        except urllib.error.URLError as error:
            self.request_logger.save_error(log_path, None, str(error.reason))
            if "CERTIFICATE_VERIFY_FAILED" in str(error.reason):
                raise RuntimeError(
                    "SSL certificate verification failed. Run `pip install certifi`, "
                    "then try `python main.py` again. On macOS Python.org installs, "
                    "you can also run the bundled `Install Certificates.command`."
                ) from error
            raise RuntimeError(f"Could not reach OpenRouter: {error.reason}") from error

        try:
            return data["choices"][0]
        except (KeyError, IndexError) as error:
            raise RuntimeError(f"Unexpected OpenRouter response: {data}") from error


def _create_ssl_context() -> ssl.SSLContext:
    try:
        import certifi
    except ImportError:
        return ssl.create_default_context()

    return ssl.create_default_context(cafile=certifi.where())
