""" Main entry point of the ONMT library """
from __future__ import division, print_function

import onmt.models
import onmt.utils
from onmt.trainer import Trainer
import sys
import onmt.utils.optimizers
onmt.utils.optimizers.Optim = onmt.utils.optimizers.Optimizer
sys.modules["onmt.Optim"] = onmt.utils.optimizers


