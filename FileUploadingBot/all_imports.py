from settings import *

import pip
import os
import sys
import time
import re
import tkinter
import pickle
import keyring
import multiprocessing
import logging
from multiprocessing.dummy import Pool as ThreadPool
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from tkinter.filedialog import askopenfilenames