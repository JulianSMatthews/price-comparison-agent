import streamlit as st
from compare_agent import compare_prices

st.title("💷 Price Comparison Agent")

query = st.text_input("Enter product name (e.g. 'wireless earbuds'):")
asin = st.text_input("Optional: Enter Amazon ASIN (10-digit code):")

if st.button("Compare Prices"):
    if not query:
        st.warning("Please enter a product name.")
    else:
        try:
            st.info("Searching, please wait...")
            results = compare_prices(query, asin)
            if results:
                for r in results:
                    st.subheader(f"{r['source']}: {r['title']}")
                    st.write(f"**Price**: {r['price']}")
                    st.markdown(f"[🔗 View Item]({r['link']})")
            else:
                st.warning("No results found.")
        except Exception as e:
            st.error(f"App error: {e}")
