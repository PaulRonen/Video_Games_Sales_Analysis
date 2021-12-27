import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

########################################################################################
# This function loads the data and does some very basic data cleaning.
@st.cache(persist = True)
def load_data():
	data = pd.read_csv(('video-game-sales.csv'))
	data.dropna(inplace = True)
	data["Year"] = data["Year"].astype("int")
	data.set_index("Rank")
	temp = data["Year"]
	temp = temp[temp <= 2020]
	return data , temp




# Here data is grouped by the Year attribute.
@st.cache(persist = True , allow_output_mutation=True)
def groupingdata(data):
	x = data.groupby("Year")
	
	return x

def dark_theme():
	st.markdown("<style>h1{color : black;}</style>" , unsafe_allow_html = True)
	st.markdown("<style>h2{color : black;}</style>" , unsafe_allow_html = True)
	st.markdown("<style>h3{color : black;}</style>" , unsafe_allow_html = True)
	st.markdown("<style>h4{color : black;}</style>" , unsafe_allow_html = True)
	st.markdown("<style>h5{color : black;}</style>" , unsafe_allow_html = True)
	st.markdown("<style>h6{color : black;}</style>" , unsafe_allow_html = True)
	

#function calling

data , data_year = load_data()	

grouped_data = groupingdata(data)

theme = st.sidebar.selectbox("Choose a Theme" ,["Light" , "Dark"])
if theme == "Dark":
	dark_theme()

########################################################################################
# The Title and Subheader for the web app.

st.title(" 🎮 Video Game Sales Analysis 🎮 ")
st.subheader("This application is a streamlit dashboard to analyze video game sales.")
st.markdown("Games don't make you violent, lag does🎮🔫")
st.markdown("Note : Detail Of sales Are Based On given Datasets, the analysis report are not accurate")
st.markdown("---")

########################################################################################


st.header("Top 10 Selling Games in the World : ")
other_sales = data[["Name","Global_Sales"]].head(10)

st.write(px.bar( other_sales,x = "Name" , y = "Global_Sales" , hover_data = ["Name" , "Global_Sales"] , color = "Global_Sales" ))
if st.checkbox("Show Raw Data",False):
	st.write(other_sales)
st.markdown("---")
########################################################################################

st.header("Top Selling Games  in different parts of the world : ")
check = st.selectbox("Select a option" , ["North America","Europe","Japan","Rest of the World"])

if check == "North America":

	st.subheader(" Highest Grossing Games in North America.")
	other_sales = data[["Name","Year","NA_Sales"]].sort_values(by = "NA_Sales",ascending = False).head(10)
	st.write(px.bar(other_sales, x = "Name" , y = "NA_Sales" , hover_data = ["Name" , "NA_Sales"] , color = "NA_Sales"))

if check == "Europe":

	st.subheader("Highest Grossing Games in Europe.")
	other_sales = data[["Name","Year","EU_Sales"]].sort_values(by = "EU_Sales",ascending = False).head(10)
	st.write(px.bar(other_sales, x = "Name" , y = "EU_Sales" , hover_data = ["Name" , "EU_Sales"] , color = "EU_Sales"))

if check == "Japan":

	st.subheader("Highest Grossing Games in Japan.")
	other_sales = data[["Name","Year","JP_Sales"]].sort_values(by = "JP_Sales",ascending = False).head(10)
	st.write(px.bar(other_sales, x = "Name" , y = "JP_Sales" , hover_data = ["Name" , "JP_Sales"] , color = "JP_Sales"))


elif check == "Rest of the World": 
	st.subheader("Highest Grossing Games in Rest of the world.")
	other_sales = data[["Name","Year","Other_Sales"]].sort_values(by = "Other_Sales",ascending = False).head(10)
	st.write(px.bar(other_sales, x = "Name" , y = "Other_Sales" , hover_data = ["Name" , "Other_Sales"] , color = "Other_Sales"))

if st.checkbox("Show Raw data",False):
	st.write(other_sales)

st.markdown("---")
########################################################################################

st.subheader("Highest Grossing Genres : ")
other_sales = data[["Genre","Global_Sales"]].groupby("Genre").agg("sum").sort_values(by = "Global_Sales",ascending = False)
other_sales["Genre"] = other_sales.index
st.write(px.bar(other_sales, x = "Genre" , y = "Global_Sales" , hover_data = ["Genre" , "Global_Sales"] , color = "Global_Sales"))
if st.checkbox("show Raw Data",False):
	st.write(other_sales)

st.markdown("---")	

########################################################################################

st.subheader("Highest Grossing Publishers : ")
other_sales = data[["Publisher","Global_Sales"]].groupby("Publisher").agg("sum").sort_values(by = "Global_Sales",ascending = False).head(20)
other_sales["Publisher"] = other_sales.index
st.write(px.bar(other_sales, x = "Publisher" , y = "Global_Sales" , hover_data = ["Publisher" , "Global_Sales"] , color = "Global_Sales"))
if st.checkbox("Show raw Data",False):
	st.write(other_sales)

st.markdown("---")	

########################################################################################

st.subheader("Highest Grossing Publisher/Genre/Game in a Particular Year : ")

user_input_year = st.text_input("Enter a year between 1970 and 2016" ,2000)
user_input_field = st.selectbox("Choose an Option" , ["Publisher" , "Genre" , "Name"])
try:
	x1 = np.int32(user_input_year)
	if np.int32(user_input_year) not in list(data_year):
		st.write("Not data found")
	else:	
		specific_df= grouped_data.get_group(np.int32(user_input_year))[["Name" ,"Genre" , "Publisher", "Global_Sales"]]
		if len(list(specific_df["Name"])) <= 15:
			st.write(px.pie(specific_df, values = "Global_Sales" , names = user_input_field , width = 900))            
		else:                                                                         				
		
			st.write(px.pie(specific_df[specific_df["Global_Sales"] > 2], values = "Global_Sales" , names = user_input_field , width = 900))

		if st.checkbox("Show data" , False):
			st.write(specific_df)
except ValueError:
	st.write("Please enter a valid value")



st.markdown("---")