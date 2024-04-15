from python:3.9
WORKDIR /app1
COPY diabetes_prediction.py /app1/
COPY model.pkl /app1/
COPY diabetes_Dataset.csv /app1/
RUN pip install numpy matplotlib seaborn scikit-learn pandas
CMD ["python", "diabetes_prediction.py", "model.pickle","diabetes_Dataset.csv"]
