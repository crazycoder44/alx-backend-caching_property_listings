# Use official Python image
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

# system deps for psycopg2
RUN apt-get update && apt-get install -y build-essential libpq-dev gcc && apt-get clean

COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /code/

# collectstatic if you want (disabled by default)
# CMD ["gunicorn", "alx-backend-caching_property_listings.wsgi:application", "--bind", "0.0.0.0:8000"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# For development you can override entrypoint to run manage.py runserver
