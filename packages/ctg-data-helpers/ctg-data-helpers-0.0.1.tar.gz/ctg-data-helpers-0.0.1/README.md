# CTG-Data-Helpers
This directory contains modules we developed to help with data processing, downloading and ingesting. 

Required dependencies:
- `logging`
- `os`
- `pathlib`
- `hashlib`
- `pkgutil`
- `io`
- `zipfile`
- `tempfile`
- `pandas`
- `requests`
- `sqlalchemy`
- `psycopg2-binary`

## Download Functions
The first set of functions in the module assist with downloading data

`get_path()` - A string representing the path to the file or directory. If a path is provided, will return that path. If a path is not provided, will provide a new path based on a temp directory and the hash of the URL.

`make_path()` - If a path doesn't exist, `get_path()` internally calls this function to build a new path. (Essentially a wrapper function around `os.mkdir` to catch errors)

`hash_url()` - Hashes the given download URL to help build the temp path if none has been given. 

`pure_download()` - Downloads the data from the URL with the capacity to handle zip files if specified. 

`download_data_cache()` - Checks before calling `pure_download()` to see if the data has previously been downloaded. If the data is already in the cache, the function just returns the path to that data, without downloading it a second time. 

## Pandas Functions
The second set of functions in the module assist with setting up the data in Pandas DataFrames for easier processing

`setup_df()` - Given a set of specified parameters, this function ingests the CSV to a DataFrame. Note: `**cli_options` is integrated with our click-based command-line-interfaces. 


## PostgreSQL Functions
These functions help with setting up the database, confirming a successful upload, and uploading the data itself

`get_engine()` - Given the set environmental variables, returns an engine to connect to the database. 

`confirm_table()` - After data has been ingested, confirms that the data was successfully uploaded to the database. 

`upload_data()` - Uploads the data of a specific DataFrame to the database given some predetermined variables

`has_primary_key()` - Checks to see if an existing table has a primary key

`set_primary_keys()` - Given a table name and a list of columns for a primary key, this function creates the primary key. 

## Extension Functions
`build_plugins_map()` - This function helps dynamically build a plugin map when using this code in a command-line environment
