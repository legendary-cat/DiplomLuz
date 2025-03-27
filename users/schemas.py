from pydantic import BaseModel, EmailStr, Field, validator
import re


class SClientRegister(BaseModel):
    client_email: EmailStr = Field(..., description="Электронная почта")
    client_password: str = Field(..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")
    client_self_sale: int = Field(ge=0)
    client_phone_number: str = Field(..., description="Номер телефона в международном формате, начинающийся с '+'")
    client_name: str = Field(..., min_length=3, max_length=50, description="Имя, от 3 до 50 символов")
    client_mid_name : str = Field(..., min_length=3, max_length=50, description="Отчество, от 3 до 50 символов")
    client_last_name: str = Field(..., min_length=3, max_length=50, description="Фамилия, от 3 до 50 символов")
    ###################################

    @validator("client_phone_number")
    @classmethod
    def validate_phone_number(cls, value: str) -> str:
        if not re.match(r'^\+\d{5,15}$', value):
            raise ValueError('Номер телефона должен начинаться с "+" и содержать от 5 до 15 цифр')
        return value

class SClientAuth(BaseModel):
    client_email: EmailStr = Field(..., description="Электронная почта")
    client_password: str = Field(..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")