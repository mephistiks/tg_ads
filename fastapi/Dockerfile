FROM python:3.10
ADD .. /code
WORKDIR /code
RUN pip install -r r.txt
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]