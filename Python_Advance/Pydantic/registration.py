from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    field_validator,
    model_validator,
    ValidationError
)
import json


# АДРЕСА
class Address(BaseModel):
    # минимум 2 символа
    city: str = Field(..., min_length=2)

    # минимум 3 символа
    street: str = Field(..., min_length=3)

    # положительное число
    house_number: int = Field(..., gt=0)


# ПОЛЬЗОВАТЕЛИ
class User(BaseModel):
    # строка, должна быть только из букв, минимум 2 символа.
    name: str = Field(..., min_length=2, pattern=r"^[A-Za-z\s]+$")

    # число, должно быть между 0 и 120
    age: int = Field(..., ge=0, le=120)

    # строка, должна соответствовать формату email
    email: EmailStr

    #  булево значение, статус занятости пользователя
    is_employed: bool

    # вложенная модель адреса
    address: Address

    # Проверка имени
    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v.replace(" ", "").isalpha():
            raise ValueError("Имя должно содержать только буквы и пробелы")
        return v

    # Проверка, что если пользователь указывает, что он занят (is_employed = true), его возраст должен быть от 18 до 65 лет.
    @model_validator(mode='after')
    def check_employment_age(self):
        if self.is_employed and not (18 <= self.age <= 65):
            raise ValueError(
                "Если пользователь занят (is_employed=true), возраст должен быть от 18 до 65 лет."
            )
        return self


# Функция регистрации
def register_user(json_string: str) -> str:
    """
    Принимает JSON-строку → проверяет → возвращает JSON или ошибку.
    """
    try:
        # Pydantic сам распарсит JSON и проверит ВСЁ
        user = User.model_validate_json(json_string)

        # Возвращаем красивый JSON (с отступами, красиво)
        return user.model_dump_json(indent=2)

    except ValidationError:
        return "Неверный формат JSON.  Ошибки валидации"
    except json.JSONDecodeError:
        return "Неверный формат JSON. Проверьте скобки и кавычки!"


# Тесты — проверим разные случаи
if __name__ == "__main__":
    print("Тестируем систему регистрации...\n")

    # Успешная регистрация
    good = """
    {
        "name": "Anna Smith",
        "age": 30,
        "email": "anna@example.com",
        "is_employed": true,
        "address": {
            "city": "Berlin",
            "street": "Main Street",
            "house_number": 42
        }
    }
    """
    print("Тест 1: Всё правильно")
    print(register_user(good))
    print("\n" + "=" * 60 + "\n")

    # Ошибка: работает в 70 лет
    bad1 = """
    {
        "name": "John Doe",
        "age": 70,
        "email": "john@example.com",
        "is_employed": true,
        "address": {
            "city": "NY",
            "street": "5th Ave",
            "house_number": 123
        }
    }
    """
    print("Тест 2: Работает в 70 лет — нельзя!")
    print(register_user(bad1))
    print("\n" + "=" * 60 + "\n")

    # Ошибка: город слишком короткий
    bad2 = """
    {
        "name": "Bob",
        "age": 25,
        "email": "bob@test.com",
        "is_employed": true,
        "address": {
            "city": "A",
            "street": "Long Street",
            "house_number": 1
        }
    }
    """
    print("Тест 3: Город из 1 буквы")
    print(register_user(bad2))
    print("\n" + "=" * 60 + "\n")

    # Пенсионер (не работает) в 70 лет — можно!
    good2 = """
    {
        "name": "Eva Adamovna",
        "age": 70,
        "email": "eva@adam.com",
        "is_employed": false,
        "address": {
            "city": "Sky",
            "street": "Paradase",
            "house_number": 1
        }
    }
    """
    print("Тест 4: Пенсионер (не работает) — всё ок!")
    print(register_user(good2))
