# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 19:25:40 2017

@author: joe
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as pdr

msft = pdr.get_data_yahoo('MSFT', '2017-12-01')

print("finished")

m = msft.tail()

print(m)
