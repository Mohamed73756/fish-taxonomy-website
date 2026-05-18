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
# CLEAN DATA (IMPORTANT)
# =====================================================

def clean_text(x):
    return str(x).replace("\xa0", " ").strip().lower()

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
st.write("Browse fish species with images and taxonomy filters.")

# =====================================================
# ORDER FILTER
# =====================================================

orders = ["all"] + sorted(filtered_df["Order"].unique().tolist())
selected_order = st.sidebar.selectbox("Order", orders)

if selected_order != "all":
    filtered_df = filtered_df[filtered_df["Order"] == selected_order]

# =====================================================
# FAMILY FILTER
# =====================================================

families = ["all"] + sorted(filtered_df["Family"].unique().tolist())
selected_family = st.sidebar.selectbox("Family", families)

if selected_family != "all":
    filtered_df = filtered_df[filtered_df["Family"] == selected_family]

# =====================================================
# SEARCH
# =====================================================

search = st.sidebar.text_input("Search Scientific Name")

if search:
    filtered_df = filtered_df[
        filtered_df["Scientific_Name"].str.contains(search.lower(), na=False)
    ]

# =====================================================
# RESULTS
# =====================================================

st.success(f"{len(filtered_df)} species found")
st.divider()

# =====================================================
# IMAGE SAFE LOADER (FIXED PART)
# =====================================================

def find_image(filename):
    """
    Robust image finder:
    - handles case mismatch
    - handles missing spaces
    - handles nested mistakes
    """

    if pd.isna(filename):
        return None

    filename = str(filename).strip().lower()

    # Try direct match in images folder
    direct_path = os.path.join(IMAGE_FOLDER, filename)
    if os.path.exists(direct_path):
        return direct_path

    # Try case-insensitive search
    if os.path.exists(IMAGE_FOLDER):
        for f in os.listdir(IMAGE_FOLDER):
            if f.lower() == filename:
                return os.path.join(IMAGE_FOLDER, f)

    return None

# =====================================================
# DISPLAY RESULTS
# =====================================================

if len(filtered_df) == 0:
    st.warning("No fish found for this selection.")

for _, row in filtered_df.iterrows():

    col1, col2 = st.columns([1, 2])

    with col1:

        img_path = find_image(row["image"])

        if img_path:
            st.image(img_path, use_container_width=True)
        else:
            st.error(f"Missing image: {row['image']}")

    with col2:

        st.subheader(row["Scientific_Name"])
        st.write(f"**Order:** {row['Order']}")
        st.write(f"**Family:** {row['Family']}")

    st.divider()
