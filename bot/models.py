from sqlalchemy import Column, Integer, String, BigInteger, Text, func, ForeignKey, DECIMAL, Boolean
from sqlalchemy.orm import relationship

from bot import Base


class Users(Base):
    __tablename__ = "db_users"

    id = Column(BigInteger, primary_key=True)
    telegram_id = Column(BigInteger, nullable=False, unique=True)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=True)
    lang_code = Column(String(5), nullable=False)
    admin = Column(Boolean, default=False)
    timestamp = Column(BigInteger, nullable=False, default=func.unix_timestamp())

    def __init__(self, telegram_id, first_name, last_name, lang_code):
        self.telegram_id = telegram_id
        self.first_name = first_name
        self.last_name = last_name
        self.lang_code = lang_code
