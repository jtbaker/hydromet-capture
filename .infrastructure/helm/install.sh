helm repo add prefect https://prefecthq.github.io/prefect-helm
helm search repo prefect # lists repos to install

helm install prefect-server prefect/prefect-server -f values.yaml
helm install prefect-worker prefect/prefect-worker -f values.yaml
