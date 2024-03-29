# Data Engineering Zoomcamp 2024 Project

## Overview

This repository contains the source code and documentation for the [Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp)'s project for 2024.

<br>

## Goal

The goal of this project is to create a solution which consists an end-to-end data ingestion, processing, persistence and visualization pipeline.

<br>

## Data Source

**National Weather Service**'s [API Web Service](https://www.weather.gov/documentation/services-web-api#/default/radar_station) provides various APIs where we can use to collect real time weather data.

A list of office ids were previously obtained and hard-coded in the data collection Python script (see [weather_data_load.py](./src/weather_data_loader.py))

For each office, we retrieve a list of weather station ids and for each station the Python script makes an API call to obtain current weather data.

<br>

## Data Collection

Instead of using existing historical data, this project is going to collect data on an hourly basis and build a batch processing pipeline to process them on a daily basis. At the end, data is presented in dashboards built by Google Cloud's Looker Studio.



<br>

## Data Visualization

The final result is a **Weather Reports** Looker report.

The first page shows the summary statistics. User can select either or both **Station ID** and **Date**.

The first dashboard shows the number of records collected for the selected station and date.

The second dashboard shows the lowest, average and highest temperature for the selected station and date.

<br>

![data visualization 01](./docs/data_visualization_01.png)

<br>

Second page shows the time series temperate data for the selected station and the date range.

<br>


![data visualization 02](./docs/data_visualization_02.png)

<br>


## Data Flow

<br>

![data flow](./docs/data_flow.svg)

<br>

## Data Pipelines

<br>

[data pipelines](./docs/pipeline.md)

<br>



## Prerequisites

Before we can execute the pipeline, we would first provision the infrastructure.

**Infrastructure Provisioning**

This includes building Cloud Storage bucket and BigQuery dataset using Terraform.


[infrastructure](./docs/infra.md)


**Docker Container Creation**

This includes building local Mage image as well as running Mage and Postgres containers.


[mage](./docs/mage.md)



## Lessons Learned

- Backfill is an important part of the design. Have to take this into consideration when designing the pipeline.
- Deciding on data visualization earlier helps narrowing down the scope and the kind of processing needed for the pipeline. Working backward from the target end state is a useful way to keep things in check.
- Documentation would probably takes as much time as development.


<br>
