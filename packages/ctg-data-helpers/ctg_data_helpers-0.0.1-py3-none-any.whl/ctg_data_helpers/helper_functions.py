# Helper functions to streamline tasks in other files

import logging
import os
from pathlib import Path
import hashlib
import re
from io import BytesIO
import zipfile
import tempfile
import pkgutil
import pandas as pd
from requests import get
import sqlalchemy as db
from sqlalchemy import create_engine, select, func

# # # # # #  DOWNLOAD FUNCTIONS # # # # # #
# These functions assist with the downloading and caching of data from a URL
# into a directory on the user's local machine.


# Get path - a string representing the path to the file or directory
# If a path is provided, will return that path
# If a path is not provided, will provide a new path based on a temp
# directory and the hash of the URL.
def get_path(url, zipped, path=None):
    '''get path - returns path'''
    # If the user has provided a path, or has set one as an environment variable use that,
    # otherwise default to platform's temp folder
    parent_dir = path or os.environ.get("DOWNLOAD_FOLDER", tempfile.gettempdir())

    hex_url = hash_url(url)

    if zipped:

        # Create a path with the hash as the name as a subdirectory of the desired folder
        # download_path = os.path.join(parent_dir, hex_url)

        download_path = f"{parent_dir}/{hex_url}"
    else:
        download_path = f"{parent_dir}/file_{hex_url}"

    return download_path


# Make Path - if path doesn't exist, make it.
# Effectively a wrapper function to catch errors for os.mkdir
def make_path(download_path):
    # Creating the directory
    try:
        os.mkdir(download_path)
    except OSError as error:
        logging.error(error)

    # Returning the path to the directory
    return download_path


def hash_url(url):
    '''Hash the url'''
    # Convert the URL string into bytes for the hashing function
    byte_url = url.encode('utf-8')

    # Running through the SHA1 Hash
    hash_object = hashlib.sha1(byte_url)
    hex_url = hash_object.hexdigest()
    logging.debug(hex_url)
    return hex_url

def pure_download(url, zipped, download_path=None):
    '''This function downloads the data'''
    # Make a request of the URL
    request = get(url)

    logging.debug(f"IN PURE DOWNLOAD: Is zipped is {zipped}")

    if not download_path:
        download_path = get_path(url, zipped, download_path)

    # If the downloaded directory needs to be unzipped, open using zipfile
    if zipped:

        # Creating the directory
        try:
            os.mkdir(download_path)
        except OSError as error:
            logging.error(error)

        # Unzip the file and extract all to the desired download_path directory
        with zipfile.ZipFile(BytesIO(request.content), "r") as zip_ref:

            zip_ref.extractall(download_path)
            logging.debug("DIRECTORY SUCCESSFULLY UNZIPPED AND DOWNLOADED")

    # If the downloaded directory does not need to be unzipped, open
    # without use of the zipfile module
    else:

        logging.debug(f"Download path is {download_path}")

        # Write contents to the file
        with open(download_path, 'wb') as file:
            logging.debug("Writing to file")
            file.write(request.content)

    # Return a string of the path to the new directory
    return str(download_path)


def download_data_cache(url, zipped, path=None):
    ''' Upon receiving a URL of a zipped directory, this function
    unzips the directory, and saves all of the files to the desired directory
    under a sub-directory which has the name of the SHA1 hash. If no directory is given,
    the download will occur in a temp directory.
    This function returns the path to the directory with the downloaded files.

    When unzip=True, the function expects a zipped directory and unzips it, extracting
    all of the files to the given directory. When unzip=False, the function expects a
    single file to download. It saves the data in a file named file_<SHA1> (where
    <SHA1> is the unique Hash, and the name of the parent directory.'''
    logging.debug("Called cache function - yes")
    # Setting logging to print debug statements
    logging.basicConfig(level=logging.DEBUG)

    download_path = get_path(url, zipped, path)

    logging.debug(f"zipped is {zipped}")

    # If the path already exists, return the string path to the user
    # and log that the files have already been downloaded
    if os.path.exists(download_path):
        logging.debug("This directory has already been recently downloaded")

    else:
        # If the path does not already exist, create a directory using the desired
        # path, and then download the files.
        # returns the path
        logging.debug("Code realizes it has not been downloaded yet")

        # Download the files
        if zipped:
            download_path = make_path(download_path)
            pure_download(url, True, download_path)
        else:
            logging.debug("Sending info to pure_download()")
            pure_download(url, False, download_path)
    return str(download_path)


# # # # # #  PANDAS FUNCTIONS # # # # # #
# These functions help with setting up the Pandas dataframe, with whatever
# encodings or other conversions that need to happen

# This function takes the path, and the click parameters, and reads
# the file from CSV to a DataFrame, returning the DataFrame

def setup_df(file_name, is_directory=False, converter_dict=None, encoding=None, usecols=None, **cli_options):
    '''This function takes the path, and the click parameters, and reads
    the file from CSV to a DataFrame, returning the DataFrame'''
    if cli_options:
        zipped = cli_options["zipped"]
        url = cli_options["url"]
        force = cli_options["force"]
    # else:
    #     logging.error("""MISSING PARAM. \nPlease pass in a dict containing the values for force, zipped and the string of the URl.
    #                      EXAMPLE: cli_options={"force":True, "zipped":True, "url":"www.mydata.org"}\n
    #                        Force --> determines whether or not the program should check the cache first
    #                        Zipped --> determines whether or not the URL download should be treated as a zip file or not
    #                        URL --> the URL link""")
    #     return


    if force:
        # If asking to re-download regardless of cache
        path = pure_download(url, zipped)
    else:
        # if looking at cache first.
        path = download_data_cache(url, zipped)

    logging.debug(f"Path to downloaded files is: {path}")

    # Using PANDAS to load a CSV as a DataFrame - select the csv you want from the directory
    if is_directory:
        path = os.path.join(path, file_name)

    df = pd.read_csv(path, converters=converter_dict, encoding=encoding, usecols=usecols)

    logging.debug(f"Ingested {file_name} to the dataframe")

    return df


# # # # # #  POSTGRESQL DATABASE FUNCTIONS # # # # # #
# These functions help with setting up the database, confirming a successful
# upload, and uploading the data itself

# Sets up the Postgres connection and returns the DB engine
def get_engine(default_db_name):
    # Getting the environmental variables and setting them as strings to concatenate
    # into our DB request
    user = os.environ.get("POSTGRES_USER", "postgres")
    pwd = os.environ.get("POSTGRES_PASSWORD", "")
    host = os.environ.get("DB_HOST", "localhost")
    port = os.environ.get("POSTGRES_PORT", 5432)
    db_name = os.environ.get("POSTGRES_DB", default_db_name)

    # URI for SQLAlchemy Engine
    uri = "postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{db_name}".format(
        user=user,
        pwd=pwd,
        host=host,
        port=port,
        db_name=db_name)

    logging.debug(f"URI is: {uri}")

    # Creating the postgres DB connection using SQLAlchemy
    # NOTE: To see all of the INSERT statements printed as they happen,
    # pass "True" to the echo parameter.
    engine = create_engine(uri, echo=False, executemany_mode='batch')

    return engine


def confirm_table(table_name, engine):
    """This function confirms that a table has been made in the DB, and returns a log
    of the count of rows added to the database. Using SQLAlchemy to load the table"""
    my_table = db.Table(table_name, db.MetaData(), autoload_with=engine)

    # Running a SELECT count(*) FROM table_name, and saving the results to query
    query = select([func.count()]).select_from(my_table)

    # Fetching all of the rows
    result, = engine.execute(query).fetchone()

    # Logging the result of the fetchall() to screen
    logging.debug(f"Loaded {result} rows to the database successfully")


def upload_data(df, name, data_type_dict, drop):
    # Calling the helper function to set up the database which returns an engine
    engine = get_engine()

    # Setting up the table for the Pandas .to_sql() method
    table_name = name

    # Converting the DataFrame to the DB
    df.to_sql(
        table_name,
        engine,
        if_exists='replace' if drop else 'append',
        index=False,
        chunksize=5000,
        dtype=data_type_dict
    )

    # Check to confirm table was loaded
    confirm_table(table_name, engine)


# Checks if there are any primary keys so far for this table
def has_primary_key(table_name, default_db_name):

    # Calling the helper function to set up the database which returns an engine
    engine = get_engine(default_db_name)

    query = f"""
            SELECT c.column_name
            FROM information_schema.key_column_usage AS c
            LEFT JOIN information_schema.table_constraints AS t
            ON t.constraint_name = c.constraint_name
            WHERE t.table_name = '{table_name}' AND t.constraint_type = 'PRIMARY KEY';
    """

    # Fetching all of the rows
    result = engine.execute(query).fetchone()

    return bool(result)


# Function to set primary keys
def set_primary_keys(table_name, col_list):

    has_pk = has_primary_key(table_name)

    if has_pk:
        logging.debug("Already has a primary key set.")
        return

    # Calling the helper function to set up the database which returns an engine
    engine = get_engine()

    col_list_strs = ", ".join(col_list)

    # Running a ALTER TABLE to set an existing column as a primary key
    query = f"""
        ALTER TABLE {table_name} 
        ADD PRIMARY KEY ({col_list_strs});"""

    # Running
    engine.execute(query)


# # # # # # EXTENSION FUNCTIONS # # # # # #
def build_plugins_map(plugins_dir):
    plugin_map = {}

    # Walk the directory of plugins
    for loader, name, _ in pkgutil.walk_packages([plugins_dir]):

        # Load each module
        module = loader.find_module(name).load_module(name)

        # If it has a registration_info() method
        if hasattr(module, "registration_info"):

            # Call the method, and save the dict returned
            data = module.registration_info()

            # Retrieve the name and entrypoint
            name = data["name"]
            function = data["entrypoint"]

            # Save them to an internal dict we will return
            plugin_map[name] = function

    return plugin_map
