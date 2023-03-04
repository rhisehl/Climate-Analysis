# Climate Analysis: Honolulu, Hawaii

Using SqlAlchemy, a Sqlite database containing station measurements for Honolulu, Hawaii was imported into Jupyter Notebook. The data was reflected to determine the available tables before casting each table to its own class.

## Exploratory Precipitation Analysis

The most recent date of the data was determiend, and data for the last year was queried. Following the query, the last year's precipitation data was graphed to show a few spiikes of precipitation around September, February, and May.

![image](https://user-images.githubusercontent.com/116215793/222919170-5841cf73-58a8-42b0-8868-2c73f7eb3100.png)

The average precipitation was .17", although the median was .02" and the maximum amount was 6.7".

## Exploratory Station Analysis

The data was separated into 9 different stations. These stations were then queried to determine how many points of observation were completed for each station. There were between 511 and 2772 observations per station.

After separating out the station with the most observations, the previous year's temperature data was analyzed. Temperatures tend to range in the mid-70s.

![image](https://user-images.githubusercontent.com/116215793/222919323-feb0d201-fed5-494a-8ef3-2742ee688691.png)
