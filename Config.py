{
    "model_uris": [
        "runs:/<run_id1>/model",
        "models:/<model_name1>/<model_version1>",
        "s3://my_bucket/path/to/model1",
        "runs:/<run_id2>/model",
        "models:/<model_name2>/<model_version2>",
        "s3://my_bucket/path/to/model2"
    ],
    "mlflow": {
        "tracking_uri": "<mlflow_tracking_url>",
        "username": "<mlflow_username>",
        "password": "<mlflow_password>"
    },
    "aws": {
        "access_key_id": "<aws_access_key_id>",
        "secret_access_key": "<aws_secret_access_key>",
        "s3_bucket": "<mlflow_s3_bucket>",
        "s3_endpoint_url": "<mlflow_s3_endpoint_url>"
    }
}
