# make sure that you have PREFECT_API_URL set in your environment before running the upgrade command.
envsubst < values.yaml | helm upgrade mychart -f -
