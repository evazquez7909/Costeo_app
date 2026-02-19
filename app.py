import streamlit as st

st.set_page_config(page_title="Costeo por kg", layout="centered")
st.title("Costeo y Precio sugerido (por kg)")

st.caption("Inputs basados en tu tabla de parámetros (materia prima, energía, mano de obra, gastos, empaque y margen).")

# -----------------------------
# 1) Inputs: Materia prima
# -----------------------------
st.subheader("Materia prima")

colA, colB = st.columns(2)

with colA:
    resina_tipo = st.selectbox("Tipo de resina", ["LLDPE", "LDPE", "HDPE"])
    costo_lldpe = st.number_input("Costo LLDPE por kg", min_value=0.0, value=25.0, step=0.1, format="%.2f")
    costo_ldpe  = st.number_input("Costo LDPE por kg",  min_value=0.0, value=24.0, step=0.1, format="%.2f")
    costo_hdpe  = st.number_input("Costo HDPE por kg",  min_value=0.0, value=22.0, step=0.1, format="%.2f")

with colB:
    kg_resina_por_kg = st.number_input("Kg de resina por kg de producto", min_value=0.0, value=1.0, step=0.01, format="%.3f")
    costo_uv = st.number_input("Costo aditivo UV por kg", min_value=0.0, value=80.0, step=0.1, format="%.2f")
    kg_uv_por_kg = st.number_input("Kg aditivo UV por kg de producto", min_value=0.0, value=0.0, step=0.001, format="%.3f")

# Resolver costo de resina según selección
costo_resina_map = {"LLDPE": costo_lldpe, "LDPE": costo_ldpe, "HDPE": costo_hdpe}
costo_resina_sel = costo_resina_map[resina_tipo]

costo_material = (costo_resina_sel * kg_resina_por_kg) + (costo_uv * kg_uv_por_kg)

# -----------------------------
# 2) Inputs: Energía
# -----------------------------
st.subheader("Energía")

col1, col2 = st.columns(2)
with col1:
    costo_energia_kwh = st.number_input("Costo de energía por kWh", min_value=0.0, value=1.5, step=0.1, format="%.3f")
with col2:
    consumo_kwh_por_kg = st.number_input("Consumo de energía por kg", min_value=0.0, value=0.5, step=0.01, format="%.3f")

costo_energia = costo_energia_kwh * consumo_kwh_por_kg

# -----------------------------
# 3) Inputs: Mano de obra
# -----------------------------
st.subheader("Mano de obra")

col3, col4 = st.columns(2)
with col3:
    costo_mo_hora = st.number_input("Costo de mano de obra por hora", min_value=0.0, value=50.0, step=1.0, format="%.2f")
with col4:
    horas_mo_por_kg = st.number_input("Horas de mano de obra por kg", min_value=0.0, value=0.05, step=0.01, format="%.3f")

costo_mo = costo_mo_hora * horas_mo_por_kg

# -----------------------------
# 4) Inputs: Otros costos
# -----------------------------
st.subheader("Otros costos")

col5, col6 = st.columns(2)
with col5:
    gastos_generales_por_kg = st.number_input("Costo de gastos generales por kg", min_value=0.0, value=5.0, step=0.1, format="%.2f")
with col6:
    empaque_por_kg = st.number_input("Costo de empaque por kg", min_value=0.0, value=2.0, step=0.1, format="%.2f")

# -----------------------------
# 5) Margen / Precio
# -----------------------------
st.subheader("Margen / Precio")

margen_pct = st.number_input("Porcentaje de margen (%)", min_value=0.0, max_value=95.0, value=20.0, step=0.5, format="%.2f")

costo_total = costo_material + costo_energia + costo_mo + gastos_generales_por_kg + empaque_por_kg

# Precio para lograr margen sobre precio de venta: margen = (precio - costo) / precio
# => precio = costo / (1 - margen)
margen = margen_pct / 100.0
precio_sugerido = (costo_total / (1 - margen)) if (1 - margen) > 0 else 0.0
utilidad = precio_sugerido - costo_total

# -----------------------------
# 6) Resultados
# -----------------------------
st.subheader("Resultados (por kg)")

c1, c2, c3 = st.columns(3)
c1.metric("Costo total", f"${costo_total:,.2f}")
c2.metric("Precio sugerido", f"${precio_sugerido:,.2f}")
c3.metric("Utilidad", f"${utilidad:,.2f}")

with st.expander("Ver desglose de costos"):
    st.write(f"- **Material:** ${costo_material:,.2f}")
    st.write(f"  - Resina ({resina_tipo}): ${costo_resina_sel:,.2f} x {kg_resina_por_kg:.3f} kg")
    st.write(f"  - Aditivo UV: ${costo_uv:,.2f} x {kg_uv_por_kg:.3f} kg")
    st.write(f"- **Energía:** ${costo_energia:,.2f}  ({costo_energia_kwh:.3f} x {consumo_kwh_por_kg:.3f})")
    st.write(f"- **Mano de obra:** ${costo_mo:,.2f}  ({costo_mo_hora:,.2f} x {horas_mo_por_kg:.3f})")
    st.write(f"- **Gastos generales:** ${gastos_generales_por_kg:,.2f}")
    st.write(f"- **Empaque:** ${empaque_por_kg:,.2f}")
