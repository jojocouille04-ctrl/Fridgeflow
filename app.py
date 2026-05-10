import streamlit as st
from datetime import datetime

st.set_page_config(page_title="FridgeFlow", page_icon="🥬", layout="centered")

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
    
    st.divider()
    if st.button("Clear All Data"):
        st.session_state.ingredients = []
        st.session_state.favorites = []
        st.session_state.history = []
        st.success("Everything cleared!")

# Main app
col1, col2 = st.columns([3, 1])
with col1:
    new_item = st.text_input("Add ingredient (e.g. chicken thighs, rice, tomatoes)", key="new")
with col2:
    if st.button("Add", use_container_width=True) and new_item.strip():
        st.session_state.ingredients.append(new_item.strip().lower())
        st.rerun()

# Show ingredients
st.markdown("### Your Fridge")
if st.session_state.ingredients:
    cols = st.columns(4)
    for i, ing in enumerate(st.session_state.ingredients[:]):
        if cols[i % 4].button(f"❌ {ing}", key=f"del{i}"):
            st.session_state.ingredients.pop(i)
            st.rerun()
else:
    st.info("Add ingredients above to get started")

# Generate recipes
if st.button("🍳 Get Recipe Ideas", type="primary", use_container_width=True):
    if not st.session_state.ingredients:
        st.error("Add at least 2-3 ingredients!")
    else:
        with st.spinner("Finding the best recipes for you..."):
            # Mock smart recipes - replace with Grok API call later
            sample_recipes = [
                {
                    "name": "One-Pan Lemon Garlic Chicken & Rice",
                    "time": 35,
                    "match": 92,
                    "missing": ["lemon"],
                    "instructions": "Season chicken with garlic and lemon. Bake with rice at 425°F for 30 min.",
                    "tips": "High protein • Great for meal prep"
                },
                {
                    "name": "Quick Veggie Stir Fry Bowl",
                    "time": 20,
                    "match": 88,
                    "missing": ["soy sauce"],
                    "instructions": "Stir fry veggies with garlic. Serve over rice.",
                    "tips": "Vegan & ready in 20 minutes"
                },
                {
                    "name": "High-Protein Greek Yogurt Chicken Salad",
                    "time": 15,
                    "match": 75,
                    "missing": ["greek yogurt"],
                    "instructions": "Mix shredded chicken with yogurt and spices.",
                    "tips": "Keto friendly"
                }
            ]
            
            st.success(f"Here are {len(sample_recipes)} great ideas!")
            
            for recipe in sample_recipes:
                with st.expander(f"**{recipe['name']}** — {recipe['time']} min • Match: {recipe['match']}%"):
                    st.write(recipe["instructions"])
                    st.caption(recipe["tips"])
                    if recipe["missing"]:
                        st.write(f"**Missing:** {', '.join(recipe['missing'])}")
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        if st.button("I Made This ✅", key=f"made_{recipe['name']}"):
                            st.session_state.history.append({
                                "name": recipe["name"],
                                "date": datetime.now().strftime("%b %d")
                            })
                            st.success("Logged! Nice work.")
                    with col_b:
                        if st.button("⭐ Save to Favorites", key=f"fav_{recipe['name']}"):
                            if recipe["name"] not in [f["name"] for f in st.session_state.favorites]:
                                st.session_state.favorites.append(recipe)
                                st.success("Saved to favorites!")
else:
    st.info("Add ingredients and click the button above")

# Shopping List
if st.session_state.ingredients:
    st.divider()
    st.subheader("🛒 Quick Shopping List")
    st.caption("Common missing items for good recipes:")
    st.write("• Olive oil, garlic, onions, salt & pepper, lemon")

# Favorites & History
tab1, tab2 = st.tabs(["⭐ Favorites", "📖 Recent Meals"])
with tab1:
    if st.session_state.favorites:
        for fav in st.session_state.favorites:
            st.write(f"• {fav['name']}")
    else:
        st.write("No favorites yet.")

with tab2:
    if st.session_state.history:
        for meal in reversed(st.session_state.history[-8:]):
            st.caption(f"✅ {meal['name']} — {meal['date']}")
    else:
        st.write("No meals logged yet.")
