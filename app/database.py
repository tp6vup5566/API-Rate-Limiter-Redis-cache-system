import asyncio

async def get_product_from_db(product_id: int):
    # simulate DB latency
    await asyncio.sleep(2)

    return {
        "id": product_id,
        "name": f"product-{product_id}"
    }