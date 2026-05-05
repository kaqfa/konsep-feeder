from datetime import datetime, timedelta
from os import path
from typing import Any, Dict, Optional

import requests
from mage_ai.io.config import ConfigFileLoader
from mage_ai.settings.repo import get_repo_path


class FeederConnect:
    """Base Feeder API connection handler - handles authentication and basic requests"""

    def __init__(self, config_profile: str = "default"):
        """
        Initialize Feeder connection

        Args:
            config_profile: Profile name from io_config.yaml (default: 'default')
        """
        # Load config from io_config.yaml
        config_path = path.join(get_repo_path(), "io_config.yaml")
        self.config_loader = ConfigFileLoader(config_path, config_profile)

        self.url = self.config_loader.get("feeder_url")
        self.username = self.config_loader.get("feeder_username")
        self.password = self.config_loader.get("feeder_password")
        self.token = None
        self.token_expired = None

        # Get token on initialization
        self._get_token()

    def _get_token(self) -> str:
        """
        Get or refresh Feeder API token

        Returns:
            str: Feeder API token

        Raises:
            RuntimeError: If failed to connect or authenticate
        """
        # Check if token exists and not expired
        if self.token and self.token_expired:
            if datetime.now() < self.token_expired:
                return self.token

        # Request new token
        payload = {
            "act": "GetToken",
            "username": self.username,
            "password": self.password,
        }

        try:
            resp = requests.post(self.url, json=payload, timeout=30)
            resp.raise_for_status()
            json_data = resp.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to connect to Feeder API: {e}")
        except ValueError as e:
            raise RuntimeError(f"Invalid JSON response from Feeder API: {e}")

        # Validate response
        if not isinstance(json_data, dict):
            raise RuntimeError(
                f"Invalid Feeder API response format: expected dict, got {type(json_data)}"
            )

        if "error_code" not in json_data:
            raise RuntimeError(
                f"Feeder API response missing 'error_code' key: {json_data}"
            )

        error_code = json_data.get("error_code")

        if error_code == 0:
            if "data" not in json_data:
                raise RuntimeError(
                    f"Feeder API response missing 'data' key: {json_data}"
                )

            if "token" not in json_data["data"]:
                raise RuntimeError(
                    f"Feeder API response data missing 'token' key: {json_data}"
                )

            self.token = json_data["data"]["token"]
            # Token expires in 10 minutes
            self.token_expired = datetime.now() + timedelta(minutes=10)

            print(f"[FeederConnect] ✅ Successfully obtained Feeder token")
            return self.token
        else:
            raise RuntimeError(
                f"Feeder API authentication failed (error_code={error_code}): {json_data}"
            )

    def execute(
        self,
        action: str,
        type: str = "get",
        filter: Optional[str] = None,
        limit: int = 5000,
        offset: int = 0,
        order: Optional[str] = None,
        data: Optional[Dict] = None,
        key: Optional[str] = None,
        debug: bool = False,
        timeout: int = 120,
    ) -> Dict[str, Any]:
        """
        Execute Feeder API action

        Args:
            action: Feeder API action name (e.g., 'GetBiodataMahasiswa')
            type: Request type (get|insert|update|delete)
            filter: Optional filter string for WHERE clause
            limit: Page size limit
            offset: Pagination offset
            order: Optional order by clause (e.g., "id_tahun_ajaran desc")
            data: Data payload for insert/update
            key: Key for update/delete operations
            debug: Print payload for debugging

        Returns:
            Dict: Feeder API response

        Raises:
            RuntimeError: If request fails or returns error
        """
        if type == "get":
            payload = {
                "token": self.token,
                "act": action,
                "limit": limit,
                "offset": offset,
            }
            if filter:
                payload["filter"] = filter
            if order:
                payload["order"] = order
        elif type == "insert":
            payload = {"act": action, "token": self.token, "record": data}
        elif type == "update":
            payload = {"act": action, "token": self.token, "record": data, "key": key}
        elif type == "delete":
            payload = {"act": action, "token": self.token, "key": key}
        else:
            raise ValueError(
                f"Invalid type: {type}. Must be 'get', 'insert', 'update', or 'delete'"
            )

        if debug:
            print(f"[FeederConnect] Payload: {payload}")

        try:
            result = requests.post(self.url, json=payload, timeout=timeout)
            result.raise_for_status()
            json_res = result.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Feeder API request failed for action '{action}': {e}")
        except ValueError as e:
            raise RuntimeError(
                f"Invalid JSON response from Feeder API for action '{action}': {e}"
            )

        # Check for token expiration
        if "error_code" not in json_res:
            raise RuntimeError(
                f"Feeder API response missing 'error_code' for action '{action}': {json_res}"
            )

        if json_res["error_code"] in (100, 106):  # Token expired
            print(
                f"[FeederConnect] ⚠️ Token expired (error_code={json_res['error_code']}), refreshing..."
            )
            self._get_token()
            # Retry with new token
            return self.execute(
                action=action,
                type=type,
                filter=filter,
                limit=limit,
                offset=offset,
                order=order,
                data=data,
                key=key,
                debug=debug,
                timeout=timeout,
            )

        return json_res
