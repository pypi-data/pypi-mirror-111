# -*- coding:utf-8 -*-
import math
import torch
import torch.nn as nn
from ..utils import LOG, addUserConfig
from ..core import AttrDict

class LossBase(nn.Module):
    def __init__(self, deepvac_config):
        super(LossBase, self).__init__()
        self.deepvac_loss_config = deepvac_config.loss
        self.initConfig()
        self.auditConfig()

    def initConfig(self):
        if self.name() not in self.deepvac_loss_config.keys():
            self.deepvac_loss_config[self.name()] = AttrDict()
        self.config = self.deepvac_loss_config[self.name()]

    def addUserConfig(self, config_name, user_give=None, developer_give=None, is_user_mandatory=False):
        module_name = 'config.loss.{}'.format(self.name())
        return addUserConfig(module_name, config_name, user_give, developer_give, is_user_mandatory)

    def name(self):
        return self.__class__.__name__

    def auditConfig(self):
        raise Exception("Not implemented!")

class MaskL1Loss(LossBase):
    def __init__(self, deepvac_config):
        super(MaskL1Loss, self).__init__(deepvac_config)

    def auditConfig(self):
        self.eps = self.addUserConfig('eps', self.config.eps, 1e-6)

    def __call__(self, pred: torch.Tensor, gt, mask):
        loss = (torch.abs(pred - gt) * mask).sum() / (mask.sum() + self.eps)
        return loss

class DiceLoss(LossBase):
    def __init__(self, deepvac_config):
        super(DiceLoss, self).__init__(deepvac_config)

    def auditConfig(self):
        self.eps = self.addUserConfig('eps', self.config.eps, 1e-6)

    def __call__(self, pred: torch.Tensor, gt, mask, weights=None):
        return self._compute(pred, gt, mask, weights)

    def _compute(self, pred, gt, mask, weights):
        if pred.dim() == 4:
            pred = pred[:, 0, :, :]
            gt = gt[:, 0, :, :]
        assert pred.shape == gt.shape
        assert pred.shape == mask.shape
        if weights is not None:
            assert weights.shape == mask.shape
            mask = weights * mask
        intersection = (pred * gt * mask).sum()
        union = (pred * mask).sum() + (gt * mask).sum() + self.eps
        loss = 1 - 2.0 * intersection / union
        assert loss <= 1
        return loss

class BalanceCrossEntropyLoss(LossBase):
    def __init__(self, deepvac_config):
        super(BalanceCrossEntropyLoss, self).__init__(deepvac_config)

    def auditConfig(self):
        self.negative_ratio = self.addUserConfig('negative_ratio', self.config.negative_ratio, 3.0)
        self.eps = self.addUserConfig('eps', self.config.eps, 1e-6)

    def __call__(self,
                pred: torch.Tensor,
                gt: torch.Tensor,
                mask: torch.Tensor,
                return_origin=False):
        positive = (gt * mask).byte()
        negative = ((1 - gt) * mask).byte()
        positive_count = int(positive.float().sum())
        negative_count = min(int(negative.float().sum()), int(positive_count * self.negative_ratio))
        loss = nn.functional.binary_cross_entropy(pred, gt, reduction='none')
        positive_loss = loss * positive.float()
        negative_loss = loss * negative.float()
        negative_loss, _ = negative_loss.view(-1).topk(negative_count)
        balance_loss = (positive_loss.sum() + negative_loss.sum()) / (positive_count + negative_count + self.eps)
        if return_origin:
            return balance_loss, loss
        return balance_loss

class BCEBlurWithLogitsLoss(LossBase):
    # BCEwithLogitLoss() with reduced missing label effects.
    def __init__(self, deepvac_config):
        super(BCEBlurWithLogitsLoss, self).__init__(deepvac_config)

    def auditConfig(self):
        self.alpha = self.addUserConfig('alpha', self.config.alpha, 0.05)
        self.reduction = self.addUserConfig('reduction', self.config.reduction, 'none')
        self.loss_fcn = nn.BCEWithLogitsLoss(reduction=self.reduction)

    def __call__(self, pred, true):
        loss = self.loss_fcn(pred, true)
        pred = torch.sigmoid(pred)
        # reduce only missing label effects
        dx = pred - true
        alpha_factor = 1 - torch.exp((dx - 1) / (self.alpha + 1e-4))
        loss *= alpha_factor
        return loss.mean()

class FocalLoss(LossBase):
    # Wraps focal loss around existing loss_fcn(), i.e. criteria = FocalLoss(nn.BCEWithLogitsLoss(), gamma=1.5)
    def __init__(self, deepvac_config):
        super(FocalLoss, self).__init__(deepvac_config)

    def auditConfig(self):
        self.alpha = self.addUserConfig('alpha', self.config.alpha, 0.25)
        self.gamma = self.addUserConfig('gamma', self.config.gamma, 1.5)
        self.reduction = self.addUserConfig('reduction', self.config.reduction, 'none')
        self.loss_fcn = nn.BCEWithLogitsLoss(reduction=self.reduction)

    def __call__(self, pred, true):
        loss = self.loss_fcn(pred, true)
        # TF implementation https://github.com/tensorflow/addons/blob/v0.7.1/tensorflow_addons/losses/focal_loss.py
        pred_prob = torch.sigmoid(pred)
        p_t = true * pred_prob + (1 - true) * (1 - pred_prob)
        alpha_factor = true * self.alpha + (1 - true) * (1 - self.alpha)
        modulating_factor = (1.0 - p_t) ** self.gamma
        loss *= alpha_factor * modulating_factor

        if self.reduction == 'mean':
            return loss.mean()
        elif self.reduction == 'sum':
            return loss.sum()
        else:
            return loss

class QFocalLoss(LossBase):
    # Wraps Quality focal loss around existing loss_fcn(), i.e. criteria = FocalLoss(nn.BCEWithLogitsLoss(), gamma=1.5)
    def __init__(self, deepvac_config):
        super(QFocalLoss, self).__init__(deepvac_config)

    def auditConfig(self):
        self.alpha = self.addUserConfig('alpha', self.config.alpha, 0.25)
        self.gamma = self.addUserConfig('gamma', self.config.gamma, 1.5)
        self.reduction = self.addUserConfig('reduction', self.config.reduction, 'none')
        self.loss_fcn = nn.BCEWithLogitsLoss()

    def __call__(self, pred, true):
        loss = self.loss_fcn(pred, true)
        pred_prob = torch.sigmoid(pred)
        alpha_factor = true * self.alpha + (1 - true) * (1 - self.alpha)
        modulating_factor = torch.abs(true - pred_prob) ** self.gamma
        loss *= alpha_factor * modulating_factor

        if self.reduction == 'mean':
            return loss.mean()
        elif self.reduction == 'sum':
            return loss.sum()
        else:
            return loss

class WingLoss(nn.Module):
    def __init__(self):
        super(WingLoss, self).__init__()

    def forward(self, pred, truth, w=10.0, epsilon=2.0):
        x = truth - pred
        c = w * (1.0 - math.log(1.0 + w / epsilon))
        absolute_x = torch.abs(x)
        losses = torch.where(w > absolute_x, w * torch.log(1.0 + absolute_x / epsilon), absolute_x - c)
        return torch.sum(losses) / (len(losses) * 1.0)
