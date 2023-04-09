from pydantic import BaseModel
class File(BaseModel):
    file : str
    color : str
