# AgriSpray AI

বাংলা-প্রথম আগাছা সনাক্তকরণ ও ফসল-নিরাপত্তা অ্যাপ (বাংলাদেশের কৃষকদের জন্য)।

## এখন যা কাজ করে
- ছবি তোলা/আপলোড → সার্ভারে সংরক্ষণ → `scans` টেবিলে রেকর্ড
- আগাছা ডাটাবেস সার্চ + অ্যাডমিন যোগ (অডিট লগসহ)
- **Crop Safety Gate** (`POST /safety-check`): নিবন্ধন, লেবেল সূত্র, ফসল, plant-back যাচাই না হলে সুপারিশ আটকে দেয়

## এখনো বাকি (সৎভাবে)
- AI সনাক্তকরণ: `PLANT_ID_API_KEY` ও `backend/main.py`-এর `TODO` অংশে আসল API কল লাগবে
- আগাছা/ওষুধের **যাচাইকৃত ডেটা** নেই, বাংলাদেশের লেবেল/সূত্র থেকে নিজে ভরতে হবে। কোনো রেট বা তথ্য বানানো হয়নি
- ফারমার লগইন, ট্রিটমেন্ট ট্র্যাকিং UI, জ্ঞানভাণ্ডার পেজ, অফলাইন মোড, ইংরেজি ভাষা
- ক্লাউড ইমেজ স্টোরেজ (এখন `backend/uploads/` ফোল্ডারে)
- অ্যাডমিন লগইন এখন সরল টোকেন (`ADMIN_TOKEN`); প্রোডাকশনের আগে আসল অথেনটিকেশন দিন

## চালানোর নিয়ম
```bash
cp .env.example backend/.env        # মান বসান
# PostgreSQL চালু করে DATABASE_URL ঠিক করুন
cd backend && python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export $(grep -v '^#' .env | xargs) && uvicorn main:app --reload   # :8000
cd ../frontend && npm install && npm run dev                         # :3000
```

## GitHub-এ আপলোড
1. github.com → New repository → নাম `agrispray-ai` (Private রাখুন) → Create
2. জিপ খুলে ফোল্ডারে গিয়ে:
```bash
git init && git add . && git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/ইউজারনেম/agrispray-ai.git
git push -u origin main
```
৩. `.env` কখনো আপলোড করবেন না (`.gitignore`-এ আছে)।

## ডিপ্লয় (পরে)
GitHub Pages শুধু স্ট্যাটিক সাইট চালায়, FastAPI/PostgreSQL চলে না। ফ্রন্টএন্ড Vercel-এ, ব্যাকএন্ড+ডাটাবেস Render/Railway-তে দিন, আর `NEXT_PUBLIC_API_URL` ও `CORS_ORIGIN` সেট করুন।
