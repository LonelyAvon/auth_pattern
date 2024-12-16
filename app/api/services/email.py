from fastapi import HTTPException
from app.api.schemas.email import EmailCreate
from app.db.repositories.email_repository import EmailRepository
import re

def is_valid_email(email):
    # Регулярное выражение для проверки адреса электронной почты
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email) is not None



class EmailService:

    def __init__(self, session) :
        self.session = session

    async def create(self, email: EmailCreate):

        if not is_valid_email(email.email):
            raise HTTPException(status_code=400, detail="Invalid email")
        
        if await EmailRepository(self.session).get_by_filter({"email": email.email}):
            raise HTTPException(status_code=400, detail="Email already exists")
        
        email = await EmailRepository(self.session).create(email)
        await EmailRepository(self.session).commit()
        return email
    