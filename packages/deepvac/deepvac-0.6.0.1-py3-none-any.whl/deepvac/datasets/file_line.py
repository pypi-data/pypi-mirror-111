import os
import numpy as np
import cv2
from PIL import Image
from ..utils import LOG
from .base_dataset import DatasetBase

class FileLineDataset(DatasetBase):
    def __init__(self, deepvac_config, fileline_path, delimiter=' ', sample_path_prefix=''):
        super(FileLineDataset, self).__init__(deepvac_config)
        self.sample_path_prefix = sample_path_prefix
        self.fileline_path = fileline_path
        self.delimiter = delimiter
        self.samples = []
        mark = []

        with open(self.fileline_path) as f:
            for line in f:
                label = self._buildLabelFromLine(line)
                self.samples.append(label)
                mark.append(label[1])

        self.len = len(self.samples)
        self.class_num = len(np.unique(mark))
        LOG.logI('FileLineDataset size: {} / {}'.format(self.len, self.class_num))

    def _buildLabelFromLine(self, line):
        line = line.strip().split(self.delimiter)
        return [line[0], int(line[1])]

    def __getitem__(self, index):
        path, target = self.samples[index]
        abs_path = os.path.join(self.sample_path_prefix, path)
        sample = self._buildSampleFromPath(abs_path)
        sample = self.compose(sample)
        return sample, target

    def _buildSampleFromPath(self, abs_path):
        #we just set default loader with Pillow Image
        sample = Image.open(abs_path).convert('RGB')
        return sample

    def __len__(self):
        return self.len

class FileLineCvStrDataset(FileLineDataset):
    def _buildLabelFromLine(self, line):
        line = line.strip().split(self.delimiter, 1)
        return [line[0], line[1]]

    def _buildSampleFromPath(self, abs_path):
        #we just set default loader with Pillow Image
        sample = cv2.imread(abs_path)
        return sample

class FileLineCvSegDataset(FileLineCvStrDataset):
    def _buildLabelFromPath(self, abs_path):
        sample = cv2.imread(abs_path, cv2.IMREAD_GRAYSCALE)
        return sample

    def __getitem__(self, index):
        image_path, label_path = self.samples[index]
        sample = self._buildSampleFromPath(os.path.join(self.sample_path_prefix, image_path.strip()))
        label = self._buildLabelFromPath(os.path.join(self.sample_path_prefix, label_path.strip()))

        sample, label = self.compose([sample, label])
        return sample, label

class FileLineCvSegAuditDataset(FileLineCvSegDataset):
    def __getitem__(self, index):
        image_path, label_path = self.samples[index]
        image_path = os.path.join(self.sample_path_prefix, image_path.strip() )
        label_path = os.path.join(self.sample_path_prefix, label_path.strip() )
        sample = self._buildSampleFromPath(image_path)
        label = self._buildLabelFromPath(label_path)

        cls_masks = {}
        for cls_idx in np.unique(label):
            cls_masks[cls_idx] = label == cls_idx
        sample, label, cls_masks, label_path = self.compose([sample, label, cls_masks, label_path])
        return sample, label, cls_masks, label_path