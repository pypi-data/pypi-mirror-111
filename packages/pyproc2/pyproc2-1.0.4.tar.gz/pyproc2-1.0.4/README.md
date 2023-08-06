### Short intro
**pyproc** is Python library for reading data from /proc/ directory.
Of course, it works only on Linux.
>#### What can it do?
>>##### Find processes
There is only one method for all filters (PID, process name, user name,etc.)
It is called `find()`.
Here are few examples:
**1. By PID**:
```python
import pyproc
pyproc.find(1)

```

**2. By process name (can return multiple results)**

```python
import pyproc
pyproc.find("python")

```
