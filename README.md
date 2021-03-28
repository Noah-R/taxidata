# What I plan to do

Predict fare amount with ML

Create some kind of web interface with an interactive map

# Datasets

## TLC Trip Records

https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page

This data provides records, in csv format, of every taxi trip taken in New York City, organized by month. It denotes where each trip starts and ends, in the form of one of the 263 zones it splits the city into. It also provides other metadata, including the start and end time of the trip, the distance travelled, and the amount and type of payment.

The analyses in this repository use data from both yellow taxis, which operate throughout the city, and green taxis, which are specifically forbidden from picking up passengers in Manhattan below West 110th Street or East 96th Street. Data is also available for for-hire vehicles(IE Uber, Lyft, black car services), but it is significantly larger, less detailed, and likely less reliable, so it is not used here.

## NWS Central Park Observation Station

https://w2.weather.gov/climate/index.php?wfo=okx (Preliminary Monthly Climate Data)

This data provides, in the form of written HTML reports, daily weather information as observed in Central Park, organized by month. It denotes the daily high, low, and average temperature, as well as precipitation, wind, and other weather conditions.

The NWS collects these observations hourly, which would be more helpful for our purposes, but it only provides it in real time. Hourly historical data is only available from third-party providers which have it warehoused, all of whom charge a high premium for API access, so daily data will have to do.

## American Community Survey

https://data.cityofnewyork.us/City-Government/Demographic-Profiles-of-ACS-5-Year-Estimates-at-th/8cwr-7pqn

This data provides, in xlsx format, demographic information for each of New York City's Neighborhood Tabulation Areas, or NTA's. A whole bunch of information is provided, this repository only uses data on racial composition, average income, average age, and total population.

The TLC taxi zones are roughly based on these NTA's, but many NTA's are split into multiple TLC zones, especially in Manhattan, and one TLC zone(Zone 55, Coney Island) combines two NTA's. They're also encoded differently, and as far as I could find there isn't any published list matching the two to each other, so the conversions between them are done from comparisons made, by hand, by me, by looking at two side-by-side maps. I think it's all right, but it's always possible that I mistyped or misread something.

## 2010 Decennial Census

https://www1.nyc.gov/assets/planning/download/pdf/planning-level/nyc-population/census2010/t_pl_p5_nta.pdf

This data provides, in a pdf table, 2010 Census population data for each Neighborhood Tabulation Area. These population numbers are a bit older than the ones used by the American Communities Survey, but this table importantly provides acreage and density information, whereas the ACS data does not.