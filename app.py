import streamlit as st
import pandas as pd
import plotly.express as px

from database import *

create_tables()

st.set_page_config(
    page_title="Mis Finanzas",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Mis Finanzas")

# ---------- DATOS ----------

expenses = get_expenses()
incomes = get_incomes()
budget = get_budget()

# ---------- DATAFRAMES ----------

expense_df = pd.DataFrame(
    expenses,
    columns=[
        "ID",
        "Fecha",
        "Categoría",
        "Monto",
        "Descripción"
    ]
) if expenses else pd.DataFrame()

income_df = pd.DataFrame(
    incomes,
    columns=[
        "ID",
        "Fecha",
        "Monto",
        "Descripción"
    ]
) if incomes else pd.DataFrame()

# ---------- CÁLCULOS ----------

total_expenses = (
    expense_df["Monto"].sum()
    if not expense_df.empty
    else 0
)

total_incomes = (
    income_df["Monto"].sum()
    if not income_df.empty
    else 0
)

balance = total_incomes - total_expenses

available_balance = budget - total_expenses

percentage = (
    total_expenses / budget
    if budget > 0
    else 0
)

# ---------- MÉTRICAS PRINCIPALES ----------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "📥 Ingresos",
        f"$ {total_incomes:.2f}"
    )

with col2:
    st.metric(
        "💸 Gastos",
        f"$ {total_expenses:.2f}"
    )

with col3:
    st.metric(
        "💰 Balance",
        f"$ {balance:.2f}"
    )

# ---------- DASHBOARD PRINCIPAL ----------

st.divider()

left_col, right_col = st.columns([2, 1])

# ---------- GRÁFICO ----------

with left_col:

    st.subheader("📊 Distribución de Gastos")

    if not expense_df.empty:

        expenses_by_category = (
            expense_df
            .groupby("Categoría")["Monto"]
            .sum()
            .reset_index()
        )

        fig = px.pie(
            expenses_by_category,
            names="Categoría",
            values="Monto",
            hole=0.4
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        st.info(
            "Aún no existen gastos registrados."
        )

# ---------- PRESUPUESTO ----------

with right_col:

    st.subheader("🎯 Presupuesto")

    st.metric(
        "💵 Presupuesto",
        f"$ {budget:.2f}"
    )

    st.metric(
        "💰 Disponible",
        f"$ {available_balance:.2f}"
    )

    st.progress(
        min(percentage, 1.0)
    )

    st.write(
        f"📊 {percentage * 100:.1f}% utilizado"
    )

    if percentage < 0.8:
        st.success(
            "✅ Vas bien con tu presupuesto"
        )

    elif percentage < 1:
        st.warning(
            "⚠️ Te estás acercando al límite"
        )

    else:
        st.error(
            "🚨 Has superado tu presupuesto"
        )