#!/bin/bash

cookie=`php ser.php` 

curl -v 'http://localhost:5588/index.php' -H "Cookie: my-session=$cookie"
