"""
Laptop Manufacturing Time & Cost Predictor
Comprehensive, Full-Featured Machine Learning Application
"""

import os
import json
import joblib
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ==============================================================================
# PAGE SETUP & PROFESSIONAL STYLING
# ==============================================================================
st.set_page_config(
    page_title="Laptop Manufacturing Time & Cost Predictor",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    /* Hide Deploy Button and Streamlit Menu */
    [data-testid="stDeployButton"],
    .stAppDeployButton,
    button[title="Deploy this app"],
    #MainMenu {
        display: none !important;
        visibility: hidden !important;
    }

    .main-title {
        font-size: 2.1rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .main-subtitle {
        font-size: 1rem;
        color: #475569;
        margin-bottom: 1.4rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        border-radius: 12px;
        padding: 18px 20px;
        border: 1px solid #E2E8F0;
        margin-bottom: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
    }
    .metric-value-time {
        font-size: 2rem;
        font-weight: 700;
        color: #0284C7;
    }
    .metric-value-cost {
        font-size: 2rem;
        font-weight: 700;
        color: #16A34A;
    }
    .metric-title {
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748B;
        font-weight: 600;
    }
    .metric-sub {
        font-size: 0.85rem;
        color: #475569;
        margin-top: 3px;
    }
    .badge-mfg {
        background-color: #DBEAFE;
        color: #1E40AF;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .badge-assembly {
        background-color: #DCFCE7;
        color: #166534;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .notice-box {
        background-color: #F8FAFC;
        border-left: 4px solid #3B82F6;
        padding: 12px 16px;
        border-radius: 6px;
        color: #334155;
        font-size: 0.9rem;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# PATH RESOLUTION & DATA LOADERS
# ==============================================================================
def resolve_file(*subpaths):
    candidates = [
        os.path.join(os.getcwd(), *subpaths),
        os.path.join(os.getcwd(), "laptop_prediction_project", *subpaths),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), *subpaths),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", *subpaths),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "laptop_prediction_project", *subpaths),
    ]
    for c in candidates:
        if os.path.exists(c):
            return os.path.abspath(c)
    return os.path.join(os.getcwd(), *subpaths)

@st.cache_resource
def load_models_and_artifacts():
    time_path = resolve_file("models", "time_model.pkl")
    cost_path = resolve_file("models", "cost_model.pkl")
    metadata_path = resolve_file("outputs", "metadata.json")
    metrics_path = resolve_file("outputs", "evaluation_metrics.json")
    importance_path = resolve_file("outputs", "feature_importances.json")
    test_preds_path = resolve_file("outputs", "test_predictions.csv")

    if not (os.path.exists(time_path) and os.path.exists(cost_path)):
        return None, None, {}, {}, {}, None

    time_model = joblib.load(time_path)
    cost_model = joblib.load(cost_path)

    metadata = {}
    if os.path.exists(metadata_path):
        with open(metadata_path, "r") as f:
            metadata = json.load(f)

    metrics = {}
    if os.path.exists(metrics_path):
        with open(metrics_path, "r") as f:
            metrics = json.load(f)

    importances = {}
    if os.path.exists(importance_path):
        with open(importance_path, "r") as f:
            importances = json.load(f)

    test_preds_df = None
    if os.path.exists(test_preds_path):
        test_preds_df = pd.read_csv(test_preds_path)

    return time_model, cost_model, metadata, metrics, importances, test_preds_df

@st.cache_data
def load_dataset():
    csv_path = resolve_file("data", "laptop_manufacturing_assembly_dataset_600_rows.csv")
    if not os.path.exists(csv_path):
        csv_path = resolve_file("laptop_manufacturing_assembly_dataset_600_rows.csv")
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    return None

time_model, cost_model, metadata, metrics, importances, test_preds_df = load_models_and_artifacts()
raw_df = load_dataset()

# ==============================================================================
# SIDEBAR
# ==============================================================================
with st.sidebar:
    st.markdown("### 💻 Laptop Production Engine")
    st.caption("Time & Cost Prediction System")
    st.markdown("---")

    menu = st.radio(
        "Navigation",
        [
            "⚡ Single Component Predictor",
            "📋 Multi-Component BOM Estimator",
            "📊 Production Analytics & EDA",
            "🎯 Model Benchmarks & Validation"
        ]
    )

    st.markdown("---")
    if time_model is not None and cost_model is not None:
        st.success("🟢 System Ready")
    else:
        st.error("🔴 Models not ready")

# Category & Profile defaults
cat_options = metadata.get("unique_values", {})
comp_profiles = metadata.get("component_profiles", {})

all_components = cat_options.get("Component_Type", sorted(raw_df["Component_Type"].unique()) if raw_df is not None else [])
all_processes = cat_options.get("Process_Type", ["Assembly", "Manufacturing"])
all_materials = cat_options.get("Material", sorted(raw_df["Material"].unique()) if raw_df is not None else [])
all_mfg_procs = cat_options.get("Manufacturing_Process", sorted(raw_df["Manufacturing_Process"].unique()) if raw_df is not None else [])
all_machines = cat_options.get("Machine_Type", sorted(raw_df["Machine_Type"].unique()) if raw_df is not None else [])
all_shifts = cat_options.get("Shift_Type", ["Day", "Night"])


# ==============================================================================
# TAB 1: SINGLE COMPONENT PREDICTOR (FULL INTERACTIVE CONTROL OF ALL VALUES)
# ==============================================================================
if menu == "⚡ Single Component Predictor":
    st.markdown('<div class="main-title">⚡ Component Manufacturing Time & Cost Predictor</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="main-subtitle">Select a component, customize any production parameters below, and calculate time and cost estimates.</div>',
        unsafe_allow_html=True
    )

    col_select, col_auto = st.columns([3, 1])
    with col_select:
        selected_component = st.selectbox(
            "Select Laptop Component or Operation:",
            all_components,
            index=0
        )
    with col_auto:
        st.write("")
        st.write("")
        auto_preset = st.checkbox("Auto-populate Typical Specs", value=True, help="Auto-fills typical factory dimensions, material, and process for the selected component.")

    # Defaults
    prof = comp_profiles.get(selected_component, {})
    def_proc = prof.get("Process_Type", "Manufacturing") if auto_preset else all_processes[0]
    def_mat = prof.get("Material", all_materials[0] if all_materials else "Plastic") if auto_preset else all_materials[0]
    def_mfg = prof.get("Manufacturing_Process", all_mfg_procs[0] if all_mfg_procs else "Injection_Molding") if auto_preset else all_mfg_procs[0]
    def_mach = prof.get("Machine_Type", all_machines[0] if all_machines else "Assembly_Workstation") if auto_preset else all_machines[0]
    def_len = prof.get("Length_mm", 100) if auto_preset else 100
    def_wid = prof.get("Width_mm", 50) if auto_preset else 50
    def_hgt = prof.get("Height_mm", 5) if auto_preset else 5
    def_comp = prof.get("Complexity_Level", 1.2) if auto_preset else 1.2

    badge_style = "badge-assembly" if def_proc == "Assembly" else "badge-mfg"
    st.markdown(
        f"Operation Category: <span class='{badge_style}'>{def_proc}</span> "
        f"| Typical Material: <b>{def_mat}</b> | Typical Machine: <b>{def_mach}</b>",
        unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)

    with st.form("single_prediction_form"):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("##### ⚙️ Process & Material Parameters")
            process_type = st.selectbox(
                "Process Type",
                all_processes,
                index=all_processes.index(def_proc) if def_proc in all_processes else 0
            )
            material = st.selectbox(
                "Raw Material / Part",
                all_materials,
                index=all_materials.index(def_mat) if def_mat in all_materials else 0
            )
            mfg_process = st.selectbox(
                "Manufacturing Method / Assembly Operation",
                all_mfg_procs,
                index=all_mfg_procs.index(def_mfg) if def_mfg in all_mfg_procs else 0
            )
            machine_type = st.selectbox(
                "Machine / Workstation Type",
                all_machines,
                index=all_machines.index(def_mach) if def_mach in all_machines else 0
            )
            shift_type = st.selectbox("Operating Shift", all_shifts, index=0)

        with col2:
            st.markdown("##### 📐 Physical Dimensions & Batch Scale")
            c1, c2, c3 = st.columns(3)
            with c1:
                length_mm = st.number_input("Length (mm)", min_value=1, max_value=1000, value=int(def_len))
            with c2:
                width_mm = st.number_input("Width (mm)", min_value=1, max_value=1000, value=int(def_wid))
            with c3:
                height_mm = st.number_input("Height (mm)", min_value=1, max_value=500, value=int(def_hgt))

            quantity = st.number_input(
                "Production Batch Volume (Units)",
                min_value=1,
                max_value=10000,
                value=50,
                step=5,
                help="The models predict total process time and cost for this specific batch size."
            )

            complexity = st.select_slider(
                "Geometry / Operation Complexity Level",
                options=[1.0, 1.1, 1.2, 1.3, 1.4],
                value=float(def_comp) if float(def_comp) in [1.0, 1.1, 1.2, 1.3, 1.4] else 1.2,
                help="1.0 = Standard geometry, 1.4 = Intricate / tight-tolerance features"
            )

        st.markdown("<br>", unsafe_allow_html=True)
        submit_btn = st.form_submit_button("⚡ Predict Time and Cost", use_container_width=True)

    if submit_btn:
        input_row = pd.DataFrame([{
            "Component_Type": selected_component,
            "Process_Type": process_type,
            "Material": material,
            "Length_mm": length_mm,
            "Width_mm": width_mm,
            "Height_mm": height_mm,
            "Production_Quantity": quantity,
            "Manufacturing_Process": mfg_process,
            "Complexity_Level": complexity,
            "Machine_Type": machine_type,
            "Shift_Type": shift_type
        }])

        pred_time = float(time_model.predict(input_row)[0])
        pred_cost = float(cost_model.predict(input_row)[0])

        pred_time = max(0.1, pred_time)
        pred_cost = max(1.0, pred_cost)

        unit_time = pred_time / quantity
        unit_cost = pred_cost / quantity

        st.markdown("---")
        st.markdown("### 🎯 Prediction Results")

        r1, r2, r3, r4 = st.columns(4)
        with r1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Total Batch Time</div>
                <div class="metric-value-time">{pred_time:.1f} <span style="font-size:1rem;color:#475569;">min</span></div>
                <div class="metric-sub">≈ <b>{pred_time / 60.0:.2f} Hours</b></div>
            </div>
            """, unsafe_allow_html=True)

        with r2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Total Batch Cost</div>
                <div class="metric-value-cost">₹{pred_cost:,.2f}</div>
                <div class="metric-sub">Total cost for {quantity} units</div>
            </div>
            """, unsafe_allow_html=True)

        with r3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Unit Cycle Time</div>
                <div class="metric-value-time">{unit_time:.2f} <span style="font-size:1rem;color:#475569;">min</span></div>
                <div class="metric-sub">Average time per piece</div>
            </div>
            """, unsafe_allow_html=True)

        with r4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Unit Production Cost</div>
                <div class="metric-value-cost">₹{unit_cost:,.2f}</div>
                <div class="metric-sub">Average cost per piece</div>
            </div>
            """, unsafe_allow_html=True)

        with st.expander("🔍 View All 11 Input Features Sent to Models"):
            st.dataframe(input_row, use_container_width=True)

        st.markdown(f"""
        <div class="notice-box">
            ℹ️ <b>Batch Scaling Note:</b> The machine learning models directly predict <b>total batch execution metrics</b> for the requested volume of <b>{quantity} units</b>. Unit metrics are calculated directly by dividing the batch estimate by quantity.
        </div>
        """, unsafe_allow_html=True)


# ==============================================================================
# TAB 2: MULTI-COMPONENT BOM ESTIMATOR
# ==============================================================================
elif menu == "📋 Multi-Component BOM Estimator":
    st.markdown('<div class="main-title">📋 Multi-Component Bill of Materials (BOM) Estimator</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="main-subtitle">Configure complete laptop assembly batches and estimate cumulative line production time and total cost.</div>',
        unsafe_allow_html=True
    )

    col_select_multi, col_bulk = st.columns([3, 1])
    with col_select_multi:
        selected_multi = st.multiselect(
            "Select Laptop Components & Sub-Systems:",
            all_components,
            default=[
                "Laptop_Casing", "Laptop_Bottom_Cover", "Laptop_Hinge",
                "Motherboard_Installation", "RAM_Installation", "SSD_Installation",
                "Display_Installation", "Battery_Installation", "Keyboard_Installation",
                "Thermal_Paste_Application", "Final_Quality_Check"
            ]
        )
    with col_bulk:
        st.write("")
        st.write("")
        bulk_q = st.number_input("Bulk Volume for All", min_value=1, max_value=2000, value=25)
        apply_bulk_btn = st.button("Set All Volumes")

    if not selected_multi:
        st.info("Select one or more components to generate a production line estimate.")
    else:
        st.markdown("#### Configure Production Volumes")
        bom_data = []

        cols_grid = st.columns(3)
        for idx, comp in enumerate(selected_multi):
            col_target = cols_grid[idx % 3]
            prof = comp_profiles.get(comp, {})
            init_val = int(bulk_q) if apply_bulk_btn else 25

            with col_target:
                q = st.number_input(
                    f"{comp.replace('_', ' ')}",
                    min_value=1,
                    max_value=10000,
                    value=init_val,
                    key=f"bom_input_{comp}"
                )
                bom_data.append({
                    "Component_Type": comp,
                    "Process_Type": prof.get("Process_Type", "Manufacturing"),
                    "Material": prof.get("Material", "Plastic"),
                    "Length_mm": prof.get("Length_mm", 100),
                    "Width_mm": prof.get("Width_mm", 50),
                    "Height_mm": prof.get("Height_mm", 5),
                    "Production_Quantity": q,
                    "Manufacturing_Process": prof.get("Manufacturing_Process", "Injection_Molding"),
                    "Complexity_Level": prof.get("Complexity_Level", 1.2),
                    "Machine_Type": prof.get("Machine_Type", "Assembly_Workstation"),
                    "Shift_Type": "Day"
                })

        if st.button("🚀 Calculate Full Production Line Estimate", type="primary", use_container_width=True):
            bom_df = pd.DataFrame(bom_data)
            times = time_model.predict(bom_df)
            costs = cost_model.predict(bom_df)

            results_df = bom_df[["Component_Type", "Process_Type", "Production_Quantity"]].copy()
            results_df["Est_Time_Mins"] = np.round(np.maximum(0.1, times), 1)
            results_df["Est_Cost_INR"] = np.round(np.maximum(1.0, costs), 2)
            results_df["Unit_Time_Mins"] = np.round(results_df["Est_Time_Mins"] / results_df["Production_Quantity"], 2)
            results_df["Unit_Cost_INR"] = np.round(results_df["Est_Cost_INR"] / results_df["Production_Quantity"], 2)

            total_time_mins = results_df["Est_Time_Mins"].sum()
            total_time_hrs = total_time_mins / 60.0
            total_cost_inr = results_df["Est_Cost_INR"].sum()
            total_items = results_df["Production_Quantity"].sum()

            st.markdown("---")
            st.markdown("### 📊 Production Summary")

            k1, k2, k3, k4 = st.columns(4)
            k1.metric("Production Operations", len(results_df))
            k2.metric("Total Component Units", f"{total_items:,}")
            k3.metric("Cumulative Line Time", f"{total_time_mins:,.1f} min", f"{total_time_hrs:.2f} hrs")
            k4.metric("Cumulative Project Cost", f"₹{total_cost_inr:,.2f}")

            st.markdown("#### Component-Wise Schedule & Cost Breakdown")
            st.dataframe(
                results_df.rename(columns={
                    "Component_Type": "Component / Operation",
                    "Process_Type": "Category",
                    "Production_Quantity": "Volume (Units)",
                    "Est_Time_Mins": "Batch Time (min)",
                    "Est_Cost_INR": "Batch Cost (₹)",
                    "Unit_Time_Mins": "Unit Time (min/pc)",
                    "Unit_Cost_INR": "Unit Cost (₹/pc)"
                }),
                use_container_width=True
            )

            c_chart1, c_chart2 = st.columns(2)
            with c_chart1:
                fig_cost = px.bar(
                    results_df,
                    x="Component_Type",
                    y="Est_Cost_INR",
                    color="Process_Type",
                    title="Cost Distribution by Component (₹)",
                    color_discrete_map={"Manufacturing": "#2563EB", "Assembly": "#10B981"}
                )
                fig_cost.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig_cost, use_container_width=True)

            with c_chart2:
                fig_time = px.pie(
                    results_df,
                    names="Component_Type",
                    values="Est_Time_Mins",
                    title="Process Time Share by Operation (Minutes)",
                    hole=0.45
                )
                st.plotly_chart(fig_time, use_container_width=True)


# ==============================================================================
# TAB 3: PRODUCTION ANALYTICS & EDA
# ==============================================================================
elif menu == "📊 Production Analytics & EDA":
    st.markdown('<div class="main-title">📊 Production Analytics & Dataset Insights</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="main-subtitle">Statistical exploration of 600 production batches across manufacturing and assembly operations.</div>',
        unsafe_allow_html=True
    )

    if raw_df is not None:
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Total Records", f"{len(raw_df)}")
        m2.metric("Input Features", "11 Parameters")
        m3.metric("Target Variables", "2 (Time & Cost)")
        m4.metric("Manufacturing Batches", f"{(raw_df['Process_Type'] == 'Manufacturing').sum()}")
        m5.metric("Assembly Batches", f"{(raw_df['Process_Type'] == 'Assembly').sum()}")

        st.markdown("---")
        t1, t2, t3 = st.tabs(["📊 Operational Distributions", "📈 Cost & Time Correlations", "🔍 Dataset Records"])

        with t1:
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                proc_counts = raw_df["Process_Type"].value_counts().reset_index()
                proc_counts.columns = ["Process_Type", "Count"]
                fig_p = px.pie(
                    proc_counts,
                    names="Process_Type",
                    values="Count",
                    title="Process Distribution (Manufacturing vs Assembly)",
                    color="Process_Type",
                    color_discrete_map={"Manufacturing": "#2563EB", "Assembly": "#059669"},
                    hole=0.45
                )
                st.plotly_chart(fig_p, use_container_width=True)

            with col_d2:
                comp_counts = raw_df["Component_Type"].value_counts().reset_index()
                comp_counts.columns = ["Component_Type", "Count"]
                fig_c = px.bar(
                    comp_counts,
                    x="Count",
                    y="Component_Type",
                    orientation="h",
                    title="Batch Records per Component",
                    color="Count",
                    color_continuous_scale="Blues"
                )
                fig_c.update_layout(yaxis=dict(autorange="reversed"))
                st.plotly_chart(fig_c, use_container_width=True)

            col_d3, col_d4 = st.columns(2)
            with col_d3:
                mat_counts = raw_df["Material"].value_counts().reset_index()
                mat_counts.columns = ["Material", "Count"]
                fig_m = px.bar(mat_counts, x="Material", y="Count", color="Count", title="Material Allocation")
                fig_m.update_layout(xaxis_tickangle=-35)
                st.plotly_chart(fig_m, use_container_width=True)

            with col_d4:
                mach_counts = raw_df["Machine_Type"].value_counts().reset_index()
                mach_counts.columns = ["Machine_Type", "Count"]
                fig_mach = px.bar(mach_counts, x="Machine_Type", y="Count", color="Count", title="Workstation & Machine Utilization", color_continuous_scale="Teal")
                fig_mach.update_layout(xaxis_tickangle=-35)
                st.plotly_chart(fig_mach, use_container_width=True)

        with t2:
            s1, s2 = st.columns(2)
            with s1:
                fig_s1 = px.scatter(
                    raw_df,
                    x="Production_Quantity",
                    y="Actual_Time_Minutes",
                    color="Process_Type",
                    hover_data=["Component_Type", "Machine_Type"],
                    title="Volume vs Actual Process Time (Minutes)",
                    color_discrete_map={"Manufacturing": "#2563EB", "Assembly": "#059669"}
                )
                st.plotly_chart(fig_s1, use_container_width=True)

            with s2:
                fig_s2 = px.scatter(
                    raw_df,
                    x="Production_Quantity",
                    y="Actual_Cost_INR",
                    color="Process_Type",
                    hover_data=["Component_Type", "Material"],
                    title="Volume vs Actual Production Cost (INR)",
                    color_discrete_map={"Manufacturing": "#2563EB", "Assembly": "#059669"}
                )
                st.plotly_chart(fig_s2, use_container_width=True)

        with t3:
            f1, f2 = st.columns(2)
            with f1:
                f_proc = st.multiselect("Filter Process Type", all_processes, default=all_processes)
            with f2:
                f_comp = st.multiselect("Filter Component", all_components, default=all_components[:4])

            filtered = raw_df[
                raw_df["Process_Type"].isin(f_proc) &
                (raw_df["Component_Type"].isin(f_comp) if f_comp else True)
            ]
            st.dataframe(filtered, use_container_width=True)


# ==============================================================================
# TAB 4: MODEL BENCHMARKS & VALIDATION
# ==============================================================================
elif menu == "🎯 Model Benchmarks & Validation":
    st.markdown('<div class="main-title">🎯 Machine Learning Model Benchmarks & Validation</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="main-subtitle">Validation of dual Random Forest regression pipelines on held-out test data (70% train / 30% test split).</div>',
        unsafe_allow_html=True
    )

    if metrics:
        s_info = metrics.get("split_info", {})
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Batches", s_info.get("total_samples", 600))
        c2.metric("Training Set (70%)", f"{s_info.get('train_samples', 420)} Batches")
        c3.metric("Held-Out Test Set (30%)", f"{s_info.get('test_samples', 180)} Batches")
        c4.metric("Random State", s_info.get("random_state", 42))

        st.markdown("---")
        st.markdown("### 🏆 Held-Out Test Set Performance Benchmarks")

        time_m = metrics.get("time_model", {})
        cost_m = metrics.get("cost_model", {})

        benchmarks = [
            {
                "Target Variable": "Process Time (Minutes)",
                "Model Pipeline": "Random Forest Regressor",
                "MAE": f"{time_m.get('random_forest', {}).get('mae', 0):.2f} min",
                "RMSE": f"{time_m.get('random_forest', {}).get('rmse', 0):.2f} min",
                "R² Score": f"{time_m.get('random_forest', {}).get('r2_score', 0):.4f}"
            },
            {
                "Target Variable": "Process Time (Minutes)",
                "Model Pipeline": "Linear Regression Baseline",
                "MAE": f"{time_m.get('linear_baseline', {}).get('mae', 0):.2f} min",
                "RMSE": f"{time_m.get('linear_baseline', {}).get('rmse', 0):.2f} min",
                "R² Score": f"{time_m.get('linear_baseline', {}).get('r2_score', 0):.4f}"
            },
            {
                "Target Variable": "Production Cost (INR)",
                "Model Pipeline": "Random Forest Regressor",
                "MAE": f"₹{cost_m.get('random_forest', {}).get('mae', 0):.2f}",
                "RMSE": f"₹{cost_m.get('random_forest', {}).get('rmse', 0):.2f}",
                "R² Score": f"{cost_m.get('random_forest', {}).get('r2_score', 0):.4f}"
            },
            {
                "Target Variable": "Production Cost (INR)",
                "Model Pipeline": "Linear Regression Baseline",
                "MAE": f"₹{cost_m.get('linear_baseline', {}).get('mae', 0):.2f}",
                "RMSE": f"₹{cost_m.get('linear_baseline', {}).get('rmse', 0):.2f}",
                "R² Score": f"{cost_m.get('linear_baseline', {}).get('r2_score', 0):.4f}"
            }
        ]
        st.table(pd.DataFrame(benchmarks))

        if test_preds_df is not None:
            st.markdown("---")
            st.markdown("### 🎯 Actual vs. Predicted Plots (180 Test Batches)")
            ap1, ap2 = st.columns(2)

            with ap1:
                fig_at = px.scatter(
                    test_preds_df,
                    x="Actual_Time_Minutes",
                    y="Predicted_Time_Minutes",
                    color="Process_Type",
                    hover_data=["Component_Type", "Production_Quantity"],
                    title="Actual vs Predicted Time (Minutes)",
                    color_discrete_map={"Manufacturing": "#2563EB", "Assembly": "#059669"}
                )
                max_t = max(test_preds_df["Actual_Time_Minutes"].max(), test_preds_df["Predicted_Time_Minutes"].max())
                fig_at.add_trace(go.Scatter(x=[0, max_t], y=[0, max_t], mode="lines", name="Ideal 45° Fit", line=dict(dash="dash", color="red")))
                st.plotly_chart(fig_at, use_container_width=True)

            with ap2:
                fig_ac = px.scatter(
                    test_preds_df,
                    x="Actual_Cost_INR",
                    y="Predicted_Cost_INR",
                    color="Process_Type",
                    hover_data=["Component_Type", "Production_Quantity"],
                    title="Actual vs Predicted Cost (INR)",
                    color_discrete_map={"Manufacturing": "#2563EB", "Assembly": "#059669"}
                )
                max_c = max(test_preds_df["Actual_Cost_INR"].max(), test_preds_df["Predicted_Cost_INR"].max())
                fig_ac.add_trace(go.Scatter(x=[0, max_c], y=[0, max_c], mode="lines", name="Ideal 45° Fit", line=dict(dash="dash", color="red")))
                st.plotly_chart(fig_ac, use_container_width=True)

        if importances:
            st.markdown("---")
            st.markdown("### 🔍 Feature Importance Ranking")
            fi1, fi2 = st.columns(2)

            t_imp = pd.DataFrame(importances.get("time_feature_importances", [])[:10])
            c_imp = pd.DataFrame(importances.get("cost_feature_importances", [])[:10])

            with fi1:
                if not t_imp.empty:
                    fig_ti = px.bar(t_imp, x="importance", y="feature", orientation="h", title="Top 10 Drivers for Time", color="importance", color_continuous_scale="Blues")
                    fig_ti.update_layout(yaxis=dict(autorange="reversed"))
                    st.plotly_chart(fig_ti, use_container_width=True)

            with fi2:
                if not c_imp.empty:
                    fig_ci = px.bar(c_imp, x="importance", y="feature", orientation="h", title="Top 10 Drivers for Cost", color="importance", color_continuous_scale="Greens")
                    fig_ci.update_layout(yaxis=dict(autorange="reversed"))
                    st.plotly_chart(fig_ci, use_container_width=True)
