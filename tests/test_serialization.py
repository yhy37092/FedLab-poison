# -*- coding: utf-8 -*-
# @Time    : 4/10/21 3:30 PM
# @Author  : Siqi Liang
# @Contact : zszxlsq@gmail.com
# @File    : test_serialization.py
# @Software: PyCharm
import unittest
import torch
import torch.nn as nn
from fedlab_core.utils import serialization


class Net(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out


class SerializationTestCase(unittest.TestCase):

    def setUp(self) -> None:
        # DO NOT change the setting below, the model is pretrained
        self.input_size = 784
        self.hidden_size = 250
        self.num_classes = 10
        self.model = Net(self.input_size, self.hidden_size, self.num_classes)
        self.model.load_state_dict(torch.load('./data/nnModel.ckpt'))

    def test_ravel_model_params_cpu(self):
        cpu_params = serialization.ravel_model_params(self.model, cuda=False)
        m_params = torch.Tensor([0])
        for param in self.model.parameters():
            m_params = torch.cat((m_params, param.data.view(-1)))
        m_params = m_params[1:]
        self.assertTrue(torch.equal(cpu_params, m_params))