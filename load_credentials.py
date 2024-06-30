#%%

import yaml

def load_credentials(file_path='credentials.yaml'):
    """
    Load the database credentials from a YAML file and return as a dictionary.

    Parameters:
    file_path (str): The path to the YAML file. Default is 'credentials.yaml'.

    Returns:
    dict: The database credentials.
    """
    with open(file_path, 'r') as file:
        credentials = yaml.safe_load(file)
    return credentials

# Example usage
if __name__ == "__main__":
    credentials = load_credentials()
    print(credentials)
