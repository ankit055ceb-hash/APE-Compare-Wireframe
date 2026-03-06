import streamlit as st

st.set_page_config(page_title="Product Plan Comparison", layout="wide")

# -------------------------
# Mock plan data (hardcoded)
# -------------------------
source_plan = {
    "PlanCode": "ABC123",
    "PolicyProduct": {
        "CarrierCode": "ABC",
        "CarrierName": "ABC Life",
        "PlanName": "Secure Plan",
    },
    "AnnuityProduct": {
        "ProductType": "Fixed",
        "IssueAge": "18-75",
    },
    "FeatureProduct": {
        "FeatureCode": "CDSC",
        "Name": "Surrender Charge Rider",
        "Description": "Declining charge over 7 years",
    },
}

target_plan = {
    "PlanCode": "XYZ456",
    "PolicyProduct": {
        "CarrierCode": "XYZ",
        "CarrierName": "XYZ Insurance",
        "PlanName": "Growth Plan",
    },
    "AnnuityProduct": {
        "ProductType": "Indexed",
        "IssueAge": "21-80",
    },
    "FeatureProduct": {
        # FeatureCode intentionally missing to demonstrate N/A handling
        "Name": "Liquidity Benefit",
        "Description": "Partial withdrawals allowed after year 1",
    },
}

# -------------------------
# UI title and plan info
# -------------------------
st.title("Product Plan Comparison")

info_col1, info_col2 = st.columns(2)
with info_col1:
    st.markdown(f"**Source Plan Code:** {source_plan['PlanCode']}")
with info_col2:
    st.markdown(f"**Target Plan Code:** {target_plan['PlanCode']}")

st.markdown("---")

# Minimal wireframe styling
st.markdown(
    """
    <style>
      .cmp-row {
        border: 1px solid #d9d9d9;
        border-radius: 4px;
        padding: 6px 8px;
        margin-bottom: 6px;
      }
      .cmp-diff {
        background-color: #fff4e5;
      }
      .cmp-header {
        font-weight: 700;
        border: 1px solid #bfbfbf;
        border-radius: 4px;
        padding: 8px;
        margin-bottom: 8px;
        background: #f7f7f7;
      }
      .obj {
        font-weight: 700;
      }
      .prop {
        padding-left: 20px;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# 3-column layout header
h1, h2, h3 = st.columns([1.2, 1.6, 1.2])
with h1:
    st.markdown('<div class="cmp-header">Source Value</div>', unsafe_allow_html=True)
with h2:
    st.markdown('<div class="cmp-header">Object / Property</div>', unsafe_allow_html=True)
with h3:
    st.markdown('<div class="cmp-header">Target Value</div>', unsafe_allow_html=True)

# Object order for display
preferred_order = ["PolicyProduct", "AnnuityProduct", "FeatureProduct"]
all_objects = set(k for k in source_plan.keys() if k != "PlanCode") | set(
    k for k in target_plan.keys() if k != "PlanCode"
)

# Optional: make object buttons look like row items
st.markdown(
    """
    <style>
      div[data-testid="stButton"] > button {
        width: 100%;
        text-align: left;
        border: 1px solid #d9d9d9;
        border-radius: 4px;
        background: white;
        padding: 8px 10px;
        font-weight: 600;
      }
      div[data-testid="stButton"] > button:hover {
        border-color: #bfbfbf;
        background: #fafafa;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

ordered_objects = [o for o in preferred_order if o in all_objects] + sorted(
    all_objects - set(preferred_order)
)

# Session state for one-open-at-a-time tree
if "open_object" not in st.session_state:
    st.session_state.open_object = None  # start collapsed

# Collapse all action
if st.button("Collapse all"):
    st.session_state.open_object = None

def safe_value(v):
    return "N/A" if v is None else str(v)

# Render comparison rows
for obj_name in ordered_objects:
    src_obj = source_plan.get(obj_name, {})
    tgt_obj = target_plan.get(obj_name, {})

    is_open = st.session_state.open_object == obj_name
    obj_label = f"▼ {obj_name}" if is_open else f"▶ {obj_name}"

    # Object row with clickable button in middle column
    c1, c2, c3 = st.columns([1.2, 1.6, 1.2])
    with c1:
        st.markdown('<div class="cmp-row"> </div>', unsafe_allow_html=True)

    with c2:
        if st.button(obj_label, key=f"obj_btn_{obj_name}", use_container_width=True):
            if st.session_state.open_object == obj_name:
                st.session_state.open_object = None
            else:
                st.session_state.open_object = obj_name

    with c3:
        st.markdown('<div class="cmp-row"> </div>', unsafe_allow_html=True)

    # Re-check open state after click update
    is_open = st.session_state.open_object == obj_name
    if not is_open:
        continue

    # Property rows (visible only for open object)
    prop_names = sorted(set(src_obj.keys()) | set(tgt_obj.keys()))
    for prop in prop_names:
        src_val = safe_value(src_obj.get(prop))
        tgt_val = safe_value(tgt_obj.get(prop))

        is_diff = src_val != tgt_val
        row_class = "cmp-row cmp-diff" if is_diff else "cmp-row"

        left_text = f"⚠ {src_val}" if is_diff else src_val
        mid_text = f"└─ {prop}"
        right_text = f"⚠ {tgt_val}" if is_diff else tgt_val

        c1, c2, c3 = st.columns([1.2, 1.6, 1.2])
        with c1:
            st.markdown(f'<div class="{row_class}">{left_text}</div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="{row_class} prop">{mid_text}</div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="{row_class}">{right_text}</div>', unsafe_allow_html=True)