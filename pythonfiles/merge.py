from io import StringIO
import pandas as pd
import pyperclip; import sys
import pdb # pdb.set_trace() ;;; 'continue' proceeds, 'next' steps
import re
import numpy as np

# fuzz is used to compare TWO strings
from fuzzywuzzy import fuzz
# process is used to compare a string to MULTIPLE other strings
from fuzzywuzzy import process



def copydf(df):
  csv_buffer = StringIO()
  df.to_csv(csv_buffer, header=True, index=True, sep='\t' )
  pyperclip.copy(csv_buffer.getvalue())
  return "Done." 

def NS_concatU(x):
    # pdb.set_trace()
    return "%s" % ', '.join(x.drop_duplicates().apply(str))

def get_ratio(row):
    pdb.set_trace()
    name = row[0]
    return fuzz.token_sort_ratio(name, "TFR Color Glow Pro Roc KC")
    
    
matchingLogic = input('\n\nExact match ("m" or "m1" or default / enter)\nor multi-column match ("m2", "m3", etc)\nor fuzzywuzzy match ("f", "f3", "f10", etc)\nor unmatch/left-outer ("u") or full-outer ("o") between both tables? \n>  ')

if (matchingLogic.startswith('f')):
  sNumOfFuzzyMatches = matchingLogic.replace('f', '')
  matchingLogic = "f"

  if (sNumOfFuzzyMatches == ""):
    sNumOfFuzzyMatches = "3"
  iNumOfFuzzyMatches = int(sNumOfFuzzyMatches)

if matchingLogic == "f":
  matchingLogic = "fw"

if matchingLogic == "fw":
  # sRatioNum = input("what ratio of confidence? eg 50, 90, etc: ")
  sRatioNum = "50"

sFirstTable = input('Please copy first (left) table (ie just one column - where blanks are not okay (if fuzzywuzzy) and duplicates are meh okay but whatever)\n and \'r\' to reverse columns,  then press Enter \n>  ')

df=pd.read_csv(StringIO(pyperclip.paste()), sep='\t', header=None)

if sFirstTable == "r":
  df = df[df.columns[::-1]]
  print("columns reversed!")

# drop all rows with missing values
df = df.dropna(how='all')
df = df.replace(np.nan, '', regex=True) # added this in 2020-03 
#pdb.set_trace()
# TRIM ALL? CELLS!
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

if df.shape[1] > 1 and matchingLogic == "fw":
  bMultiColumnDF = False
  df[1] = df[0]
  
  meltMultiColumnIndexIntoSingleColumnIndex = input("Whoa there, multi-column for fuzzy detected...do you want to melt into a single column (removing blanks ofc) and assume this columns is the primary index? Y/n - ")
        
  if meltMultiColumnIndexIntoSingleColumnIndex == "y" or meltMultiColumnIndexIntoSingleColumnIndex == "Y":                      
      #print("Multi-column for fuzzy detected; melting now, removing blanks now, and assuming first column is the primary index...\n")
      bMultiColumnDF = True
      lValueVars = df.columns.tolist()
      pass #lol
      originalDF = df.copy()
      df['index'] = df[0]
      df = df.melt(id_vars=['index'], value_vars=lValueVars)
  
  df = df.dropna()

  if meltMultiColumnIndexIntoSingleColumnIndex == "y" or meltMultiColumnIndexIntoSingleColumnIndex == "Y":                      
      df.columns = [1, 'variable', 0]
      df = df.drop(['variable'], axis=1)
      df = df[[0,1]] # re-order the columns
                                                    
else:
  bMultiColumnDF = False

if df.shape[1] == 1:
   df[1] = df[0]

# pdb.set_trace()

if (matchingLogic == "f"):
  for index, row in df.iterrows():
    # UPPERCASE EVERYTHING
    
    # pdb.set_trace()
    
    row[0] = row[0].upper()  
  
    # custom fuzzy logic for Innova
    #row[0] = re.sub('GOLF DISC', 'DISC', str(row[0])).upper()

    #row[0] = re.sub('ASSORTED', 'ASRT', str(row[0]))
    #row[0] = re.sub('150', '0050', str(row[0]))
    #row[0] = re.sub('151-159', '5159', str(row[0]))
    #row[0] = re.sub('160-164', '6064', str(row[0]))
    #row[0] = re.sub('165-169', '6569', str(row[0]))
    #row[0] = re.sub('170-172', '7072', str(row[0]))
    #row[0] = re.sub('173-175', '7375', str(row[0]))
    #row[0] = re.sub('150', '0050', str(row[0]))
    #row[0] = re.sub('151-164', '5164', str(row[0]))
    #row[0] = re.sub('165-169', '6569', str(row[0]))
    #row[0] = re.sub('170-174', '7074', str(row[0]))
    #row[0] = re.sub('175-177', '7577', str(row[0]))
    #row[0] = re.sub('178-180', '7880', str(row[0]))
     
    # UPPERCASE EVERYTHING AND GET RID OF NON-ALPHANUMERICS
    #drow[0] = re.sub('[^0-9a-zA-Z]+', '', str(row[0])).upper()


csv_buffer = StringIO()
df.to_csv(csv_buffer, header=False, index=False, sep='\t' )
pyperclip.copy(csv_buffer.getvalue())

# pdb.set_trace()
if df.shape[0] > df.drop_duplicates(subset=[df.columns[0]], keep='first').shape[0]:
  print("\nDuplicates (and/or empty cells?) found in first column; grouping them and NS_CONCATUing the other columns now...\n")
  # pdb.set_trace()
  # f = {df.columns[1]: lambda x: "%s" % ', '.join(x.apply(str))}
  f = {df.columns[1]: lambda x: "%s" % ', '.join(x.drop_duplicates().apply(str))}
  df = df.groupby(df.columns[0]).agg(f)
  df.reset_index(level=df.index.names, inplace=True)
  csv_buffer = StringIO()
  df.to_csv(csv_buffer, header=False, index=False, sep='\t' )
  pyperclip.copy(csv_buffer.getvalue())

input('Please copy second (right) table (ie one column, the values being a foreign key of the previous table\'s primary key; duplicates ARE ok, blanks are okay). then press Enter  \n>  ')

# pdb.set_trace()
# skip_blank_lines=0
df2=pd.read_csv(StringIO(pyperclip.paste()), sep='\t', header=None, skip_blank_lines=0)
# replace all NaNs with blanks since NaN is fuzzy-matched with 'Name" lol..
df2 = df2.replace(np.nan, '', regex=True)
df2 = df2.applymap(lambda x: x.strip() if isinstance(x, str) else x)
# drop all rows with missing values
# df2 = df2.dropna(how='all') - doesnt seem to do shit?
# what's the difference between dropna and skip_blank_lines=false?  dunno!
# pdb.set_trace() df = df.replace(np.nan, '', regex=True)

# CONVERT FIRST COLUMN CELLS TO STRING
df2[df2.columns[0]].astype(str)
df[df.columns[0]].astype(str)

# pdb.set_trace()
if df2.shape[1] == 1:
   df2[1] = df2[0]

#npdb.set_trace()

df = df.astype(str)
df2 = df2.applymap(str)

if (matchingLogic == "f"):
  pass 
  # for index, row in df2.iterrows():
     # row[0] = re.sub('[^0-9a-zA-Z]+', '', row[0]).upper()

if (matchingLogic == "fw"):

  # pdb.set_trace()
  df3 = pd.DataFrame()
  # df3 = df3.append({"0": sValueToAppend},ignore_index=True)
  
  for row0 in df2.iloc[0:,1]:
    # pdb.set_trace()
    if row0 == '':
      df3 = df3.append({"0": "", "1": ""},ignore_index=True)
    else:   
      dfAppliedLambda = df.apply(lambda row: fuzz.token_sort_ratio(row[0], row0), axis=1)
      df8 = df.copy()
      df8[2] = dfAppliedLambda
      df8 = df8.sort_values([2], ascending=0)
    
      sValueToAppend = ""

      if bMultiColumnDF:
        # pdb.set_trace()
        # COMBINE duplicates in d8 so that the iNumOfFuzzyMatches number of fuzzy matches doesn't display redundant values
        # COMMENT OUT THE CODE BELOW, or add "if bMultiColumnDF", IF IT CAUSES ANY ISSUES
        # pdb.set_trace()
        # TOO SLOW? COMMENT OUT THE CODE BELOW ... #
        df8 = df8.pivot_table(values=[0,2], index=[1], aggfunc=[NS_concatU, np.max]).reset_index()
        # df8.columns = ["blah", 0, "blah2", 1, 2]
        df8.columns = [1, 0, "blah2", "blah", 2]
        df8 = df8[[0,1,2]]
        df8 = df8.sort_values([2], ascending=0)
 
      for rowbleh in df8.iloc[:iNumOfFuzzyMatches].iterrows():
        # sValueToAppend += str(fuzz.token_sort_ratio(row0, rowbleh)) + " " + rowbleh + "    "
        # sValueToAppend += rowbleh[1][2] + " " + rowbleh + "    "
        # pdb.set_trace()
        if bMultiColumnDF:
          # pdb.set_trace()
          sValueToAppend += str(rowbleh[1][2]) + "%=>" + rowbleh[1][0] + "/" + rowbleh[1][1] + "             "
        else: 
          sValueToAppend += str(rowbleh[1][2]) + "%=>" + rowbleh[1][1] + "             "
      # pdb.set_trace()
      # df8.iloc[0][1] vs df8.iloc[0][0]
      df3 = df3.append({"0": df8.iloc[0][1], "1": sValueToAppend},ignore_index=True)
 
  csv_buffer = StringIO()
  df3.to_csv(csv_buffer, header=False, index=False, sep='\t' )
  pyperclip.copy(csv_buffer.getvalue())
elif (matchingLogic == "u" or matchingLogic == "o"):
  # pdb.set_trace()
  df3 = pd.merge(df, df2, on=[0], how="outer", indicator=True ).query('_merge=="right_only"') #right_only vs left_only vs both
  df3.dropna()
  df3 = df3.drop(['1_x', '_merge'], axis=1)
  df3.rename(columns={ df3.columns[0]: "right_outer" }, inplace = True)

  df4 = pd.merge(df, df2, on=[0], how="outer", indicator=True ).query('_merge=="left_only"') #right_only vs left_only vs both
  df4.dropna()
  df4 = df4.drop(['1_y', '_merge'], axis=1)
  df4.rename(columns={ df4.columns[0]: "left_outer" }, inplace = True)

  csv_buffer = StringIO()
  #df3.to_csv(csv_buffer, header=True, index=False, sep='\t' )
  pd.DataFrame(df3[df3.columns[0]]).to_csv(csv_buffer, header=True, index=False, sep='\t' )

  csv_buffer2 = StringIO()
  # df4.to_csv(csv_buffer2, header=True, index=False, sep='\t' )
  pd.DataFrame(df4[df4.columns[0]]).to_csv(csv_buffer2, header=True, index=False, sep='\t' )

  if (matchingLogic == "o"):
    pyperclip.copy(csv_buffer2.getvalue() + "\n\n" + csv_buffer.getvalue())
  else:
    pyperclip.copy(csv_buffer2.getvalue())

  pass
elif (matchingLogic == "o"):
  # pdb.set_trace()
  df3 = pd.merge(df, df2, on=[0], how="outer", indicator=True ) # .query('_merge=="outer"') #right_only vs left_only vs both
  df3.dropna()
  # df3 = df3.drop(['1_x', '_merge'], axis=1)

  csv_buffer = StringIO()
  df3.to_csv(csv_buffer, header=False, index=False, sep='\t' )
  pyperclip.copy(csv_buffer.getvalue())
  pass
else:
  # pdb.set_trace()
  # If left_on and right_on are same a and b, can we use on = ['a', 'b']?
  # df8 = df2.iloc[0:2,0:].append(df2.iloc[4:,0:])
  # pdb.set_trace()
  # NEED TO OBVIOUSLY FIX THE CODE BELOW
  # df['year']=df['year'].astype(int)
  # pdb.set_trace()
  # pdb.set_trace()

  df[0]=df[0].astype(str)
  df[1]=df[1].astype(str)
  df2[0]=df2[0].astype(str)
  df2[1]=df2[1].astype(str)
  # pdb.set_trace()
  
  df3 = df2.merge(df, on=[df.columns[0]], how='left', sort=False)
  df3.dropna()

  # DOING SOME CRAZY RE-ARRANGEMENT
  #print("The length is " + str(df3.shape[1]))
  #q = list(reversed(range(2,df3.shape[1])))
  #print(q)
  #a = []
  #b = [a.append(df3.columns[i]) for i in q]
  #if len(a) == 0:
  #  a = [df3.columns[1]] 
  # DUPLICATED CODE BELOW: df3[a].to_csv(csv_buffer, header=False, index=False, sep='\t' )


  # VS DROPPING FIRST COLUMN
  df3 = df3.drop(df3.columns[0], axis=1)

  # NOW: PRINT AND COPY MERGED DATA
  print(df3)
  csv_buffer = StringIO()
  df3.to_csv(csv_buffer, header=False, index=False, sep='\t' )
  # df3[a].to_csv(csv_buffer, header=False, index=False, sep='\t' )
  pyperclip.copy(csv_buffer.getvalue())
  
print("Okay the new table is now copied to your clipboard.  AND jik: writing mergeresults.tab now.  Have fun!")

file = open('mergeresults.tab', 'w')
file.write(csv_buffer.getvalue())
file.close()
