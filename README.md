# prefect-geopandas-serializer
PandasSerializer adapted for GeoPandas

> **Warning**: This project is very experimental.  It has only been minimally tested on the `parquet` file format which is itself expermintal in `GeoPandas` (as of 12/08/2021)

## Installation

```python
pip install prefect-geopandas-serializer
``` 

## Example Usage

From the `prefect` [docs](https://docs.prefect.io/core/):

> Prefect offers a notion of task "checkpointing" that ensures that every time a task is successfully run, its return value is written to persistant storage based on the configuration in a Result object for the task.

> The default setting in Prefect Core is that checkpointing is globally turned off, and the default setting in Prefect Cloud 0.9.1+ is that checkpointing is globally turned on. For more information, read the concepts documentation on [Results](https://docs.prefect.io/core/concepts/results.html#pipeline-persisted-results) and the setup tutorial on [Using Results](https://docs.prefect.io/core/advanced_tutorials/using-results.html).

> To enable checkpointing for local testing, set the `PREFECT__FLOWS__CHECKPOINTING` environment variable to true.

To persist geodata as a `parquet` file and enable caching use `GeoPandasSerializer` as a serializer when
using `Result`:

```python
import geopandas as gpd
from prefect import Flow
from prefect.results import LocalResult
from prefect import task
from prefect_geopandas_serializer.serializers import GeoPandasSerializer


@task(checkpoint=True, result=LocalResult(serializer=GeoPandasSerializer("parquet")))
def read_file(filepath):
    return gpd.read_file(filepath)

with Flow("Do something") as flow:
    geodata = read_file("mydata.geojson")
```
