from rest_framework import status

SUCCESS_STATUS_CODES = [
    status.HTTP_200_OK,
    status.HTTP_201_CREATED,
    status.HTTP_202_ACCEPTED,
    status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
    status.HTTP_204_NO_CONTENT,
    status.HTTP_205_RESET_CONTENT,
    status.HTTP_206_PARTIAL_CONTENT,
    status.HTTP_207_MULTI_STATUS,
    status.HTTP_208_ALREADY_REPORTED,
    status.HTTP_226_IM_USED,
]

ERROR_CODE_MESSAGE_MAPPING = {
    status.HTTP_400_BAD_REQUEST: "The request format is invalid, please check the request and try again",
    status.HTTP_401_UNAUTHORIZED: "You are not authorized to access this resource",
    status.HTTP_403_FORBIDDEN: "You are not allowed to access this resource",
    status.HTTP_404_NOT_FOUND: "No record found",
    status.HTTP_405_METHOD_NOT_ALLOWED: "Method not allowed",
    status.HTTP_406_NOT_ACCEPTABLE: "Not acceptable",
    status.HTTP_408_REQUEST_TIMEOUT: "Request timeout",
    status.HTTP_409_CONFLICT: "The request could not be completed due to a conflict with the current state of the target resource",
    status.HTTP_500_INTERNAL_SERVER_ERROR: "Failed to process the request due to an internal server error",
}