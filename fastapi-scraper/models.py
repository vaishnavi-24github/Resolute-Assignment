from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Metadata(Base):
    __tablename__ = "metadata"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String, index=True)
    url = Column(String)
    title = Column(String)
    description = Column(String)
    keywords = Column(String)