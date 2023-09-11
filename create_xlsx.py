import os
import pandas as pd
from openpyxl import load_workbook


def create_asn_sheet(raw_data):  # raw_data is a list of dictionary
    # Check if the folder doesn't already exist
    if not os.path.exists('data'):
        # Create the folder
        os.makedirs('data')
    else:
        pass

    # Create an empty DataFrame
    df = pd.DataFrame()

    # Iterate through the dictionaries in the data list
    for item in raw_data:
        # Convert dictionary values to strings and join them with a separator
        item = {k: ', '.join(v) for k, v in item.items()}
        # Create a temporary DataFrame for each dictionary
        temp_df = pd.DataFrame(item, index=[0])
        # Append the temporary DataFrame to the main DataFrame
        df = df._append(temp_df, ignore_index=True)

    # Save the DataFrame to an XLSX file
    df.to_excel('data/ASN.xlsx', index=False)


def create_org_sheet(raw_data):  # raw_data is a list of dictionary
    # Check if the folder doesn't already exist
    if not os.path.exists('data'):
        # Create the folder
        os.makedirs('data')
    else:
        pass

    # Create an empty DataFrame
    df = pd.DataFrame()

    # Iterate through the dictionaries in the raw data list
    for item in raw_data:
        # Convert dictionary values to strings and join them with a separator
        item = {k: ', '.join(v) for k, v in item.items()}
        # Create a temporary DataFrame for each dictionary
        temp_df = pd.DataFrame(item, index=[0])
        # Append the temporary DataFrame to the main DataFrame
        df = df._append(temp_df, ignore_index=True)

    # Save the DataFrame to an XLSX file
    df.to_excel('data/Org.xlsx', index=False)


def create_poc_sheet(raw_data):  # raw_data is a list of dictionary
    # Check if the folder doesn't already exist
    if not os.path.exists('data'):
        # Create the folder
        os.makedirs('data')
    else:
        pass

    # Create an empty DataFrame
    df = pd.DataFrame()

    # Iterate through the dictionaries in the raw data list
    for item in raw_data:
        # Convert dictionary values to strings and join them with a separator
        item = {k: ', '.join(v) for k, v in item.items()}
        # Create a temporary DataFrame for each dictionary
        temp_df = pd.DataFrame(item, index=[0])
        # Append the temporary DataFrame to the main DataFrame
        df = df._append(temp_df, ignore_index=True)

    # Save the DataFrame to an XLSX file
    df.to_excel('data/POC.xlsx', index=False)


def create_net_resource_sheet(raw_data):  # raw_data is a list of dictionary
    # Check if the folder doesn't already exist
    if not os.path.exists('data'):
        # Create the folder
        os.makedirs('data')
    else:
        pass

    # Create an empty DataFrame
    df = pd.DataFrame()

    # Iterate through the dictionaries in the raw data list
    for item in raw_data:
        # Convert dictionary values to strings and join them with a separator
        item = {k: ', '.join(v) for k, v in item.items()}
        # Create a temporary DataFrame for each dictionary
        temp_df = pd.DataFrame(item, index=[0])
        # Append the temporary DataFrame to the main DataFrame
        df = df._append(temp_df, ignore_index=True)
    # Specify the output file name
    output_file = 'data/Net_resource.xlsx'

    # Write the DataFrame to the XLSX file
    df.to_excel(output_file, index=False)
