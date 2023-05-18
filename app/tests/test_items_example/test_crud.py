import random
import string

from app.items_example import crud, schema


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def test_create_item() -> None:
    name = random_lower_string()
    description = random_lower_string()
    num = 1
    price = 1

    item_in = schema.ItemCreate(
        name=name,
        description=description,
        num=num,
        price=price,
    )
    item = crud.create_item(item_in)
    assert item
