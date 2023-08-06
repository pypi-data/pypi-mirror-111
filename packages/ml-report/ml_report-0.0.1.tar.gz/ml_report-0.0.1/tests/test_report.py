from sklearn.datasets import load_iris

from ml_report import Report


ds = load_iris(as_frame=True)
df = ds["data"]
print(df)

report = Report(

)
