# pyservicebinding
![PyPI - Downloads](https://img.shields.io/pypi/dm/pyservicebinding)
![Release](https://img.shields.io/pypi/v/pyservicebinding)
![Supported Python Versions](https://img.shields.io/pypi/pyversions/pyservicebinding)
[![CI](https://github.com/baijum/pyservicebinding/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/baijum/pyservicebinding/actions/workflows/ci.yml)
> Kubernetes Service Binding Library for Python Applications

This is a Python module to retrieve bindings from a file-system created through
an implementation of [Service Binding Specification for
Kubernetes](https://github.com/k8s-service-bindings/spec).

You can install this package using pip:

```bash
pip install pyservicebinding
```


The `ServiceBinding` object can be instantiated like this:
```python
from pyservicebinding import binding
try:
    sb = binding.ServiceBinding()
except binding.ServiceBindingRootMissingError as msg:
    # log the error message and retry/exit
    print("SERVICE_BINDING_ROOT env var not set")
```

To get bindings for a specific `type`, say `postgres`:

```python
bindings_list = sb.bindings("postgres")
```

To get bindings for a specific `type`, say `mysql`, and `provider`, say `mariadb`:

```python
bindings_list = sb.bindings("mysql", "mariadb")
```

To get all bindings irrespective of the `type` and `provider`:

```python
bindings_list = sb.all_bindings()
```

This is the complete API of the module:
```python

class ServiceBindingRootMissingError(Exception):
    pass


class ServiceBinding:

    def __init__(self):
        """
        - raise ServiceBindingRootMissingError if SERVICE_BINDING_ROOT env var not set
        """

    def all_bindings(self) -> list[dict[str, str]]:
        """Get all bindings as a list of dictionaries

        - return empty list if no bindings found
        """

    def bindings(self, _type: str, provider: typing.Optional[str] = None) -> list[dict[str, str]]:
        """Get filtered bindings as a list of dictionaries

        - return empty dictionary if no binding found
        - filter the result with the given _type input
        - if provider input is given, filter bindings using the given type and provider
        """
```
