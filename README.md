# plotdelice
A collection of functions to plot old school style graphs with significance bars.

## Gallery
**Violin plot**

```python
from plotdelice.graphs import violinplot_delice
import pandas as pd

# read data
df = pd.read_csv("path_to_your_file.csv")

# define what you want to plot
x_group = "genotype"
y_variable = "angle"
y_label = r'Somite Angle [°]'

# plot
violinplot_delice(df,x_group,y_variable,violin_width=0.8,y_label=y_label,palette="Greens_d",point_size=40,jitter=0.09)
```


![alt text](assets/image.png)

**Scatter plot**

**Custom marker plot**

**Multilevel plot**

