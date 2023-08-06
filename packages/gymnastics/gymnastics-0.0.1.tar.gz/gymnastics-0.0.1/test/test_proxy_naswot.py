import torch

from gymnastics.benchmarks import NDSSearchSpace
from gymnastics.proxies import Proxy, NASWOT


def test_proxy_naswot():
    searchspace = NDSSearchSpace(
        "/Users/jackturner/work/nds/data/ResNet.json", searchspace="ResNet"
    )
    data = torch.rand((1, 3, 32, 32))
    for _ in range(10):
        model = searchspace.sample_random_architecture()
        y, _ = model(data)
        print(y.size())

    minibatch: torch.Tensor = torch.rand(10, 3, 32, 32)

    proxy: Proxy = NASWOT()
    proxy.score(model, minibatch)
