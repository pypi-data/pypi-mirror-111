import base64
import time
from typing import TYPE_CHECKING, List, Optional

import requests
from Crypto.Cipher import AES
from Crypto.Hash import CMAC

from .const import APIGW_URL, IOT_EP, OFFICIALAPI_URL, AuthType
from .helper import CHSesame2MechStatus
from .history import CHSesame2History

if TYPE_CHECKING:
    from .chsesame2 import CHSesame2, CHSesame2CMD


class SesameCloud:
    def __init__(self, device: "CHSesame2") -> None:
        """Construct and send a Request to the cloud.

        Args:
            device (CHSesame2): The device for which you want to query.
        """
        self._device = device

    def requestAPI(
        self, method: str, url: str, json: Optional[dict] = None
    ) -> requests.Response:
        """A Wrapper of `requests.request`.

        Args:
            method (str): HTTP method to use: `GET`, `OPTIONS`, `HEAD`, `POST`, `PUT`, `PATCH`, or `DELETE`.
            url (str): URL to send.
            json (Optional[dict], optional): JSON data for the body to attach to the request. Defaults to `None`.

        Raises:
            RuntimeError: An HTTP error occurred.

        Returns:
            requests.Response: The server's response to an HTTP request.
        """
        try:
            response = requests.request(
                method,
                url,
                json=json,
                auth=self._device.authenticator,
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise RuntimeError(e)

        return response

    def getSign(self) -> str:
        """Generate a AES-CMAC tag.

        Returns:
            str: AES-CMAC tag.
        """
        unixtime = int(time.time())
        secret = self._device.getSecretKey()
        cobj = CMAC.new(secret, ciphermod=AES)
        cobj.update(unixtime.to_bytes(4, "little")[1:4])
        sign = cobj.hexdigest()

        return sign

    def getMechStatus(self) -> CHSesame2MechStatus:
        """Retrive a mechanical status of a device.

        Returns:
            CHSesame2MechStatus: Current mechanical status of the device.
        """
        if self._device.authenticator.login_method == AuthType.WebAPI:
            url = "{}/{}".format(OFFICIALAPI_URL, self._device.getDeviceUUID())
            response = self.requestAPI("GET", url)
            r_json = response.json()
            return CHSesame2MechStatus(dictdata=r_json)
        else:
            url = "https://{}/things/sesame2/shadow?name={}".format(
                IOT_EP, self._device.getDeviceUUID()
            )

            response = self.requestAPI("GET", url)
            r_json = response.json()
            return CHSesame2MechStatus(rawdata=r_json["state"]["reported"]["mechst"])

    def sendCmd(self, cmd: "CHSesame2CMD", history_tag: str = "pysesame3") -> bool:
        """Send a locking/unlocking command.

        Args:
            cmd (CHSesame2CMD): Lock, Unlock and Toggle.
            history_tag (CHSesame2CMD): The key tag to sent when locking and unlocking.

        Returns:
            bool: `True` if success, `False` if not.
        """
        if self._device.authenticator.login_method == AuthType.WebAPI:
            url = "{}/{}/cmd".format(OFFICIALAPI_URL, self._device.getDeviceUUID())
            sign = self.getSign()
        elif self._device.authenticator.login_method == AuthType.SDK:
            url = "{}/device/v1/iot/sesame2/{}".format(
                APIGW_URL, self._device.getDeviceUUID()
            )
            sign = self.getSign()[0:8]

        payload = {
            "cmd": int(cmd),
            "history": base64.b64encode(history_tag.encode()).decode(),
            "sign": sign,
        }

        try:
            response = self.requestAPI("POST", url, payload)

            return response.ok
        except RuntimeError:
            return False

    def getHistoryEntries(self) -> List[CHSesame2History]:
        """Retrieve the history of all events with a device.

        Returns:
            list[CHSesame2History]: A list of events.
        """
        if self._device.authenticator.login_method == AuthType.WebAPI:
            url = "{}/{}/history?page=0&lg=10".format(
                OFFICIALAPI_URL, self._device.getDeviceUUID()
            )
        elif self._device.authenticator.login_method == AuthType.SDK:
            url = "{}/device/v1/sesame2/{}/history?page=0&lg=10&a={}".format(
                APIGW_URL, self._device.getDeviceUUID(), self.getSign()[0:8]
            )

        ret = []

        response = self.requestAPI("GET", url)
        for entry in response.json():
            ret.append(CHSesame2History(**entry))

        return ret
