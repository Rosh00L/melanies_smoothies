# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(f"My parents New Healthy Diner! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!"""
)

Name_on_order = st.text_input("Name on Smoothie")
st.write("Name on your smoothie will be:", Name_on_order)

cnx = st.connection ("snowflake")
session = cnx.session()
#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_List = st.multiselect(
    'Choose up to 5 ingredients:'
    ,my_dataframe
    ,max_selections=5
    )

if ingredients_List:   
    ingredients_string =' '
    
    for fruit_chosen in ingredients_List:
        ingredients_string +=fruit_chosen + ' '
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
        
    #st.write(ingredients_string)

    #Build a SQL Insert Statement & Test It
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,Name_on_order)
            values ('""" +ingredients_string+ """','""" +Name_on_order+ """' )"""

    #For check SQL and troubleshooting
    #st.write(my_insert_stmt)
    #st.stop
    ######
    
    time_to_insert= st.button('Submit Order') 
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered!', icon="✅")   



