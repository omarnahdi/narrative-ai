# Start with the OFFICIAL AWS base image for Python 3.11 on Lambda.
# This image is guaranteed to be supported and includes the Lambda Runtime Interface Client.
FROM public.ecr.aws/lambda/python:3.11

RUN dnf install -y git

# Set the working directory for our application.
WORKDIR /var/task

# Copy the Python requirements file into the container.
COPY requirements.txt .

# Install the Python dependencies.
# Using --no-cache-dir reduces the size of the final image.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container.
COPY narrativeai_run.py .
COPY instructions.py .
COPY fix_brave_tool.py .
COPY JinaToolAsync.py .
COPY agent_team.py .
COPY structured_models.py .

# Set the CMD to our application's handler.
# The AWS base image provides the correct ENTRYPOINT automatically,
# which will execute this command.
CMD [ "narrativeai_run.handler" ]