import pandas as pd
import numpy as np
import plotly.graph_objs as go
import datetime as dt
from datetime import datetime, timezone, timedelta
import random
import os

#plotly ve dash kütüphaneleri
import plotly.graph_objs as go
import dash
from dash import Dash,dcc,html,Input,Output,callback
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.Container import Container
from datetime import date
import base64

#uyarıları susturmak için
import warnings
warnings.filterwarnings("ignore")

#pdf raporlama için
import base64
from fpdf import FPDF
#from fpdf.enums import XPos, YPos
import math
import sys
import webbrowser
