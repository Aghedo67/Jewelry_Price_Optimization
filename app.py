import streamlit as st
import anthropic
import json

# ── Page config ────────────────────────────────────────────
st.set_page_config(
    page_title="Gem · AI Price Intelligence",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=DM+Mono:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Mono', monospace; }

.stApp { background: #0a0a0f; color: #e8e4dc; }

/* Hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* Sidebar */
[data-testid="stSidebar"] { background: #0f0f17 !important; border-right: 1px solid #1a1a2a; }
[data-testid="stSidebar"] * { color: #b8b4ac !important; }
[data-testid="stSidebar"] .stTextInput input {
    background: #13131e !important; border-color: #2a2a3a !important;
    color: #e8e4dc !important; font-family: 'DM Mono', monospace !important;
    font-size: 0.78rem !important;
}
[data-testid="stSidebar"] .stTextInput input:focus { border-color: #c9a96e !important; }

/* Selectbox */
.stSelectbox > div > div {
    background: #13131e !important;
    border: 1px solid #2a2a3a !important;
    border-radius: 3px !important;
    color: #e8e4dc !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.78rem !important;
}
.stSelectbox > div > div:focus-within { border-color: #c9a96e !important; }
[data-testid="stSelectboxVirtualDropdown"] {
    background: #13131e !important; border: 1px solid #2a2a3a !important;
}

/* Button */
.stButton > button {
    background: #c9a96e; color: #0a0a0f; border: none;
    border-radius: 2px; font-family: 'DM Mono', monospace;
    font-size: 0.72rem; font-weight: 500;
    letter-spacing: 0.3em; text-transform: uppercase;
    padding: 0.75rem 2rem; width: 100%;
    transition: all 0.2s;
}
.stButton > button:hover { background: #dfc08a; transform: translateY(-1px); }
.stButton > button:disabled { opacity: 0.4; }

/* Spinner */
.stSpinner > div { border-top-color: #c9a96e !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-track { background: #0a0a0f; }
::-webkit-scrollbar-thumb { background: #2a2a3a; border-radius: 2px; }

div[data-testid="column"] { padding: 0 0.5rem; }
</style>
""", unsafe_allow_html=True)

# ── Constants ──────────────────────────────────────────────
CATEGORIES    = ["Ring", "Necklace", "Bracelet", "Earring", "Pendant",
                 "Brooch", "Anklet", "Bangle", "Charm", "Watch"]
METALS        = ["Gold", "Silver", "Platinum", "Rose Gold", "White Gold",
                 "Titanium", "Palladium", "Stainless Steel", "Copper", "Bronze"]
GEMS          = ["None", "Diamond", "Ruby", "Emerald", "Sapphire", "Pearl",
                 "Amethyst", "Opal", "Topaz", "Garnet", "Turquoise", "Aquamarine"]
COLORS        = ["Yellow", "White", "Rose", "Silver", "Gold",
                 "Black", "Blue", "Red", "Green", "Multi"]
GENDERS       = ["Female", "Male", "Unisex"]
SKU_QUALITIES = ["1 — Basic", "2 — Standard", "3 — Premium",
                 "4 — Luxury", "5 — Ultra Luxury"]

SYSTEM_PROMPT = """You are a world-class jewelry pricing expert and market analyst with deep knowledge of the global jewelry market. You predict optimal retail prices for jewelry pieces based on their attributes.

When given jewelry attributes, you:
1. Analyze the combination of materials, gem, category, gender, and quality
2. Consider market positioning and comparable pieces
3. Provide a precise USD price prediction
4. Give a recommended price range (min–max)
5. Explain the 3–4 key factors driving the price in clear business language
6. Rate market demand as Low / Medium / High / Very High

Respond ONLY with valid JSON in exactly this structure — no markdown, no extra text:
{
  "predicted_price": 1250,
  "price_min": 950,
  "price_max": 1650,
  "confidence": 87,
  "demand": "High",
  "factors": [
    { "name": "Material Premium", "impact": "high",   "detail": "Platinum commands 3-4x premium over silver due to rarity and durability" },
    { "name": "Gem Value",        "impact": "high",   "detail": "Diamond solitaire adds significant intrinsic and perceived value" },
    { "name": "Category Demand",  "impact": "medium", "detail": "Rings are the highest-demand category, especially for female buyers" },
    { "name": "Quality Tier",     "impact": "medium", "detail": "SKU quality 4 targets luxury segment with refined craftsmanship" }
  ],
  "market_note": "Brief 1-2 sentence market insight for business analysts."
}

Be precise and realistic with pricing. Use current real-world jewelry market knowledge."""


def impact_color(impact: str) -> str:
    return {"high": "#c9a96e", "medium": "#8a9bb8", "low": "#6a6560"}.get(impact, "#6a6560")


def demand_color(demand: str) -> str:
    return {"Very High": "#7ab87a", "High": "#c9a96e",
            "Medium": "#8a9bb8",    "Low": "#b87a7a"}.get(demand, "#6a6560")


def call_claude(api_key: str, attributes: dict) -> dict:
    client = anthropic.Anthropic(api_key=api_key)
    user_prompt = f"""Predict the optimal retail price for this jewelry piece:
- Category: {attributes['category']}
- Main Metal: {attributes['metal']}
- Main Gem: {attributes['gem']}
- Main Color: {attributes['color']}
- Target Gender: {attributes['gender']}
- SKU Quality: {attributes['sku']}

Return only the JSON as specified."""

    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )
    raw = message.content[0].text.strip()
    clean = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(clean)


# ══════════════════════════════════════════════════════════
# SIDEBAR — API KEY
# ══════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style='padding: 1.2rem 0 1.6rem;'>
        <div style='font-family: Cormorant Garamond, serif; font-size: 1.6rem;
                    font-weight: 300; letter-spacing: 0.18em; color: #c9a96e;'>◈ GEM</div>
        <div style='font-size: 0.6rem; letter-spacing: 0.28em; color: #4a4540;
                    text-transform: uppercase; margin-top: 0.2rem;'>AI Price Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    api_key = st.text_input(
        "Anthropic API Key",
        type="password",
        placeholder="sk-ant-…",
        help="Get your key at console.anthropic.com",
    )

    st.markdown("""
    <div style='margin-top: 1.2rem; background: #13131e; border-left: 3px solid #c9a96e;
                border-radius: 0 4px 4px 0; padding: 0.9rem 1rem;
                font-size: 0.68rem; color: #5a5550; line-height: 1.7;'>
        Enter your Anthropic API key above. It is used only for this session and
        never stored. Get a key at
        <a href="https://console.anthropic.com" target="_blank"
           style="color:#c9a96e;">console.anthropic.com</a>.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style='font-size: 0.62rem; color: #3a3530; line-height: 1.9;'>
        <strong style='color:#5a5550; letter-spacing:0.15em;'>HOW IT WORKS</strong><br>
        1. Enter your API key<br>
        2. Configure jewelry attributes<br>
        3. Click Predict Price<br>
        4. Get AI-powered market analysis
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════
st.markdown("""
<div style='border-bottom: 1px solid #1a1a2a; padding: 2rem 2.5rem 1.6rem;
            display: flex; align-items: flex-end; gap: 2rem; flex-wrap: wrap;
            background: #0a0a0f;'>
    <div>
        <div style='font-family: Cormorant Garamond, serif; font-size: 3rem;
                    font-weight: 300; letter-spacing: 0.1em; color: #e8e4dc; line-height: 1;'>
            <span style='color:#c9a96e;'>◈</span> Gem
        </div>
        <div style='font-family: Cormorant Garamond, serif; font-style: italic;
                    font-size: 0.95rem; color: #6a6560; letter-spacing: 0.2em; margin-top: 0.2rem;'>
            AI Price Intelligence
        </div>
    </div>
    <div style='flex: 1; max-width: 520px; font-size: 0.65rem; letter-spacing: 0.12em;
                color: #3a3530; line-height: 1.85;'>
        Describe your jewelry piece — the AI analyzes material rarity, market demand,
        category positioning, and quality tier to recommend an optimal retail price
        with full explainability for business analysts.
    </div>
    <div style='margin-left: auto; font-size: 0.58rem; letter-spacing: 0.2em;
                color: #2a2a3a; text-transform: uppercase;'>
        Powered by Claude AI
    </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# MAIN LAYOUT — FORM + RESULT
# ══════════════════════════════════════════════════════════
col_form, col_result = st.columns([1, 1], gap="medium")

# ── LEFT: FORM ────────────────────────────────────────────
with col_form:
    st.markdown("""
    <div style='padding: 2rem 1.5rem 0;'>
        <div style='font-size:0.58rem; letter-spacing:0.3em; color:#c9a96e;
                    text-transform:uppercase; margin-bottom:0.3rem;'>Configure</div>
        <div style='font-family: Cormorant Garamond, serif; font-size:1.5rem;
                    font-weight:300; color:#e8e4dc; letter-spacing:0.08em; margin-bottom:1.5rem;'>
            Jewelry Attributes
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown("<div style='padding: 0 1.5rem;'>", unsafe_allow_html=True)

        category = st.selectbox("Category",    ["— select —"] + CATEGORIES)
        metal    = st.selectbox("Main Metal",  ["— select —"] + METALS)
        gem      = st.selectbox("Main Gem",    ["— select —"] + GEMS)
        color    = st.selectbox("Main Color",  ["— select —"] + COLORS)
        gender   = st.selectbox("Target Gender", ["— select —"] + GENDERS)
        sku      = st.selectbox("SKU Quality", ["— select —"] + SKU_QUALITIES)

        st.markdown("</div>", unsafe_allow_html=True)

    all_selected = "— select —" not in [category, metal, gem, color, gender, sku]
    has_key      = bool(api_key and api_key.startswith("sk-ant"))

    # progress bar
    filled = sum(1 for v in [category, metal, gem, color, gender, sku]
                 if v != "— select —")
    st.markdown("<div style='padding: 0 1.5rem;'>", unsafe_allow_html=True)

    if filled < 6:
        st.markdown(f"""
        <div style='font-size:0.62rem; color:#3a3530; letter-spacing:0.12em;
                    text-align:center; margin: 0.6rem 0;'>
            {filled} / 6 attributes selected
        </div>
        """, unsafe_allow_html=True)
        prog_w = int((filled / 6) * 100)
        st.markdown(f"""
        <div style='height:2px; background:#1a1a2a; border-radius:2px; margin-bottom:1rem;'>
            <div style='height:100%; width:{prog_w}%; background:#c9a96e;
                        border-radius:2px; transition:width 0.3s;'></div>
        </div>
        """, unsafe_allow_html=True)

    if not has_key and all_selected:
        st.markdown("""
        <div style='background:#1e1a13; border:1px solid #3a3020; border-radius:4px;
                    padding:0.9rem 1.1rem; font-size:0.72rem; color:#c9a96e;
                    margin-bottom:1rem; letter-spacing:0.05em;'>
            ⚠ Enter your Anthropic API key in the sidebar to predict.
        </div>
        """, unsafe_allow_html=True)

    predict_clicked = st.button(
        "◈  Predict Price",
        disabled=not (all_selected and has_key),
    )

    # Show selected tags
    if all_selected:
        tags_html = " ".join([
            f"<span style='display:inline-block;background:#1e1e2e;border:1px solid #2a2a3a;"
            f"border-radius:2px;padding:0.18rem 0.55rem;font-size:0.6rem;"
            f"letter-spacing:0.12em;color:#6a6560;text-transform:uppercase;"
            f"margin:0.15rem;'>{v}</span>"
            for v in [category, metal, gem, color, gender, sku]
        ])
        st.markdown(f"""
        <div style='margin-top:1.2rem;'>
            <div style='font-size:0.56rem;letter-spacing:0.22em;color:#2a2a3a;
                        text-transform:uppercase;margin-bottom:0.5rem;'>Selected</div>
            {tags_html}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ── RIGHT: RESULT ─────────────────────────────────────────
with col_result:
    st.markdown("""
    <div style='padding: 2rem 1.5rem 0;'>
        <div style='font-size:0.58rem; letter-spacing:0.3em; color:#4a4540;
                    text-transform:uppercase; margin-bottom:0.3rem;'>Optimal Price</div>
        <div style='font-family: Cormorant Garamond, serif; font-size:1.5rem;
                    font-weight:300; color:#e8e4dc; letter-spacing:0.08em; margin-bottom:1.5rem;'>
            AI Prediction
        </div>
    </div>
    """, unsafe_allow_html=True)

    result_placeholder = st.empty()

    if not predict_clicked:
        result_placeholder.markdown("""
        <div style='display:flex; flex-direction:column; align-items:center;
                    justify-content:center; height:400px; gap:1rem; text-align:center;'>
            <div style='font-family: Cormorant Garamond, serif; font-size:4rem;
                        color:#1e1e2a; font-weight:300;'>◊</div>
            <div style='font-size:0.62rem; letter-spacing:0.22em; color:#2a2a3a;
                        text-transform:uppercase; line-height:2.2;'>
                Select all attributes<br>and click Predict Price
            </div>
        </div>
        """, unsafe_allow_html=True)

    else:
        attrs = {
            "category": category, "metal": metal, "gem": gem,
            "color": color, "gender": gender, "sku": sku,
        }

        with st.spinner("Analyzing market data…"):
            try:
                r = call_claude(api_key, attrs)

                dc = demand_color(r.get("demand", ""))

                # ── Price card ─────────────────────────────
                st.markdown(f"""
                <div style='background:#0f0f17; border:1px solid #2a2a3a; border-radius:6px;
                            padding:2rem; position:relative; overflow:hidden; margin: 0 1.5rem 1.2rem;'>
                    <div style='position:absolute;top:0;left:0;width:100%;height:2px;
                                background:linear-gradient(90deg,transparent,#c9a96e,transparent);'></div>
                    <div style='text-align:center;'>
                        <div style='font-size:0.6rem;letter-spacing:0.3em;color:#4a4540;
                                    text-transform:uppercase;margin-bottom:0.8rem;'>
                            Recommended Retail Price
                        </div>
                        <div style='font-family: Cormorant Garamond, serif; font-size:4.5rem;
                                    font-weight:300; color:#c9a96e; line-height:1;
                                    letter-spacing:-0.02em;'>
                            ${r.get("predicted_price", 0):,}
                        </div>
                        <div style='font-size:0.7rem;color:#4a4540;letter-spacing:0.15em;
                                    margin-top:0.7rem;'>
                            Range: <span style='color:#7a7570;'>
                                ${r.get("price_min",0):,} – ${r.get("price_max",0):,}
                            </span>
                        </div>
                    </div>
                    <div style='display:grid;grid-template-columns:1fr 1fr;gap:1.4rem;
                                margin-top:1.6rem;padding-top:1.4rem;border-top:1px solid #1a1a2a;'>
                        <div>
                            <div style='font-size:0.56rem;letter-spacing:0.22em;color:#4a4540;
                                        text-transform:uppercase;margin-bottom:0.5rem;'>Confidence</div>
                            <div style='height:3px;background:#1a1a2a;border-radius:2px;overflow:hidden;margin-bottom:0.4rem;'>
                                <div style='height:100%;width:{r.get("confidence",0)}%;
                                            background:linear-gradient(90deg,#c9a96e,#dfc08a);
                                            border-radius:2px;'></div>
                            </div>
                            <div style='font-family: Cormorant Garamond, serif;
                                        font-size:1.4rem; color:#c9a96e;'>
                                {r.get("confidence", 0)}%
                            </div>
                        </div>
                        <div>
                            <div style='font-size:0.56rem;letter-spacing:0.22em;color:#4a4540;
                                        text-transform:uppercase;margin-bottom:0.5rem;'>Market Demand</div>
                            <div style='display:inline-block;background:#13131e;
                                        border:1px solid {dc}44;border-radius:3px;
                                        padding:0.35rem 0.8rem;font-size:0.75rem;
                                        letter-spacing:0.1em;color:{dc};margin-top:0.15rem;'>
                                ● {r.get("demand","—")}
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # ── Price Drivers ──────────────────────────
                st.markdown("""
                <div style='padding: 0 1.5rem;'>
                    <div style='font-size:0.58rem;letter-spacing:0.28em;color:#4a4540;
                                text-transform:uppercase;margin-bottom:0.8rem;'>
                        Price Drivers
                    </div>
                """, unsafe_allow_html=True)

                for f in r.get("factors", []):
                    ic = impact_color(f.get("impact", "low"))
                    st.markdown(f"""
                    <div style='background:#13131e;border:1px solid #2a2a3a;border-radius:4px;
                                padding:0.85rem 1rem;margin-bottom:0.55rem;'>
                        <div style='display:flex;align-items:center;gap:0.6rem;margin-bottom:0.3rem;'>
                            <div style='width:6px;height:6px;border-radius:50%;
                                        background:{ic};flex-shrink:0;'></div>
                            <div style='font-size:0.72rem;font-weight:500;color:#b8b4ac;
                                        letter-spacing:0.05em;'>{f.get("name","")}</div>
                            <div style='margin-left:auto;font-size:0.56rem;letter-spacing:0.15em;
                                        text-transform:uppercase;padding:0.12rem 0.45rem;
                                        border-radius:2px;color:{ic};background:{ic}18;'>
                                {f.get("impact","")}
                            </div>
                        </div>
                        <div style='font-size:0.68rem;color:#4a4540;line-height:1.65;
                                    padding-left:1.2rem;'>{f.get("detail","")}</div>
                    </div>
                    """, unsafe_allow_html=True)

                # ── Market Insight ─────────────────────────
                if r.get("market_note"):
                    st.markdown(f"""
                    <div style='background:#0f0f17;border-left:3px solid #c9a96e;
                                border-radius:0 4px 4px 0;padding:0.9rem 1.1rem;margin-top:0.4rem;'>
                        <div style='font-size:0.56rem;letter-spacing:0.25em;color:#c9a96e;
                                    text-transform:uppercase;margin-bottom:0.4rem;'>Market Insight</div>
                        <div style='font-size:0.72rem;color:#6a6560;line-height:1.7;'>
                            {r.get("market_note","")}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

                # ── Recalculate nudge ──────────────────────
                st.markdown("""
                <div style='font-size:0.6rem;color:#2a2a3a;text-align:center;
                            letter-spacing:0.1em;margin-top:1rem;'>
                    Change any attribute on the left to recalculate
                </div>
                """, unsafe_allow_html=True)

            except json.JSONDecodeError:
                st.error("The AI returned an unexpected format. Please try again.")
            except anthropic.AuthenticationError:
                st.error("Invalid API key. Check your key in the sidebar.")
            except anthropic.RateLimitError:
                st.error("Rate limit reached. Wait a moment and try again.")
            except Exception as e:
                st.error(f"Prediction failed: {e}")
