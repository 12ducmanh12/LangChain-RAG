from pydantic import BaseModel
from typing import List, Optional, Union

class Resource(BaseModel):
    field: Union[str, None]
    source:str
    type:str