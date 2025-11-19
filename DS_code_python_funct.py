# -*- coding: utf-8 -*-
"""
Created on 15 sept 2025

DS and Vulnarabilities run file NAture paper 2025
based on last update of ENCORE and EXIOBASE

@author: DNB FS-IFA NC5452 (sebastien gallet)
"""
import os
path_DS_store = 'I:\\FS\\FS\\Statsp\\000-Beleidsmedewerkers\\Sebastien Gallet\\Biodiv\\OS-2025\\DS_Vuln_update\\'
os.chdir(path_DS_store)

import importlib
import time
import DS_functions as funct
importlib.reload(funct)

start = time.time()
funct.global_run(path_DS_store)
end = time.time()
print(f"Execution time: {end - start:.4f} seconds")

import gc
gc.collect()
## end

