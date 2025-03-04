
ARG UBUNTU_VER=18.04
ARG CONDA_VER=latest
ARG OS_TYPE=x86_64
ARG PY_VER=3.9
ARG PANDAS_VER=1.3

FROM ubuntu:${UBUNTU_VER}
# System packages 
RUN apt-get update && apt-get install -yq curl wget jq vim

# Use the above args 
ARG CONDA_VER
ARG OS_TYPE
# Install miniconda to /miniconda
RUN curl -LO "http://repo.continuum.io/miniconda/Miniconda3-${CONDA_VER}-Linux-${OS_TYPE}.sh"
RUN bash Miniconda3-${CONDA_VER}-Linux-${OS_TYPE}.sh -p /miniconda -b
RUN rm Miniconda3-${CONDA_VER}-Linux-${OS_TYPE}.sh
ENV PATH=/miniconda/bin:${PATH}
RUN conda update -y conda
RUN conda init

ARG PY_VER
ARG PANDAS_VER
# Install pyspark & related packages from conda 
RUN conda install openjdk -y
RUN conda install pyspark -y
RUN conda install -c conda-forge findspark -y

# Copy necessary files and change working dir
RUN mkdir deps_001
WORKDIR /deps_001
COPY input_files/ ./input_files/
COPY src/ ./src/
COPY main.py .
COPY run_scripts.sh .


##| ############
##| Ingest jobs
##| ############
CMD ["sh", "-c", "python main.py -j IngestJob -ind /deps_001/input_files/properties.json -outd /deps_001/properties_parquet_files && python main.py -j IngestJob -ind /deps_001/input_files/amenities.txt -outd /deps_001/amenities_parquet_files"]

##| ############
##| Export jobs
##| ############
# CMD ["python", "main.py", "-j", "ExportJob", "-ind", "/deps_001", "-outd", "/deps_001"]
