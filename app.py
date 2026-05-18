import streamlit as st
import pandas as pd
import os

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Fish Taxonomy Database",
    page_icon="🐟",
    layout="wide"
)

# =====================================================
# OCEAN THEME
# =====================================================

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(to bottom, #dff6ff, #ffffff);
    }

    h1, h2, h3 {
        color: #0b3d91;
    }

    .stSidebar {
        background-color: #cfefff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_excel("fish_data.xlsx")
df.columns = df.columns.str.strip()

# =====================================================
# CLEAN DATA (SAFE FOR TAXONOMY)
# =====================================================

def clean_text(x):
    return str(x).replace("\xa0", " ").strip()

for col in ["Order", "Family", "Scientific_Name", "image"]:
    df[col] = df[col].apply(clean_text)

IMAGE_FOLDER = "images"

# =====================================================
# WORKING COPY
# =====================================================

filtered_df = df.copy()

# =====================================================
# TITLE
# =====================================================

st.title("🐟 Marine Fish Taxonomy Database")
st.write("Browse marine fish by Order, Family, and Species.")

# =====================================================
# ORDER FILTER
# =====================================================

orders = ["All"] + sorted(filtered_df["Order"].dropna().unique().tolist())
selected_order = st.sidebar.selectbox("Order", orders)

if selected_order != "All":
    filtered_df = filtered_df[filtered_df["Order"] == selected_order]

# =====================================================
# FAMILY FILTER
# =====================================================

families = ["All"] + sorted(filtered_df["Family"].dropna().unique().tolist())
selected_family = st.sidebar.selectbox("Family", families)

if selected_family != "All":
    filtered_df = filtered_df[filtered_df["Family"] == selected_family]

# =====================================================
# SEARCH
# =====================================================

search = st.sidebar.text_input("Search Scientific Name")

if search:
    filtered_df = filtered_df[
        filtered_df["Scientific_Name"].str.contains(search, case=False, na=False)
    ]

# =====================================================
# RESULTS
# =====================================================

st.success(f"{len(filtered_df)} species found")
st.divider()

# =====================================================
# IMAGE HANDLER
# =====================================================

def get_image_path(filename):
    if pd.isna(filename):
        return None

    filename = str(filename).strip()

    direct_path = os.path.join(IMAGE_FOLDER, filename)
    if os.path.exists(direct_path):
        return direct_path

    if os.path.exists(IMAGE_FOLDER):
        for f in os.listdir(IMAGE_FOLDER):
            if f.lower() == filename.lower():
                return os.path.join(IMAGE_FOLDER, f)

    return None

# =====================================================
# DISPLAY
# =====================================================

if len(filtered_df) == 0:
    st.warning("No fish found for this selection.")

for _, row in filtered_df.iterrows():

    col1, col2 = st.columns([1, 2])

    with col1:
        img_path = get_image_path(row["image"])

        if img_path:
            st.image(img_path, use_container_width=True)
        else:
            st.error(f"Missing image: {row['image']}")

    with col2:
        st.subheader(row["Scientific_Name"])
        st.write(f"**Order:** {row['Order']}")
        st.write(f"**Family:** {row['Family']}")

    st.divider()
