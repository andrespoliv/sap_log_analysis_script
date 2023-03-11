<h1>SAP Log analysis script</h1>

<p>This is a script made to read and process 4 types of SAP information and output the results in a CSV format.</p>

<h2>Type of information supported</h2>
<ul>
    <li>Role assignment: information from table AGR_DEFINE</li>
    <li>User lock activity: information from report RSUSR100N</li>
    <li>Table activity: information from table DBTABLOG</li>
    <li>User status and credentials: information from table USR02</li>
</ul>

<h2>Installation</h2>

<code>pip install -r requirements.txt</code>

<h2>Usage</h2>
<p>NOTE: Before usage, fill up all of the .txt files with the corresponding data.</p>
<code>python log_search.py --help</code>
<p>Type this to list all of the parameters:</p>
<code>python log_search.py --help</code>
<p>For role assignment use a command like this:</p>
<code>python .\log_search.py -f "/filepath" -enc utf16 -sH 3 -eH 17128 -g role_assignment</code>
<p>For User lock activity use a command like this:</p>
<code>python .\log_search.py -f "/filepath" -enc cp1252 -sH 20 -eH 38501 -g user_change</code>
<p>For table activity use a command like this:</p>
<code>python .\log_search.py -f "/filepath" -enc utf8 -sH 3 -eH 700000 -g datalog_table</code>
<p>For User status and credentials use a command like this:</p>
<code>python .\log_search.py -f "/filepath" -enc cp1252 -sH 3 -eH 11018 -g user_logon</code>