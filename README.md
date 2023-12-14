# Bikesharing Data Analysis and Dashboard🚲
Dataset by: Capital Bikeshare

## 📓 Data Analysis with Jupyter Notebook
See the detail of analysis and visualization on the [notebook](https://github.com/Rizal-A/Bike-Sharing-Analysis/blob/main/Data_Analysis_Bike_Rent.ipynb)

### Defining Business Question
- How does Bike Sharing Rent compare between casual and registered types?
- What is the trend of Bike Sharing Rent per year?
- What are the Bike Sharing Rent trends by day, month and year?
- During what time of day do most Bike Rent events occur?
- How is Bike Sharing Rent seasonally, what are the highest and lowest seasons for bike rentals?
- What are the factors that influence the number of Bike Sharing Rent?

### Insights and Conclusions
1. The number of users with registered type is 2.6 million while casual users are only 600000 which means that registered users are more. this shows a substantial difference, with registered users about 4x more than casual users.

2. The number of Bike Sharing Rent fluctuates but the number of bike rentals increased in 2012 which was dominated by registered bike users.

3. The number of Bike Sharing Rent increased in 2012 and peaked in September, for bicycle use is dominated on weekdays (Monday - Friday) and peaks on Fridays, this is also seen where on holidays the number of bicycle renters decreases but there is an interesting thing that casual type bicycle renters increase on weekends.

4. The highest average number of bicycle rentals in the morning and afternoon can be seen in the graph of bicycle rentals based on peak hours at 8am and 5pm. This indicates that bicycles are rented when going to work and returning from work.

5. Bike Sharing Rent is highest in the Fall season, which is probably the best weather for traveling by bicycle, and lowest in the Spring season, where the temperature is quite cold due to the transition from the Winter season.

6. Bike Sharing Rent is influenced by the weather, bike renters increase when the weather is good and decrease when the weather is unfavorable, especially during rainy and bad weather.
The number of bicycle rentals is strongly influenced by temperature, there is a strong positive relationship between temp and atemp on the number of bicycle rentals. This indicates that the number of renters increases as the temperature increases and decreases when the temperature is low while bicycle rentals have a slight negative relationship with hum and windspeed showing that as humidity and windspeed increase, there is a slight decrease in the number of bicycle rentals.

##  📟 Dashboard with Streamlit

### Streamlit Cloud
⚠️ View the dashboard directly on this link: [dashboard](https://bikesharing-dashboard-pratwib.streamlit.app/)

The dashboard shows the number of total users across the year and season. It also shows the difference casual users and registered users use of the bikesharing service, based day of the week.

### Run Streamlit on Local

#### Install Dependencies

To install all the required libraries, open your terminal/command prompt, navigate to project folder, and run the following command:

```bash
pip install -r requirements.txt
```

#### Run Dashboard
```bash
streamlit run dashboard.py
```
