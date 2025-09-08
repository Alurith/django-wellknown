from asgiref.sync import iscoroutinefunction
from django.utils.cache import patch_vary_headers
from django.utils.decorators import sync_and_async_middleware


@sync_and_async_middleware
def gpc_middleware(get_response):
    if iscoroutinefunction(get_response):

        async def middleware(request):
            request.gpc = request.headers.get("Sec-GPC") == "1"
            response = await get_response(request)
            if request.gpc:
                patch_vary_headers(response, ["Sec-GPC"])
            return response
    else:

        def middleware(request):
            request.gpc = request.headers.get("Sec-GPC") == "1"
            response = get_response(request)
            if request.gpc:
                patch_vary_headers(response, ["Sec-GPC"])
            return response

    return middleware
