import os, json, pathlib
import openai, backoff
from openai.error import RateLimitError

openai.api_key = os.getenv("OPENAI_API_KEY")

SYSTEM_MSG = "You are a marketing copywriter. Given title and description, return three bullet points and a catchy tagline."

@backoff.on_exception(backoff.expo, RateLimitError, max_tries=3)
def summarize(title, description):
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role":"system","content":SYSTEM_MSG},
                {"role":"user","content":f"Title: {title}\nDescription: {description}"}
            ],
            temperature=0.7,
            max_tokens=120
        )
        return resp.choices[0].message.content.strip()
    except RateLimitError:
        # fallback placeholder
        return f"- **{title}**: Great product! (summary unavailable due to API limits)"

def main():
    raw = json.loads(pathlib.Path("products_raw.json").read_text(encoding="utf-8"))
    for item in raw:
        item["summary"] = summarize(item["title"], item.get("description",""))
    pathlib.Path("products_enriched.json").write_text(
        json.dumps(raw, indent=2), encoding="utf-8"
    )

if __name__=="__main__":
    main()
