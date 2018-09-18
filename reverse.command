python3 -c "from io import StringIO ; import pandas ; import pyperclip; import sys ; df=pandas.read_csv(StringIO(pyperclip.paste()), sep='\t') ; df = df[df.columns[::-1]] ; csv_buffer = StringIO() ; df.to_csv(csv_buffer, index=False, sep='\t' ) ; pyperclip.copy(csv_buffer.getvalue())" 
osascript -e 'tell application "Terminal" to close first window' & exit