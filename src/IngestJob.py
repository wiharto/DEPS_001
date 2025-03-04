
from pyspark.sql.types import StructType, StructField
from pyspark.sql.types import BooleanType, DateType, IntegerType, StringType


"""
Job: convert properties.json to a parquet file.
Output: a parquet folder called properties_parquet_files with parquet files in it.
"""
def json_to_parquet(spark_session, input_dir, output_dir):
    print("Starting json_to_parquet job")
    schema = StructType([
        StructField("active",BooleanType(),True),
        StructField("discovered_dt",DateType(),True),
        StructField("property_id",IntegerType(),True)
        ])
    # read file
    try:
        df = spark_session.read.schema(schema).json(f"{input_dir}")
    except Exception as e:
        print(e)
    # write to parquet
    try:
        df.write.parquet(f"{output_dir}")
    except Exception as e:
        print(e)


"""
Job: convert amenities.txt to parquet file.
Output: a folder called amenities_parquet_files with parquet files in it.
"""
def txt_to_parquet(spark_session, input_dir, output_dir):
    print("Starting txt_to_parquet job")
    schema = StructType([
        StructField("property_id",IntegerType(),True),
        StructField("amenity_id",StringType(),True)
        ])
    # read file
    try:
        df = spark_session.read.schema(schema).option("header", "false").option("sep", " ").csv(f"{input_dir}")
    except Exception as e:
        print(e)
    # write to parquet
    try:
        df.write.parquet(f"{output_dir}")
    except Exception as e:
        print(e)


"""
Job: determines if a properties.json or amenities.txt needs to be parsed.
Output: None. Error if file extension isn't recognized.
"""
def ingest_job(spark_session, input_dir, output_dir):
    print("Starting Ingest Job. Checking file extension")
    # Get file extension to determine which file to convert to parquet
    ext = input_dir.split(".")[1]

    if ext == "json":
        try:
            json_to_parquet(spark_session, input_dir, output_dir)
        except Exception as e:
            print(e)
    elif ext == "txt":
        try:
            txt_to_parquet(spark_session, input_dir, output_dir)
        except Exception as e:
            print(e)
    else:
        print("Unidentified file extension")
