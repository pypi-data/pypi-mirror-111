from glob import glob
from os.path import basename
from os.path import splitext

from setuptools import setup
from setuptools import find_packages


def _requires_from_file(filename):
    return open(filename).read().splitlines()


DESCRIPTION="ORPHE ANALYTICIS SDK for Python"
LONG_DESCRIPTION= """
ORPHE ANALYTICIS SDK for Python is a client library that accesses the ORPHE ANALYTICS resource API and real-time API.

## Install

You can install ORPHE ANALYTICIS SDK for Python (hereafter intdash-py) using PyPI. Install with the following command.

```
$ pip install orphe
```

## Usage

To start using ORPHE ANALYTICIS SDK, create a client. To create a client, use the URL of the connection destination and the credentials of the edge account (token or user name/password combination). See intdash client for other available parameters.

```python
import orphe

analytics = orphe.Analytics(
    url = "https://example.analytics.orphe.ai",
    token = "your_token",
)
```

Example:
An example for retrieving and storing a value is given below.

```python
import orphe

# Generate a client with a URL and an edge token
analytics = orphe.Analytics(
    url = "https://example.analytics.orphe.ai",
    token= "your_token"
)
# Get data by specifying the measurement UUID
analyzed = analytics.load(
    measurement_uuid = "e07cdf8c-83e6-46cf-8a03-e315eef6162a",
)

# Extract, analyze and display values
for gait in analyzed.gait.left:
    print(f"left/{gait.time}/{gait.quaternion_w}/{gait.quaternion_x}/{gait.quaternion_y}/{gait.quaternion_z}")

for gait in analyzed.gait.right:
    print(f"right/{gait.time}/{gait.quaternion_w}/{gait.quaternion_x}/{gait.quaternion_y}/{gait.quaternion_z}")

# To save the value, use [orphe.Unit]
units = []
for gait in analyzed.gait.left:
    units.append(orphe.Unit(
        time = gait.time,
        id = "Height",
        value = 160
    ))

# Save the data by specifying the measurement UUID and the list of [orphe.Unit].
analytics.save(
    measurement_uuid="e07cdf8c-83e6-46cf-8a03-e315eef6162a",
    units=units
)
```

After analytics.load is performed, the retrieved valuesanalyzed will contain the values retrieved from ORPHE CORE and the values analyzed by ANALYTICS.
By gait, the data of gait analysis is retrieved, and left and right data can be retrieved respectively.

In addition, if you want to perform real-time analysis, you can use the following method.

```python
import orphe

# Generate a client with a URL and an edge token
analytics = orphe.Analytics(
    url = "https://example.analytics.orphe.ai",
    token= "your_token"
)

# Defines a callback for realtime. [value] will contain the raw and parsed data.
def callback(value : orphe.AnalyticsValue) -> None:
    if value.gait.left.stride != None:
        print(value.gait.left.stride)
    if value.gait.left.euler_x != None:
        print(value.gait.left.euler_x)

# Start real-time acquisition by specifying the callback and the ID of the edge.
analytics.realtime(
    callback = callback,
    edge_uuid="08058fc6-3374-407a-b9ed-fcbe81217ac9",
)
```

## Documentation 

Documentation and links to additional resources are available at https://analytics.orphe.ai

"""

setup(
    name="orphe",
    version="0.0.1",
    python_requires=">=3.5",
    url="https://orphe.shoes/",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    install_requires=_requires_from_file('requirements.txt'),
    author='no new folk studio Inc.',
    author_email='support@no-new-folk.com',
    keywords='orphe, orphe analytics',
    license="Apache License 2.0",    
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
)
