from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import openai
import requests
from bs4 import BeautifulSoup

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI Key
openai.api_key = "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"

@app.post("/ai/keyword-research")
async def keyword_research(request: Request):
    data = await request.json()
    text = data.get("text", "")
    prompt = f"Generate a list of low-competition, high-traffic SEO keywords related to: {text}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return {"results": response.choices[0].message.content.strip()}
    except Exception as e:
        return {"error": str(e)}

@app.post("/ai/meta-generator")
async def meta_description(request: Request):
    data = await request.json()
    text = data.get("text", "")
    prompt = f"Write a professional and SEO-optimized meta description for: {text}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return {"results": response.choices[0].message.content.strip()}
    except Exception as e:
        return {"error": str(e)}

@app.post("/ai/title-generator")
async def blog_titles(request: Request):
    data = await request.json()
    text = data.get("text", "")
    prompt = f"Generate 5 creative and SEO-friendly blog titles for the topic: {text}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return {"results": response.choices[0].message.content.strip()}
    except Exception as e:
        return {"error": str(e)}

@app.post("/word-counter")
async def word_counter(request: Request):
    data = await request.json()
    text = data.get("text", "")
    words = len(text.split())
    characters = len(text)
    return {"words": words, "characters": characters}

@app.post("/keyword-density")
async def keyword_density(request: Request):
    data = await request.json()
    text = data.get("text", "")
    words = text.lower().split()
    total_words = len(words)
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    density = {k: f"{(v/total_words)*100:.2f}%" for k, v in freq.items()}
    return {"density": density}

@app.post("/sitemap-generator")
async def sitemap_generator(request: Request):
    data = await request.json()
    urls = data.get("urls", [])
    sitemap = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
    sitemap += "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n"
    for url in urls:
        sitemap += f"  <url><loc>{url}</loc></url>\n"
    sitemap += "</urlset>"
    return {"sitemap": sitemap}

@app.get("/robots-generator")
def robots():
    return {"robots": "User-agent: *\nDisallow:"}

@app.post("/meta-analyzer")
async def meta_analyzer(request: Request):
    data = await request.json()
    url = data.get("url", "")
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        title = soup.title.string if soup.title else ""
        desc = ""
        tag = soup.find("meta", attrs={"name": "description"})
        if tag:
            desc = tag.get("content", "")
        return {"title": title, "description": desc}
    except Exception as e:
        return {"error": str(e)}

@app.post("/page-checker")
async def page_checker(request: Request):
    data = await request.json()
    url = data.get("url", "")
    try:
        r = requests.get(url)
        headers = dict(r.headers)
        size_kb = len(r.content) / 1024
        return {"headers": headers, "size_kb": f"{size_kb:.2f} KB"}
    except Exception as e:
        return {"error": str(e)}
