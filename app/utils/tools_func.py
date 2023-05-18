from typing import Any


async def paginated_find(
    model: Any,
    query: dict = {},
    current: int = 1,
    page_size: int = 10,
    sort: str = "_id",
) -> dict:
    total = await model.find(query).count()
    results = (
        await model.find(query)
        .sort("-" + sort)
        .skip((current - 1) * page_size)
        .limit(page_size)
        .to_list()
    )
    return {"list": results, "current": current, "page_size": page_size, "total": total}
