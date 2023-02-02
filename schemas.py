from pydantic import BaseModel
from typing import Union

class GetPersons(BaseModel):
    sort: str
    email: Union[str, None] = None
    company: Union[str, None] = None
    job_title: Union[str, None] = None
    gender: Union[str, None] = None

class ResponseStatus(BaseModel):
    status: str
    data: Union[dict, str] = None