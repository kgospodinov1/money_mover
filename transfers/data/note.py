from pydantic import BaseModel, constr


class AddNoteData(BaseModel):
    note: constr(min_length=1, max_length=10000)
