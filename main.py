
import argparse
from src.IngestJob import ingest_job
from src.ExportJob import *
from pyspark.sql import SparkSession


"""
This is the application entry point.
The decision whether an IngestJob or an ExportJob should be performed is decided here.
SparkSession also created here, and passed to other functions.
"""
if __name__ == "__main__":
    # Get args from command line
    parser = argparse.ArgumentParser()
    parser.add_argument("--job_name", "-j", required=True)
    parser.add_argument("--input_dir", "-ind", required=True)
    parser.add_argument("--output_dir", "-outd", required=True)
    args = parser.parse_args()

    # Create SparkSession
    spark = SparkSession.builder.appName(args.job_name).getOrCreate()

    # determine if args.job_name == IngestJob or ExportJob
    if args.job_name == "IngestJob":
        try:
            ingest_job(spark, args.input_dir, args.output_dir)
        except Exception as e:
            print(e)
    elif args.job_name == "ExportJob":
        try:
            export_job(spark, args.input_dir, args.output_dir)
        except Exception as e:
            print(e)

    # Close SparkSession
    spark.stop()

