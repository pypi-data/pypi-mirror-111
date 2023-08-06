import logging
import os
from typing import Optional

import grpc
from zeebe_grpc.gateway_pb2_grpc import GatewayStub

from pyzeebe.credentials.base_credentials import BaseCredentials
from pyzeebe.errors import (ZeebeBackPressureError,
                            ZeebeGatewayUnavailableError, ZeebeInternalError)
from pyzeebe.grpc_internals.grpc_channel_utils import (create_channel,
                                                       create_connection_uri)

logger = logging.getLogger(__name__)


class ZeebeAdapterBase(object):
    _channel: grpc.aio.Channel
    _gateway_stub: GatewayStub

    def __init__(self, hostname: str = None, port: int = None, credentials: BaseCredentials = None,
                 secure_connection: bool = False, max_connection_retries: int = -1):
        self.credentials = credentials
        self.secure_connection = secure_connection
        self.connection_uri = create_connection_uri(
            hostname, port, credentials
        )
        self.secure_connection = secure_connection
        self.connected = False
        self.retrying_connection = False
        self._max_connection_retries = max_connection_retries
        self._current_connection_retries = 0

    def connect(self, channel: Optional[grpc.aio.Channel] = None):
        self.retrying_connection = True
        self.connected = True
        if channel:
            self._channel = channel
        else:
            self._channel = create_channel(
                self.connection_uri, self.credentials, self.secure_connection
            )

        self._gateway_stub = GatewayStub(self._channel)

    async def disconnect(self):
        await self._close()

    def _should_retry(self):
        return self._max_connection_retries == -1 or self._current_connection_retries < self._max_connection_retries

    async def _common_zeebe_grpc_errors(self, rpc_error: grpc.aio.AioRpcError):
        if self.is_error_status(rpc_error, grpc.StatusCode.RESOURCE_EXHAUSTED):
            raise ZeebeBackPressureError()
        elif self.is_error_status(rpc_error, grpc.StatusCode.UNAVAILABLE):
            self._current_connection_retries += 1
            if not self._should_retry():
                await self._close()
            raise ZeebeGatewayUnavailableError()
        elif self.is_error_status(rpc_error, grpc.StatusCode.INTERNAL):
            self._current_connection_retries += 1
            if not self._should_retry():
                await self._close()
            raise ZeebeInternalError()
        else:
            raise rpc_error

    @staticmethod
    def is_error_status(rpc_error: grpc.aio.AioRpcError, status_code: grpc.StatusCode):
        return rpc_error.code() == status_code

    async def _close(self):
        try:
            await self._channel.close()
        except Exception as exception:
            logger.exception(
                f"Failed to close channel, {type(exception).__name__} exception was raised"
            )
