from rest_framework.response import Response

class CustomResponse(Response):
    def __init__(self, status=None, message=None, data=None, **kwargs):
        response_data = {
            'status': status,
            'message': message,
            'data': data
        }
        response_data.update(kwargs)
        super().__init__(response_data, **kwargs)
