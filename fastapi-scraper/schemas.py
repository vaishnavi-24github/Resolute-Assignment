from pydantic import BaseModel

class MetadataSchema(BaseModel):
    task_id: str
    url: str
    title: str | None
    description: str | None
    keywords: str | None

    class Config:
        orm_mode = True