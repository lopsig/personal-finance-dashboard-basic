import streamlit as st

from database import *

create_tables()

st.title("⚙️ Configuración")

st.subheader("🎯 Presupuesto Mensual")

current_budget = get_budget()

new_budget = st.number_input(
    "Presupuesto Mensual",
    min_value=0.0,
    value=float(current_budget),
    step=10.0
)

if st.button("Guardar Configuración"):

    update_budget(new_budget)

    st.success(
        "Presupuesto actualizado correctamente"
    )