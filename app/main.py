from fastapi import FastAPI, Depends, HTTPException, Header
from typing import Optional
import redis
import json
from .core.config import settings
from .core.storage import JSONStorage
from .core.notification import ConsoleNotification
from .services.scraper import WebScraper

app = FastAPI()
storage = JSONStorage()
notification = ConsoleNotification()
redis_client = redis.from_url(settings.REDIS_URL)

async def verify_token(x_token: str = Header(...)):
    if x_token != settings.API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")
    return x_token

@app.get("/")
async def health_check():
    return {"status": "ok"}

@app.post("/scrape/")
async def scrape_products(
    pages: Optional[int] = 5,
    proxy: Optional[str] = None,
    token: str = Depends(verify_token)
):
    scraper = WebScraper(proxy=proxy)
    all_products = []
    updated_count = 0
    
    page = 1
    while pages is None or page <= pages:
        try:
            products = scraper.scrape_page(page)
            if not products:
                break
                
            all_products.extend(products)
            updated_count += len(products)
            page += 1
        except Exception as e:
            print(f"Error scraping page {page}: {e}")
            break
    
    if all_products:
        storage.save_products(all_products)
        
    notification.notify(
        f"Scraping completed. Total products updated: {updated_count}"
    )
    
    return {"message": f"Successfully scraped {updated_count} products"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
