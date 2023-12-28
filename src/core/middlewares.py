from fastapi import Request, Response
from starlette.types import ASGIApp, Scope, Receive, Send, Message


class BaseMiddleware:
    def __init__(
            self,
            app: ASGIApp,
    ) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        async def send_wrapper(message: Message) -> None:
            await send(message)

        await self.app(scope, receive, send_wrapper)
