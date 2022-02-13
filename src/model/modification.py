from typing import Dict, Union

from pydantic import BaseModel


class Modification(BaseModel):
    type: str
    params: Dict[str, Union[str, int]]
