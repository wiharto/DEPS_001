
import json


"""
Job: 
* Create a temp view of properties and amenities from parquet files.
* Run the supplied SQL query to generate results.
Output: a JSON file, which contains a list of ONLY active properties and their associated amenities.
"""
def active_properties_and_amenities(spark_session, input_dir, output_dir):
    print("Starting active_properties_and_amenities job")
    # Create temp views for tables needed
    spark_session.read.parquet(f"{input_dir}/properties_parquet_files").createOrReplaceTempView("properties_view")
    spark_session.read.parquet(f"{input_dir}/amenities_parquet_files").createOrReplaceTempView("amenities_view")

    query = """
        SELECT 
            properties_view.property_id,
            amenities_view.amenity_id 
        FROM properties_view JOIN amenities_view 
            ON properties_view.property_id = amenities_view.property_id
        WHERE properties_view.active = True
    """

    results_df = spark_session.sql(query)
    df_json = results_df.toJSON() # json string
    # convert string pipe delimited to a list and write output to json file
    with open(f'{output_dir}/active_properties_and_amenities.json', 'w') as file:
        for row in df_json.collect():
            line = json.loads(row) # converts to dict for easier transformation
            line["amenity_id"] = line["amenity_id"].split("|")
            file.write(f"\n{str(line)}")
    file.close()


"""
Job: 
* Create a temp view of properties and amenities from parquet files.
* Run the supplied SQL query to generate results.
Output: a folder with a CSV file containing number of properties grouped by year and month.
"""
def total_properties_with_discovered_date(spark_session, input_dir, output_dir):
    print("Starting total_properties_with_discovered_date job")
    # Create temp views for tables needed
    spark_session.read.parquet(f"{input_dir}/properties_parquet_files").createOrReplaceTempView("properties_view")

    query = """
        SELECT 
            YEAR(discovered_dt) as year, 
            MONTH(discovered_dt) as month, 
            count(*) as num_of_properties
        FROM properties_view 
        GROUP BY year, month 
        ORDER BY year, month
    """

    results_df = spark_session.sql(query)
    results_df.write.options(header='True').csv(f"{output_dir}/properties_count_by_date_report")


"""
Job: calls 2 functions above.
Output: None. Error otherwise.
"""
def export_job(spark_session, input_dir, output_dir):
    print("Starting Export Job")
    # Create JSON report only for active properties and their amenities
    try:
        active_properties_and_amenities(spark_session, input_dir, output_dir)
    except Exception as e:
        print(e)
    # Create csv file for count of properties within certain year and month
    try:
        total_properties_with_discovered_date(spark_session, input_dir, output_dir)
    except Exception as e:
        print(e)

