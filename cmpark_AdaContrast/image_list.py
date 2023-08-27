import os
import numpy as np
import torch
from PIL import Image
from torch.utils.data import Dataset


def load_image(img_path):
    img = Image.open(img_path)
    img = img.convert("RGB")
    return img


class ImageList(Dataset):
    def __init__(
        self,
        image_root: str,
        label_file: str,
        transform=None,
        pseudo_item_list=None,
    ):
        self.image_root = image_root
        self._label_file = label_file
        self.transform = transform

        assert (
            label_file or pseudo_item_list
        ), f"Must provide either label file or pseudo labels."
        self.item_list = (
            self.build_index(label_file) if label_file else pseudo_item_list
        )

    def build_index(self, label_file):
        """Build a list of <image path, class label> items.

        Args:
            label_file: path to the domain-net label file

        Returns:
            item_list: a list of <image path, class label> items.
        """
        # read in items; each item takes one line
        with open(label_file, "r") as fd:
            lines = fd.readlines()
        lines = [line.strip() for line in lines if line]

        item_list = []
        for item in lines:
            img_file, label = item.split()
            img_path = os.path.join(self.image_root, img_file)
            label = int(label)
            item_list.append((img_path, label, img_file))

        return item_list

    def __getitem__(self, idx):
        """Retrieve data for one item.

        Args:
            idx: index of the dataset item.
        Returns:
            img: <C, H, W> tensor of an image
            label: int or <C, > tensor, the corresponding class label. when using raw label
                file return int, when using pseudo label list return <C, > tensor.
        """
        img_path, label, _ = self.item_list[idx]
        img = load_image(img_path)
        if self.transform:
            img = self.transform(img)

        return img, label, idx

    def __len__(self):
        return len(self.item_list)

def list_mixup_data(x, y, x_t=None, alpha=None, use_cuda=True, sim=None):
    '''Returns mixed inputs, pairs of targets, and lambda'''
    if alpha > 0:
        lam = np.random.beta(alpha, alpha)
    else:
        lam = 1

    
    batch_size = x.size()[0]
    lam_list = torch.Tensor(np.repeat(lam,batch_size)).reshape(-1,1,1,1).cuda()

    if use_cuda:
        index = torch.randperm(batch_size).cuda()
    else:
        index = torch.randperm(batch_size)

    # filter_same_class = y == y[index] ## cond1
    # filter_same_sim = sim.argmax(1) == sim[index].argmax(1) ## cond2
    # filter_index = filter_same_class ## cond1 and cond2 always true
    filter_index = y == sim.argmax(1)
    
    lam_list[filter_index] = 1

    target_x = x if x_t == None else x_t
    mixed_x = lam_list * x + (1 - lam_list) * target_x[index, :]

    y_a, y_b = y, y[index]
    return mixed_x, y_a, y_b, lam_list, index

def mixup_data(x, y, x_t=None, alpha=None, use_cuda=True):
    '''Returns mixed inputs, pairs of targets, and lambda'''
    if alpha > 0:
        lam = np.random.beta(alpha, alpha)
    else:
        lam = 1

    batch_size = x.size()[0]
    if use_cuda:
        index = torch.randperm(batch_size).cuda()
    else:
        index = torch.randperm(batch_size)
    
    target_x = x if x_t == None else x_t
    mixed_x = lam * x + (1 - lam) * target_x[index, :]

    y_a, y_b = y, y[index]
    return mixed_x, y_a, y_b, lam, index

