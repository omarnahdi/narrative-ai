# --------------------------------------------------------------------------------
# STAGE 1: Builder (Compiling dependencies)
# --------------------------------------------------------------------------------
FROM python:3.11-slim as builder

# Install build tools.
# - git: required for your 'git+' dependency in requirements.txt
# - g++, make, cmake, libcurl4-openssl-dev: required to compile 'awslambdaric'
RUN apt-get update && apt-get install -y \
    git \
    g++ \
    make \
    cmake \
    unzip \
    libcurl4-openssl-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

COPY requirements.txt .

# Install dependencies into a specific target folder.
# We must install 'awslambdaric' manually for custom images.
RUN pip install --target /build/dependencies --no-cache-dir \
    awslambdaric \
    -r requirements.txt

# --------------------------------------------------------------------------------
# STAGE 2: Final Runtime (The actual lightweight image)
# --------------------------------------------------------------------------------
FROM python:3.11-slim

# Install ONLY the runtime libraries needed by awslambdaric.
# Without 'libcurl4' and 'libstdc++6', the container will crash with "InvalidImage".
RUN apt-get update && apt-get install -y \
    libcurl4 \
    libstdc++6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /var/task

# 1. Copy the compiled dependencies from the builder stage
COPY --from=builder /build/dependencies /var/task

# 2. Copy your specific application files
COPY narrativeai_run.py .
COPY instructions.py .
COPY fix_brave_tool.py .
COPY JinaToolAsync.py .
COPY agent_team.py .
COPY structured_models.py .

# 3. Set the Entrypoint to the Lambda Runtime Interface Client
ENTRYPOINT [ "python", "-m", "awslambdaric" ]

# 4. Set the CMD to your specific handler
CMD [ "narrativeai_run.handler" ]