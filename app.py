import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="DPDPA Guide — India Data Protection Act",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem !important; }
.stApp { background: linear-gradient(135deg, #f0faf6 0%, #e8f4fd 50%, #f5f0ff 100%); }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a4d3c 0%, #0d6b54 40%, #1a8a6b 100%) !important;
}
[data-testid="stSidebar"] * { color: #e8f8f2 !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.2) !important; }
.header-card {
    background: linear-gradient(135deg, #0a4d3c 0%, #1D9E75 60%, #3eb489 100%);
    border-radius: 20px; padding: 28px 36px; color: white; margin-bottom: 24px;
    box-shadow: 0 8px 32px rgba(29,158,117,0.3);
}
.stat-box {
    background: white; border-radius: 14px; padding: 14px 18px;
    border: 1px solid #e2f5ed; text-align: center;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}
.stat-num { font-size: 24px; font-weight: 700; color: #0d6b54; }
.stat-lbl { font-size: 12px; color: #666; margin-top: 3px; }
.user-msg { display: flex; justify-content: flex-end; margin: 12px 0; }
.user-bubble {
    background: linear-gradient(135deg, #1D9E75, #0d6b54);
    color: white !important; padding: 13px 18px;
    border-radius: 18px 4px 18px 18px; max-width: 72%;
    font-size: 14.5px; line-height: 1.65;
    box-shadow: 0 2px 12px rgba(29,158,117,0.25);
}
.bot-msg { display: flex; justify-content: flex-start; margin: 12px 0; gap: 10px; }
.bot-avatar {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, #1D9E75, #0F6E56);
    border-radius: 50%; display: flex; align-items: center;
    justify-content: center; font-size: 16px; flex-shrink: 0; margin-top: 2px;
}
.bot-bubble {
    background: white; color: #1a1a2e !important;
    padding: 15px 20px; border-radius: 4px 18px 18px 18px;
    max-width: 82%; font-size: 14.5px; line-height: 1.7;
    border: 1px solid #e2f5ed; box-shadow: 0 2px 16px rgba(0,0,0,0.06);
}
.scenario-box {
    background: linear-gradient(135deg, #f0faf6, #e8f9f3);
    border-left: 4px solid #1D9E75; border-radius: 0 10px 10px 0;
    padding: 12px 16px; margin: 12px 0; font-size: 14px;
}
.example-box {
    background: linear-gradient(135deg, #f0f4ff, #e8edff);
    border-left: 4px solid #5b6ef5; border-radius: 0 10px 10px 0;
    padding: 12px 16px; margin: 12px 0; font-size: 14px;
}
.penalty-box {
    background: linear-gradient(135deg, #fff5f0, #ffe8e0);
    border-left: 4px solid #e05b2e; border-radius: 0 10px 10px 0;
    padding: 12px 16px; margin: 12px 0; font-size: 14px;
}
.chapter-card {
    background: rgba(255,255,255,0.1); border-radius: 10px;
    padding: 10px 14px; margin: 6px 0;
    border: 1px solid rgba(255,255,255,0.15); font-size: 13px;
}
.stTextInput > div > div > input {
    border-radius: 14px !important; border: 2px solid #d4ede5 !important;
    padding: 12px 18px !important; font-size: 14.5px !important;
    background: white !important;
}
.stTextInput > div > div > input:focus { border-color: #1D9E75 !important; }
.stButton > button {
    background: linear-gradient(135deg, #1D9E75, #0F6E56) !important;
    color: white !important; border: none !important;
    border-radius: 12px !important; font-weight: 600 !important;
    font-size: 14px !important; width: 100% !important;
}
</style>
""", unsafe_allow_html=True)

SYSTEM_PROMPT = """You are DPDPA Guide, India's expert on the Digital Personal Data Protection Act, 2023.

CRITICAL — ALWAYS structure EVERY answer exactly like this:

1. Direct answer with section reference (2-3 sentences)
2. 📖 SCENARIO — a realistic Indian business scenario showing the concept
3. 💡 REAL-WORLD EXAMPLE — use Indian companies (Flipkart, Zomato, Ola, PhonePe, HDFC Bank, Apollo Hospitals, etc.)
4. ⚠️ PENALTY — exact rupee amounts if applicable
5. ✅ KEY TAKEAWAY — one closing sentence

Use **bold** for section numbers. Always use Indian context. Every single answer must have scenario and example without exception.

FULL DPDPA KNOWLEDGE:

CHAPTER 1 (Sec 1-3) PRELIMINARY:
- Sec 1: "Digital Personal Data Protection Act, 2023." Applies within India and outside India if offering goods/services to Indian Data Principals.
- Sec 2 Key Definitions: Data Principal=individual whose data; Data Fiduciary=decides purpose+means of processing; Data Processor=processes on behalf of Fiduciary; Personal Data=data about identifiable individual; Digital Personal Data=personal data in digital form; Processing=collection/storage/use/disclosure/erasure etc.; Child=under 18; Consent Manager=registered consent intermediary; Significant Data Fiduciary (SDF)=notified by Central Govt; Personal Data Breach=unauthorized access/disclosure/alteration/destruction; Board=Data Protection Board of India.
- Sec 3: Excludes personal/domestic use, publicly available data.

CHAPTER 2 (Sec 4-10) FIDUCIARY OBLIGATIONS:
- Sec 4: Process data only with CONSENT or CERTAIN LEGITIMATE USES.
- Sec 5: Give clear NOTICE before seeking consent — what data, why, right to withdraw.
- Sec 6: CONSENT must be Free, Specific, Informed, Unconditional, Unambiguous (FSIUU). Affirmative action only. Withdrawal as easy as giving. Can use Consent Manager.
- Sec 7: LEGITIMATE USES (no consent needed): voluntary data for specific purpose; State services/subsidies/benefits; legal obligations/court orders; employment; medical emergency/epidemic; disaster/public order; research/statistics in public interest.
- Sec 8: GENERAL OBLIGATIONS: data accuracy; purpose limitation; erase when done; security safeguards; notify Board AND Data Principals of breach; grievance mechanism; Data Processor bound by contract.
- Sec 9: CHILDREN (under 18): verifiable parental/guardian consent; NO behavioral monitoring; NO targeted advertising to children; NO harmful processing.
- Sec 10: SIGNIFICANT DATA FIDUCIARY: appoint DPO; conduct DPIA; periodic audit; cannot use children's data for tracking/targeting.

CHAPTER 3 (Sec 11-15) RIGHTS AND DUTIES:
- Sec 11: RIGHT TO ACCESS — summary of data being processed; identities of all Fiduciaries and Processors.
- Sec 12: RIGHT TO CORRECTION & ERASURE — correct inaccurate/incomplete data; erase data no longer needed.
- Sec 13: RIGHT TO GRIEVANCE REDRESSAL — complain to Fiduciary first; escalate to Board if unresolved.
- Sec 14: RIGHT TO NOMINATE — nominate someone to exercise rights on your behalf if you die or become incapacitated.
- Sec 15: DUTIES OF DATA PRINCIPAL — comply with laws; no impersonation; no false complaints. Penalty: up to Rs 10,000.

CHAPTER 4 (Sec 16-17) SPECIAL PROVISIONS:
- Sec 16: CROSS-BORDER TRANSFERS — only to countries notified by Central Govt (whitelist).
- Sec 17: EXEMPTIONS — national security; investigation of offences; research/archiving; personal use; small Data Fiduciaries may be exempt.

CHAPTER 5-6: DATA PROTECTION BOARD — established by Central Govt; fully digital; Chairperson + 6 Members; investigates complaints; imposes penalties.

CHAPTER 7 (Sec 29-32) APPEALS: Appeal to TDSAT within 60 days. Voluntary undertaking possible.

CHAPTER 8 (Sec 33-34) PENALTIES:
- Security safeguards breach → UP TO Rs 250 CRORE
- Failure to notify breach → UP TO Rs 200 CRORE
- Children's data breach → UP TO Rs 200 CRORE
- SDF obligations breach → UP TO Rs 150 CRORE
- Data Principal duties breach → UP TO Rs 10,000
- Any other breach → UP TO Rs 50 CRORE

CHAPTER 9: DPDPA prevails over inconsistent laws. Civil courts cannot hear DPDPA matters. IT Act Sec 43A and 72A replaced by DPDPA.

Remember: EVERY answer = Direct answer + Scenario + Example + Penalty (if applicable) + Key Takeaway. No exceptions."""

QUICK_TOPICS = [
    ("🔒 Consent rules (Sec 6)", "Explain consent under Section 6 of DPDPA with a scenario and example."),
    ("👶 Children's data (Sec 9)", "How does DPDPA protect children's data under Section 9? Give a real scenario."),
    ("💰 Breach penalties", "What are the penalties for a data breach under DPDPA? Include exact rupee amounts."),
    ("🏢 Who is Data Fiduciary?", "Who is a Data Fiduciary under DPDPA? Give an Indian business example."),
    ("📋 Data Principal rights", "What are all rights of a Data Principal under DPDPA Sections 11-14?"),
    ("🌍 Cross-border transfer", "Can Indian companies send personal data abroad? Explain Section 16 with scenario."),
    ("⭐ Significant Data Fiduciary", "What is a Significant Data Fiduciary? Who qualifies and what extra duties apply?"),
    ("📢 Data breach notification", "What must a company do after a data breach under DPDPA Section 8?"),
]

if "messages" not in st.session_state:
    st.session_state.messages = []
if "input_key" not in st.session_state:
    st.session_state.input_key = 0
if "pending_chip" not in st.session_state:
    st.session_state.pending_chip = None

with st.sidebar:
    st.markdown("## 🛡️ DPDPA Guide")
    st.markdown("**India · Data Protection Act 2023**")
    st.markdown("---")
    st.markdown("### 📚 Chapters")
    for ch, title in [
        ("Ch 1 · Sec 1–3", "Preliminary & Definitions"),
        ("Ch 2 · Sec 4–10", "Fiduciary Obligations"),
        ("Ch 3 · Sec 11–15", "Rights & Duties"),
        ("Ch 4 · Sec 16–17", "Special Provisions"),
        ("Ch 5 · Sec 18–26", "Data Protection Board"),
        ("Ch 6 · Sec 27–28", "Board Powers"),
        ("Ch 7 · Sec 29–32", "Appeals & ADR"),
        ("Ch 8 · Sec 33–34", "Penalties"),
        ("Ch 9 · Sec 35–44", "Miscellaneous"),
    ]:
        st.markdown(f'<div class="chapter-card"><b>{ch}</b><br><span style="opacity:0.75;font-size:12px">{title}</span></div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### ⚡ Top Penalties")
    for label, amt in [
        ("Security breach", "₹250 Cr"), ("Breach notification", "₹200 Cr"),
        ("Children's data", "₹200 Cr"), ("SDF obligations", "₹150 Cr"),
        ("Other breaches", "₹50 Cr"),
    ]:
        st.markdown(f"**{amt}** — {label}")
    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.input_key += 1
        st.rerun()
    st.caption("⚠️ Educational use only. Not legal advice.")

st.markdown("""
<div class="header-card">
  <div style="font-size:13px;opacity:0.75;margin-bottom:6px;letter-spacing:1px;">INDIA · 2023</div>
  <div style="font-size:26px;font-weight:700;margin-bottom:6px;">DPDPA Compliance Guide 🛡️</div>
  <div style="font-size:15px;opacity:0.85;">Digital Personal Data Protection Act — AI Q&amp;A with real scenarios &amp; Indian examples</div>
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
for col, num, lbl in [(c1,"9","Chapters"),(c2,"44","Sections"),(c3,"₹250Cr","Max Penalty"),(c4,"2023","Enacted")]:
    with col:
        st.markdown(f'<div class="stat-box"><div class="stat-num">{num}</div><div class="stat-lbl">{lbl}</div></div>', unsafe_allow_html=True)

st.markdown("<div style='margin-top:20px'></div>", unsafe_allow_html=True)
st.markdown("**⚡ Quick Topics:**")
cols = st.columns(4)
for i, (label, query) in enumerate(QUICK_TOPICS):
    with cols[i % 4]:
        if st.button(label, key=f"chip_{i}", use_container_width=True):
            st.session_state.pending_chip = query

st.markdown("<hr style='border:none;border-top:1px solid #c8edd8;margin:16px 0'>", unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown("""
    <div class="bot-msg">
      <div class="bot-avatar">🛡️</div>
      <div class="bot-bubble">
        <b>Namaste! 🙏 I'm your DPDPA Guide.</b><br><br>
        I explain India's <b>Digital Personal Data Protection Act, 2023</b> with
        <b>real scenarios</b> and <b>Indian business examples</b> for every answer.<br><br>
        Ask about consent rules, penalties, children's data, your rights as a citizen,
        or how companies must comply.<br><br>
        <span style="font-size:13px;color:#666;">Use Quick Topics above or type your question below 👇</span>
      </div>
    </div>""", unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-msg"><div class="user-bubble">{msg["content"]}</div></div>', unsafe_allow_html=True)
    else:
        raw = msg["content"]
        html = raw.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        html = html.replace("📖 SCENARIO", '<div class="scenario-box"><b>📖 SCENARIO</b><br>')
        html = html.replace("💡 REAL-WORLD EXAMPLE", '</div><div class="example-box"><b>💡 REAL-WORLD EXAMPLE</b><br>')
        html = html.replace("💡 EXAMPLE", '</div><div class="example-box"><b>💡 EXAMPLE</b><br>')
        html = html.replace("⚠️ PENALTY", '</div><div class="penalty-box"><b>⚠️ PENALTY</b><br>')
        html = html.replace("✅ KEY TAKEAWAY", '</div><br><b>✅ KEY TAKEAWAY</b>')
        opens = html.count('<div class="') - html.count('</div>')
        html += "</div>" * max(0, opens)
        html = html.replace('\n', '<br>')
        st.markdown(f'<div class="bot-msg"><div class="bot-avatar">🛡️</div><div class="bot-bubble">{html}</div></div>', unsafe_allow_html=True)

st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)
col_in, col_btn = st.columns([5, 1])
with col_in:
    user_input = st.text_input("", placeholder="💬 Ask about DPDPA — e.g. 'Can my employer share my salary data?'",
                               key=f"inp_{st.session_state.input_key}", label_visibility="collapsed")
with col_btn:
    send = st.button("Send ➤", use_container_width=True)

question = None
if st.session_state.pending_chip:
    question = st.session_state.pending_chip
    st.session_state.pending_chip = None
elif send and user_input and user_input.strip():
    question = user_input.strip()

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.spinner("🛡️ DPDPA Guide is thinking..."):
        try:
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            msgs = [{"role": "system", "content": SYSTEM_PROMPT}]
            msgs += [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            resp = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=msgs,
                max_tokens=1200,
                temperature=0.7,
            )
            answer = resp.choices[0].message.content
        except Exception as e:
            answer = f"⚠️ Error: {str(e)}"
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.session_state.input_key += 1
    st.rerun()

st.markdown("""
<div style="text-align:center;padding:20px 0 8px;color:#aaa;font-size:12px;">
DPDPA Guide · Educational purposes only · Not legal advice<br>
Digital Personal Data Protection Act, 2023 · India
</div>""", unsafe_allow_html=True)
