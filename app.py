import streamlit as st
from datetime import datetime

# === CONFIGURATION PWA ===
st.set_page_config(
    page_title="FridgeFlow",
    page_icon="🥬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Ajout des métadonnées PWA
st.markdown("""
    <head>
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black">
        <meta name="theme-color" content="#10b981">
        <link rel="manifest" href="manifest.json">
    </head>
""", unsafe_allow_html=True)

st.title("🥬 FridgeFlow")
st.subheader("What can I make with what I have?")

# Session state
if "ingredients" not in st.session_state:
    st.session_state.ingredients = []
if "favorites" not in st.session_state:
    st.session_state.favorites = []
if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar
with st.sidebar:
    st.header("Preferences")
    diet = st.selectbox("Diet", ["Anything", "Vegetarian", "Vegan", "Keto", "High-Protein"])
    max_time = st.slider("Max time (minutes)", 10, 60, 30)
    
    if st.button("Clear All Data"):
        st.session_state.ingredients = []
        st.session_state.favorites = []
        st.session_state.history = []
        st.success("Everything cleared!")

# Main interface
col1, col2 = st.columns([3,1])
with col1:
    new_item = st.text_input("Add ingredient (chicken, rice, tomatoes...)", key="new_item")
with col2:
    if st.button("Add", use_container_width=True) and new_item:
        st.session_state.ingredients.append(new_item.strip().lower())
        st.rerun()

st.markdown("### Your Fridge")
if st.session_state.ingredients:
    for i, ing in enumerate(st.session_state.ingredients):
        if st.button(f"❌ {ing}", key=f"del{i}"):
            st.session_state.ingredients.pop(i)
            st.rerun()
else:
    st.info("Add ingredients above ↑")

if st.button("🍳 Get Smart Recipe Ideas", type="primary", use_container_width=True):
    if len(st.session_state.ingredients) < 2:
        st.error("Add at least 2 ingredients!")
    else:
        with st.spinner("Grok is thinking of delicious recipes..."):
            # Future : On pourra mettre du vrai Grok ici
            recipes = [
                {"name": "One-Pan Garlic Chicken Rice", "time": 35, "match": "94%", "tips": "High protein"},
                {"name": "Quick Asian Veggie Stir Fry", "time": 18, "match": "89%", "tips": "Vegan"},
                {"name": "Creamy Greek Yogurt Chicken Bowl", "time": 12, "match": "82%", "tips": "Keto friendly"}
            ]
            for r in recipes:
                with st.expander(f"**{r['name']}** — {r['time']} min • {r['match']}"):
                    st.caption(r["tips"])
                    col_a, col_b = st.columns(2)
                    with col_a:
                        if st.button("✅ I Made This", key=r['name']):
                            st.session_state.history.append({"name": r['name'], "date": datetime.now().strftime("%b %d")})
                            st.success("Great job!")
                    with col_b:
                        if st.button("⭐ Favorite", key="fav"+r['name']):
                            st.session_state.favorites.append(r)
                            st.success("Saved to favorites!")

# Tabs
tab1, tab2 = st.tabs(["⭐ Favorites", "📖 History"])
with tab1:
    st.write(st.session_state.favorites if st.session_state.favorites else "No favorites yet")
with tab2:
    for meal in reversed(st.session_state.history[-10:]):
        st.caption(f"✅ {meal['name']} — {meal['date']}")

st.caption("FridgeFlow • Installable App")
