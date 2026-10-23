import os, uuid, json
from fastapi import FastAPI, UploadFile, File, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row

DB = os.getenv("DATABASE_URL", "")
ADMIN = os.getenv("ADMIN_TOKEN", "")
PLANT_KEY = os.getenv("PLANT_ID_API_KEY", "")
os.makedirs("uploads", exist_ok=True)

app = FastAPI(title="AgriSpray AI")
app.add_middleware(CORSMiddleware, allow_origins=[os.getenv("CORS_ORIGIN", "http://localhost:3000")],
                   allow_methods=["*"], allow_headers=["*"])
pool = ConnectionPool(DB, kwargs={"row_factory": dict_row}, open=False) if DB else None

@app.on_event("startup")
def start():
    if pool:
        pool.open()
        with pool.connection() as c:
            c.execute(open(os.path.join(os.path.dirname(__file__), "schema.sql")).read())

def need_db():
    if not pool: raise HTTPException(503, "DATABASE_URL সেট করা হয়নি (setup required)")

def need_admin(token):
    if not ADMIN or token != ADMIN: raise HTTPException(401, "অ্যাডমিন টোকেন প্রয়োজন")

@app.get("/health")
def health():
    return {"db": bool(pool), "ai_identification": bool(PLANT_KEY)}

@app.get("/weeds")
def weeds(q: str = ""):
    need_db()
    with pool.connection() as c:
        return c.execute("SELECT * FROM weeds WHERE %s='' OR name_bn ILIKE %s OR name_en ILIKE %s OR scientific_name ILIKE %s ORDER BY name_bn LIMIT 50",
                         (q, f"%{q}%", f"%{q}%", f"%{q}%")).fetchall()

class Weed(BaseModel):
    name_bn: str; name_en: str | None = None; scientific_name: str | None = None
    category: str | None = None; features: str | None = None; sources: list[str] = []

@app.post("/weeds")
def add_weed(w: Weed, x_admin_token: str = Header("")):
    need_admin(x_admin_token); need_db()
    with pool.connection() as c:
        r = c.execute("INSERT INTO weeds(name_bn,name_en,scientific_name,category,features,sources) VALUES(%s,%s,%s,%s,%s,%s) RETURNING id",
                      (w.name_bn, w.name_en, w.scientific_name, w.category, w.features, w.sources)).fetchone()
        c.execute("INSERT INTO audit_log(table_name,row_id,action,detail) VALUES('weeds',%s,'create',%s)", (r["id"], json.dumps(w.model_dump())))
        return r

@app.get("/herbicides")
def herbicides():
    need_db()
    with pool.connection() as c:
        return c.execute("SELECT id,brand,active_ingredient,registered_bd,verified_at FROM herbicides ORDER BY brand").fetchall()

class SafetyInput(BaseModel):
    herbicide_id: int; current_crop: str | None = None
    next_crop: str | None = None; days_until_planting: int | None = None

@app.post("/safety-check")
def safety_check(s: SafetyInput):
    """Crop Safety Gate: any unverifiable item withholds the recommendation."""
    need_db()
    with pool.connection() as c:
        h = c.execute("SELECT * FROM herbicides WHERE id=%s", (s.herbicide_id,)).fetchone()
    if not h: raise HTTPException(404, "পণ্য পাওয়া যায়নি")
    problems = []
    if h["registered_bd"] is not True: problems.append("বাংলাদেশে নিবন্ধনের তথ্য যাচাই করা হয়নি")
    if not h["verified_at"] or not h["source_url"]: problems.append("লেবেল/সূত্র ও যাচাইয়ের তারিখ নেই")
    if s.current_crop and s.current_crop not in (h["approved_crops"] or []): problems.append("বর্তমান ফসলে অনুমোদিত নয়")
    if s.next_crop:
        need = (h["plant_back_days"] or {}).get(s.next_crop)
        if need is None: problems.append("পরবর্তী ফসলের plant-back তথ্য নেই")
        elif s.days_until_planting is not None and s.days_until_planting < need:
            problems.append(f"পরবর্তী ফসল লাগাতে কমপক্ষে {need} দিন অপেক্ষা করতে হবে")
    if problems:
        return {"safe_to_recommend": False, "warnings": problems,
                "note": "নিরাপত্তা যাচাই করা যায়নি, তাই সুপারিশ আটকে রাখা হয়েছে। স্থানীয় কৃষি কর্মকর্তার পরামর্শ নিন।"}
    return {"safe_to_recommend": True, "label": h["label_instructions"], "source": h["source_url"],
            "note": "এটি ফসলের নিরাপত্তার নিশ্চয়তা নয়। লেবেল অনুসরণ করুন।"}

@app.post("/scans")
async def scan(file: UploadFile = File(...)):
    need_db()
    path = f"uploads/{uuid.uuid4().hex}_{os.path.basename(file.filename or 'img')}"
    open(path, "wb").write(await file.read())
    # TODO: call a real plant-ID API with PLANT_KEY here. Never fabricate a result.
    msg = "AI সনাক্তকরণ সার্ভিস সেটআপ করা হয়নি" if not PLANT_KEY else "API কী আছে, কিন্তু API কল এখনো লেখা হয়নি"
    with pool.connection() as c:
        return c.execute("INSERT INTO scans(image_path,status,result) VALUES(%s,'not_configured',%s) RETURNING id,status,result",
                         (path, json.dumps({"message": msg}))).fetchone()

@app.get("/scans")
def scans():
    need_db()
    with pool.connection() as c:
        return c.execute("SELECT id,status,result,created_at FROM scans ORDER BY id DESC LIMIT 30").fetchall()
