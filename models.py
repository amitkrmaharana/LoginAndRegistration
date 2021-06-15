from sqlalchemy import Column, Integer, String

from application import database
from logger import logger


class Users(database.Model):
    """
    This represents the table of the database provided in the credentials. It provides the user details required
    for registration process to complete.
    """
    try:
        id = Column(Integer, primary_key=True)
        first_name = Column(String(128))
        last_name = Column(String(100))
        email = Column(String(100))
        contact = Column(String(100))
        username = Column(String(200), unique=True)
        password = Column(String(200))
    except Exception as e:
        logger.exception(e)

    def __init__(self, id, first_name, last_name, email, contact, username, password):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.contact = contact
        self.username = username
        self.password = password
