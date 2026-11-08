# Theres this thing called cache that will skip if nothing changes so for example 
# that python and workdir since it will always be like that skip that all on second build onwards

# Official python image from dockerhub. If your not using python. For example java you can use openjdk:17-jdk-slim or node:18-slim etc.
FROM python:3.10-slim 

# Set the working directory inside the container and only run commands there
WORKDIR /app

# Installing dependencies required for building python packages
# This is the foundation, compiler. You will see the error when you build the docker file
RUN apt-get update && apt-get install -y \ 
    gcc \ 
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# After the foundation is done copy all of the dependencies that are on requirement.txt then install all of the things that are in there?
COPY requirement.txt .
# --no-cache-dir after the container is close throw all the temporary stuff away
RUN pip install --no-cache-dir -r requirement.txt

# Copy the application code into the container
COPY . .

# # Expose the port your Flask app runs on
EXPOSE 5000

# Command to run application using Python
CMD ["python", "main.py"]