import streamlit as st
import pandas as pd
import plotly.express as px
from database import *


create_tables()

st.set_page_config(
    page_title="Personal Finance Dashboard",
    page_icon="💰",
    layout="wide",
)

st.title("💰 Mis Finanzas")
st.subheader("Registrar Gasto")

with st.form("expense_form"):
    date = st.date_input("Fecha")
    category = st.selectbox(
        "Categoria",
        [
            "Comida",
            "Transporte",
            "Agua",
            "Luz",
            "Educación",
            "Entretenimiento",
            "Tarjeta de Credito",
            "Otros"
        ]
    )

    amount = st.number_input("Monto", min_value=0.0, step=0.01)
    description = st.text_input("Descripción")
    submitted = st.form_submit_button("Guardar")

    if submitted:
        insert_expense(
            str(date),
            category,
            amount,
            description,
        )

        st.success("Gasto guardado correctamente")



# -----DATA FRAME EXPENSES------
expenses = get_expenses()
if expenses:

    df = pd.DataFrame(
        expenses,
        columns=[
            "ID",
            "Fecha",
            "Categoría",
            "Monto",
            "Descripción"
        ]
    )
    # df["Monto"] = df["Monto"].map(
    #     lambda x: f"$ {x:,.2f}"
    # )

    #-----METRICS-----
    total_expenses = df["Monto"].sum()
    number_of_expenses = df["Monto"].count()
    average_expenses = df["Monto"].mean()

    #--------MONTHLY BUDGET-------
    st.divider()
    st.subheader("🎯 Presupuesto mensual")
    budget = st.number_input("Presupuesto Mensual", min_value=0.0, step=0.1, value=300.00)

    available_balance = budget - total_expenses

    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            "💵 Presupuesto",
            f"$ {budget:,.2f}",
        )
    with col2:
        st.metric(
            "💰 Disponible",
            f"$ {available_balance:,.2f}",
        )

    if budget > 0:
        percentage = total_expenses / budget
    else:
        percentage = 0

    st.progress(min(percentage, 1.0))
    st.write(f"Has utilizado {percentage * 100:.2f}% de tu presupuesto.")

    if percentage < 0.8:
        st.subheader("✅ Vas bien con tu presupuesto")
    elif percentage < 1:
        st.warning("⚠️ Te estás acercando al límite de tu presupuesto")
    else:
        st.error("🚨 Has superado tu presupuesto mensual")

    # -----GROUP EXPENSES BY CATEGORY - Graphics-------
    st.divider()
    expenses_by_category = (
        df.groupby("Categoría")["Monto"].sum().reset_index()
    )

    st.subheader("📊 Gastos por categoría")


    fig = px.pie(
        expenses_by_category,
        names = "Categoría",
        values = "Monto",
    )

    st.plotly_chart(fig, use_container_width=True)


    # ------EXPENSE HISTORY------
    st.divider()
    st.subheader("Historial de gastos")
    df = df.drop(
        columns=["ID"]
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "💰 Total Gastado",
            f"$ {total_expenses:.2f}",
        )
    with col2:
        st.metric(
            "📊 Número de Gastos",
            number_of_expenses,
        )
    with col3:
        st.metric(
            "📈 Promedio por Gasto",
            f"$ {average_expenses:.2f}",
        )

    st.dataframe(
        df,
        use_container_width=True
    )


# -------INCOMES-------
st.divider()
st.subheader("📥 Registrar ingreso")

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

    income_submitted = st.form_submit_button("Guardar Ingreso")

    if income_submitted:

        insert_income(
            str(income_date),
            income_amount,
            income_description
        )

        st.success("Ingreso guardado correctamente")

# -----INCOMES HISTORY------
st.subheader("📥 Historial de ingresos")
incomes = get_incomes()
if incomes:
    income_df = pd.DataFrame(
        incomes,
        columns=[
            "ID",
            "Fecha",
            "Monto",
            "Descripción",
        ]
    )

    income_df = income_df.drop(
        columns=["ID"]
    )

    total_incomes = income_df["Monto"].sum()

    # -----METRIC BALANCE------
    balance = total_incomes - total_expenses

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "📥 Ingresos",
            f"$ {total_incomes:.2f}",
        )

    with col2:
        st.metric(
            "💸 Gastos",
            f"$ {total_expenses:.2f}",
        )

    with col3:
        st.metric(
            "💰 Balance",
            f"$ {balance:.2f}",
        )




    st.dataframe(
        income_df,
        use_container_width=True
    )


