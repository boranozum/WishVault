from rest_framework.views import exception_handler

from base.constants import ERROR_CODE_MESSAGE_MAPPING
from base.response import RestResponse


def custom_exception_handler(exc, content):
    response = exception_handler(exc, content)

    if response.status_code in list(ERROR_CODE_MESSAGE_MAPPING.keys()):
        return RestResponse(
            status=response.status_code,
            message=ERROR_CODE_MESSAGE_MAPPING[response.status_code]
        )

    return RestResponse(
        status=response.status_code,
        message='An error occurred'
    )

