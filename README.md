What I plan to do:

Validate entries against payment type, zones 264/265, out-of-bounds data, zero distance, same zone

.describe() each month for passenger count, trip distance, pickup/dropoff datetime normalized for Jan 1st 2000, money amounts(nullify tip where payment type is cash)

Predict fare amount/number of available fares based on
    Pickup zone
        Will use tabular proxy quantities
            Population/population density
            Average income
            Demographic composition
            Density/proximity of subway stops
    Time of day
    Day of week
    Day of year(Holidays)
    Weather

Ideally, predictions could be made probabilistically, but this seems to be impractical

Create some kind of web interface with an interactive map

---

Datasets

TLC trip record data - https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page

This data provides records, in csv format, of every taxi trip taken in New York City, organized by month. It denotes where each trip starts and ends, in the form of one of the 263 zones it splits the city into. It also provides other metadata, including the start and end time of the trip, the distance travelled, and the amount and type of payment.

The analyses in this repository use data from both yellow taxis, which operate throughout the city, and green taxis, which are specifically forbidden from picking up passengers in Manhattan below West 110th Street or East 96th Street. Data is also available for for-hire vehicles(IE Uber, Lyft, black car services), but it is significantly larger, less detailed, and likely less reliable, so it is not used here.

NWS Central Park Observation Station - https://w2.weather.gov/climate/index.php?wfo=okx (Preliminary Monthly Climate Data)

This data provides, in the form of written HTML reports, daily weather information as observed in Central Park, organized by month. It denotes the daily high, low, and average temperature, as well as precipitation, wind, and other weather conditions.

The NWS collects these observations hourly, which would be more helpful for our purposes, but it only provides it in real time. Hourly historical data is only available from third-party providers which have it warehoused, all of whom charge a high premium for API access, so daily data will have to do.