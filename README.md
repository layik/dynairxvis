# DynAIRxVIS

Python package for DynAIRx visualization.

The package is designed to visualize the results of the DynAIRx first design study into charts to support Structured Medication Review (SMR) in primary care. The first evaluation confirmed the effectiveness of 11 out 14 charts.

## Installation

```bash
# once published on pypi
pip install dynairxvis
# development version
# pip install git+githubURL
```
# Use
Hypothetical dataframe (notice blood_pressure is there just for WIP work)
```py
import pandas as pd
df = pd.DataFrame({
    'Blood_Pressure': [120, 130, 125, 140, 140],
    'Condition': ['Diabetes', 'Hypertension', 'Asthma', 'COPD', 'Asthma'],
    'Start_Date': pd.to_datetime(['2021-01-01', '2021-01-02', '2021-01-03', '2021-01-06', '2022-01-06']),
    'End_Date': pd.to_datetime(['2021-06-01', '2021-02-02', '2021-08-03', '2021-10-04', '2022-06-06']),
    'Pain_Scale': pd.Categorical(['low', 'high', 'medium', 'extreme', 'high'], ordered=True)
})
```

Then when looking at NTO, we can do
```py
# the package will check the given column types and should find
# NOT (Nominal, Ordinal and Temporal) sequence within the columns
# print(df.columns)
plot_charts(df, column_refs=['Start_Date', 'End_Date', 'Pain_Scale', 'Condition'])
```
One of the charts will be this:

![image](https://github.com/user-attachments/assets/e518bdc9-6889-4b15-8dbc-eeba194a682a)

See more details of this in the 'getting_started.ipynb' notebook.

## Notebooks
The package includes a Jupyter notebook called 'getting_started.ipynb' that demonstrates how to use the package. It also shows the six different category of data combinations used in the design study evaluation.

## Tests
To run the tests, run the following command:

```bash
python -m pytest
```

## Acknowledgements
