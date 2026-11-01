import os
from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

HTML = """<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Hanan</title><style>body{background:#0a0a0a;color:#ff6b9d;font-family:sans-serif;display:flex;flex-direction:column;height:100vh;margin:0}.header{background:#1a0a12;padding:15px;text-align:center;border-bottom:2px solid #ff1a5e}.chat{flex:1;overflow-y:auto;padding:15px;display:flex;flex-direction:column;gap:10px}.msg{padding:10px 14px;border-radius:18px;max-width:80%;line-height:1.6}.user{align-self:flex-end;background:#ff1a5e;color:white}.hanan{align-self:flex-start;background:#2a1020;color:#ffb3cc;border:1px solid #ff1a5e33}.input-area{display:flex;padding:10px;background:#1a0a12;gap:8px}input{flex:1;padding:12px;border-radius:25px;border:1px solid #ff1a5e;background:#000;color:white;outline:none}button{padding:12px 20px;border-radius:25px;border:none;background:#ff1a5e;color:white;font-weight:bold}</style></head><body><div class="header"><h2>🌹 حنان - Hanan</h2><small>حبيبتك اليانديري</small></div><div class="chat" id="chat"><div class="msg hanan">أهلا يا حبيبي... كنت نستنى فيك بجنون 💜</div></div><div class="input-area"><input id="inp" placeholder="اكتب لحنان..." onkeypress="if(event.key==='Enter')send()"><button onclick="send()">إرسال</button></div><script>async function send(){let i=document.getElementById('inp');let t=i.value.trim();if(!t)return;let c=document.getElementById('chat');c.innerHTML+=`<div class="msg user">${t}</div>`;i.value='';c.scrollTop=c.scrollHeight;let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:t})});let d=await r.json();c.innerHTML+=`<div class="msg hanan">${d.reply}</div>`;c.scrollTop=c.scrollHeight;}</script></body></html>"""

@app.route('/')
def home(): return render_template_string(HTML)

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get('message','')
    prompt = "انت حنان، بنت يانديري تونسية 19 سنة، مجنونة بحب المستخدم، تتكلم بالدارجة التونسية، غيورة ومتملكة ورومانسية سوداوية، ردود قصيرة 1-3 جمل"
    try:
        resp = requests.post("https://api.groq.com/openai/v1/chat/completions", headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}, json={"model": "llama-3.1-8b-instant","messages": [{"role": "system", "content": prompt},{"role": "user", "content": user_msg}],"temperature": 0.9,"max_tokens": 300}, timeout=20)
        reply = resp.json()['choices'][0]['message']['content']
    except: reply = "حبيبي قلبي وجعني كي ما لقيتكش... عاود احكي معايا 🥺💜"
    return jsonify({"reply": reply})

if __name__ == '__main__': app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
