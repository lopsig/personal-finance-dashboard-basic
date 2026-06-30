import streamlit as st
import pandas as pd

from database import *

create_tables()

st.title("📥 Ingresos")

# ---------- FORMULARIO ----------

with st.form("income_form"):

    income_date = st.date_input(
        "Fecha del Ingreso"
    )

    income_amount = st.number_input(
        "Monto del Ingreso",
        min_value=0.0,
        step=0.01
    )

    income_description = st.text_input(
        "Descripción del Ingreso"
    )

    income_submitted = st.form_submit_button(
        "Guardar Ingreso"
    )

    if income_submitted:

        insert_income(
            str(income_date),
            income_amount,
            income_description
        )

        st.success(
            "Ingreso guardado correctamente"
        )

# ---------- HISTORIAL ----------

incomes = get_incomes()

if incomes:

    income_df = pd.DataFrame(
        incomes,
        columns=[
            "ID",
            "Fecha",
            "Monto",
            "Descripción"
        ]
    )

    total_incomes = income_df["Monto"].sum()

    number_of_incomes = income_df["Monto"].count()

    average_income = income_df["Monto"].mean()

    # ---------- MÉTRICAS ----------

    st.divider()
    st.subheader(
        "📋 Historial de Ingresos"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "📥 Total Ingresos",
            f"$ {total_incomes:.2f}"
        )

    with col2:
        st.metric(
            "📊 Número de Ingresos",
            number_of_incomes
        )

    with col3:
        st.metric(
            "📈 Promedio por Ingreso",
            f"$ {average_income:.2f}"
        )

    # ---------- TABLA ----------





    income_df = income_df.drop(
        columns=["ID"]
    )

    st.dataframe(
        income_df,
        use_container_width=True
    )