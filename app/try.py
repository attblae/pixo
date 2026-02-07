from fastapi import Depends, status, HTTPException
from fastapi.exceptions import RequestValidationError
from schemes import TokenOut
from datetime import datetime, timedelta
from consts import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
import sqlite3