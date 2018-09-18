from io import StringIO
import pandas as pd
import pyperclip; import sys
import numpy as np
import pdb
from tabulate import tabulate

# sHeader = input("Is the first row header? y/n ")
sConversion = input("c2t or f2t? (or t2f or t2c?) ")
sHeader = "n"

if sConversion == "f2t" or sConversion == "f2c":
  df=pd.read_fwf(StringIO(pyperclip.paste()), header=list(map(lambda x: 0 if x == "y" else None, sHeader))[0])
if sConversion == "c2f" or sConversion == "c2f":
  df=pd.read_csv(StringIO(pyperclip.paste()), sep=',\s*', header=list(map(lambda x: 0 if x == 'y' else None, sHeader))[0])
if sConversion == "t2c" or sConversion == "t2f":
  df=pd.read_csv(StringIO(pyperclip.paste()), sep='\t', header=list(map(lambda x: 0 if x == 'y' else None, sHeader))[0])

if sConversion == "f2c" or sConversion == "t2c":
  csv_buffer = StringIO()
  df.to_csv(csv_buffer, header=False, index=False, sep=',' )
  sReturn = csv_buffer.getvalue()
if sConversion == "c2t" or sConversion == "f2t":
  csv_buffer = StringIO()
  df.to_csv(csv_buffer, header=False, index=False, sep='\t' )
  sReturn = csv_buffer.getvalue()
if sConversion == "c2f" or sConversion == "t2f":
  sReturn = tabulate(df.values.tolist(), list(df.columns), tablefmt="plain")

pyperclip.copy(sReturn)
print("Your table format was converted...")

