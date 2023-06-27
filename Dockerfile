# import python image version 3.8
FROM python:3.8

# set working directory
WORKDIR /app

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies from requirements.txt 
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -U numpy

# copy the content of the local directory to the working directory
# COPY /chatgpt3 ./chatgpt3
COPY .env .
COPY .env.example .
COPY main.py .
COPY helpers.py .
COPY google-sheet-credentials.json .

# command to run on container start
CMD ["python", "-u", "main.py"]
