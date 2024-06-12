import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    st.write("# Welcome to Terraform Code Generator 👋")

    st.markdown(
        """
        This tool will help you generate Terraform code effortlessly, and estimate your infrastructure costs ! 🚀
    """
    )


if __name__ == "__main__":
    run()