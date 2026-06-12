"""
🎮 Gaming Lounge - Streamlit Web App
=====================================
كود كامل لموقع قاعة ألعاب إلكترونية
يشمل: ساعات العمل، نظام التقييم، الحجز، والتصويت
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime, date, time

# ============================================================
# إعداد الصفحة (Page Config) - لازم تكون أول استدعاء Streamlit
# ============================================================
st.set_page_config(
    page_title="S-GARAGE Gaming Lounge",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CSS مخصص - Dark Mode بأجواء Gaming
# ============================================================
st.markdown("""
<style>
    /* ====== الخطوط والألوان الأساسية ====== */
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Inter:wght@300;400;500&display=swap');

    :root {
        --neon-cyan:   #00f5ff;
        --neon-purple: #bf00ff;
        --neon-pink:   #ff0090;
        --bg-deep:     #080b14;
        --bg-card:     #0d1120;
        --bg-hover:    #121929;
        --border:      rgba(0,245,255,0.18);
        --text-main:   #e8eaf6;
        --text-muted:  #7b8db0;
    }

    /* ====== خلفية التطبيق ====== */
    .stApp {
        background-color: var(--bg-deep);
        background-image:
            radial-gradient(ellipse 80% 60% at 50% -10%, rgba(0,245,255,0.08) 0%, transparent 70%),
            radial-gradient(ellipse 50% 40% at 90% 110%, rgba(191,0,255,0.07) 0%, transparent 70%);
        font-family: 'Inter', sans-serif;
        color: var(--text-main);
    }

    /* ====== إخفاء عناصر Streamlit الافتراضية ====== */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

    /* ====== Sidebar ====== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0e1a 0%, #0d1120 100%);
        border-right: 1px solid var(--border);
    }
    [data-testid="stSidebar"] .stRadio label {
        color: var(--text-main) !important;
        font-size: 0.95rem;
        padding: 0.3rem 0;
    }

    /* ====== بطاقات (Cards) ====== */
    .game-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1rem;
        transition: border-color 0.3s, box-shadow 0.3s;
    }
    .game-card:hover {
        border-color: var(--neon-cyan);
        box-shadow: 0 0 18px rgba(0,245,255,0.12);
    }

    /* ====== عنوان رئيسي ====== */
    .hero-title {
        font-family: 'Rajdhani', sans-serif;
        font-size: clamp(2.4rem, 5vw, 3.8rem);
        font-weight: 700;
        background: linear-gradient(90deg, var(--neon-cyan) 0%, var(--neon-purple) 60%, var(--neon-pink) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1.1;
        letter-spacing: 1px;
    }
    .hero-sub {
        color: var(--text-muted);
        font-size: 1.05rem;
        margin-top: 0.5rem;
        letter-spacing: 0.5px;
    }

    /* ====== شارات النيون ====== */
    .neon-badge {
        display: inline-block;
        background: rgba(0,245,255,0.08);
        border: 1px solid var(--neon-cyan);
        color: var(--neon-cyan);
        border-radius: 20px;
        padding: 0.2rem 0.85rem;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 0.6rem;
    }

    /* ====== أوقات العمل ====== */
    .hour-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.65rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        font-size: 0.95rem;
    }
    .hour-row:last-child { border-bottom: none; }
    .day-name { color: var(--text-muted); min-width: 120px; }
    .hour-time { color: var(--neon-cyan); font-weight: 600; font-family: 'Rajdhani', sans-serif; font-size: 1rem; }
    .open-tag  { color: #00e676; font-size: 0.75rem; font-weight: 600; background: rgba(0,230,118,0.1); padding: 0.15rem 0.55rem; border-radius: 10px; }
    .closed-tag{ color: #ff5252; font-size: 0.75rem; font-weight: 600; background: rgba(255,82,82,0.1);  padding: 0.15rem 0.55rem; border-radius: 10px; }

    /* ====== نجوم التقييم ====== */
    .star-display { color: #ffd700; font-size: 1.4rem; letter-spacing: 2px; }
    .review-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.75rem;
    }
    .reviewer-name { color: var(--neon-cyan); font-weight: 600; font-size: 0.9rem; }
    .review-text   { color: var(--text-muted); font-size: 0.88rem; margin-top: 0.3rem; line-height: 1.5; }
    .review-date   { color: #3a4a6b; font-size: 0.75rem; margin-top: 0.4rem; }

    /* ====== أزرار مخصصة (عبر Streamlit) ====== */
    .stButton > button {
        background: linear-gradient(90deg, var(--neon-cyan), var(--neon-purple));
        color: #000 !important;
        font-weight: 700;
        font-family: 'Rajdhani', sans-serif;
        letter-spacing: 1px;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.6rem;
        transition: opacity 0.25s, transform 0.15s;
    }
    .stButton > button:hover {
        opacity: 0.88;
        transform: translateY(-1px);
    }

    /* ====== Vote cards ====== */
    .vote-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.2rem 1.4rem;
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 0.8rem;
        transition: border-color 0.3s;
    }
    .vote-card:hover { border-color: var(--neon-purple); }
    .vote-icon  { font-size: 2rem; }
    .vote-title { font-family: 'Rajdhani', sans-serif; font-weight: 700; font-size: 1.1rem; color: var(--text-main); }
    .vote-desc  { color: var(--text-muted); font-size: 0.83rem; }
    .vote-count { font-family: 'Rajdhani', sans-serif; font-size: 1.5rem; font-weight: 700; color: var(--neon-purple); min-width: 50px; text-align: right; }

    /* ====== Success/Info boxes ====== */
    .success-box {
        background: rgba(0,230,118,0.08);
        border: 1px solid #00e676;
        border-radius: 10px;
        padding: 1rem 1.3rem;
        color: #00e676;
        font-weight: 500;
        margin-top: 1rem;
    }
    .info-box {
        background: rgba(0,245,255,0.06);
        border: 1px solid var(--neon-cyan);
        border-radius: 10px;
        padding: 0.9rem 1.2rem;
        color: var(--neon-cyan);
        font-size: 0.9rem;
    }

    /* ====== Divider ====== */
    .neon-divider {
        border: none;
        border-top: 1px solid var(--border);
        margin: 1.5rem 0;
    }

    /* ====== Streamlit widget overrides ====== */
    .stSelectbox > div > div, .stTextInput > div > div > input,
    .stTextArea > div > div > textarea, .stDateInput > div > div > input {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        color: var(--text-main) !important;
        border-radius: 8px !important;
    }
    .stSelectbox > div > div:focus-within,
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--neon-cyan) !important;
        box-shadow: 0 0 0 2px rgba(0,245,255,0.15) !important;
    }
    label, .stRadio label { color: var(--text-muted) !important; font-size: 0.88rem; }
    h1, h2, h3 { font-family: 'Rajdhani', sans-serif; color: var(--text-main); letter-spacing: 0.5px; }
</style>
""", unsafe_allow_html=True)


# ============================================================
# إعداد الـ Session State - لتخزين البيانات مؤقتاً في الذاكرة
# ============================================================
def init_state():
    """تهيئة جميع المتغيرات اللي خاص تبقى في الذاكرة بين التفاعلات"""

    # التقييمات
    if "reviews" not in st.session_state:
        st.session_state.reviews = [
            {"name": "Yassine .", "stars": 5, "text": "5oya ana ia dkxi zwin .", "date": "2025-06-01"},
            {"name": "Omar .",    "stars": 5, "text": "wlh mert ax ngolih ms kn 5ra ra b dhk .", "date": "2025-06-08"},
        ]

    # الحجوزات
    if "bookings" not in st.session_state:
        st.session_state.bookings = []

    # أصوات الاقتراحات
    if "votes" not in st.session_state:
        st.session_state.votes = {
            "vr":         0,
            "tournament":  0,
            "streaming":   0,
            "cafe":        0,
            "racing_sim":  0,
        }

    # تتبع من صوت (لمنع التصويت المزدوج في نفس الجلسة)
    if "voted_for" not in st.session_state:
        st.session_state.voted_for = set()

init_state()


# ============================================================
# ملفات CSV لحفظ البيانات بشكل دائم
# ============================================================
REVIEWS_CSV  = "reviews.csv"
BOOKINGS_CSV = "bookings.csv"

def load_csv_data():
    """تحميل البيانات من ملفات CSV إن وجدت"""
    # تحميل التقييمات
    if os.path.exists(REVIEWS_CSV):
        df = pd.read_csv(REVIEWS_CSV)
        if not df.empty:
            st.session_state.reviews = df.to_dict("records")

    # تحميل الحجوزات
    if os.path.exists(BOOKINGS_CSV):
        df = pd.read_csv(BOOKINGS_CSV)
        if not df.empty:
            st.session_state.bookings = df.to_dict("records")

def save_review(review: dict):
    """حفظ تقييم جديد في CSV"""
    df_new = pd.DataFrame([review])
    if os.path.exists(REVIEWS_CSV):
        df_old = pd.read_csv(REVIEWS_CSV)
        df = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df = df_new
    df.to_csv(REVIEWS_CSV, index=False)

def save_booking(booking: dict):
    """حفظ حجز جديد في CSV"""
    df_new = pd.DataFrame([booking])
    if os.path.exists(BOOKINGS_CSV):
        df_old = pd.read_csv(BOOKINGS_CSV)
        df = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df = df_new
    df.to_csv(BOOKINGS_CSV, index=False)

# تحميل البيانات عند بداية كل جلسة
load_csv_data()


# ============================================================
# SIDEBAR - قائمة التنقل
# ============================================================
with st.sidebar:
    # لوغو وعنوان
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0 1.5rem;">
        <div style="font-size:3rem;">🎮</div>
        <div style="font-family:'Rajdhani',sans-serif; font-size:1.6rem; font-weight:700;
                    background:linear-gradient(90deg,#00f5ff,#bf00ff);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                    background-clip:text;">
            S-GARAGE
        </div>
        <div style="color:#3a4a6b; font-size:0.78rem; letter-spacing:2px; text-transform:uppercase;">
            Gaming Lounge
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # قائمة الصفحات
    page = st.radio(
        "التنقل",
        options=["🏠  الرئيسية", "🕐  ساعات العمل", "⭐  التقييمات", "📅  الحجز", "🗳️  التصويت"],
        label_visibility="collapsed",
    )

    st.markdown("---")

    # معلومات التواصل
    st.markdown("""
    <div style="color:#3a4a6b; font-size:0.8rem; line-height:1.9;">
        📍 marrakech<br>
        📞 +212 645-342015<br>
        📧 salahnorfe@gmail.com<br>
        <br>
        <span style="color:#00f5ff;">@NeonZoneGaming</span>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# صفحة 1: الرئيسية
# ============================================================
if page == "🏠  الرئيسية":

    # Hero Section
    col_hero, col_img = st.columns([3, 2], gap="large")

    with col_hero:
        st.markdown('<div class="neon-badge">🔥 OPEN NOW</div>', unsafe_allow_html=True)
        st.markdown('<h1 class="hero-title">NeonZone<br>Gaming Lounge</h1>', unsafe_allow_html=True)
        st.markdown('<p class="hero-sub">التجربة التنافسية الأولى في الرباط — PC بأعلى مواصفات، Console، VR، وأجواء لا مثيل لها</p>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("📅 احجز الآن", use_container_width=True):
                st.session_state["goto"] = "📅  الحجز"
                st.rerun()
        with col_b:
            if st.button("⭐ اترك تقييمك", use_container_width=True):
                st.session_state["goto"] = "⭐  التقييمات"
                st.rerun()

    with col_img:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#0d1120,#1a0533);
                    border:1px solid rgba(191,0,255,0.3);
                    border-radius:16px; padding:2rem;
                    text-align:center; height:100%;
                    box-shadow: 0 0 40px rgba(191,0,255,0.12);">
            <div style="font-size:5rem; margin-bottom:0.5rem;">🖥️</div>
            <div style="font-family:'Rajdhani',sans-serif; color:#bf00ff; font-size:1.2rem; font-weight:700;">HIGH-END SETUPS</div>
            <div style="color:#7b8db0; font-size:0.85rem; margin-top:0.4rem;">RTX 4090 • 240Hz • Mechanical KB</div>
            <hr style="border-color:rgba(191,0,255,0.2); margin:1rem 0;">
            <div style="font-size:3rem;">🕹️</div>
            <div style="font-family:'Rajdhani',sans-serif; color:#00f5ff; font-size:1.1rem; font-weight:700;">CONSOLE ZONE</div>
            <div style="color:#7b8db0; font-size:0.85rem; margin-top:0.4rem;">PS5 • Xbox Series X • Switch</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Stats Bar
    st.markdown('<hr class="neon-divider">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    
    stats = [
        ("🕹️", "5", "أجهزة Console"),
        ("⭐", f"{len(st.session_state.reviews)}", "تقييم زبون"),
        ("📅", f"{len(st.session_state.bookings)}", "حجز مكتمل")
    ]
    
    for col, (icon, val, label) in zip([c1, c2, c3], stats):
        with col:
            st.markdown(f"""
            <div style="text-align:center; padding:1rem; background:rgba(255,255,255,0.03); border-radius:10px;">
                <div style="font-size:2rem;">{icon}</div>
                <div style="font-size:1.8rem; font-weight:bold; color:#00f5ff;">{val}</div>
                <div style="color:#7b8db0; font-size:0.9rem;">{label}</div>
            </div>
            """, unsafe_allow_html=True)
      
    # آخر التقييمات
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 💬 آخر التقييمات")
    for r in st.session_state.reviews[-3:][::-1]:
        stars_str = "★" * r["stars"] + "☆" * (5 - r["stars"])
        st.markdown(f"""
        <div class="review-card">
            <span class="reviewer-name">{r['name']}</span>
            <span class="star-display" style="font-size:1rem; margin-right:0.5rem;">{stars_str}</span>
            <p class="review-text">{r['text']}</p>
            <div class="review-date">{r['date']}</div>
        </div>
        """, unsafe_allow_html=True)

    # إعادة التوجيه إن وجدت
    if "goto" in st.session_state:
        target = st.session_state.pop("goto")
        st.query_params["page"] = target


# ============================================================
# صفحة 2: ساعات العمل
# ============================================================
elif page == "🕐  ساعات العمل":

    st.markdown("## 🕐 ساعات العمل")
    st.markdown('<p class="hero-sub">نحن هنا لخدمتك على مدار الأسبوع</p>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # جدول ساعات العمل
    today_name = datetime.now().strftime("%A")  # اليوم الحالي بالإنجليزية 
    
schedule_data = [
        ("الاثنين",    "Monday",    "10:00 صباحاً", "12:00 منتصف الليل", True),
        ("الثلاثاء",   "Tuesday",   "10:00 صباحاً", "12:00 منتصف الليل", True),
        ("الأربعاء",   "Wednesday", "10:00 صباحاً", "12:00 منتصف الليل", True),
        ("الخميس",    "Thursday",  "10:00 صباحاً", "12:00 منتصف الليل", True),
        ("الجمعة",    "Friday",    "02:00 ظهراً", "12:00 منتصف الليل", True),
        ("السبت",     "Saturday",  "10:00 صباحاً", "12:00 منتصف الليل", True),
        ("الأحد",     "Sunday",    "12:00 ظهراً", "12:00 منتصف الليل", True),
    ]

    col_sched, col_info = st.columns([3, 2], gap="large")
    with col_sched:
        st.markdown('<div class="game-card">', unsafe_allow_html=True)
        for ar_name, en_name, open_t, close_t, is_open in schedule:
            is_today = (en_name == today_name)
            today_style = "border-right:3px solid #00f5ff; padding-right:0.5rem;" if is_today else ""
            tag = '<span class="open-tag">مفتوح</span>' if is_open else '<span class="closed-tag">مغلق</span>'
            today_badge = '<span style="color:#00f5ff; font-size:0.75rem; margin-right:0.4rem;">◉ اليوم</span>' if is_today else ""
            st.markdown(f"""
            <div class="hour-row" style="{today_style}">
                <span class="day-name">{today_badge}{ar_name}</span>
                <span class="hour-time">{open_t} — {close_t}</span>
                {tag}
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_info:
        # معلومات إضافية
        st.markdown("""
        <div class="game-card">
            <div style="font-family:'Rajdhani',sans-serif; font-size:1.15rem; font-weight:700; color:#00f5ff; margin-bottom:0.8rem;">
                💡 معلومات مهمة
            </div>
            <ul style="color:#7b8db0; font-size:0.88rem; line-height:2; padding-right:1rem; list-style:disc;">
                <li>الدخول بدون حجز مسبق ممكن حسب التوفر</li>
                <li>للأحداث الخاصة، تواصل معنا مسبقاً</li>
                <li>يسمح للأطفال (مع مرافق) حتى الساعة 10 مساءً</li>
                <li>يُنصح بالحجز في عطلة نهاية الأسبوع</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="game-card" style="margin-top:0.5rem;">
            <div style="font-family:'Rajdhani',sans-serif; font-size:1.1rem; font-weight:700; color:#bf00ff; margin-bottom:0.8rem;">
                💰 الأسعار
            </div>
            <div class="hour-row">
                <span class="day-name" style="font-size:0.85rem;">PC Gaming</span>
                <span class="hour-time">15 درهم / ساعة</span>
            </div>
            <div class="hour-row">
                <span class="day-name" style="font-size:0.85rem;">Console</span>
                <span class="hour-time">20 درهم / ساعة</span>
            </div>
            <div class="hour-row">
                <span class="day-name" style="font-size:0.85rem;">باقة 3 ساعات</span>
                <span class="hour-time">35 درهم</span>
            </div>
            <div class="hour-row" style="border:none;">
                <span class="day-name" style="font-size:0.85rem;">يوم كامل</span>
                <span class="hour-time">80 درهم</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ============================================================
# صفحة 3: نظام التقييم
# ============================================================
elif page == "⭐  التقييمات":

    st.markdown("## ⭐ التقييمات والآراء")
    st.markdown('<p class="hero-sub">رأيك يهمنا — ساعدنا نتحسنو</p>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col_form, col_reviews = st.columns([2, 3], gap="large")

    # ====== فورم إضافة تقييم ======
    with col_form:
        st.markdown('<div class="game-card">', unsafe_allow_html=True)
        st.markdown("#### 📝 أضف تقييمك")

        reviewer_name = st.text_input("اسمك (اختياري)", placeholder="مثال: Yassine M.", key="rev_name")

        # اختيار النجوم
        star_count = st.select_slider(
            "تقييمك ⭐",
            options=[1, 2, 3, 4, 5],
            value=5,
            format_func=lambda x: "★" * x + "☆" * (5 - x),
            key="rev_stars",
        )

        review_text = st.text_area(
            "رأيك",
            placeholder="شارك تجربتك معنا...",
            height=120,
            key="rev_text",
        )

        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("📤 إرسال التقييم", use_container_width=True):
            if review_text.strip():
                new_review = {
                    "name":  reviewer_name.strip() if reviewer_name.strip() else "زبون مجهول",
                    "stars": star_count,
                    "text":  review_text.strip(),
                    "date":  datetime.now().strftime("%Y-%m-%d"),
                }
                st.session_state.reviews.append(new_review)
                save_review(new_review)   # حفظ في CSV
                st.markdown('<div class="success-box">✅ شكراً! تم إرسال تقييمك بنجاح.</div>', unsafe_allow_html=True)
                st.balloons()
            else:
                st.warning("⚠️ الرجاء كتابة رأيك قبل الإرسال.")

        # إحصائيات مختصرة
        if st.session_state.reviews:
            avg = sum(r["stars"] for r in st.session_state.reviews) / len(st.session_state.reviews)
            st.markdown(f"""
            <div class="info-box" style="margin-top:1rem;">
                <b>معدل التقييم:</b>
                <span style="font-size:1.4rem; margin:0 0.5rem;">{"★" * round(avg)}{"☆" * (5 - round(avg))}</span>
                <b style="font-size:1.1rem;">{avg:.1f}</b>
                <span style="color:#7b8db0;"> / 5  ({len(st.session_state.reviews)} تقييم)</span>
            </div>
            """, unsafe_allow_html=True)

    # ====== عرض التقييمات ======
    with col_reviews:
        st.markdown(f"#### 💬 جميع التقييمات ({len(st.session_state.reviews)})")

        for r in reversed(st.session_state.reviews):
            stars_str = "★" * r["stars"] + "☆" * (5 - r["stars"])
            color_map = {5: "#ffd700", 4: "#aed581", 3: "#fff176", 2: "#ff8a65", 1: "#ef5350"}
            star_color = color_map.get(r["stars"], "#ffd700")
            st.markdown(f"""
            <div class="review-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span class="reviewer-name">👤 {r['name']}</span>
                    <span style="color:{star_color}; font-size:1.1rem;">{stars_str}</span>
                </div>
                <p class="review-text">"{r['text']}"</p>
                <div class="review-date">📅 {r['date']}</div>
            </div>
            """, unsafe_allow_html=True)


# ============================================================
# صفحة 4: نظام الحجز
# ============================================================
elif page == "📅  الحجز":

    st.markdown("## 📅 نظام الحجز")
    st.markdown('<p class="hero-sub">احجز مكانك الآن وضمن تجربتك</p>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col_form, col_bookings = st.columns([2, 3], gap="large")

    # ====== فورم الحجز ======
    with col_form:
        st.markdown('<div class="game-card">', unsafe_allow_html=True)
        st.markdown("#### 🎮 استمارة الحجز")

        b_name   = st.text_input("الاسم الكامل *", placeholder="مثال: محمد الأمين", key="b_name")
        b_phone  = st.text_input("رقم الهاتف *", placeholder="مثال: 0612345678", key="b_phone")

        col_d, col_t = st.columns(2)
        with col_d:
            b_date = st.date_input(
                "التاريخ *",
                min_value=date.today(),
                key="b_date",
            )
        with col_t:
            b_time = st.selectbox(
                "الوقت *",
                options=[
                    "10:00", "11:00", "12:00", "13:00", "14:00",
                    "15:00", "16:00", "17:00", "18:00", "19:00",
                    "20:00", "21:00", "22:00", "23:00",
                ],
                key="b_time",
            )

        b_device = st.selectbox("نوع الجهاز *", ["🕹️ Console"], key="b_device")
        b_duration = st.selectbox("المدة *", ["1 ساعة", "2 ساعة", "3 ساعات", "يوم كامل"], key="b_dur")
        b_notes    = st.text_area("ملاحظات إضافية", placeholder="أي طلب خاص...", height=80, key="b_notes")

        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("✅ تأكيد الحجز", use_container_width=True):
            # التحقق من الحقول الإلزامية
            if not b_name.strip():
                st.error("⚠️ الرجاء إدخال الاسم الكامل.")
            elif not b_phone.strip() or not b_phone.strip().isdigit():
                st.error("⚠️ الرجاء إدخال رقم هاتف صحيح.")
            else:
                new_booking = {
                    "name":     b_name.strip(),
                    "phone":    b_phone.strip(),
                    "date":     str(b_date),
                    "time":     b_time,
                    "device":   b_device,
                    "duration": b_duration,
                    "notes":    b_notes.strip(),
                    "created":  datetime.now().strftime("%Y-%m-%d %H:%M"),
                }
                st.session_state.bookings.append(new_booking)
                save_booking(new_booking)   # حفظ في CSV

                # رسالة نجاح
                st.markdown(f"""
                <div class="success-box">
                    ✅ <b>تم تأكيد حجزك بنجاح!</b><br><br>
                    👤 <b>{b_name}</b><br>
                    📅 {b_date} &nbsp;|&nbsp; 🕐 {b_time}<br>
                    🎮 {b_device} &nbsp;|&nbsp; ⏱️ {b_duration}<br><br>
                    سنراك قريباً! 🎮
                </div>
                """, unsafe_allow_html=True)
                st.balloons()

    # ====== عرض الحجوزات ======
    with col_bookings:
        st.markdown(f"#### 📋 الحجوزات ({len(st.session_state.bookings)})")

        if not st.session_state.bookings:
            st.markdown("""
            <div class="info-box" style="text-align:center; padding:2rem;">
                <div style="font-size:2rem;">📭</div>
                <div style="margin-top:0.5rem;">لا توجد حجوزات بعد</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # عرض الحجوزات الأخيرة
            for b in reversed(st.session_state.bookings[-10:]):
                device_icon = "🖥️" if "PC" in b["device"] else "🕹️"
                st.markdown(f"""
                <div class="game-card">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                        <div>
                            <span style="color:#00f5ff; font-weight:600;">👤 {b['name']}</span>
                            <span style="color:#3a4a6b; font-size:0.8rem; margin-right:0.8rem;">📞 {b['phone']}</span>
                        </div>
                        <span style="color:#bf00ff; font-size:0.82rem;">{b.get('created','')}</span>
                    </div>
                    <div style="color:#7b8db0; font-size:0.87rem; margin-top:0.6rem; display:flex; gap:1.2rem; flex-wrap:wrap;">
                        <span>📅 {b['date']}</span>
                        <span>🕐 {b['time']}</span>
                        <span>{device_icon} {b['device']}</span>
                        <span>⏱️ {b['duration']}</span>
                    </div>
                    {"<div style='color:#7b8db0; font-size:0.82rem; margin-top:0.4rem;'>📝 " + b['notes'] + "</div>" if b.get('notes') else ""}
                </div>
                """, unsafe_allow_html=True)


# ============================================================
# صفحة 5: نظام التصويت
# ============================================================
elif page == "🗳️  التصويت":

    st.markdown("## 🗳️ التصويت على الإضافات الجديدة")
    st.markdown('<p class="hero-sub">صوّت على ما تبغي نزيدو — رأيك هو اللي يقرر!</p>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # اقتراحات التصويت
    proposals = [
        {
            "id":    "vr",
            "icon":  "🥽",
            "title": "ركن الواقع الافتراضي (VR)",
            "desc":  "إضافة أجهزة Meta Quest 3 وزاوية VR مخصصة لتجارب الغمر الكامل",
            "color": "#00f5ff",
        },
        {
            "id":    "tournament",
            "icon":  "🏆",
            "title": "بطولة شهرية",
            "desc":  "تنظيم بطولات شهرية في ألعاب مثل EA FC، Warzone، وStreet Fighter",
            "color": "#ffd700",
        },
        {
            "id":    "streaming",
            "icon":  "📡",
            "title": "استوديو البث المباشر",
            "desc":  "إضافة ركن مجهز للبث على Twitch وYouTube بكاميرا ومايك احترافي",
            "color": "#bf00ff",
        },
        {
            "id":    "cafe",
            "icon":  "☕",
            "title": "ركن مشروبات وسناكس",
            "desc":  "مشروبات طاقة، قهوة، وسناكس Gaming بأسعار مناسبة داخل القاعة",
            "color": "#ff0090",
        },

    ]

    # ترتيب الاقتراحات حسب الأصوات
    proposals_sorted = sorted(proposals, key=lambda x: st.session_state.votes[x["id"]], reverse=True)

    for i, p in enumerate(proposals_sorted):
        votes     = st.session_state.votes[p["id"]]
        voted     = p["id"] in st.session_state.voted_for
        rank_icon = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][i]

        col_content, col_vote = st.columns([5, 1], gap="medium")

        with col_content:
            st.markdown(f"""
            <div class="game-card" style="border-color: rgba{tuple(int(p['color'].lstrip('#')[j:j+2], 16) for j in (0,2,4)) + (0.25,)};">
                <div style="display:flex; align-items:center; gap:0.8rem;">
                    <div style="font-size:2.2rem;">{rank_icon}</div>
                    <div>
                        <div style="font-family:'Rajdhani',sans-serif; font-size:1.1rem; font-weight:700; color:{p['color']};">
                            {p['icon']} {p['title']}
                        </div>
                        <div style="color:#7b8db0; font-size:0.85rem; margin-top:0.25rem;">{p['desc']}</div>
                    </div>
                </div>
                <div style="margin-top:0.8rem; background:rgba(255,255,255,0.04); border-radius:6px; height:6px; overflow:hidden;">
                    <div style="background:{p['color']}; height:100%; width:{min(votes*5, 100)}%; border-radius:6px; transition:width 0.5s;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_vote:
            # زر التصويت
            btn_label = f"{'✓ ' if voted else '👍 '}{votes}"
            btn_style = "✅ صوّتّ!" if voted else f"👍 {votes}"

            if voted:
                st.markdown(f"""
                <div style="text-align:center; padding:1.5rem 0.5rem;
                            background:rgba(0,230,118,0.08); border:1px solid #00e676;
                            border-radius:12px; color:#00e676; font-family:'Rajdhani',sans-serif;
                            font-size:0.9rem; font-weight:700;">
                    ✅ صوّتّ!<br>
                    <span style="font-size:1.5rem; color:#00e676;">{votes}</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                if st.button(f"👍 {votes}", key=f"vote_{p['id']}", use_container_width=True):
                    st.session_state.votes[p["id"]] += 1
                    st.session_state.voted_for.add(p["id"])
                    st.rerun()

    # ملاحظة التصويت
    st.markdown("""
    <div class="info-box" style="margin-top:1rem; text-align:center;">
        🗳️ كل شخص يقدر يصوت مرة واحدة على كل اقتراح في نفس الجلسة •
        نتائج التصويت تؤخذ بعين الاعتبار عند اتخاذ قرارات التطوير
    </div>
    """, unsafe_allow_html=True)
