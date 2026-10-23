# AgriSpray AI

বাংলা-প্রথম আগাছা সনাক্তকরণ ও ফসল-নিরাপত্তা অ্যাপ।

ফাইল: `index.html` (ফ্রন্টএন্ড), `main.py` (FastAPI ব্যাকএন্ড), `schema.sql` (PostgreSQL), `docker-compose.yml` (লোকাল ডাটাবেস)।

## যা কাজ করে
- ছবি আপলোড → `scans` টেবিলে রেকর্ড
- আগাছা সার্চ + অ্যাডমিন যোগ (অডিট লগসহ)
- Crop Safety Gate (`POST /safety-check`): যাচাই না হলে সুপারিশ আটকে দেয়

## এখনো বাকি
- AI সনাক্তকরণ (`PLANT_ID_API_KEY` ও `main.py`-এর TODO)
- যাচাইকৃত আগাছা/ওষুধের ডেটা (কিছু বানানো হয়নি)
- লগইন, ট্রিটমেন্ট ট্র্যাকিং, জ্ঞানভাণ্ডার, অফলাইন মোড, ইংরেজি ভাষা

## চালানো
```bash
docker compose up -d
pip install -r requirements.txt
export DATABASE_URL=postgresql://postgres:password@localhost:5432/agrispray ADMIN_TOKEN=বদলান
uvicorn main:app --reload
```
এরপর `index.html` ব্রাউজারে খুলুন।

## অনলাইনে
`index.html` GitHub Pages-এ চলবে (Settings → Pages → main branch)। ব্যাকএন্ড Render/Railway-তে দিয়ে `index.html`-এর `API` ঠিকানা বদলান।
