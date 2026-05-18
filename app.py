import streamlit as st
import pandas as pd
import os

# ----------------------------
# PAGE CONFIG
# ----------------------------

st.set_page_config(
    page_title="Fish Taxonomy Database",
    page_icon="🐟",
    layout="wide"
)

IMAGE_FOLDER = "images"

# ----------------------------
# LOAD DATA
# ----------------------------

df = pd.read_excel("fish_data.xlsx")
df.columns = df.columns.str.strip()

# ----------------------------
# TITLE
# ----------------------------

st.title("🐟 Fish Taxonomy Database")

st.write("Interactive fish species database with taxonomy and images.")

# ----------------------------
# SIDEBAR FILTERS
# ----------------------------

st.sidebar.header("Filters")

# ORDER FILTER
orders = ["All"] + sorted(df["Order"].dropna().unique().tolist())
selected_order = st.sidebar.selectbox("Order", orders)

if selected_order != "All":
    df = df[df["Order"] == selected_order]

# FAMILY FILTER
families = ["All"] + sorted(df["Family"].dropna().unique().tolist())
selected_family = st.sidebar.selectbox("Family", families)

if selected_family != "All":
    df = df[df["Family"] == selected_family]

# SEARCH
search = st.sidebar.text_input("Search Scientific Name")

if search:
    df = df[df["Scientific_Name"].str.contains(search, case=False, na=False)]

# ----------------------------
# RESULTS
# ----------------------------

st.success(f"{len(df)} species found")

st.divider()

# ----------------------------
# DISPLAY RESULTS
# ----------------------------

for _, row in df.iterrows():

    col1, col2 = st.columns([1, 2])

    with col1:
        img_path = os.path.join(IMAGE_FOLDER, str(row["image"]).strip())

        if os.path.exists(img_path):
            st.image(img_path, use_container_width=True)
        else:
            st.error(f"Missing image: {row['image']}")

    with col2:
        st.subheader(row["Scientific_Name"])
        st.write(f"**Order:** {row['Order']}")
        st.write(f"**Family:** {row['Family']}")

    st.divider()
