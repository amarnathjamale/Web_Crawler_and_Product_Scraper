# Use an official Python runtime as the base image
FROM python:3

# Install git to clone the repo
RUN apt-get update && apt-get install -y git

# Set the working directory
WORKDIR /app

# Clone the repository from GitHub
RUN git clone https://github.com/amarnathjamale/Web_Crawler_and_Product_Scraper.git .

# Install required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that Flask will run on
EXPOSE 5000


# Run the Flask application
CMD ["python", "/app/server.py"]
