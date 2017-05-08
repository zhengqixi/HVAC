# Cooper Union Energy Data Visualization

## Description

Visualize Cooper Union energy data with Highcharts.

## Background

This application is currently under development for our ME452 HVAC course. Developed by [Zhengqi Xi](https://github.com/zhengqixi) and [Ryan Yun](https://github.com/ryanyun).

## API

Base URL
`energy.cooper.edu/analytics/engine`

after that...

### `/metadata`
gets all of the metadata, such as which distribution boards are on which utility, etc...

### `/standard/<query>`
a standard request...i.e not night and day.

- if `<query>` is 'total_usage', then total usage data will be returned.
- if `<query>` is 'utility_comparison', then utility comparison data will be returned
- if `<query>` is a distribution board, then data for the distribution board will be returned

the API expects `start` and `end` to be present. `start` and `end` are the start and end times of the data being queried.
`start` and `end` are milliseconds from the UNIX Epoch time.

example:
`/standard/utility_comparison?start=1448946000000&end=1449946000000`

### `/night_day/<query>`
the night and day split request

largely the same requirements as `/standard/`, except the JSON returned will contain a field for the offpeak times and another
for the onpeak times.

In addition, two additional arguments must be provided:
`peak_start` and `peak_end`, which are the start and end times of peak hour, respectively
They must follow the following format: HH:MM in military time