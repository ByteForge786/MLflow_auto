import os
import json
import mlflow.pyfunc
import requests

# Path to the config file
CONFIG_FILE = 'config.json'
# Parent folder where models will be saved
MODEL_PARENT_FOLDER = 'models'

def check_mlflow_alive(tracking_uri, username, password):
    try:
        response = requests.get(tracking_uri, auth=(username, password))
        if response.status_code == 200:
            print("MLflow is running and accessible.")
            return True
        else:
            print(f"MLflow is not accessible. Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"Failed to connect to MLflow: {e}")
        return False

def configure_aws(access_key_id, secret_access_key, s3_endpoint_url):
    os.environ['AWS_ACCESS_KEY_ID'] = access_key_id
    os.environ['AWS_SECRET_ACCESS_KEY'] = secret_access_key
    os.environ['MLFLOW_S3_ENDPOINT_URL'] = s3_endpoint_url

def load_and_save_model(model_uri, dest_folder):
    # Ensure the destination folder exists
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    
    model_name = model_uri.split('/')[-1]
    model_folder = os.path.join(dest_folder, model_name)
    if not os.path.exists(model_folder):
        os.makedirs(model_folder)
    
    try:
        model = mlflow.pyfunc.load_model(model_uri)
        mlflow.pyfunc.save_model(path=model_folder, python_model=model)
        print(f"Model saved in: {model_folder}")
    except Exception as e:
        print(f"Failed to load and save model from {model_uri}: {e}")

def main():
    # Load config
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)

    # Configure MLflow
    mlflow_config = config.get('mlflow', {})
    tracking_uri = mlflow_config.get('tracking_uri')
    username = mlflow_config.get('username')
    password = mlflow_config.get('password')

    # Configure AWS
    aws_config = config.get('aws', {})
    access_key_id = aws_config.get('access_key_id')
    secret_access_key = aws_config.get('secret_access_key')
    s3_endpoint_url = aws_config.get('s3_endpoint_url')

    # Set AWS environment variables
    configure_aws(access_key_id, secret_access_key, s3_endpoint_url)

    # Check if MLflow is alive
    if not check_mlflow_alive(tracking_uri, username, password):
        return

    # Load URIs from config file
    uris = config.get('model_uris', [])
    if not uris:
        print("No model URIs found in the config file.")
        return

    # Load and save each model
    for uri in uris:
        load_and_save_model(uri, MODEL_PARENT_FOLDER)

if __name__ == "__main__":
    main()
