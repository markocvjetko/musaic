import os
import yaml
import torch
import torch.optim as optim
import json
from helper import *
from torch.optim.lr_scheduler import LambdaLR


def get_optimizer_class(name: str):
    if name == "Adam":
        return optim.Adam
    else:
        raise ValueError("Choose optimizer from: Adam")
        return


def get_lr_scheduler(optimizer, total_epochs: int, verbose: bool = True):
    """
    Scheduler to linearly decrease learning rate,
    so thatlearning rate after the last epoch is 0.
    """
    lr_lambda = lambda epoch: (total_epochs - epoch) / total_epochs
    lr_scheduler = LambdaLR(optimizer, lr_lambda=lr_lambda, verbose=verbose)
    return lr_scheduler


def save_config(config: dict, model_dir: str):
    """Save config file to `model_dir` directory"""
    config_path = os.path.join(model_dir, "config.yaml")
    with open(config_path, "w") as stream:
        yaml.dump(config, stream)


def save_vocab(vocab, model_dir: str):
    """Save vocab file to `model_dir` directory"""
    vocab_path = os.path.join(model_dir, "vocab.pt")
    torch.save(vocab, vocab_path)

def _save_checkpoint(self, epoch):
    """Save model checkpoint to `self.model_dir` directory"""
    epoch_num = epoch + 1
    if epoch_num % self.checkpoint_frequency == 0:
        model_path = "checkpoint_{}.pt".format(str(epoch_num).zfill(3))
        model_path = os.path.join(self.model_dir, model_path)
        torch.save(self.model, model_path)

def save_model(model, model_path):
    """Save final model to `self.model_dir` directory"""
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, model_path)

    torch.save(model, filename)

def save_loss(self):
    """Save train/val loss as json file to `self.model_dir` directory"""
    loss_path = os.path.join(self.model_dir, "loss.json")
    with open(loss_path, "w") as fp:
        json.dump(self.loss, fp)