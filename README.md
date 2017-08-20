
# A simple moodle analyser, way to use:

## requirements.txt 

for python virtualenv migration

## 1-10 python script 

are demos for data visualization, starting point

## amended_urls.py 

for manually add new eventname's hyperlink templates, which I did not extract thoroughly because there are plenty of them and hardcoded in moodle's source code. I choose to print eventnames that do not have templates so far, and since these urls relate to the url column of dataframe, if you dont need this column for your analysis or plotting, just ignore the warning and need not rerun

## init.py 

is core data munging lib

## event_files_list.cpklz

do not need to re-generated, clone and use it if your moodle version is around 3.1

## urls.cpklz

the url templates file, clone and use it if your moodle version is around 3.1

## plots_register.py

add more extended data processing functions here

## data folder

place for all processed data, only for quick presentation of visualization, no need to clone them(but must have this folder and keep its hierarchy!), just generate your own

## out folder

place for all plotting results, only for quick presentation of visualization, no need to clone them(but must have this folder and keep its hierarchy!), just generate your own

## misc folder

some resources used, must have this folder and keep its hierarchy if you want to test the plottings
