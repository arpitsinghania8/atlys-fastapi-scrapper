import requests
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_fixed
from typing import List, Dict, Optional
from ..core.config import settings

class WebScraper:
    def __init__(self, proxy: Optional[str] = None):
        self.proxy = proxy
        self.session = requests.Session()
        if proxy:
            self.session.proxies = {"http": proxy, "https": proxy}

    @retry(stop=stop_after_attempt(settings.RETRY_ATTEMPTS),
           wait=wait_fixed(settings.RETRY_WAIT_SECONDS))
    def scrape_page(self, page_number: int) -> List[Dict]:
        url = f"{settings.BASE_URL}page/{page_number}"
        response = self.session.get(url)
        response.raise_for_status()
        
        print(f"Response status: {response.status_code}")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the products container with correct class
        products_container = soup.find('ul', class_='products columns-4')
        print(f"Found products container: {products_container is not None}")
        
        products = []
        if products_container:
            # Find all list items within the products container
            product_items = products_container.find_all('li')
            print(f"Number of products found: {len(product_items)}")
            
            for product in product_items:
                try:
                    title = product.find('h2', class_='woo-loop-product__title').text.strip()
                    price = product.find('span', class_='woocommerce-Price-amount amount').text.strip().replace('$', '')
                    # Find image in div with mf-product-thumbnail class
                    image_div = product.find('div', class_='mf-product-thumbnail')
                    image_url = ''
                    if image_div:
                        image = image_div.find('img')
                        image_url = image['src'] if image else ''
                    
                    products.append({
                        "product_title": title,
                        "product_price": price,
                        "path_to_image": image_url
                    })
                except (AttributeError, ValueError) as e:
                    print(f"Error parsing product: {e}")
                    continue
        
        return products
