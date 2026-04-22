from models import *
from database import *
from fastapi import FastAPI
from typing import *
from sqlmodel import Session

SessionDep = Annotated(Session , Depends=get_session)