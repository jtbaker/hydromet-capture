# Use a slim Python base image
FROM python:3.13-slim-bookworm AS base

# Builder stage: install uv and dependencies
FROM base AS builder

# Copy uv binary from the official image (fast, no extra install steps)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Optional: set env vars for uv performance and reproducibility
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

WORKDIR /app

# Copy only dependency files first for better build caching
COPY uv.lock pyproject.toml /app/

# Install dependencies into a virtual environment, no dev packages
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# Copy the rest of the application code
COPY . /app

# Install the project itself (non-editable, for production)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Final stage: minimal runtime image
FROM base

# Copy the virtual environment and app code from builder
COPY --from=builder /app /app
ENV PATH="/app/.venv/bin:$PATH"
WORKDIR /app
# Activate the venv in PATH
ENV PATH="/app/.venv/bin:$PATH"
