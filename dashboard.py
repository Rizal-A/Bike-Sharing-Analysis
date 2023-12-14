import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from millify import millify

df = pd.read_csv("data/bike_day_clean.csv")
df2 = pd.read_csv("data/bike_hour_clean.csv")
df["date_day"] = pd.to_datetime(df["date_day"])
df2["date_day"] = pd.to_datetime(df2["date_day"])




#FUNGSI user
def create_user_df(df):
    bikeday_usertype = df[['casual','registered']].sum().reset_index()
    bikeday_usertype.rename(columns={'index':'User type',0:'count'}, inplace=True)

    return bikeday_usertype

#FUNGSI annual
def create_annual_df(df):
    bike_year = df[['year','casual','registered','total_rent']]
    bike_year['year'] = bike_year['year'].map({0:2011, 1:2012})

    bike_year = bike_year.groupby('year').agg({'casual':'sum',
                                    'registered':'sum',
                                    'total_rent':'sum'}).reset_index()
    bike_year_melt = pd.melt(bike_year, id_vars='year', value_vars=['casual','registered'], var_name='type')

    return bike_year_melt

#fungsi monthly
def create_monthy_df(df):
    month_trend = df[['date_day','casual','registered','total_rent']]
    month_trend = month_trend.resample(rule='M', on='date_day').agg({'casual':'sum', 'registered':'sum','total_rent':'sum'})
    month_trend.index = month_trend.index.strftime('%b %Y')
    month_trend.reset_index(inplace=True)
    month_trend.rename(columns={'date_day':'month_period'}, inplace=True)
    return month_trend

#fungsi weekdays

def create_weekdays_df(df):
    bike_dayname = df[['date_day','casual','registered','total_rent']]
    bike_dayname['days'] = pd.to_datetime(bike_dayname['date_day']).dt.day_name()

    bike_dayname = bike_dayname.groupby('days').agg({'casual':'sum',
                                    'registered':'sum',
                                    'total_rent':'sum'}).reset_index()
    
    weekdays_type = pd.melt(bike_dayname, id_vars='days', value_vars=['casual','registered'], var_name='type')
    return weekdays_type

#fungsi holidays
def create_holidays_df(df):
    bike_holidays = df[['holiday','casual','registered','total_rent']]
    bike_holidays['holiday'] = bike_holidays['holiday'].map({0:'Not Holiday', 1:'Holiday'})
    bike_holidays = bike_holidays.groupby('holiday').agg({'casual':'sum',
                                                        'registered':'sum',
                                                        'total_rent':'sum'}).reset_index()
    
    holidays_rent = pd.melt(bike_holidays, id_vars='holiday', value_vars=['casual','registered'], var_name='type')
    return holidays_rent

# #fungsi hours
def create_hours_df(df2):
    bike_hour = df2[['hour','casual','registered','total_rent']]
    bike_hour = bike_hour.groupby('hour').agg({'casual':'mean',
                                                'registered':'mean',
                                                'total_rent':'mean'}).reset_index()
    return bike_hour
#fungsi season
def create_season_df(df):
    bike_season = df[['season','casual', 'registered', 'total_rent']]
    bike_season['season'] = bike_season['season'].map({1:'Spring', 2:'Summer', 3:'Fall', 4:'Winter'})
    bike_season = bike_season.groupby('season').agg({'casual':'sum', 'registered':'sum', 'total_rent':'sum'}).reset_index()
    return bike_season

#fungsi season_user
def create_season_user_df(df):
    bike_season_user = df[['season', 'casual','registered']]
    bike_season_user['season'] = bike_season_user['season'].map({1:'Spring', 2:'Summer', 3:'Fall', 4:'Winter'})
    bike_season_user = bike_season_user.groupby('season').agg({'casual':'sum', 'registered':'sum'}).reset_index()
    season_user_rent = pd.melt(bike_season_user, id_vars='season', value_vars=['casual','registered'], var_name='type')
    return season_user_rent

#fungsi weather
def create_weather_df(df):
    bike_weather = df[['weathersit','casual', 'registered','total_rent']]
    bike_weather['weathersit'] = bike_weather['weathersit'].map({1:'Clear', 2:'Cloudy', 3:'Rainy', 4:'Stormy'})
    bike_weather = bike_weather.groupby('weathersit').agg({'casual':'sum', 'registered':'sum', 'total_rent':'sum'}).reset_index()
    
    return bike_weather
#fungsi weather_user
def create_weather_user_df(df):
    bike_weather_user = df[['weathersit', 'casual','registered']]
    bike_weather_user['weathersit'] = bike_weather_user['weathersit'].map({1:'Clear', 2:'Cloudy', 3:'Rainy', 4:'Stormy'})
    bike_weather_user = bike_weather_user.groupby('weathersit').agg({'casual':'sum', 'registered':'sum'}).reset_index()
    weather_user_rent = pd.melt(bike_weather_user, id_vars='weathersit', value_vars=['casual','registered'], var_name='type')
    return weather_user_rent
    
def create_weather_season_df(df2):
    weather_season = df2[['weathersit','season','total_rent']]
    weather_season['weathersit'] = weather_season['weathersit'].map({1:'Clear', 2:'Cloudy', 3:'Rainy', 4:'Stormy'})
    weather_season['season'] = weather_season['season'].map({1:'Spring', 2:'Summer', 3:'Fall', 4:'Winter'})
    weather_season = weather_season.groupby(['weathersit','season']).agg({'total_rent':'sum'}).reset_index()
    return weather_season
    
datetime_columns = ["date_day", "date_day"]

df.sort_values("date_day", inplace=True)
df.reset_index(inplace=True)


for column in datetime_columns:
    df[column] = pd.to_datetime(df[column])


#Komponen filter
min_date = df["date_day"].min()
max_date = df["date_day"].max()

with st.sidebar:
    #menambahkan logo perusahaan
    st.header("Bike Sharing Rent")
    #mengambil start_date & end_date dari date input

    start_date, end_date = st.date_input(
        label="Rentang Waktu", min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = df[(df["date_day"] >= str(start_date))&
                 (df["date_day"] <= str(end_date))]

hourly_df = df2[(df2["date_day"] >= str(start_date))&
                 (df2["date_day"] <= str(end_date))]
#open

users_df = create_user_df(main_df)
annual_df = create_annual_df(main_df)
monthly_df = create_monthy_df(main_df)
weekdays_df = create_weekdays_df(main_df)
holidays_df = create_holidays_df(main_df)
hours_df = create_hours_df(hourly_df)
weekdays_df = create_weekdays_df(main_df)
season_df = create_season_df(main_df)
season_user_df = create_season_user_df(main_df)
weather_df = create_weather_df(main_df)
weather_user_df = create_weather_user_df(main_df)
weather_season_df = create_weather_season_df(main_df)


#header

st.header('Bike Sharing Rent :bike:')
tab1, tab2= st.tabs(["Annual & Monthly Dashboard", "Daily Dashboard"])

with tab1:
    st.subheader("Total Bike Sharing Rent")
    col1, col2, col3 = st.columns(3)

    with col1:
        total_rents = main_df['total_rent'].sum()
        st.metric("Total Bike Rent", millify(total_rents))

    with col2:
        total_casual_rents = main_df['casual'].sum()
        st.metric("Non Member Bike Rent", millify(total_casual_rents))

    with col3:
        total_registered_rents = main_df['registered'].sum()
        st.metric("Member Bike Rent", millify(total_registered_rents))


    #Bike Sharing Rent Trend
    color = ['#1d3557','#219ebc']
    st.subheader("Bike Sharing Rent Trend")

    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35,15))

    sns.barplot(data= annual_df.sort_values('value',ascending=False), x='year', y='value', hue='type', palette=color, ax=ax[0])
    ax[0].set_xlabel(None)
    ax[0].set_ylabel(None)
    ax[0].tick_params(axis='both', labelsize=30)
    ax[0].set_title('Annual Bike Sharing Rent by Year', fontsize=40)
    ax[0].legend(fontsize=30)

    sns.lineplot(data = monthly_df, x='month_period', y='casual', 
                ax=ax[1], marker="o", color="#219ebc", label='casual')
    sns.lineplot(data = monthly_df, x='month_period', y='registered', 
                ax=ax[1], marker="o", color="#1d3557", label='registered')
    ax[1].set_xlabel(None)
    ax[1].set_ylabel(None)
    ax[1].tick_params(axis='x', rotation=90, labelsize=30)
    ax[1].tick_params(axis='y', labelsize=30)
    ax[1].set_title('Monthly Period Bike Sharing Rent', fontsize=40)
    ax[1].legend(fontsize=30)
    plt.tight_layout()
    st.pyplot(fig)

    #Season Bike Sharing Rent
    st.subheader("Season Bike Sharing Rent")

    col1, col2, col3 = st.columns(3)

    with col1:
        max_season_rent = season_df.sort_values('total_rent', ascending=False).head(1)
        max_season_rent = max_season_rent['season'].values[0]
        max_season_value = str(max_season_rent)
        st.metric("Highest Bike Rent", max_season_value)

    with col2:
        max_season_casual = season_df.sort_values('casual', ascending=False).head(1)
        max_season_casual = max_season_casual['season'].values[0]
        max_season_casual_value = str(max_season_casual)
        st.metric("Highest Non Member Bike Rent", max_season_casual_value)

    with col3:
        max_season_registered = season_df.sort_values('registered', ascending=False).head(1)
        max_season_registered = max_season_registered['season'].values[0]
        max_season_registered_value = str(max_season_registered)
        st.metric("Highest Member Bike Rent", max_season_registered_value)
    

    season_order = ['Spring','Summer','Fall','Winter']
    fig, ax = plt.subplots(nrows=1, ncols=2,figsize=(20,8))
    max_season = season_df.loc[season_df['total_rent'].idxmax(), 'season']

    # Create a palette with different colors for the highest bar
    palette = ['#1d3557' if season == max_season else '#219ebc' for season in season_order]

    sns.barplot(data=season_df, x='season', y='total_rent', order=season_order, palette=palette, ax=ax[0])
    ax[0].set_xlabel(None)
    ax[0].set_ylabel(None)
    ax[0].tick_params(axis='both', labelsize=15)
    ax[0].set_title('Bike Sharing Rent by Season', fontsize=30)

    sns.barplot(data=season_user_df.sort_values('value',ascending=False), x='season', y='value', hue='type',
            palette=['#1d3557','#219ebc','#219ebc'], ax=ax[1])
    ax[1].set_xlabel(None)
    ax[1].set_ylabel(None)
    ax[1].tick_params(axis='both', labelsize=15)
    ax[1].set_title('Bike Sharing Rent Season by User', fontsize=30)
    ax[1].legend(fontsize=20)
    
    st.pyplot(fig)


    #weather Bike Sharing Rent
    st.subheader("Weather Bike Sharing Rent")

    col1, col2, col3 = st.columns(3)

    with col1:
        max_weather_rent = weather_df.sort_values('total_rent', ascending=False).head(1)
        max_weather_rent = max_weather_rent['weathersit'].values[0]
        max_weather_value = str(max_weather_rent)
        st.metric("Highest Bike Rent", max_weather_value)

    with col2:
        max_weather_casual = weather_df.sort_values('casual', ascending=False).head(1)
        max_weather_casual = max_weather_casual['weathersit'].values[0]
        max_weather_casual_value = str(max_weather_casual)
        st.metric("Highest Non Member Bike Rent", max_weather_casual_value)

    with col3:
        max_weather_registered = weather_df.sort_values('registered', ascending=False).head(1)
        max_weather_registered = max_weather_registered['weathersit'].values[0]
        max_weather_registered_value = str(max_weather_registered)
        st.metric("Highest Member Bike Rent", max_weather_registered_value)

    list_season = ['Spring','Summer','Fall','Winter']
    weather_order = ['Clear','Cloudy','Rainy','Stormy']
    
    max_weather = weather_season_df.loc[weather_season_df['total_rent'].idxmax(), 'weathersit']
    
    fig = plt.figure(figsize=(15,15))
    # Create a palette with different colors for the highest bar
    palette = ['#1d3557' if weather == max_weather else '#219ebc' for weather in weather_order]
    for i in range(0,len(list_season)):
        plt.subplot(2, 2, i+1)
        sns.barplot(data= weather_season_df[weather_season_df['season']==list_season[i]], x='weathersit', y='total_rent', order=weather_order,
                    palette=palette)
        plt.title(f'Bike Rent Season {list_season[i]}', fontsize=30)
        plt.xlabel(None)
        plt.ylabel(None)
        plt.tick_params(axis='both', labelsize = 20)
        plt.tight_layout()

    st.pyplot(fig)
    

    


with tab2 : 
    st.subheader("Hourly Bike Sharing Rent")
    col1, col2, col3 = st.columns(3)

    with col1:
        avg_rents = hourly_df['total_rent'].mean()
        st.metric("Average Bike Rent", millify(avg_rents))

    with col2:
        avg_casual_rents = hourly_df['casual'].mean()
        st.metric("Average Non Member Bike Rent", millify(avg_casual_rents))

    with col3:
        avg_registered_rents = hourly_df['registered'].mean()
        st.metric("Average Member Bike Rent", millify(avg_registered_rents))

    #Daily Bike Sharing Rent
    st.subheader("Daily Bike Sharing Rent")

    order_days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(15,5))

    sns.barplot(data=weekdays_df.sort_values('value',ascending=False), x='days', y='value', hue='type',ax=ax[0], order=order_days, 
                palette=color)
    ax[0].set_xlabel(None)
    ax[0].set_ylabel(None)
    ax[0].tick_params(axis='x', rotation=25, labelsize=10)
    ax[0].tick_params(axis='y', labelsize=10)
    ax[0].set_title('Weekdays Bike Rent', fontsize=15)


    sns.barplot(data= holidays_df.sort_values('value', ascending=False), x= 'holiday', y='value', 
                palette=color, ax=ax[1], hue='type')
    ax[1].set_xlabel(None)
    ax[1].set_ylabel(None)
    ax[1].tick_params(axis='x', labelsize=10)
    ax[1].tick_params(axis='y', labelsize=10)
    ax[1].set_title('Bike Rent on Holiday', fontsize=15)
    ax[1].legend(fontsize=15)

    st.pyplot(fig)

    #Hourly Bike Sharing Rent
    st.subheader("Hourly Bike Sharing Rent")

    fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(12,10))

    ax[0].plot(hours_df['hour'],hours_df['total_rent'])
    ax[0].fill_between(hours_df.hour.values, hours_df.total_rent.values, color='#219ebc')
    ax[0].set_xlabel(None)
    ax[0].set_ylabel(None)
    ax[0].set_xlim(0,23)
    ax[0].set_ylim(ymin= 0)
    ax[0].set_xticks(np.arange(24), hours_df['hour'])
    ax[0].set_title('Bike Rent Hour', fontsize=15)

    ax[1].stackplot(hours_df['hour'],hours_df['casual'], hours_df['registered'],
                    alpha=0.5,
                    colors=['#219ebc','#1d3557'],
                    labels=['casual', 'registered'])
    ax[1].set_xlabel(None)
    ax[1].set_ylabel(None)
    ax[1].set_xlim(0,23)
    ax[1].set_ylim(ymin= 0)
    ax[1].set_xticks(np.arange(24), hours_df['hour'])
    ax[1].set_title('Bike Rent Hour by User Type', fontsize=15)
    ax[1].legend()
    plt.tight_layout()

    st.pyplot(fig)
