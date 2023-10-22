import pytest
from custom_typing import OptimalParameters


@pytest.fixture
def sample_data():
    params = OptimalParameters([1, 2, 3], [30, 45, 60], [0.1, 0.2, 0.3])
    temperature = [100, 200, 300]
    return params, temperature
