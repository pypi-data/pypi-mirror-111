import threading
import typing as t
import sys
from .mvc import Proxy
from enum import Enum, auto
from http.client import HTTPException
from xmlrpc.client import ServerProxy, ProtocolError, Transport


class ClientTransport(Transport):
    def __init__(self, token: str = None, headers=()) -> None:
        self._token = token
        self._headers = headers

        if self._token:
            client_headers = [
                ('X-Client-Token', token)]
 
            self._headers = self._headers + tuple(client_headers)

        super().__init__(headers=self._headers)

    def request(self, host, handler, request_body, verbose=False) -> t.Any:
        try:
            return super().request(
                host, handler, request_body, verbose)
        except ProtocolError as e:
            if e.errcode == 401:
                raise HTTPException(
                    "Ошибка авторизации клиента (токен клиент-сервер)")
            if e.errcode == 404:
                raise HTTPException(
                    "Невозможно выполнить подключение к API")

            raise


class ProxyState(Enum):
    BUSY = auto()
    COMLETE = auto()
    FAULT = auto()
    PENDING = auto()
    READY = auto()


class RemoteProxy(Proxy):
    def __init__(self, uri, token) -> None:
        super().__init__()

        self.__server_proxy = ServerProxy(
            uri, transport=ClientTransport(
                token=token))

        self.__lock = threading.Lock()
        self.__state = ProxyState.READY

    @property
    def state(self) -> "ProxyState":
        return self.__state

    @state.setter
    def state(self, state: "ProxyState") -> None:
        self.__state = state
        self.notify_observers(
                "ProxyStateChanged", data=self.__state)

    def exec(self, method: str, *args) -> t.Optional[t.Any]:
        if self.__lock.locked():
            self.state = ProxyState.BUSY
            return

        self.__lock.acquire()

        result: t.Any = None
        try:
            self.state = ProxyState.PENDING

            func = getattr(self.__server_proxy, method)
            result = func(*args)

            self.state = ProxyState.COMLETE
        except:
            self.notify_observers(
                "ProxyError", data=str(sys.exc_info()[1]))
            self.state = ProxyState.FAULT
        
        self.__lock.release()

        return result
