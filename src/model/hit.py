from typing import List, Union

from pydantic import BaseModel

from src.model.value import Value, FreqValue

Hit = List[Union[Value, FreqValue]]

HitWithFrequency = List[FreqValue]

HitWithoutFrequency = List[Value]
