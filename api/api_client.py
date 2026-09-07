import requests
import allure

from utils.logger import get_logger


class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")
        self.logger = get_logger(__name__)
        self.headers = {}

    # ==========================================================
    # MASK SENSITIVE DATA
    # ==========================================================
    @staticmethod
    def _mask_headers(headers):
        if not headers:
            return headers
        masked_headers = headers.copy()

        for key in masked_headers:
            if key.lower() == "authorization":
                masked_headers[key] = "Bearer ***"
        return masked_headers

    @staticmethod
    def _mask_payload(payload):
        if not isinstance(payload, dict):
            return payload
        masked_payload = payload.copy()
        sensitive_fields = {
            "password",
            "accesstoken",
            "refreshtoken",
            "token",
            "secret"
        }
        for key in masked_payload:
            if key.lower() in sensitive_fields:
                masked_payload[key] = "***"
        return masked_payload

    # ==========================================================
    # RESPONSE LOGGING
    # ==========================================================
    def _log_response(self, method, url, response):
        status_code = response.status_code

        if 200 <= status_code < 300:
            self.logger.info(f"{method} {url} - Status: {status_code}")

        elif 400 <= status_code < 500:
            self.logger.warning(f"{method} {url} - Client Error: "f"{status_code}")

        elif status_code >= 500:
            self.logger.error(f"{method} {url} - Server Error: "f"{status_code}")

        else:
            self.logger.warning(f"{method} {url} - Unexpected Status: "f"{status_code}")
        self.logger.debug(f"{method} Response Body: {response.text}")

    # ==========================================================
    # ALLURE REQUEST
    # ==========================================================
    def _attach_request(self, method, url, params=None, headers=None, data=None, json=None):
        request_details = (
            f"Method: {method}\n"f"URL: {url}\n"f"Params: {params}\n"f"Headers: {headers}\n"f"Data: {data}\n"f"JSON: {json}"
        )
        allure.attach(request_details, name=f"{method} Request", attachment_type=allure.attachment_type.TEXT)

    # ==========================================================
    # ALLURE RESPONSE
    # ==========================================================
    def _attach_response(self, method, response):
        content_type = response.headers.get("content-type", "").lower()
        if "application/json" in content_type:
            attachment_type = allure.attachment_type.JSON
        else:
            attachment_type = allure.attachment_type.TEXT
        allure.attach(response.text, name=f"{method} Response - {response.status_code}",
                      attachment_type=attachment_type)

    # ==========================================================
    # COMMON REQUEST METHOD
    # ==========================================================
    def _request(self, method, endpoint, params=None, headers=None, data=None, json=None):
        url = f"{self.base_url}{endpoint}"
        # Start with default/client headers
        request_headers = self.headers.copy()
        # Add/override request-specific headers
        if headers is not None:
            request_headers.update(headers)
        masked_headers = self._mask_headers(request_headers)
        masked_json = self._mask_payload(json)
        # ------------------------------------------------------
        # DEBUG LOGGING
        # ------------------------------------------------------
        self.logger.debug(f"{method} URL: {url}")
        self.logger.debug(f"{method} Params: {params}")
        self.logger.debug(f"{method} Headers: {masked_headers}")
        self.logger.debug(f"{method} Request Body: {masked_json}")
        try:
            self._attach_request(method, url, params=params, headers=masked_headers, data=data, json=masked_json)
            # --------------------------------------------------
            # SEND REQUEST
            # --------------------------------------------------
            response = requests.request(
                method=method, url=url, params=params, headers=request_headers, data=data, json=json
            )
            # --------------------------------------------------
            # ATTACH RESPONSE TO ALLURE
            # --------------------------------------------------
            self._attach_response(method, response)
            # --------------------------------------------------
            # RESPONSE LOGGING
            # --------------------------------------------------
            self._log_response(method, url, response)
            return response
        except requests.exceptions.RequestException as e:
            self.logger.critical(f"{method} request failed completely: {e}")
            allure.attach(str(e), name=f"{method} Request Exception", attachment_type=allure.attachment_type.TEXT)
            raise

    # ==========================================================
    # GET
    # ==========================================================
    def get(self, endpoint, params=None, headers=None):
        return self._request("GET", endpoint, params=params, headers=headers)

    # ==========================================================
    # POST
    # ==========================================================
    def post(self, endpoint, data=None, json=None, params=None, headers=None):
        return self._request("POST", endpoint, data=data, json=json, params=params, headers=headers)

    # ==========================================================
    # PUT
    # ==========================================================
    def put(self, endpoint, data=None, json=None, params=None, headers=None):
        return self._request("PUT", endpoint, data=data, json=json, params=params, headers=headers)

    # ==========================================================
    # PATCH
    # ==========================================================
    def patch(self, endpoint, data=None, json=None, params=None, headers=None):
        return self._request("PATCH", endpoint, data=data, json=json, params=params, headers=headers)

    # ==========================================================
    # DELETE
    # ==========================================================
    def delete(self, endpoint, params=None, headers=None):
        return self._request("DELETE", endpoint, params=params, headers=headers)