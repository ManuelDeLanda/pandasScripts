from io import StringIO # OLD!
import pandas as pd
import pyperclip; import sys
import numpy as np
import pdb
import re
import copy

def money_to_float(money_str):
    try:
      if len(str(money_str)) == 0:
        money_str = '0'
      # remove all non digits, then replace parentheses with negative
      sReturn = re.sub('[^0-9.\-\(\)]','', str(money_str))
      sReturn = re.sub('[(]', '-', re.sub('[)]', '', sReturn))

      if len(sReturn) == 0 or sReturn == "." or str(money_str).count('.') > 1 or sReturn == "-" or sReturn == ".-" or sReturn == "-." or str(money_str).count('-') > 1 or ("-" in str(money_str) and str(money_str)[:1] != "-"):
        sReturn = '0'
      return float(sReturn)
    except:
      pdb.set_trace()
      
def NS_concat(x):
    # pdb.set_trace()
    return "%s" % ', '.join(x.apply(str))

def NS_concatU(x):
    # pdb.set_trace()
    return "%s" % ', '.join(x.drop_duplicates().apply(str))

# date code
# df.[df.column[0]] = pd.to_datetime(df.[df.column[0]])
# df.query('B==3')['A']
  
input('Please copy the table/dataframe and press return.')
sHeader = input("Is the first row header? y/n ")

# CLIPBOARD DATA
# pdb.set_trace()
df=pd.read_csv(StringIO(pyperclip.paste()), sep='\t', header=list(map(lambda x: 0 if x == 'y' else None, sHeader))[0])
# TEST DATA
# df=pd.read_csv(StringIO("\nAccount        Name        Rep        Manager        Product        Quantity        Price        Status\n714466        Trantow-Barrows        Craig Booker        Debra Henley        CPU        1        30000        presented\n714466        Trantow-Barrows        Craig Booker        Debra Henley        Software        1        10000        presented\n714466        Trantow-Barrows        Craig Booker        Debra Henley        Maintenance        2        5000        pending\n737550        Fritsch, Russel and Anderson        Craig Booker        Debra Henley        CPU        1        35000        declined\n146832        Kiehn-Spinka        Daniel Hilton        Debra Henley        CPU        2        65000        won\n218895        Kulas Inc        Daniel Hilton        Debra Henley        CPU        2        40000        pending\n218895        Kulas Inc        Daniel Hilton        Debra Henley        Software        1        10000        presented\n412290        Jerde-Hilpert        John Smith        Debra Henley        Maintenance        2        5000        pending\n740150        Barton LLC        John Smith        Debra Henley        CPU        1        35000        declined\n141962        Herman LLC        Cedric Moss        Fred Anderson        CPU        2        65000        won\n163416        Purdy-Kunde        Cedric Moss        Fred Anderson        CPU        1        30000        presented\n239344        Stokes LLC        Cedric Moss        Fred Anderson        Maintenance        1        5000        pending\n239344        Stokes LLC        Cedric Moss        Fred Anderson        Software        1        10000        presented\n307599        Kassulke, Ondricka and Metz        Wendy Yule        Fred Anderson        Maintenance        3        7000        won\n688981        Keeling LLC        Wendy Yule        Fred Anderson        CPU        5        100000        won\n729833        Koepp Ltd        Wendy Yule        Fred Anderson        CPU        2        65000        declined\n729833        Koepp Ltd        Wendy Yule        Fred Anderson        Monitor        2        5000        presented"), sep='\t', header=list(map(lambda x: 0 if x == "y" else None, sHeader))[0])

print(df)

pivotArray = ["blah"]

while pivotArray != "":

  sPivotArray = input('\nEnter Your IndexColumns ColumnColumns ValueColumns aggValues? \n ex:\n\t0,1 2,3 6,5 np.sum,len\n\t3,7 4 5,6 len,np.sum-np.mean\n\t3,7 4 5 np.sum \n\n  > ')
  pivotArray = sPivotArray.split(" ")
  # 0,1 2,3 3,6,7,8 -> [0, 1], [2, 5], [3, 6, 7, 8]]

  if pivotArray[0] != "pdb":
    aColumnColumns = []
    aValueColumns = []

    # Index columns
    if sHeader == "y":
      aIndexColumns = [df.columns[i] for i in eval("[" + pivotArray[0] + "]")]
    else:
      aIndexColumns = [i for i in eval("[" + pivotArray[0] + "]")]
    # Column columns
    if len(pivotArray) - 1 > 0:    
      if sHeader == "y":
        aColumnColumns = [df.columns[i] for i in eval("[" + pivotArray[1] + "]")]
      else:
        aColumnColumns = [i for i in eval("[" + pivotArray[1] + "]")]   
    # Value columns   
    if len(pivotArray) - 1 > 1:
      if sHeader == "y":
        aValueColumns = [df.columns[i] for i in eval("[" + pivotArray[2] + "]")]
      else:
        aValueColumns = [i for i in eval("[" + pivotArray[2] + "]")]   
    # aggfunc info
    if len(pivotArray) - 1 > 2:
      aAggFunc = []
      for sValue, sAgg in zip(aValueColumns, pivotArray[3].split(",")):
        aAggFunc.append('"{}":[{}]'.format(sValue, sAgg.replace('-', ',')))
        
    tempdf = copy.copy(df)
    
    # pdb.set_trace()
    # convert all value columns into floats (remove commas, $, etc)
    
    for item in aAggFunc:
      # pdb.set_trace()
      
      if item.split(':')[1] != '[NS_concat]' and item.split(':')[1] != '[NS_concatU]':
        if sHeader == "y":
          tempdf[item.split(':')[0].replace('"', '')] = tempdf[item.split(':')[0].replace('"', '')].apply(money_to_float)
        else:
          tempdf[int(item.split(':')[0].replace('"', ''))] = tempdf[int(item.split(':')[0].replace('"', ''))].apply(money_to_float)
    # 33  2,36 np.sum,NS_concatU
    # pdb.set_trace()
    # NS_concat test
    # pivotdf = pd.pivot_table(tempdf, index=aIndexColumns, columns=None, values=['ORIGINAL GROSS AMT', 'MERCHANT NAME'], aggfunc={"ORIGINAL GROSS AMT":[NS_concat], "MERCHANT NAME":[np.sum]}, fill_value=0)

    if sHeader == "y":
      sCommand = 'pivotdf = pd.pivot_table(tempdf, index=' + str(aIndexColumns) + ', columns=' + ('None' if len(aColumnColumns) == 0 else str(aColumnColumns)) + ', values='+ ('None' if len(aValueColumns) == 0 else str(aValueColumns)) +', aggfunc={' + ', '.join(['%-2s' % (i,) for i in aAggFunc]) + '}, fill_value=0)'
    else:
      sCommand = 'pivotdf = pd.pivot_table(tempdf, index=' + str(aIndexColumns) + ', columns=' + ('None' if len(aColumnColumns) == 0 else str(aColumnColumns)) + ', values='+ ('None' if len(aValueColumns) == 0 else str(aValueColumns)) +', aggfunc={' + ', '.join(['%-2s' % (i.replace('"', ''),) for i in aAggFunc]) + '}, fill_value=0)'
    
    exec(sCommand)
    print("\n" + str(pivotdf))
    print("\nThe '" + sPivotArray + "' pivot table's python code is:\n\n " + sCommand + "\n")

    csv_buffer = StringIO()
    pivotdf.to_csv(csv_buffer, header=True, index=True, sep='\t' )
    pyperclip.copy(csv_buffer.getvalue())
  else:
    pdb.set_trace()
    