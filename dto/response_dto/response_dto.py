from pydantic import BaseModel


class ResponseDto(BaseModel):
    """
    Data Transfer Object representing a general response structure with an optional data payload.

    Attributes:
        Data (object, optional): An optional data payload. Defaults to None.
        Success (bool): Indicates whether the operation was successful.
        Message (str): A message describing the operation result.
        Status (int): The status code of the operation.
    """

    Data: object = None
    Success: bool
    Message: str
    Status: int
