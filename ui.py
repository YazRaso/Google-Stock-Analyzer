import streamlit as st
from main import *

# Creating UI using streamlit
st.sidebar.title("About📌")
st.sidebar.write("""Hello! 😊👋🏻 I am Yazdan Rasoulzadeh, a software and finance enthusiast pursuing a Bachelors in both Computer Science and Business Administration. With Q4 coming to an end, I decided to build this passion project in order to deepen my understanding of stock terminology 📊 but also working with data 📈, especially within the context of turning data into meaningful visuals.  

All the code for this project can be found [here](https://github.com/YazRaso) at my GitHub repo 💻, my LinkedIn can be found [here](https://ca.linkedin.com/in/yazdan-rasoulzadeh-a77a3b309) 🌐.  

I look forward to connecting with you! 🤝 This is not in any shape or form financial advice. 🚫💸""")

st.title("On Alphabet's Stock in 2024: A Detailed Report 📈")

st.write(f"2024 has been a relatively strong year for Alphabet's stock (Google) "
         "as we approach the end of Q4, this report has been designed for a visual representation of the stocks performance")

cand_stick()