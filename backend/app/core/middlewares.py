# https://fastapi.tiangolo.com/tutorial/middleware/
# - Create a Middleware
# - Add a middleware to app
#   - Two ways, decorator ==> @app.middleware("http")
#   - Add app.addleware_func()


import time

from starlette.middleware.base import BaseHTTPMiddleware

from fastapi import Request, Response


# Use-Cases:
# - Logging (Requests / Responses)
# - Auth / API-Key prüfen
# - Request-Zeit messen
# - Header hinzufügen --> Done
# - Exception-Handling


class CustomMiddleware(BaseHTTPMiddleware):
    """We call this: class based Middleware ..."""

    async def __add_process_time_header__(self, request: Request, call_next) -> None:
        """Header hinzufügen"""
        start_time = time.perf_counter()  # why perf_counter here?

        response: Response = await call_next(request)

        process_time = 1000 * (time.perf_counter() - start_time)
        #  TODO: Understand Response headers Option see in api-docs
        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers
        response.headers[
            "X-Process-Time-Ghislain-this-is-how-to-add-extra-info-in-header-custom-middleware-ghislain"
        ] = f"{str(process_time)} ms"
        for item_tuple in response.headers.items():
            print(*item_tuple)
        return response

    async def dispatch(self, request: Request, call_next) -> Response:
        respo = await self.__add_process_time_header__(request, call_next)
        return respo
