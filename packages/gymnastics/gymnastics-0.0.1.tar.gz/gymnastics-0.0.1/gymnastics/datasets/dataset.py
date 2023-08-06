import torch

from abc import ABC, abstractmethod
from typing import Tuple


class Dataset(ABC):
    @abstractmethod
    def set_transforms(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_data_sets(
        self, path: str, val_split_percentage: float, seed: int, download: bool
    ) -> Tuple[
        torch.utils.data.Dataset,  # train set
        torch.utils.data.Dataset,  # val set
        torch.utils.data.Dataset,  # test set
        int,  # labels
    ]:
        raise NotImplementedError

    def get_data_loaders(self, train_set, val_set, test_set):

        self.train_loader = torch.utils.data.DataLoader(
            train_set,
            batch_size=self.batch_size,
            shuffle=True,
            num_workers=self.num_workers,
            pin_memory=True,
        )

        self.val_loader = torch.utils.data.DataLoader(
            val_set,
            batch_size=self.batch_size,
            shuffle=False,
            num_workers=self.num_workers,
            pin_memory=True,
        )

        self.test_loader = torch.utils.data.DataLoader(
            test_set,
            batch_size=self.batch_size,
            shuffle=False,
            num_workers=self.num_workers,
            pin_memory=True,
        )

        return self.train_loader, self.val_loader, self.test_loader

    def sample_minibatch(self, train: bool = True) -> Tuple[torch.Tensor, torch.Tensor]:

        if train:
            dataloader = self.train_loader
        else:
            dataloader = self.val_loader

        inputs, classes = next(iter(dataloader))

        return inputs, classes
