# Atlys FastAPI Web Scraper

A web scraping application built with FastAPI to scrape product information from e-commerce websites.

## Features

- Scrapes product information (title, price, images)
- Redis caching support
- Proxy support
- Configurable retry mechanism
- JSON storage for scraped data

## Prerequisites

- Python 3.8+
- Redis (optional)
- pip

## Installation

1. Clone the repository:

```bash
git clone https://github.com/arpitsinghania8/atlys-fastapi-scrapper.git
cd atlys-fastapi-scrapper
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables by copying the example file:

```bash
cp .env.example .env
```

4. Update the `.env` file with your configuration:

```properties
API_TOKEN=your_api_token
REDIS_URL=redis://localhost:6379
BASE_URL=https://dentalstall.com/shop/
RETRY_ATTEMPTS=3
RETRY_WAIT_SECONDS=5
```

## Running Redis (Optional)

If you want to use Redis caching:

```bash
# Install Redis using Homebrew
brew install redis

# Start Redis server
brew services start redis

# Verify Redis is running
redis-cli ping
```

## Running the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Health Check

```
GET /
```

### Scrape Products

```
POST /scrape/
Headers:
  x-token: your_api_token
Query Parameters:
  pages: number of pages to scrape (optional, default=5)
  proxy: proxy URL (optional)
```

## Example Usage

Using curl:

```bash
curl -X POST "http://localhost:8000/scrape/?pages=2" \
  -H "x-token: your_api_token"
```

## Project Structure

```
atlys-fastapi-scrapper/
├── app/
│   ├── core/
│   │   ├── config.py
│   │   ├── storage.py
│   │   └── notification.py
│   ├── services/
│   │   └── scraper.py
│   └── main.py
├── .env
├── requirements.txt
└── README.md
```

## License

MIT
