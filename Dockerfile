FROM python:2.7
WORKDIR /app
COPY . .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["python", "sudoku.py"]