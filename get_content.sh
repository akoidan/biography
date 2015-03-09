#!/bin/sh

PROJECT_ROOT=`pwd`

cd $PROJECT_ROOT

wget https://raw.githubusercontent.com/twbs/bootstrap/master/dist/js/bootstrap.min.js -P $PROJECT_ROOT/akoidan_bio/static/
wget https://raw.githubusercontent.com/twbs/bootstrap/master/dist/css/bootstrap.min.css -P $PROJECT_ROOT/akoidan_bio/static/
wget http://code.jquery.com/jquery-2.1.3.min.js -O $PROJECT_ROOT/akoidan_bio/static/jquery.js
wget https://github.com/eternicode/bootstrap-datepicker/blob/master/dist/css/bootstrap-datepicker.min.css#L8 -P $PROJECT_ROOT/akoidan_bio/static/
wget https://raw.githubusercontent.com/eternicode/bootstrap-datepicker/master/dist/js/bootstrap-datepicker.min.js -P $PROJECT_ROOT/akoidan_bio/static/


