# DynAIRxVIS

Python package for DynAIRx visualization. The package uses `matplotlib` to generate static charts.

The package is designed to visualise the results of the DynAIRx first design study into charts to support Structured Medication Review (SMR) in primary care. The first evaluation confirmed the effectiveness of 11 out 14 charts. These were the charts used for each of the six categories of data combinations:
- Nominal (N)
- Quantitative (Q)
- Nominal, Quantitative (NQ)
- Nominal, Temporal (NT)
- Nominal, Quantitative, Temporal (NQT)
- Nominal, Temporal, Ordinal (NTO)

See the table below for how these data types are used within the design study.

## Installation

```bash
# once published on pypi (WIP)
pip install dynairxvis
# development version
# pip install git+githubURL
```
# Use
The package can be used for "quality" charts for any of the above data type combinations. Hypothetical dataframe (notice blood_pressure is there just for WIP work) and your data could be for anything with same data types.

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
# NOT (Nominal, Temporal and Ordinal) sequence within the columns
# print(df.columns)
plot_charts(df, column_refs=['Start_Date', 'End_Date', 'Pain_Scale', 'Condition'])
```
The `plot_charts` function will plot the charts for the given data. It does so by checking the data types of the columns and then plotting the appropriate charts. One of the charts will be this:

![image](https://github.com/user-attachments/assets/6f6e43c2-df39-4c1e-8738-f98a5e7e94b0)

Another example is when looking at NQT and we use the Q column as the value to change
the height of the Gantt bars.
```py
plot_charts(df, column_refs=['Start_Date', 'End_Date', 'Pain_Scale', 'Condition'], values=df['Blood_Pressure'],
use_values_as_height=True)
```
![image](https://github.com/user-attachments/assets/18e95c20-b04a-41ad-b6de-77b1fb44478b)

See more details of this in the 'getting_started.ipynb' notebook.

## Notebooks
The package includes a Jupyter notebook called 'getting_started.ipynb' that demonstrates how to use the package. It also shows the six different category of data combinations used in the design study evaluation.

## Tests
To run the tests, run the following command:

```bash
python -m pytest
```

## The datatypes in SMRs

| **Categories**                             | **Combinations of data types**  | **Final chart options**                                                                 |
|--------------------------------------------|----------------------------------|----------------------------------------------------------------------------------------|
| Conditions, Medications, Investigations    | N (Name)                        | Donut, Pie, and List (Table)                                                           |
| Conditions, Medications                    | N, T (Name, Date)               | Gantt, Pie, Line, Donut, Scatter, Heatmap                                              |
| Conditions                                 | N, T, O (Name, Date, Severity)  | Gantt, Heatmap, Line, Scatter                                                          |
| Investigations                             | Q (Quantity)                    | Box, Dot (Wilkinson), Histogram, Violin                                                |
| Investigations                             | N, Q (Name, Quantity)           | Bar, Scatter, Heatmap, Table, Pie, Donut, Radar                                        |
| Investigations                             | N, Q, T (Name, Quantity, Date)  | Gantt, Heatmap, Line, Scatter                                                          |

## Acknowledgements
