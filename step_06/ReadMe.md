# Caching

Caching is an important feature of Taipy. Tasks can be skipped if input Data Nodes of tasks have changed or not. If none of the input Data Nodes have been changed after a first submission, tasks will be skipped. Time and ressources are saved thanks to this mechanism.

```python
def filter_by_month(df, month):
    df['Date'] = pd.to_datetime(df['Date']) 
    df = df[df['Date'].dt.month == month]
    return df

def count_values(df):
    return len(df)
```
