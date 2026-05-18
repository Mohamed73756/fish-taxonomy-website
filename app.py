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
# OCEAN THEME (LIGHT BLUE)
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
# CLEAN DATA (CRITICAL FIX)
# =====================================================

for col in ["Order", "Family", "Scientific_Name", "image"]:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip()

# =====================================================
# WORKING DATAFRAME COPY
# =====================================================

filtered_df = df.copy()

IMAGE_FOLDER = "images"

# =====================================================
# TITLE
# =====================================================

st.title("🐟 Marine Fish Taxonomy Database")
st.write("Browse fish species by taxonomy with images.")

# =====================================================
# ORDER FILTER
# =====================================================

order_list = ["All"] + sorted(filtered_df["Order"].dropna().unique().tolist())

selected_order = st.sidebar.selectbox("Order", order_list)

if selected_order != "All":
    filtered_df = filtered_df[
        filtered_df["Order"] == selected_order
    ]

# =====================================================
# FAMILY FILTER (DEPENDS ON ORDER)
# =====================================================

family_list = ["All"] + sorted(filtered_df["Family"].dropna().unique().tolist())

selected_family = st.sidebar.selectbox("Family", family_list)

if selected_family != "All":
    filtered_df = filtered_df[
        filtered_df["Family"] == selected_family
    ]

# =====================================================
# SEARCH
# =====================================================

search = st.sidebar.text_input("Search Scientific Name")

if search:
    filtered_df = filtered_df[
        filtered_df["Scientific_Name"].str.contains(
            search,
            case=False,
            na=False
        )
    ]

# =====================================================
# RESULTS COUNT
# =====================================================

st.success(f"{len(filtered_df)} species found")

st.divider()

# =====================================================
# DISPLAY RESULTS
# =====================================================

for _, row in filtered_df.iterrows():

    col1, col2 = st.columns([1, 2])

    # -------------------------
    # IMAGE
    # -------------------------
    with col1:

        img_file = str(row["image"]).strip()
        img_path = os.path.join(IMAGE_FOLDER, img_file)

        if os.path.exists(img_path):
            st.image(img_path, use_container_width=True)
        else:
            st.error(f"Missing image: {img_file}")

    # -------------------------
    # TEXT INFO
    # -------------------------
    with col2:

        st.subheader(row["Scientific_Name"])
        st.write(f"**Order:** {row['Order']}")
        st.write(f"**Family:** {row['Family']}")

    st.divider()
