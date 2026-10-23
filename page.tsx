"use client";
import { useEffect, useRef, useState } from "react";
const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const tiles = ["ওষুধের পরামর্শ", "ফসল সুরক্ষা যাচাই", "উপকার ও অপকার বিশ্লেষণ", "আগের স্ক্যানের ইতিহাস", "আগাছার জ্ঞানভাণ্ডার"];

export default function Home() {
  const [health, setHealth] = useState<any>(null);
  const [offline, setOffline] = useState(false);
  const [msg, setMsg] = useState("");
  const [busy, setBusy] = useState(false);
  const file = useRef<HTMLInputElement>(null);

  useEffect(() => { fetch(`${API}/health`).then(r => r.json()).then(setHealth).catch(() => setOffline(true)); }, []);

  async function upload(f: File) {
    setBusy(true); setMsg("");
    const fd = new FormData(); fd.append("file", f);
    try {
      const r = await fetch(`${API}/scans`, { method: "POST", body: fd });
      const d = await r.json();
      setMsg(r.ok ? (d.result?.message ?? "স্ক্যান সংরক্ষিত হয়েছে") : (d.detail ?? "ত্রুটি হয়েছে"));
    } catch { setMsg("সার্ভারের সাথে সংযোগ নেই। ইন্টারনেট দেখে আবার চেষ্টা করুন।"); }
    setBusy(false);
  }

  return (<main>
    <h1>🌿 AgriSpray AI</h1>
    {offline && <div className="glass warn">ব্যাকএন্ড চালু নেই (setup required)।</div>}
    {health && !health.ai_identification && <div className="glass warn">AI সনাক্তকরণ এখনো সেটআপ করা হয়নি।</div>}
    <input ref={file} type="file" accept="image/*" capture="environment" hidden
      onChange={e => e.target.files?.[0] && upload(e.target.files[0])} />
    <button className="hero" disabled={busy} onClick={() => file.current?.click()}>
      {busy ? "আপলোড হচ্ছে…" : "আগাছার ছবি তুলুন"}</button>
    {msg && <p className="glass">{msg}</p>}
    <div className="grid">{tiles.map(t => <button key={t} className="glass tile">{t}</button>)}</div>
    <p className="mut">সনাক্তকরণ ১০০% নিশ্চিত নয়। ওষুধ ব্যবহারের আগে লেবেল পড়ুন ও স্থানীয় কৃষি কর্মকর্তার পরামর্শ নিন।</p>
  </main>);
}
