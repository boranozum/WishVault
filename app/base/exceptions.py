from rest_framework.views import exception_handler
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR

from base.constants import ERROR_CODE_MESSAGE_MAPPING
from base.response import RestResponse


def custom_exception_handler(exc, content):
    print(exc)
    response = exception_handler(exc, content)
    if response is None:
        return RestResponse(
            status=HTTP_500_INTERNAL_SERVER_ERROR,
            message=ERROR_CODE_MESSAGE_MAPPING[HTTP_500_INTERNAL_SERVER_ERROR]
        )

    if response.status_code in list(ERROR_CODE_MESSAGE_MAPPING.keys()):
        return RestResponse(
            status=response.status_code,
            message=ERROR_CODE_MESSAGE_MAPPING[response.status_code]
        )

    return RestResponse(
        status=response.status_code,
        message='An error occurred'
    )

