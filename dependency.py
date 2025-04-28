from typing import Annotated
from fastapi import Depends
from database import get_db
from sqlalchemy.orm import Session

db_dependency = Annotated[Session, Depends(get_db)]