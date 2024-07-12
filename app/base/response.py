from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


class RestResponse(Response):
    def __init__(self, message=None, status=HTTP_200_OK, content=None, *args, **kwargs):
        data = {
            'status': status,
            'message': message,
            'content': content
        }
        super().__init__(data=data, status=status, *args, **kwargs)
