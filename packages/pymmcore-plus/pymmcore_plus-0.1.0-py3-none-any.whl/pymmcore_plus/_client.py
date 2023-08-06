import atexit
import subprocess
import sys
import threading
import time

from loguru import logger
from Pyro5 import api, core, errors
from typing_extensions import Protocol

from . import _server
from ._serialize import register_serializers


class CallbackProtocol(Protocol):
    def receive_core_callback(self, signal_name: str, args: tuple) -> None:
        """Will be called by server with name of signal, and tuple of args."""


class RemoteMMCore(api.Proxy):
    def __init__(
        self,
        host=_server.DEFAULT_HOST,
        port=_server.DEFAULT_PORT,
        timeout=5,
        verbose=False,
        cleanup_new=True,
        cleanup_existing=True,
        connected_socket=None,
        callback=None,
    ):
        register_serializers()
        ensure_server_running(
            host, port, timeout, verbose, cleanup_new, cleanup_existing
        )

        uri = f"PYRO:{_server.CORE_NAME}@{host}:{port}"
        super().__init__(uri, connected_socket=connected_socket)

        self._cb_thread = None
        self._callbacks = set()
        if callback is not None:
            self.register_callback(callback)

    def register_callback(self, callback: CallbackProtocol):
        class_cb = getattr(type(callback), "receive_core_callback", None)
        if class_cb is None:
            raise TypeError("Callbacks must have a 'receive_core_callback' method.")
        if not hasattr(class_cb, "_pyroExposed"):
            class_cb._pyroExposed = True

        self._callbacks.add(callback)
        self._cb_thread = DaemonThread()
        self._cb_thread._daemon.register(callback)
        self.connect_remote_callback(callback)  # must come after register()
        self._cb_thread.start()

    def __exit__(self, exc_type, exc_value, traceback):
        logger.debug("closing pyro client")
        for cb in self._callbacks:
            self.disconnect_remote_callback(cb)
        if self._cb_thread is not None:
            self._cb_thread._daemon.close()
        super().__exit__(exc_type, exc_value, traceback)
        if exc_value is not None:
            sys._original_exchook_, sys.excepthook = sys.excepthook, errors.excepthook

    def __getattr__(self, name):
        if name in ("_cb_thread", "_callbacks"):
            return object.__getattribute__(self, name)
        return super().__getattr__(name)

    def __setattr__(self, name, value):
        if name in ("_cb_thread", "_callbacks"):
            return object.__setattr__(self, name, value)
        return super().__setattr__(name, value)


def _get_remote_pid(host, port):
    import psutil

    for proc in psutil.process_iter(["connections"]):
        for pconn in proc.info["connections"] or []:
            if pconn.laddr.port == port and pconn.laddr.ip == host:
                return proc


def new_server_process(host, port, timeout=5, verbose=False):
    """Create a new daemon process"""
    cmd = [sys.executable, _server.__file__, "-p", str(port), "--host", host]
    if verbose:
        cmd.append("--verbose")

    proc = subprocess.Popen(cmd)

    uri = f"PYRO:{core.DAEMON_NAME}@{host}:{port}"
    remote_daemon = api.Proxy(uri)

    while timeout > 0:
        try:
            remote_daemon.ping()
            return proc
        except Exception:
            timeout -= 0.1
            time.sleep(0.1)
    raise TimeoutError(f"Timeout connecting to server {uri}")


def ensure_server_running(
    host, port, timeout=5, verbose=False, cleanup_new=True, cleanup_existing=False
):
    """Ensure that a server daemon is running, or start one."""
    uri = f"PYRO:{core.DAEMON_NAME}@{host}:{port}"
    remote_daemon = api.Proxy(uri)
    try:
        remote_daemon.ping()
        logger.debug("Found existing server:\n{}", remote_daemon.info())
        if cleanup_existing:
            proc = _get_remote_pid(host, port)
            if proc is not None:
                atexit.register(proc.kill)

    except errors.CommunicationError:
        logger.debug("No server found, creating new mmcore server")
        proc = new_server_process(host, port, verbose=verbose)
        if cleanup_new:
            atexit.register(proc.kill)
        return proc


class DaemonThread(threading.Thread):
    def __init__(self, daemon=True):
        self._daemon = api.Daemon()
        self._stop_event = threading.Event()
        super().__init__(
            target=self._daemon.requestLoop, name="DaemonThread", daemon=daemon
        )

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.stop()
