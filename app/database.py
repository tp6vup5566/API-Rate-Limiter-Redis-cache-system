import asyncio
import logging
logger = logging.getLogger(__name__)

async def get_product_from_db(product_id: int):

    logger.info(f"Querying database for product {product_id}")

    await asyncio.sleep(2)

    return {
        "id": product_id,
        "name": f"product-{product_id}"
    }