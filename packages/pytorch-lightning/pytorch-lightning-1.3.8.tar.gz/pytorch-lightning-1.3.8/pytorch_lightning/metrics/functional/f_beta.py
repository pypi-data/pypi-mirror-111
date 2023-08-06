# Copyright The PyTorch Lightning team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import Optional

from torch import Tensor
from torchmetrics.functional import f1 as _f1
from torchmetrics.functional import fbeta as _fbeta

from pytorch_lightning.metrics.utils import (
    _TORCHMETRICS_GREATER_EQUAL_0_4,
    _TORCHMETRICS_LOWER_THAN_0_4,
    deprecated_metrics,
)


@deprecated_metrics(target=_fbeta, skip_if=_TORCHMETRICS_GREATER_EQUAL_0_4)
@deprecated_metrics(target=_fbeta, args_mapping={"multilabel": None}, skip_if=_TORCHMETRICS_LOWER_THAN_0_4)
def fbeta(
    preds: Tensor,
    target: Tensor,
    num_classes: int,
    beta: float = 1.0,
    threshold: float = 0.5,
    average: str = "micro",
    multilabel: Optional[bool] = None
) -> Tensor:
    """
    .. deprecated::
        Use :func:`torchmetrics.functional.fbeta`. Will be removed in v1.5.0.
    """


@deprecated_metrics(target=_f1, skip_if=_TORCHMETRICS_GREATER_EQUAL_0_4)
@deprecated_metrics(target=_f1, args_mapping={"multilabel": None}, skip_if=_TORCHMETRICS_LOWER_THAN_0_4)
def f1(
    preds: Tensor,
    target: Tensor,
    num_classes: int,
    threshold: float = 0.5,
    average: str = "micro",
    multilabel: Optional[bool] = None
) -> Tensor:
    """
    .. deprecated::
        Use :func:`torchmetrics.functional.f1`. Will be removed in v1.5.0.
    """
