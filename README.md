The Data Engineering Project Series (DEPS) showcases my expertise in designing and implementing data solutions that address practical challenges. Each project demonstrates proficiency with different technologies and methodologies in the data engineering field, highlighting my ability to build production-ready data pipelines. These independent projects reflect my approach to solving data problems, from initial architecture design to successful implementation. They represent my technical capabilities and problem-solving skills in data engineering.

> [!NOTE]
> The projects in DEPS are demonstration assignments originally created for technical interviews, designed to showcase technical skills and problem-solving capabilities.

# DEPS_001: Data Ingest & Query Pipeline Using PySpark

## Summary

This application runs 2 spark jobs, Ingest and Export.\
**_Ingest job_** ingests data from `input_files` folder and convert them to parquet files.\
**_Export job_** queries the data prepared by ingest job to answer the following questions:

1. A filtered list of only active properties and their associated amenities.
2. A summary report of the number of properties that have a discovered date within a particular year and month.

There are 4 results created by this application:

* 2 folders of parquet files as a result of the ingest job.
* 1 line separated JSON file to answer export job # 1.
* 1 folder, which contains a csv file to answer export job # 2.

## Tools

* Docker
* Python
* Pyspark


> [!NOTE]  
> Run IngestJob first, then run ExportJob. 
> ExportJob is dependent on the success of the creation of parquet files from IngestJob.


## How To Run `IngestJob`

1. Make sure you are inside the `deps_001` directory.
2. Inside `Dockerfile`, make sure that the `CMD` (line 42) under `IngestJob` is uncommented.
3. Build the docker image by running `docker build -t ingest-job .` on terminal.
4. Run the docker container by running `docker run -v <local-path>:/deps_001 ingest-job` on terminal.
5. Check your local path. There should be 2 directories created called `properties_parquet_files` and 
`amenities_parquet_files`. All parquet files should be in there.

```
<local-path>     -> local directory that you want to sync with the container path.
/deps_001        -> container directory where the results should be. 

Example: 
`docker run -v /Users/Projects/deps_001:/deps_001 ingest-job`

Since the local path `/Users/Projects/deps_001` is bound to `/deps_001` container path where the results should be,
the results will be written to the local path.
```

## How To Run `ExportJob`

1. Make sure you are inside the `deps_001` directory.
2. Inside `Dockerfile`, make sure that the `CMD` (line 42) under `IngestJob` is commented
3. Inside `Dockerfile`, make sure that the `CMD` (line 47) under `ExportJob` is uncommented.
4. Build the docker image by running `docker build -t export-job .` on terminal.
5. Run the docker container by running `docker run -v <local-path>:/deps_001 export-job` on terminal.
6. Check your local path. There should be a file called `active_properties_and_amenities.json` and
a directory called `properties_count_by_date_report` and the csv file is inside of it.

- **_active_properties_and_amenities.json_** - contains a filtered list of ONLY active properties and their associated amenities.
- **_properties_count_by_date_report_** - contains a file, which is a summary report of the number of properties that have a discovered
date within a particular year and month. 
