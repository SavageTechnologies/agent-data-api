from typing import List, Optional

from pydantic import BaseModel


class BaseModelSchema(BaseModel):

    def update(self, model, custom_fields: Optional[List[str]] = None) -> bool:
        return update_model_with_json(model, json_schema=self, custom_fields=custom_fields)


def update_model_field_with(model, json_schema, field: str) -> bool:  # TODO clean this up
    did_update = False
    previous_value = getattr(model, field)
    updated_value = getattr(json_schema, field)
    if isinstance(updated_value, List):
        processed_list = []
        for v in updated_value:
            to_add = v
            if isinstance(v, BaseModel):
                to_add = v.model_dump()
            processed_list.append(to_add)
        if previous_value != processed_list:
            setattr(model, field, processed_list)
            did_update = True
    elif isinstance(updated_value, BaseModel):
        j = updated_value.model_dump()
        setattr(model, field, j)
        did_update = True
    elif previous_value != updated_value:
        setattr(model, field, updated_value)
        did_update = True
    return did_update


def update_model_with_json(model, json_schema, custom_fields: Optional[List[str]] = None) -> bool:  # TODO clean this up
    fields = custom_fields
    if fields is None:
        fields = json_schema.Meta.update_fields
    is_dirty = False
    for field in fields:
        did_update_field = update_model_field_with(model, json_schema, field)
        if did_update_field:
            is_dirty = True

    return is_dirty
