from typing import Union, List, Dict
from typing_extensions import Annotated, TypeAliasType

# TypeAliasType is necessary to avoid recursion error when validating this
# type with Pydantic
JSONSerializable = TypeAliasType(
    "JSONSerializable",
    Union[str,
        int, 
        float, 
        bool, 
        None, 
        List['JSONSerializable'],
        Dict[str, 'JSONSerializable']
    ],
)

JsonDict = Dict[str, 'JSONSerializable']


