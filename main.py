from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import requests
from bs4 import BeautifulSoup

app = FastAPI()

# Enable CORS for frontend access (like Lovable.dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === CONFIG ===
openai.api_key = "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"

# === Models ===
class TextInput(BaseModel):
    text: str

class URLInput(BaseModel):
    url: str

# === AI TOOLS ===
@app.post("/ai/keyword-research")
def ai_keyword_research(input: TextInput):
    prompt = f"Generate 10 SEO keywords for this topic: {input.text}. Include competition level and estimated search volume."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return {"results": response.choices[0].message.content.strip()}

@app.post("/ai/meta-generator")
def ai_meta_generator(input: TextInput):
    prompt = f"Write an SEO meta title and meta description for this content:\n\n{input.text}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return {"meta": response.choices[0].message.content.strip()}

@app.post("/ai/title-generator")
def ai_title_generator(input: TextInput):
    prompt = f"Suggest 5 engaging blog titles for the topic:\n\n{input.text}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return {"titles": response.choices[0].message.content.strip()}

# === LOCAL PYTHON TOOLS ===
@app.post("/word-counter")
def word_counter(input: TextInput):
    words = input.text.split()
    return {"word_count": len(words), "character_count": len(input.text)}

@app.post("/keyword-density")
def keyword_density(input: TextInput):
    from collections import Counter
    import re
    words = re.findall(r"\b\w+\b", input.text.lower())
    total = len(words)
    freq = Counter(words)
    density = {word: f"{(count/total)*100:.2f}%" for word, count in freq.items()}
    return {"total_words": total, "density": density}

@app.post("/sitemap-generator")
async def sitemap_generator(request: Request):
    body = await request.json()
    urls = body.get("urls", [])
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in urls:
        xml += f"<url><loc>{url}</loc></url>\n"
    xml += "</urlset>"
    return {"sitemap": xml}

@app.get("/robots-generator")
def robots_generator():
    return {
        "robots": "User-agent: *\nDisallow:\nAllow: /\nSitemap: https://yourdomain.com/sitemap.xml"
    }

@app.post("/meta-analyzer")
def meta_analyzer(input: URLInput):
    try:
        res = requests.get(input.url, timeout=5)
        soup = BeautifulSoup(res.text, "html.parser")
        title = soup.title.string if soup.title else ""
        description = soup.find("meta", attrs={"name": "description"})
        keywords = soup.find("meta", attrs={"name": "keywords"})
        return {
            "title": title,
            "description": description["content"] if description else "",
            "keywords": keywords["content"] if keywords else ""
        }
    except Exception as e:
        return {"error": str(e)}

@app.post("/page-checker")
def page_checker(input: URLInput):
    try:
        res = requests.get(input.url, timeout=5)
        size_kb = len(res.content) / 1024
        headers = dict(res.headers)
        return {
            "size_kb": f"{size_kb:.2f} KB",
            "headers": headers
        }
    except Exception as e:
        return {"error": str(e)}
