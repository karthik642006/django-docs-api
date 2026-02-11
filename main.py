from fastapi import FastAPI, Query
import requests
from bs4 import BeautifulSoup

app = FastAPI()

BASE_URL = "https://docs.djangoproject.com/en/stable/"


@app.get("/fetch-docs")
def fetch_docs(path: str = Query(...)):
    try:
        # Build full URL
        full_url = BASE_URL + path.strip("/") + "/"

        # Request page like a real browser
        response = requests.get(
            full_url,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        if response.status_code != 200:
            return {
                "error": "Page not found",
                "url": full_url
            }

        soup = BeautifulSoup(response.text, "html.parser")

        # Try to get main documentation area
        main_content = soup.find("div", {"role": "main"})

        # Fallback if not found
        if not main_content:
            main_content = soup.body

        if not main_content:
            return {
                "error": "Could not extract content",
                "url": full_url
            }

        text = main_content.get_text(separator="\n", strip=True)

        return {
            "url": full_url,
            "content": text[:8000]
        }

    except Exception as e:
        return {
            "error": str(e)
        }
