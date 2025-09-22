# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file into the container at /code
COPY ./requirements.txt /code/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the rest of the application's code into the container
COPY ./app /code/app
COPY ./data /code/data
COPY ./scripts /code/scripts

# Run the seeding script to initialize the vector database
RUN --mount=type=secret,id=openai_api_key \
    export OPENAI_API_KEY=$(grep OPENAI_API_KEY /run/secrets/openai_api_key | cut -d '=' -f2 | tr -d '"') && \
    python scripts/seed_vector_db.py

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run uvicorn server
# The --host 0.0.0.0 is crucial for Docker to expose the port correctly
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]