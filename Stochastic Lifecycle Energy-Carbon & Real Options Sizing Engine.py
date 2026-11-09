import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="AIMeCHA Stochastic Energy-Carbon Engine",
    page_icon="⚙️",
    layout="wide",
)

st.title(
    "🌊 Stochastic Lifecycle Energy-Carbon & Real Options Sizing Engine"
)
st.markdown(
    "*Interactive Decision-Support Tool based on Stochastic Infrastructure Lifecycle Optimization Framework.*"
)

# ==========================================
# SIDEBAR: USER INPUT PARAMETERS
# ==========================================
st.sidebar.header("🎛️ Simulation Parameters")

st.sidebar.subheader("Hydraulic & Organic Loading")
q_initial = st.sidebar.number_input(
    "Initial Flow Q_avg (m³/day)",
    min_value=5000.0,
    max_value=100000.0,
    value=25000.0,
    step=1000.0,
)
mu_q = st.sidebar.slider(
    "Flow Annual Growth Drift (μ_Q)", 0.0, 0.1, 0.03, 0.005
)
sigma_q = st.sidebar.slider(
    "Hydraulic Volatility (σ_Q)", 0.05, 0.30, 0.12, 0.01
)

c_baseline = st.sidebar.number_input(
    "Baseline BOD Concentration (mg/L)",
    min_value=100.0,
    max_value=500.0,
    value=280.0,
    step=10.0,
)
theta = st.sidebar.slider("Mean-Reversion Speed (θ)", 0.01, 0.50, 0.15, 0.01)
sigma_c = st.sidebar.slider("BOD Volatility (σ_C)", 10.0, 100.0, 35.0, 5.0)
rho_qc = st.sidebar.slider(
    "Infiltration Correlation (ρ_QC)", -0.9, 0.0, -0.45, 0.05
)

st.sidebar.subheader("Simulation Horizon")
simulation_days = st.sidebar.slider(
    "Simulation Duration (Days)", 90, 365, 365, 30
)

# ==========================================
# CORE COMPUTATIONAL ENGINE
# ==========================================


@st.cache_data
def run_stochastic_simulation(
    days, q_init, mu_q, sigma_q, c_base, theta, sigma_c, rho_qc
):
  np.random.seed(42)
  dt_year = 1.0 / 365.0
  dt_day = 1.0

  # Cholesky decomposition for correlated noise
  cov_matrix = [[1.0, rho_qc], [rho_qc, 1.0]]
  l_chol = np.linalg.cholesky(cov_matrix)

  Q = np.zeros(days)
  C_BOD = np.zeros(days)
  Q[0] = q_init
  C_BOD[0] = c_base

  for t in range(1, days):
    z = np.random.normal(0, 1, 2)
    z_corr = l_chol @ z
    dW_Q = z_corr[0] * np.sqrt(dt_year)
    dW_C = z_corr[1] * np.sqrt(dt_day)

    # Geometric Brownian Motion for Flow
    Q[t] = Q[t - 1] + mu_q * Q[t - 1] * dt_year + sigma_q * Q[t - 1] * dW_Q
    Q[t] = max(Q[t], 1000.0)

    # Ornstein-Uhlenbeck for BOD Concentration
    C_BOD[t] = (
        C_BOD[t - 1]
        + theta * (c_base - C_BOD[t - 1]) * dt_day
        + sigma_c * dW_C
    )
    C_BOD[t] = max(C_BOD[t], 30.0)

  # Electromechanical & Aeration Calculations
  m_bod = (Q * C_BOD) / 1000.0
  aor_sote_ratio = 1.8
  o2_fraction = 0.232
  rho_air = 1.204
  e_blower = 0.65
  r_gas = 0.287
  t1 = 293.15
  p1 = 101.3
  p2 = 150.0
  k_ratio = 1.4

  mass_air_per_day = (m_bod * aor_sote_ratio) / o2_fraction
  q_air = mass_air_per_day / (rho_air * 24.0)
  win = mass_air_per_day / 86400.0
  pressure_term = ((p2 / p1) ** ((k_ratio - 1.0) / k_ratio)) - 1.0
  p_aero = q_air * win * r_gas * t1 / (2.83e4 * e_blower) * pressure_term

  df = pd.DataFrame({
      'Day': np.arange(1, days + 1),
      'Hydraulic_Flow_m3_day': np.round(Q, 2),
      'BOD_Concentration_mg_L': np.round(C_BOD, 2),
      'BOD_Mass_Load_kg_day': np.round(m_bod, 2),
      'Blower_Airflow_Nm3_hr': np.round(q_air, 2),
      'Aeration_Power_kW': np.round(p_aero, 2),
  })
  return df


# Execute simulation with user parameters
df_sim = run_stochastic_simulation(
    simulation_days,
    q_initial,
    mu_q,
    sigma_q,
    c_baseline,
    theta,
    sigma_c,
    rho_qc,
)

# ==========================================
# DASHBOARD METRICS & KPIs
# ==========================================
col1, col2, col3, col4 = st.columns(4)
col1.metric(
    "Mean Daily Flow",
    f"{df_sim['Hydraulic_Flow_m3_day'].mean():,.0f} m³/day",
)
col2.metric(
    "Mean BOD Concentration",
    f"{df_sim['BOD_Concentration_mg_L'].mean():.1f} mg/L",
)
col3.metric(
    "Avg Aeration Power Demand", f"{df_sim['Aeration_Power_kW'].mean():,.1f} kW"
)
col4.metric(
    "Total Energy Intensity",
    f"{(df_sim['Aeration_Power_kW'].sum() * 24) / 1000:,.1f} MWh/yr",
)

st.markdown('---')

# ==========================================
# INTERACTIVE VISUALIZATIONS (PLOTLY)
# ==========================================
st.subheader(
    '📈 Dynamic Hydraulic Flow & Organic Loading (Infiltration Inflow Effects)'
)
fig_flow = px.line(
    df_sim,
    x='Day',
    y=['Hydraulic_Flow_m3_day'],
    labels={'value': 'Flow (m³/day)', 'variable': 'Parameter'},
    title='Stochastic Influent Flow Progression',
)
st.plotly_chart(fig_flow, use_container_width=True)

col_a, col_b = st.columns(2)

with col_a:
  st.subheader('🧪 BOD Concentration Profile')
  fig_bod = px.line(
      df_sim,
      x='Day',
      y='BOD_Concentration_mg_L',
      title='Ornstein-Uhlenbeck BOD Mean-Reversion',
  )
  st.plotly_chart(fig_bod, use_container_width=True)

with col_b:
  st.subheader('⚡ Blower Aeration Power Demand')
  fig_power = px.line(
      df_sim,
      x='Day',
      y='Aeration_Power_kW',
      title='Instantaneous Blower Power ($P_{aero}$)',
  )
  st.plotly_chart(fig_power, use_container_width=True)

# ==========================================
# REPORT EXPORT FEATURE
# ==========================================
st.markdown('---')
st.subheader('📥 Export Simulation Report')
st.markdown(
    'Download the complete time-series simulation dataset for compliance'
    ' reporting, auditing, or further real options analysis.'
)


@st.cache_data
def convert_df_to_csv(df):
  return df.to_csv(index=False).encode('utf-8')


csv_data = convert_df_to_csv(df_sim)

st.download_button(
    label='Download Simulation Data (CSV)',
    data=csv_data,
    file_name='stochastic_sewerage_simulation_report.csv',
    mime='text/csv',
)
