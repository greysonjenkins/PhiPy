import streamlit as st
import string

# Custom CSS for styling
st.markdown("""
<style>
    .main-premise {
        font-size: 18px;
        font-weight: bold;
        margin-top: 10px;
    }
    .sub-premise-1 {
        font-size: 16px;
        margin-left: 20px;
        color: #1E90FF;
    }
    .sub-premise-2 {
        font-size: 14px;
        margin-left: 40px;
        color: #32CD32;
    }
    .conclusion {
        font-size: 20px;
        font-weight: bold;
        color: #FF4500;
        margin-top: 20px;
    }
    .premise-container {
        background-color: #f0f2f6;
        padding:2px;
        border-radius: 3px;
        margin-bottom: 10px;
    }
    .sub-premise-container {
        background-color: #e6e9ef;
        padding: 2px;
        border-radius: 3px;
        margin-top: 5px;
        margin-bottom: 10px;
    }
    .premise-header {
        font-weight: bold;
        margin-bottom: 5px;
    }
</style>
""", unsafe_allow_html=True)


def roman_numeral(num):
    values = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    numerals = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
    result = ""
    for i, value in enumerate(values):
        while num >= value:
            result += numerals[i]
            num -= value
    return result.lower()


def create_premise(prefix, is_main_argument=False, level=0):
    container_class = "premise-container" if level == 0 else "sub-premise-container"
    with st.container():
        st.markdown(f"<div class='{container_class}'>", unsafe_allow_html=True)
        if is_main_argument:
            st.markdown(f"<div class='premise-header'>Premise {prefix} (Main Argument {prefix} Conclusion)</div>",
                        unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='premise-header'>Premise {prefix}</div>", unsafe_allow_html=True)

        premise = st.text_input("Enter premise", key=f"premise_{prefix}")

        sub_premises = []

        if level < 2 and st.checkbox(f"Add sub-premises to {prefix}", key=f"check_{prefix}", value=False):
            num_sub_premises = st.number_input(f"Number of sub-premises for {prefix}", min_value=1, value=1, step=1,
                                               key=f"num_{prefix}")

            for i in range(num_sub_premises):
                if level == 0:
                    sub_prefix = f"{prefix}.{string.ascii_lowercase[i]}"
                elif level == 1:
                    sub_prefix = f"{prefix}.{roman_numeral(i + 1)}"
                sub_premise = create_premise(sub_prefix, level=level + 1)
                sub_premises.append(sub_premise)

        st.markdown("</div>", unsafe_allow_html=True)

    return {"premise": premise, "sub_premises": sub_premises}


def display_premise(premise_dict, prefix, level=0):
    if premise_dict['premise']:
        if level == 0:
            st.markdown(f"<div class='main-premise'>{prefix}. {premise_dict['premise']}</div>", unsafe_allow_html=True)
        elif level == 1:
            st.markdown(f"<div class='sub-premise-1'>{prefix}. {premise_dict['premise']}</div>", unsafe_allow_html=True)
        elif level == 2:
            st.markdown(f"<div class='sub-premise-2'>{prefix}. {premise_dict['premise']}</div>", unsafe_allow_html=True)

    for i, sub_premise in enumerate(premise_dict['sub_premises']):
        if level == 0:
            sub_prefix = string.ascii_lowercase[i]
        elif level == 1:
            sub_prefix = roman_numeral(i + 1)
        display_premise(sub_premise, sub_prefix, level + 1)


def create_argument():
    st.title("Argument Outliner")

    # Overall Argument
    st.header("Overall Argument")

    num_main_arguments = st.number_input("Number of main arguments/premises in overall argument", min_value=2, value=2,
                                         step=1)

    main_arguments = []
    for i in range(num_main_arguments):
        main_argument = create_premise(str(i + 1), is_main_argument=True)
        main_arguments.append(main_argument)

    overall_conclusion = st.text_input("Overall Conclusion")

    if st.button("Generate Argument Outline"):
        st.write("Overall Argument:")
        for i, arg in enumerate(main_arguments, 1):
            display_premise(arg, str(i), level=0)
        st.markdown(f"<div class='conclusion'>{len(main_arguments) + 1}. {overall_conclusion}</div>",
                    unsafe_allow_html=True)


if __name__ == "__main__":
    create_argument()