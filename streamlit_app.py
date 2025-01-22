import streamlit as st
import pandas as pd

# Пример данных о продуктах
PRODUCTS = {
    "Кабачок": {"Белки": 0.6, "Жиры": 0.3, "Углеводы": 4.6, "Калории": 24},
    "Томат (помидор)": {"Белки": 1.1, "Жиры": 0.2, "Углеводы": 3.7, "Калории": 20},
    "Капуста брокколи": {"Белки": 3, "Жиры": 0.4, "Углеводы": 5.2, "Калории": 28},
    "Шампиньоны свежие": {"Белки": 4.3, "Жиры": 1, "Углеводы": 0.1, "Калории": 27},
    "Сыр Адыгейский": {"Белки": 18.5, "Жиры": 14, "Углеводы": 0, "Калории": 240},
    "Перец сладкий красный": {"Белки": 1.3, "Жиры": 0, "Углеводы": 5.3, "Калории": 27},
    "Лук репчатый": {"Белки": 1.4, "Жиры": 0, "Углеводы": 9.6, "Калории": 42},
}

# Заголовок
st.title("Калькулятор продуктов")

# Инициализация состояния для хранения данных таблицы
if "data" not in st.session_state:
    st.session_state.data = []

# Функция добавления строки
def add_row():
    st.session_state.data.append({"Продукт": "", "Вес": 0, "Белки": 0, "Жиры": 0, "Углеводы": 0, "Калории": 0})

# Кнопка добавления продукта
if st.button("Добавить продукт"):
    add_row()

# Таблица данных
to_remove = None  # Индекс строки для удаления
for i, row in enumerate(st.session_state.data):
    col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 6, 2, 2, 2, 2, 2])

    # Кнопка удаления строки (выровненная по нижнему краю)
    with col1:
        st.markdown("<div style='height: 38px;'></div>", unsafe_allow_html=True)  # Пустое место для выравнивания
        if st.button("❌", key=f"remove_{i}"):
            to_remove = i  # Помечаем строку для удаления

    # Выпадающий список с продуктами
    with col2:
        product = st.selectbox("Продукт", [""] + list(PRODUCTS.keys()), key=f"product_{i}")
        row["Продукт"] = product

    # Поле ввода веса
    with col3:
        weight = st.number_input("Вес, гр", min_value=0, value=row["Вес"], step=1, key=f"weight_{i}")
        row["Вес"] = weight

    # Поля для Белков, Жиров, Углеводов и Калорий
    if product:
        nutrients = PRODUCTS[product]
        row["Белки"] = nutrients["Белки"] * weight / 100
        row["Жиры"] = nutrients["Жиры"] * weight / 100
        row["Углеводы"] = nutrients["Углеводы"] * weight / 100
        row["Калории"] = nutrients["Калории"] * weight / 100

    with col4:
        st.text("Белки")
        st.write(round(row["Белки"], 2))
    with col5:
        st.text("Жиры")
        st.write(round(row["Жиры"], 2))
    with col6:
        st.text("Углеводы")
        st.write(round(row["Углеводы"], 2))
    with col7:
        st.text("Калории")
        st.write(round(row["Калории"], 2))

# Удаление строки, если кнопка была нажата
if to_remove is not None:
    st.session_state.data.pop(to_remove)

# Преобразование данных в DataFrame для расчетов
df = pd.DataFrame(st.session_state.data)

# Итоговые значения
if not df.empty:
    total = df[["Вес", "Белки", "Жиры", "Углеводы", "Калории"]].sum()
    st.markdown("### Итого")
    st.write(
        pd.DataFrame(
            total.values.reshape(1, -1),
            columns=["Вес, гр", "Бел, гр", "Жир, гр", "Угл, гр", "Кал, ккал"],
        )
    )

    # Значения на 100 грамм
    per_100g = total / total["Вес"] * 100
    st.markdown("### На 100 грамм")
    st.write(
        pd.DataFrame(
            per_100g.values.reshape(1, -1),
            columns=["Вес, гр", "Бел, гр", "Жир, гр", "Угл, гр", "Кал, ккал"],
        )
    )
