
FROM python:3.12.4-alpine

# Install Poetry
RUN pip install poetry

# Set environment variables for Poetry
ENV PATH=/usr/local/bin:$PATH
ENV POETRY_HOME=/root/.poetry

WORKDIR /app

# Copy everything into the container at container root
COPY . .

# Install the project dependencies using Poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction

# Expose the port the app runs on
EXPOSE 5001

# Run app.py when the container launches
CMD ["python", "main.py"]

