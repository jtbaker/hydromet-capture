FROM debian:stable-slim

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Download latest DuckDB CLI (adjust version as needed)
ENV DUCKDB_VERSION=1.3.1
RUN wget -O /usr/local/bin/duckdb "https://github.com/duckdb/duckdb/releases/download/v${DUCKDB_VERSION}/duckdb_cli-linux-amd64.zip" \
    && apt-get update && apt-get install -y unzip \
    && unzip /usr/local/bin/duckdb -d /usr/local/bin/ \
    && chmod +x /usr/local/bin/duckdb \
    && rm /usr/local/bin/duckdb

ENTRYPOINT ["duckdb", "-ui"]
