from pydantic import BaseModel
from datetime import datetime


def to_camel_case(arg: str) -> str:
    string_split = arg.split("_")
    return string_split[0] + "".join(word.capitalize() for word in string_split[1:])

def convert_datetime_to_iso_8601(arg: datetime) -> str:
    return arg.astimezone().isoformat(sep="T", timespec="milliseconds")


class SharedModel(BaseModel):
    class Config:
        allow_population_by_field_name = True
        alias_generator = to_camel_case
        use_enum_values = True
        json_encoders = {
            datetime: convert_datetime_to_iso_8601,
        }
        arbitrary_types_allowed = True