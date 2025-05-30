import streamlit as st
from compare_agent import compare_prices

# ✅ Debug panel to check loaded secrets (safely)
with st.expander("🔐 API Key Debug Info", expanded=False):
    st.markdown("**Loaded Secrets:**")
    keys_loaded = list(st.secrets.keys())
    if keys_loaded:
        st.success(f"Secrets loaded: {', '.join(keys_loaded)}")
    else:
        st.error("⚠️ No secrets loaded.")
st.title("🔍 Online Price Comparison")

query = st.text_input("Enter product name")
asin = st.text_input("Amazon ASIN (optional)")

if st.button("Compare"):
    results = compare_prices(query, asin)
    if results:
        for r in results:
            st.markdown(f"**{r['source']}**: [{r['title']}]({r['link']}) — {r['price']}")
    else:
        st.warning("No results found.")
