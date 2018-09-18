from io import StringIO
import pandas as pd
import pyperclip; import sys
import pdb
from collections import Counter

sInput = input("Find unique combinations (c) or permutations (p / any key)?")

df=pd.read_csv(StringIO(pyperclip.paste()), sep='\t', header=None)

# pdb.set_trace()
if sInput == "c":
  df = df.apply(Counter, axis='columns').value_counts()

  heck0 = []
  heck = []
  for blah in df.index:
    for x in blah: heck = heck + ([x] *  blah[x])
    heck0.append(heck)
    heck = []
  
  # tempDF = pd.DataFrame([(key, value) for key, value in df.index])
  tempDF = pd.DataFrame(heck0)
  df = pd.DataFrame(df)
  df = df.reset_index(drop=True)
  tempDF[tempDF.shape[0]-1] = df[df.columns[0]]
  df = tempDF
else:
  df = df.groupby([i for i in range(0, len(df.columns))]).size().reset_index(name='count')
# pdb.set_trace()

csv_buffer = StringIO()
df.to_csv(csv_buffer, index=False, header=False, sep='\t' )
pyperclip.copy(csv_buffer.getvalue())
print("The de-duplicated table is now pasted to your clipboard. ")
