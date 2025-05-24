import streamlit as st
import math
import re

# Session state for history
if 'history' not in st.session_state:
    st.session_state.history = []

# Title and description
st.title("🧮 Multi-Mode Calculator")
st.markdown("Switch between different calculator modes using the tabs below.")

# Helper function for safe evaluation
def safe_eval(expr, mode):
    try:
        # Only allow math functions in scientific mode
        allowed_names = {
            **{k: v for k, v in math.__dict__.items() if not k.startswith("__")},
            "abs": abs,
            "round": round
        } if mode == "Scientific" else {}
        return eval(expr, {"__builtins__": {}}, allowed_names)
    except Exception as e:
        return f"Error: {e}"

# Tabs for calculator modes
tab1, tab2, tab3, tab4 = st.tabs(["Basic", "Scientific", "Programmer", "Custom"])

with tab1:
    st.subheader("🧾 Basic Calculator")
    num1 = st.number_input("First number", key="basic_num1")
    num2 = st.number_input("Second number", key="basic_num2")
    operation = st.selectbox("Operation", ["Add", "Subtract", "Multiply", "Divide"])
    
    if st.button("Calculate", key="basic_calc"):
        with st.spinner("Calculating..."):
            if operation == "Add":
                result = num1 + num2
            elif operation == "Subtract":
                result = num1 - num2
            elif operation == "Multiply":
                result = num1 * num2
            elif operation == "Divide":
                result = "Error: Division by zero" if num2 == 0 else num1 / num2
            st.session_state.history.append(f"{num1} {operation} {num2} = {result}")
            st.success(f"Result: {result}")

with tab2:
    st.subheader("📐 Scientific Calculator")
    expr = st.text_input("Enter expression (e.g., sin(1), log(10), 2**3)", key="sci_expr")

    if expr:
        with st.spinner("Evaluating..."):
            result = safe_eval(expr, mode="Scientific")
            st.session_state.history.append(f"{expr} = {result}")
            if isinstance(result, str) and result.startswith("Error"):
                st.error(result)
            else:
                st.success(f"Result: {result}")

with tab3:
    st.subheader("🧑‍💻 Programmer Calculator")
    number = st.text_input("Enter number", key="prog_input")
    base = st.selectbox("Convert from", ["Binary", "Decimal", "Hexadecimal"])

    def convert_programmer(num_str, base):
        try:
            if base == "Binary":
                dec = int(num_str, 2)
            elif base == "Hexadecimal":
                dec = int(num_str, 16)
            else:
                dec = int(num_str)
            return {
                "Binary": bin(dec),
                "Decimal": dec,
                "Hexadecimal": hex(dec)
            }
        except ValueError:
            return {"Error": "Invalid number format."}

    if number:
        with st.spinner("Converting..."):
            result = convert_programmer(number, base)
            if "Error" in result:
                st.error(result["Error"])
            else:
                st.session_state.history.append(f"{number} ({base}) => {result}")
                st.code(result, language="json")

with tab4:
    st.subheader("🧩 Custom Mode")
    st.markdown("Input any mathematical formula using standard Python syntax.")
    user_expr = st.text_area("Formula input", placeholder="e.g., 3 * (2 + 5) / sqrt(9)")

    if user_expr:
        with st.spinner("Processing..."):
            result = safe_eval(user_expr, mode="Scientific")
            st.session_state.history.append(f"{user_expr} = {result}")
            if isinstance(result, str) and result.startswith("Error"):
                st.error(result)
            else:
                st.success(f"Result: {result}")

# Calculation History
with st.expander("📜 Calculation History"):
    for entry in st.session_state.history:
        st.write(entry)
    if st.button("Clear History"):
        st.session_state.history.clear()
        st.success("History cleared.")

# Footer
st.caption("🔹 Built with Streamlit — Responsive and lightweight calculator app.")
