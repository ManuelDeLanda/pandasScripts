from io import StringIO
import pandas as pd
import pyperclip; import sys
import numpy as np
import pdb

sHeader = input("Is the first row header? y/n ")

sNumOfSamples = input("How many samples rows from each column do you want? ")

# CLIPBOARD DATA
df=pd.read_csv(StringIO(pyperclip.paste()), sep='\t', header=list(map(lambda x: 0 if x == 'y' else None, sHeader))[0])
# TEST DATA
# df=pd.read_csv(StringIO("\nAccount	Name	Rep	Manager	Product	Quantity	Price	Status\n714466	Trantow-Barrows	Craig Booker	Debra Henley	CPU	1	30000	presented\n714466	Trantow-Barrows	Craig Booker	Debra Henley	Software	1	10000	presented\n714466	Trantow-Barrows	Craig Booker	Debra Henley	Maintenance	2	5000	pending\n737550	Fritsch, Russel and Anderson	Craig Booker	Debra Henley	CPU	1	35000	declined\n146832	Kiehn-Spinka	Daniel Hilton	Debra Henley	CPU	2	65000	won\n218895	Kulas Inc	Daniel Hilton	Debra Henley	CPU	2	40000	pending\n218895	Kulas Inc	Daniel Hilton	Debra Henley	Software	1	10000	presented\n412290	Jerde-Hilpert	John Smith	Debra Henley	Maintenance	2	5000	pending\n740150	Barton LLC	John Smith	Debra Henley	CPU	1	35000	declined\n141962	Herman LLC	Cedric Moss	Fred Anderson	CPU	2	65000	won\n163416	Purdy-Kunde	Cedric Moss	Fred Anderson	CPU	1	30000	presented\n239344	Stokes LLC	Cedric Moss	Fred Anderson	Maintenance	1	5000	pending\n239344	Stokes LLC	Cedric Moss	Fred Anderson	Software	1	10000	presented\n307599	Kassulke, Ondricka and Metz	Wendy Yule	Fred Anderson	Maintenance	3	7000	won\n688981	Keeling LLC	Wendy Yule	Fred Anderson	CPU	5	100000	won\n729833	Koepp Ltd	Wendy Yule	Fred Anderson	CPU	2	65000	declined\n729833	Koepp Ltd	Wendy Yule	Fred Anderson	Monitor	2	5000	presented"), sep='\t', header=list(map(lambda x: 0 if x == "y" else None, sHeader))[0])

sRowsOfSamples = []

for column in df:

  dfColumn = pd.DataFrame(df[column])
  dfColumn = dfColumn.drop_duplicates()
  # print("deduplicated table: " + str(dfColumn.shape[0]) + "  num of Samples: " + str(sNumOfSamples))
  if dfColumn.shape[0] < int(sNumOfSamples):
    sThisNumOfSamples = dfColumn.shape[0]
  else:
    sThisNumOfSamples = int(sNumOfSamples)

  # pdb.set_trace()
  dfSample = dfColumn.sample(n=int(sThisNumOfSamples))
  sNewRow = ', '.join(str(s) for s in (dfSample[dfSample.columns[0]]))
  sRowsOfSamples.append(sNewRow)

if sHeader == "y":
  dfReturn = pd.DataFrame({'columns': df.columns.values.tolist(), 'samples': sRowsOfSamples})
else:
  dfReturn = pd.DataFrame(sRowsOfSamples)

csv_buffer = StringIO()
dfReturn.to_csv(csv_buffer, header=False, index=False, sep='\t' )
pyperclip.copy(csv_buffer.getvalue())
