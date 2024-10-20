from pydantic import BaseModel, EmailStr, ConfigDict, Field


class MailMassageSchema(BaseModel):
    to: EmailStr
    subject: str
    body: str
    from_name: str | None = None

