import pytest
import numpy as np
from core.base_model import BaseModel

def test_base_model_compile():
    model = BaseModel()
    compiled = model.compile(optimizer='sgd')
    assert compiled._is_compiled is True
    assert compiled._optimizer == 'sgd'

def test_base_model_predict():
    model = BaseModel().compile()
    X = np.random.rand(10, 5)
    pred = model.predict(X)
    assert pred.shape == (10, 1)
