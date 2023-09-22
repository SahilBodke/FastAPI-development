FROM python:3.11.5 

WORKDIR /usr/src/app 

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . . 

# Same as running uvicorn app.main:app --host 0.0.0. --port 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]  