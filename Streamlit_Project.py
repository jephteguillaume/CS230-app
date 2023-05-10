"""
Name: Jephte Guillaume
Final Project
Description: Meteorite Landings Streamlit Project
Date: 5/10/23
"""
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

def readData():
    data = pd.read_csv('CS230-app/Meteorite_Landings copy.csv')
    # drop irrelevant columns
    data = data.drop(columns=['nametype', 'GeoLocation', 'fall', 'id'])
    # drop rows without values
    data = data.dropna()
    # renames latitude, longitude, mass, classification columns
    data = data.rename(columns={'reclat': 'latitude', 'reclong': 'longitude', 'mass (g)': 'Mass', 'recclass': 'Class'})
    # converts values in mass column from grams to pounds
    data['Mass'] = data['Mass']/453.592
    return data

def compareMeteorites(data, meteorites):
    # sorts dataframe to where name is in list of selected meteorites
    df = data[data.name.isin(meteorites)]

    # rotates dataframe using dataframe.transpose()
    rotatedDF = df.transpose()
    # prints transposed dataframe as a table
    st.table(rotatedDF)
    # maps latitude and longitude using streamlit map
    st.map(df)

def classMass(data, minMass):
    # sort dataframe to meteorites with mass more than the slider value
    df = data[data.Mass >= minMass]
    fig, ax = plt.subplots()

    # the pie chart data is the number of the different values in class column
    pieData = df.Class.value_counts()
    title = f"Pie Chart of Meteorite Classification over {minMass:.2f} pounds"
    plt.title(title)

    # sets labels to the index of the pieData series
    plt.pie(pieData, labels=pieData.index, autopct='%.2f')
    st.write(pieData)
    st.pyplot(fig)

def avgMass(data, graphRange):
    # sorts dataframe to be between tuple values of graphRange
    df = data[data.year >= graphRange[0]]
    df = df[df.year <= graphRange[1]]

    # group meteorites by year and the means of each group
    mass = df.groupby('year').mean()
    st.write("Graph Data - Mean values grouped by year")
    st.write(mass.drop(columns=['latitude', 'longitude']))
    fig, ax = plt.subplots()
    title = f"Meteorite mass over time from {graphRange[0]} to {graphRange[1]}"
    plt.title(title)

    # bar graph with year on x-axis and height on y-axis
    plt.bar(mass.index, mass.Mass, width=3)
    plt.xlabel("Year")
    plt.ylabel("Average Mass (pounds) of Meteorites")
    st.pyplot(fig)

def massByYear(data, type):
    # plot scatter plot of specific meteorite type by year
    df = data[data.Class.isin([type])]
    fig, ax = plt.subplots()
    plt.scatter(df['year'], df['Mass'], s=10)
    plt.xlabel('Year')
    plt.ylabel('Mass (pounds)')
    plt.title(f'{type} Mass Over Time')
    st.pyplot(fig)


def main():
    data = readData()
    st.title("Meteorite Landings Streamlit Project")
    st.subheader("Jephte Guillaume")
    # selects page in sidebar using radio selection
    page = st.sidebar.radio("Page Selection",
    ("Raw Data", "Compare Meteorites", "Weight vs Classification Chart", "Average Weight Over Time Graph", "Meteorite Type by Year Scatter Plot"))
    st.subheader(page)
    # if else to change what data is on page
    if page == "Raw Data":
        st.write(data)
    elif page == "Compare Meteorites":
        # selects multiple meteorite names into type list
        # finds all unique meteorite names and puts into list
        meteorite_names = data['name'].unique().tolist()
        selected_meteorites = st.multiselect("Select meteorites by name:", options=meteorite_names)
        compareMeteorites(data, selected_meteorites)
    elif page == "Weight vs Classification Chart":
        # gets biggest and smallest mass values for streamlit slider
        minMass = data.Mass.min()
        maxMass = data.Mass.max()

        # slider to determine minimum mass of meteorite for classMass function
        massFilter = st.slider("Minimum Mass", int(minMass), int(maxMass), int(minMass), 1)
        classMass(data, massFilter)
    elif page == "Average Weight Over Time Graph":
        # converts year to integer values
        data.year.astype(int)

        # gets min and max year values for slider
        startYear = data.year.min()
        endYear = data.year.max()

        # two sided slider to choose range of years
        yearFilter = st.slider("Select Years to Graph", int(startYear), int(endYear), (int(startYear), int(endYear)), step=1)
        avgMass(data, yearFilter)
    elif page == "Meteorite Type by Year Scatter Plot":
        # finds all unique meteorite types and puts into list
        meteorite_types = data['Class'].unique().tolist()
        selected_m = st.selectbox('Chose meteorite type:', options=meteorite_types)
        massByYear(data, selected_m)
main()
