# 🌊 AIMeCHA: Stochastic Sewerage Energy-Carbon & Real Options Engine

> **Smart Infrastructure Decision-Support Tool**  
> *Transforming static wastewater treatment designs into dynamic, carbon-optimized, and financially resilient asset management strategies.*

---

## ⚡ What Does This Tool Do?

Traditional municipal sewerage planning relies on static numbers that ignore real-world changes like weather storms, population surges, energy tariff hikes, and carbon taxes. 

**AIMeCHA** changes that by running **stochastic simulations** (thousands of real-world scenarios) to help municipal engineers and utilities:
- 📉 **Reduce Energy Demand** by up to **24.8%** using dynamic Variable Frequency Drive (VFD) controls.
- 🌱 **Cut Scope 2 Carbon Emissions** by up to **31.2%** via solar microgrid and smart blower optimization.
- 💰 **Save up to 18.5% in Lifecycle Costs** by timing equipment upgrades using **Real Options Analysis (ROA)**.

---

## 📊 How It Works (The 4-Step Process)

```
  1. STOCHASTIC LOADING               2. ELECTROMECHANICAL PHYSICS
  ┌─────────────────────────┐         ┌─────────────────────────┐
  │ • Hydraulic Growth (GBM)│  ────►  │ • Dynamic Blower Power  │
  │ • BOD Load (OU Process) │         │ • Raw Sewage Pumping    │
  │ • Wet-Weather Inflow    │         │ • Auxiliary Mixing      │
  └─────────────────────────┘         └─────────────────────────┘
               │                                   │
               ▼                                   ▼
  3. CARBON & COST TRACKING           4. REAL OPTIONS DECISION
  ┌─────────────────────────┐         ┌─────────────────────────┐
  │ • Dynamic Grid Emissions│  ────►  │ • Phased Capacity Sizing│
  │ • Solar Microgrid Offsets│        │ • High-Efficiency Upgrades│
  │ • Carbon Tax Liabilities│         │ • Optimal Timing Window │
  └─────────────────────────┘         └─────────────────────────┘
```

---

## 🔑 Core Features & Interactive Capabilities

| Feature | Description | Interactive UI Control |
| :--- | :--- | :--- |
| **🌊 Hydraulic Loading Engine** | Simulates flow growth and seasonal weather spikes. | Sliders for $\mu_Q$ (Growth Rate) & $\sigma_Q$ (Volatility) |
| **🧪 Organic Load (BOD) Engine** | Models raw wastewater strength with wet-weather dilution ($ρ_{QC} < 0$). | Sliders for Baseline BOD & Mean Reversion Speed ($\theta$) |
| **⚡ Blower Aeration Energy** | Computes exact electrical power ($kW$) based on daily oxygen demand. | Automatic real-time physics calculation |
| **🌱 Scope 2 Carbon Tracking** | Measures greenhouse gas footprint against dynamic electricity grid factors. | On-site Solar PV microgrid offset toggle |
| **📥 Report Export** | Generates full time-series datasets ready for auditing and compliance. | **One-Click CSV Export** button |

---

## 🚀 Quick Start (Run in 3 Steps)

### 1. Clone & Navigate
```bash
git clone https://github.com/your-username/stochastic-sewerage-roa.git
cd stochastic-sewerage-roa
```

### 2. Install Requirements
```bash
pip install -r requirements.txt
```

### 3. Launch Web App
```bash
streamlit run app.py
```
*Your browser will automatically open `http://localhost:8501` with the interactive UI engine!*

---

## 📁 Project File Structure

```text
├── app.py              # Main interactive web dashboard & computational engine
├── requirements.txt    # Required Python packages (Streamlit, Pandas, NumPy, Plotly)
└── README.md           # Visual guide and project documentation
```

---

## 📖 Based On Research

This software implements the mathematical formulations established in:
* **Hosdi, H. B. (2026a).** *Stochastic cost modeling and real options analysis for municipal sewerage infrastructure development.*
* **Hosdi, H. B. (2026b).** *Stochastic hydraulic design and real options sizing of municipal sewerage systems.*
* **Hosdi, H. B. (2026c).** *Stochastic Lifecycle Energy-Carbon Optimization and Real Options Sizing for Municipal Sewerage Systems.*

---
*Created by **EUR ING Tc. Hazwan B. Hosdi** (Planning and Engineering Department, Indah Water Konsortium / WorldQuant University).*
