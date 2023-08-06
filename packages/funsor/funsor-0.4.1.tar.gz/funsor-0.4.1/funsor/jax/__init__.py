# Copyright Contributors to the Pyro project.
# SPDX-License-Identifier: Apache-2.0

from jax.core import Tracer
from jax.interpreters.xla import DeviceArray

from funsor.tensor import tensor_to_funsor
from funsor.terms import to_funsor
from funsor.util import quote

from . import distributions as _
from . import ops as _

del _  # flake8


to_funsor.register(DeviceArray)(tensor_to_funsor)
to_funsor.register(Tracer)(tensor_to_funsor)


@quote.register(DeviceArray)
def _quote(x, indent, out):
    """
    Work around JAX's DeviceArray not supporting reproducible repr.
    """
    out.append(
        (indent, "np.array({}, dtype=np.{})".format(repr(x.copy().tolist()), x.dtype))
    )
