from io import StringIO
import pandas as pd
import pyperclip; import sys
import numpy as np
import pdb
import re
import copy
import time
import functools
import readline # for up arrow history functionality
from collections import Counter

def melt_df(df, aColumns):
  pass
  pass
  # [elem for elem in aColumns if elem not in [aColumns[3], aColumns[4]]]
  # convert strings to ints
  # pdb.set_trace()
  dfColumns = df.columns.to_list()
  aColumns = list(map(lambda x: int(x), aColumns)) 
  a_id_vars = [elem for elem in dfColumns if elem not in list(map(lambda x: dfColumns[x], aColumns)) ]
  return df.melt(id_vars=a_id_vars)

def explode_df(df, iIndexToExplode, sDelimiter):
  ## explode_df(df, 0, '; ')
  ##iIndexToExplode = 1
  ##sDelimiter = "; "
  ## pdb.set_trace()
  #aColumns = list(df.columns)
  #del aColumns[iIndexToExplode]
  ## explode
  #explosion_df = pd.DataFrame(df[df.columns[iIndexToExplode]].str.split(sDelimiter).tolist(), index=[ df[element] for element in aColumns ]).stack()
  #explosion_df = explosion_df.reset_index([0] + aColumns)
  ## re-arrange columns
  #aNewColumns = explosion_df.columns.tolist()
  #del aNewColumns[len(aNewColumns)-1]
  #aNewColumns.insert(iIndexToExplode, 0)
  #explosion_df = explosion_df[aNewColumns]
  #explosion_df.rename(columns = {0 : df.columns.to_list()[iIndexToExplode] + " EXPLODED"}, inplace = True) 
  iIndexToExplode = [int(elem) for elem in iIndexToExplode]
  #pdb.set_trace()
  exploding_df = df.T.T
  for i in iIndexToExplode:
    exploding_df = unnesting(exploding_df, [i], sDelimiter)
  return exploding_df

def unnesting(df, aColumns, sDelimiter):
    # pdb.set_trace()
    dfcopy = copy.copy(df)
    for i in aColumns:
        dfcopy[dfcopy.columns[i]] = dfcopy[dfcopy.columns[i]].astype(str).str.split(sDelimiter)
    aColumns = list(map(lambda x: dfcopy.columns.to_list()[x], aColumns))
    idx = dfcopy.index.repeat(dfcopy[aColumns[0]].str.len()) # index of rows
    df1 = pd.concat([pd.DataFrame({x: np.concatenate(dfcopy[x].values)}) for x in aColumns], axis=1)
    df1.index = idx
    df999 = df1.join(df.drop(aColumns, 1), how='left')
    aRearrangeColumns = df999.columns.to_list()[1:]
    aRearrangeColumns.insert ( df.columns.get_loc(aColumns[0]), aColumns[0])
    df999 = df999[aRearrangeColumns]
    return df999

def copy_df(df):
  copy_df_to_clipboard(df, True)

def copy_df_to_clipboard(df, indexTrueOrFalse):
  csv_buffer = StringIO()
  df.to_csv(csv_buffer, header=True, index=indexTrueOrFalse, sep='\t' )
  pyperclip.copy(csv_buffer.getvalue())
  print("Copied to Clipboard.\n")
  return "Copied to Clipboard.\n" 

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
    except Exception as e:
      # might need to program NS_concat, NS_concatU, and intersection differently in lines far, far below
      pdb.set_trace()
      
def NS_concat(x):
    # pdb.set_trace()
    return "%s" % ', '.join(x.apply(str))

def NS_concatU(x):
    # pdb.set_trace()
    return "%s" % ', '.join(x.drop_duplicates().apply(str))

# intersection is VERY EXPERIMENTAL, NOT WORKING CONSISTENTLY, NEED TO COME UP WITH MORE TEST CASES IN PANDAS TESTING SPREADSHEET, JAVASCRIPT VERSION OF THIS IS BETTER!
def intersection(x):
    # pdb.set_trace()
    # [i for i in list1 if i in list2]
    # list comprehensions
    # return ''.join(functools.reduce(lambda a,b: [i for i in a if i in b], [list(words) for words in x]))
    # [j for j in [i for i in y[1] if i in y[0]] if j in y[1]]
    try:
      sReturn = ''.join(functools.reduce(lambda a,b: [j for j in [i for i in a if i in b] if j in a], [list(words) for words in x]))
    except Exception as e:
      sReturn = e
    return sReturn
    # ''.join(functools.reduce(lambda a,b: [j for j in [i for i in a if i in b] if j in b], [list(words) for words in ['test', 'tes']]))
    # ''.join(functools.reduce(lambda a,b: [j for j in [i for i in b if i in a] if j in [k for k in a if k in b]], [list(words) for words in x]))

def sample10(x):
    # pdb.set_trace()
    x = pd.Series(x.apply(str).unique())
    if (len(x) < 10):
      iSampleSize = len(x)
      sReturn = ", ".join(x)
    else:
      iSampleSize = 10
      sReturn = ", ".join(x.sample(n=iSampleSize, replace=True))
    return sReturn
    # return ''.join(functools.reduce(lambda a,b: [j for j in [i for i in a if i in b] if j in a], [list(words) for words in x]))



# date code
# df.[df.column[0]] = pd.to_datetime(df.[df.column[0]])
# df.query('B==3')['A']asdfsdfdsaf
print("Never forget: df.iloc[:,:] is the same as df!\n")
print('Please copy the table/dataframe into your clipboard.\n')
sHeader = input("Is the first row header? y/n (default y) \n\t > ")
if sHeader != "n":
  sHeader = "y"
# sHeader = input("Is the first row header? y/n ")

# CLIPBOARD DATA
# pdb.set_trace()
df=pd.read_csv(StringIO(pyperclip.paste()), dtype=str, sep='\t', header=list(map(lambda x: 0 if x == 'y' else None, sHeader))[0])
df.dropna(how='all')
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
if df.columns.to_list()[0] == "Unnamed: 0":
  df = df.rename(columns={"Unnamed: 0": "custom_index"})
  df = df.set_index('custom_index')
  print("\n\nfirst cell in clipboard was blank, therefore setting this first column as the index!\n\n")
# TEST DATA
# df=pd.read_csv(StringIO("\nAccount	Name	Rep	Manager	Product	Quantity	Price	Status\n714466	Trantow-Barrows	Craig Booker	Debra Henley	CPU	1	30000	presented\n714466	Trantow-Barrows	Craig Booker	Debra Henley	Software	1	10000	presented\n714466	Trantow-Barrows	Craig Booker	Debra Henley	Maintenance	2	5000	pending\n737550	Fritsch, Russel and Anderson	Craig Booker	Debra Henley	CPU	1	35000	declined\n146832	Kiehn-Spinka	Daniel Hilton	Debra Henley	CPU	2	65000	won\n218895	Kulas Inc	Daniel Hilton	Debra Henley	CPU	2	40000	pending\n218895	Kulas Inc	Daniel Hilton	Debra Henley	Software	1	10000	presented\n412290	Jerde-Hilpert	John Smith	Debra Henley	Maintenance	2	5000	pending\n740150	Barton LLC	John Smith	Debra Henley	CPU	1	35000	declined\n141962	Herman LLC	Cedric Moss	Fred Anderson	CPU	2	65000	won\n163416	Purdy-Kunde	Cedric Moss	Fred Anderson	CPU	1	30000	presented\n239344	Stokes LLC	Cedric Moss	Fred Anderson	Maintenance	1	5000	pending\n239344	Stokes LLC	Cedric Moss	Fred Anderson	Software	1	10000	presented\n307599	Kassulke, Ondricka and Metz	Wendy Yule	Fred Anderson	Maintenance	3	7000	won\n688981	Keeling LLC	Wendy Yule	Fred Anderson	CPU	5	100000	won\n729833	Koepp Ltd	Wendy Yule	Fred Anderson	CPU	2	65000	declined\n729833	Koepp Ltd	Wendy Yule	Fred Anderson	Monitor	2	5000	presented"), sep='\t', header=list(map(lambda x: 0 if x == "y" else None, sHeader))[0])

# remove empty rows dont need dat shit
df = df.dropna(how='all')

tempdf = df.T.T
tempdf.columns = [str(a) + " " + b for a,b in zip(list(range(0, len(df.columns))), df.columns) ]
print(tempdf)
print("["+str(len(tempdf.axes[0])) + " rows x " + str(len(tempdf.axes[1])) + " columns]")

# print dataframe with index'd columns:
# df.columns = [str(a) + " " + b for a,b in zip(list(range(0, len(df.columns))), df.columns) ]

pivotArray = ["blah"]
processeddf = ""

def printstrdf(scoped_temp_df):
    print("\n" + str(scoped_temp_df))
    print("\n["+str(len(scoped_temp_df.axes[0])) + " rows x " + str(len(scoped_temp_df.axes[1])) + " columns]")

while pivotArray != "":
  sPrompt = "\n\nEnter Your IndexColumns ColumnColumns ValueColumns aggValues? "
  sPrompt += "\n ex: "
  sPrompt += "\n\t 0,1 2,3 6,5 np.sum,len "
  sPrompt += "\n\t 3,7 4 5,6 len,np.sum-np.mean "
  sPrompt += "\n\t 3,7 4 5 np.sum "
  sPrompt += "\n\t 1  0 listaggU-len "
  sPrompt += "\n\t 0  1 intersection-listaggU "
  sPrompt += "\n\t explode 0 \"; \" "
  sPrompt += "\n\t melt 0,1,4 "
  sPrompt += "\n\t unique "
  sPrompt += "\n\t uniquec "
  sPrompt += "\n\t provision "

  print(sPrompt)
  sPrompt = "\n\n\n  > "
  sPivotArray = input(sPrompt)
  sPivotArray = sPivotArray.replace("listagg", "NS_concat").strip()
  pivotArray = sPivotArray.split(" ")
  # 0,1 2,3 3,6,7,8 -> [0, 1], [2, 5], [3, 6, 7, 8]]

  df = df.dropna(how='all')
  # if pivotArray[0] == "df" or pivotArray[0].strip() == "":
  #  print("\n" + str(df))
  #  pass
  # pdb.set_trace()
  if pivotArray[0] == "unique" or pivotArray[0] == "uniquep" or pivotArray[0] == "u" or pivotArray[0] == "uniquesort" or pivotArray[0] == "usort":

    pass
    sCommand = sPivotArray
    # pdb.set_trace()

    if (len(pivotArray) > 1):
      if pivotArray[1][0:1] == "-":
        pivotArray[1] = ",".join([str(a) for a in list(range(0,len(df.columns))) if a not in   [int(b) for b in pivotArray[1][1:].split(",")]    ])
      if pivotArray[1][0] == "*":
        pivotArray[1] = ",".join([str(a) for a in list(range(0, len(df.columns)))])

      # conosider INVERSE function - df[df.columns[ [ a for a in list(range(0,len(unique_df0.columns))) if a not in [ int(a) for a in pivotArray[1].split(',') ] ] ]]
      unique0 = df[df.columns[   [ int(a) for a in pivotArray[1].split(',') ]   ]]
      # consider changing to df.groupby(df.columns.to_list())
    else:
      unique0 = df.T.T
    # count is whatever
    sCountColumn = 'count' + ''.join([ '_' for i in re.findall("count", ';'.join(unique0.columns)) ])
    unique_df = unique0.groupby([unique0.columns[i] for i in range(0, len(unique0.columns))]).size().reset_index(name=sCountColumn )

    if pivotArray[0] == "uniquesort" or pivotArray[0] == "usort":
      # # for some reason for combinations the last column is a random integer so I need to make sure it is 'count'
      # df = df.rename(columns={ df.columns[df.shape[1]-1]: "count" })
      # df.columns = [0,1,'count']
      unique_df = unique_df.sort_values(by=sCountColumn, ascending=False)

    printstrdf(unique_df)
    copy_df_to_clipboard(unique_df, False)

    #csv_buffer = StringIO()
    #unique_df.to_csv(csv_buffer, header=True, index=False, sep='\t' )
    #pyperclip.copy(sCommand + "\n" + csv_buffer.getvalue())
    processeddf = copy.copy(unique_df)
  elif pivotArray[0] == "uniquec" or pivotArray[0] == "uc" or pivotArray[0] == "uniquecsort" or pivotArray[0] == "ucsort":
    # pdb.set_trace()
    print("\n renaming columns to integers because combinations don't care about columns \n\n")
    sCommand = sPivotArray
    pass
    unique_df = df.apply(Counter, axis='columns').value_counts()

    heck0 = []
    heck = []
    for blah in unique_df.index:
      for x in blah: heck = heck + ([x] *  blah[x])
      heck0.append(heck)
      heck = []
    
    # tempDF = pd.DataFrame([(key, value) for key, value in df.index])
    tempDF = pd.DataFrame(heck0)
    unique_df = pd.DataFrame(unique_df)
    unique_df = unique_df.reset_index(drop=True)
    #pdb.set_trace()
    tempDF[tempDF.shape[0]-1] = unique_df[unique_df.columns[0]]
    unique_df = tempDF

    if pivotArray[0] == "uniquecsort" or pivotArray[0] == "ucsort":
      # # for some reason for combinations the last column is a random integer so I need to make sure it is 'count'
      # df = df.rename(columns={ df.columns[df.shape[1]-1]: "count" })
      # df.columns = [0,1,'count']
      # unique_df = unique_df.sort_values(by='count', ascending=False)
      pass

    printstrdf(unique_df)
    copy_df_to_clipboard(unique_df, False)

    processeddf = copy.copy(unique_df)
  elif pivotArray[0] == "melt":
    pass
    sCommand = sPivotArray
    # pdb.set_trace() 
    if sCommand.strip() == "melt": # if strictly melt then: melt all columns!
    	# pass
    	sCommand = "melt " + ','.join(str(elem) for elem in list(range(0,len(df.columns))))
    	aColumns = sCommand.split(" ")[1].split(",")
    else:
      if sCommand.split(" ")[1][0:1] == "-": # '-'' means inverse the columns
        list0 = [str(x) for x in list(range(0,len(df.columns)))]
        list1 = sCommand.split(" ")[1][1:].split(",")
        sCommand = "melt " + ','.join([x for x in list0 if x not in list1])
        aColumns = sCommand.split(" ")[1].split(",")
      else:
    	  aColumns = sCommand.split(" ")[1].split(",")
    melted_df = melt_df(df, aColumns)
    #print(aColumns)
    printstrdf(melted_df)
    copy_df_to_clipboard(melted_df, False)
    #csv_buffer = StringIO()
    #melted_df.to_csv(csv_buffer, header=True, index=False, sep='\t' )
    #pyperclip.copy(sCommand + "\n" + csv_buffer.getvalue())
    processeddf = copy.copy(melted_df)
  elif pivotArray[0] == "explode":
    pass
    # pdb.set_trace()
    #sCommand = sPivotArray

    if pivotArray[1][0:1] == "-":
      #pivotArray[1][1:].split(",")
      #list(range(0,len(df.columns)))
      pivotArray[1] = ",".join([str(a) for a in list(range(0,len(df.columns))) if a not in   [int(b) for b in pivotArray[1][1:].split(",")]    ])
    if pivotArray[1] == "*":
      pivotArray[1] = ",".join([ str(a) for a in list(range(0,len(df.columns))) if a not in    [int(b) for b in pivotArray[1][1:].split(",")]      ])    
    #sCommand = "explode 0 \"; \""
    sCommand = " ".join(pivotArray)

    if ("\"" in sCommand):
      sDelimiter = re.search("\".*\"", sCommand).group()
    else:
      sDelimiter = sCommand.strip().split(" ")[2]
    # pivotArray[0]


    sDelimiter = sDelimiter.replace("\"", "")
    sCommandWithoutDelimiter = " ".join([sCommand.split(" ")[0], sCommand.split(" ")[1]])
    iIndexToExplode = sCommandWithoutDelimiter.split(" ")[1].split(",") # sCommand.replace(sDelimiter, "").strip().split(" ")[1]
    #print(iIndexToExplode)
    exploded_df = explode_df(df, iIndexToExplode, sDelimiter)
    exploded_df = exploded_df.replace(np.nan, '', regex=True)
    exploded_df = exploded_df.replace('^nan$', '', regex=True) # consider fixing this dumb hack to remove the string "nan"

    #print("\n" + str(exploded_df))
    #print("["+str(len(exploded_df.axes[0])) + " rows x " + str(len(exploded_df.axes[1])) + " columns]")
    
    printstrdf(exploded_df)
    copy_df_to_clipboard(exploded_df, False)

    #csv_buffer = StringIO()
    #exploded_df.to_csv(csv_buffer, header=True, index=False, sep='\t' )
    #pyperclip.copy(sCommand + "\n" + csv_buffer.getvalue())
    processeddf = copy.copy(exploded_df)
    # pdb.set_trace()
    
  elif pivotArray[0] == "pdb":
    print("Entering pdb.set_trace() now.  Remember within pdb you can type 'interact' to enter multi-line commands, and remember to escape debugger commands with '!' (eg !list('abc') ) \n\ndf.fillna('', inplace=True)\n- you're welcome.\n")
    pdb.set_trace()
  elif pivotArray[0] == "provision":
    pass
    # figure out what to do here?
    df = copy.copy(processeddf)
    copy_df_to_clipboard(df, False)
    # print("["+str(len(df.axes[0])) + " rows x " + str(len(df.axes[1])) + " columns]")
  elif pivotArray[0][:1].isdigit() or pivotArray[0] == "pivot": # else: # pivot
    # pdb.set_trace()
    # print("\n" + str(df))
    aColumnColumns = []
    aValueColumns = []

    if pivotArray[2] == "*":
      pivotArray[2] = ",".join([ str(a) for a in list(range(0,len(df.columns))) if a not in    [int(b) for b in pivotArray[:2] if b != '']      ])
    sCommand = " ".join(pivotArray)
    # Index columns
    # pdb.set_trace()
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
    # pdb.set_trace()
    if len(pivotArray) - 1 > 1:
      if sHeader == "y":
        aValueColumns = [df.columns[i] for i in eval("[" + pivotArray[2] + "]")]
      else:
        aValueColumns = [i for i in eval("[" + pivotArray[2] + "]")]   
    # aggfunc info
    if len(pivotArray) - 1 > 2:
      aAggFunc = []
      if (len(pivotArray[3].split(",")) == 1 and len(aValueColumns) > 1):
        #pivotArray[3] = ','.join([pivotArray[3]] * 4)
        pivotArray[3] = ','.join([pivotArray[3]] * len(aValueColumns))
      for sValue, sAgg in zip(aValueColumns, pivotArray[3].split(",")):
        aAggFunc.append('"{}":[{}]'.format(sValue, sAgg.replace('-', ',')))
        
    # df is the backup and tempdf is the working df because I am sometimes converting columns into floats for some aggregate functions.  df is the backup with all columns as strictly strings
    tempdf = copy.copy(df)

    # convert all value columns into floats (remove commas, $, etc)
    
    for item in aAggFunc:
      # pdb.set_trace()
      
      # NEED TO CONVERT THE COLUMNS INTO FLOATS IF AND ONLY IF THERE IS NO NS_CONCAT or intersection (ie text aggregation) taking place, might need to expand this out if mixed column types eg NS_CONCAT-np.mean or np.sum-NS_CONCAT
      # if item.split(':')[1] != '[NS_concat]' and item.split(':')[1] != '[NS_concatU]':
      # pdb.set_trace()
      if ('NS_concat' not in item.split(':')[1] and 'intersection' not in item.split(':')[1] and 'sample10' not in item.split(':')[1]):
        if sHeader == "y":
          # pdb.set_trace()
          tempdf[item.split(':')[0].replace('"', '')] = tempdf[item.split(':')[0].replace('"', '')].apply(money_to_float)
        else:
          tempdf[int(item.split(':')[0].replace('"', ''))] = tempdf[int(item.split(':')[0].replace('"', ''))].apply(money_to_float)
    # 33  2,36 np.sum,NS_concatU
    # pdb.set_trace()
    # NS_concat test
    # pivotdf = pd.pivot_table(tempdf, index=aIndexColumns, columns=None, values=['ORIGINAL GROSS AMT', 'MERCHANT NAME'], aggfunc={"ORIGINAL GROSS AMT":[NS_concat], "MERCHANT NAME":[np.sum]}, fill_value=0)

    # add , margins=True to the below for totals 
    if sHeader == "y":
      sCommand = 'pivotdf = pd.pivot_table(tempdf, index=' + str(aIndexColumns) + ', columns=' + ('None' if len(aColumnColumns) == 0 else str(aColumnColumns)) + ', values='+ ('None' if len(aValueColumns) == 0 else str(aValueColumns)) +', aggfunc={' + ', '.join(['%-2s' % (i,) for i in aAggFunc]) + '}, fill_value=0)'
    else:
      sCommand = 'pivotdf = pd.pivot_table(tempdf, index=' + str(aIndexColumns) + ', columns=' + ('None' if len(aColumnColumns) == 0 else str(aColumnColumns)) + ', values='+ ('None' if len(aValueColumns) == 0 else str(aValueColumns)) +', aggfunc={' + ', '.join(['%-2s' % (i.replace('"', ''),) for i in aAggFunc]) + '}, fill_value=0)'
    
    exec(sCommand)

    printstrdf(pivotdf)
    #print("\n" + str(pivotdf))
    #print("\n["+str(len(pivotdf.axes[0])) + " rows x " + str(len(pivotdf.axes[1])) + " columns]")

    print("\nThe '" + sPivotArray + "' pivot table's python code is:\n\n " + sCommand + "\n")

    # pdb.set_trace()
    
    # Flatten the columns if and only if the df's columns' tolist is a tuple (colummns are a "hierarchical index")
    # comment this out for vendor summary report only
    # pdb.set_trace()
    if str(type(pivotdf.columns.tolist()[0])) == "<class 'tuple'>":
      ind = pd.Index(['_'.join(map(str, e)) for e in pivotdf.columns.tolist()])
      pivotdf.columns = ind
    #     pass
    try:
      sJavascriptCommand = "aPivotInstructions = " + str([aIndexColumns, aColumnColumns, aValueColumns, sPivotArray.replace("NS_concat", "listagg").replace("np.sum", "sum").split(" ")[3].split(",")])
      # aPivotInstructions = [["Manager"], ["Rep"], ["Status"], ["listagg"]]
    except:
      sJavascriptCommand = "sJavascriptCommand - unable to generate"

    copy_df_to_clipboard(pivotdf, True)
    pyperclip.copy(sCommand + "\n" + sJavascriptCommand + "\n" + sPivotArray + "\n" + pyperclip.paste())
    #csv_buffer = StringIO()
    #pivotdf.to_csv(csv_buffer, header=True, index=True, sep='\t' )
    #pyperclip.copy(sCommand + "\n" + sJavascriptCommand + "\n" + sPivotArray + "\n" + csv_buffer.getvalue())
    #processeddf = copy.copy(exploded_df)
    # pyperclip.copy(sPivotArray + "\n\n" + csv_buffer.getvalue() + "\n\nRAW:" + str(pivotdf))
  else:
    printstrdf(df)
    copy_df_to_clipboard(df, False)
    #pdb.set_trace()
    #csv_buffer = StringIO()
    #df.to_csv(csv_buffer, header=True, index=True, sep='\t' )
    #pyperclip.copy(csv_buffer.getvalue())
    #csv_buffer = StringIO()
    #pivotdf.to_csv(csv_buffer, header=True, index=True, sep='\t' )
    #pyperclip.copy(sCommand + "\n" + sJavascriptCommand + "\n" + sPivotArray + "\n" + csv_buffer.getvalue())

    pass
