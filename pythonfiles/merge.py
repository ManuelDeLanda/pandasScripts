from io import StringIO # OLD-replace with mac version
import pandas as pd
import pyperclip; import sys
import pdb

input('Please copy first table (at least 2 columns, first column is primary key duplicates NOT ok).')
df=pd.read_csv(StringIO(pyperclip.paste()), sep='\t', header=None)
if df.shape[0] > df.drop_duplicates(subset=[df.columns[0]], keep='first').shape[0]:
  print("\nDuplicates (or empty cells) found in first column; grouping them and NS_CONCATing the other columns now...\n")
  f = {df.columns[1]: lambda x: "%s" % ', '.join(x)}
  df = df.groupby(df.columns[0]).agg(f)
  df.reset_index(level=df.index.names, inplace=True)
  csv_buffer = StringIO()
  df.to_csv(csv_buffer, header=False, index=False, sep='\t' )
  pyperclip.copy(csv_buffer.getvalue())
  
input('Please copy second table (precisely two columns, first column is foreign key duplicates ARE ok).')
df2=pd.read_csv(StringIO(pyperclip.paste()), sep='\t', header=None)
df[df.columns[0]].astype(str)
df2[df2.columns[0]].astype(str)
df3 = df2.merge(df, on=[df.columns[0]], how='left', sort=False)
print(df3)
print("The length is " + str(df3.shape[1]))
q = list(reversed(range(2,df3.shape[1])))
print(q)
a = []
b = [a.append(df3.columns[i]) for i in q]
if len(a) == 0:
  a = [df3.columns[1]] 
csv_buffer = StringIO()
df3[a].to_csv(csv_buffer, header=False, index=False, sep='\t' )
pyperclip.copy(csv_buffer.getvalue())
