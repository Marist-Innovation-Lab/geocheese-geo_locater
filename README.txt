0. Pull latest changes. Major Refactoring (2017-08-05)

1. Download and Install Pycharm (This will make handling packages much easier)

2. Download Microsoft Visual C++ Compiler for Python 2.7 -> https://www.microsoft.com/en-us/download/details.aspx?id=44266 

3. Download Microsoft Visual Studio Build Tools -> https://www.visualstudio.com/downloads/#build-tools-for-visual-studio-2017

4. Download the necessary packages (geocoder, geoip2, urllib3)
    * Recommend installing packages from Pycharm, this will make your life easier
      File->Settings->Project:<Name of Project>->Project:Interpreter->Select Interpreter->Click the "+" symbol
    * If not then run the following command, replace name where appropriate -> "python -m pip install <package name>"

5. Run command "python setup.py install" in directory with geo_cheese setup.py file

6. After changes are made to the files in the module run command "python setup.py develop" 

7. How to use module, after install:
    * from geo_cheese import find_loc
    * Example Usage: find_loc("local_dbs/GeoLite2-City.mmdb", "local_dbs/GeoIP2-ISP.mmdb", "40.75.116.161")
    * Generic Usage: find_loc(<Location of GeoLite2-City File>, <Location of GeoIP2-ISP File>, <IP Address>)


 `````````````````````````````````````````````````````````          `````````````````````````````````
```````````````````````````````````````````````````                   ``````````````````````````````
`````````````````````````````````````````````                ``          ```````````````````````````
````````````````````````````````````````               `.:/+ssss+:`         ````````````````````````
```````````````````````````````````              `.:/ossso+//::/+oso:.         `````````````````````
```````````````````````````````             `-/+ssso+//:::::::::::/+oso/.         ``````````````````
``````````````````````````             `-/+ssoo+/::::/++ooooo++/::::::+oso:`        ````````````````
```````````````````````           `-:+ssoo+/:::::::/ooo+++++++oo+::::::::+oso:`        `````````````
`````````````````````         `-/osso+/:::::::::::/oo+++++++++++o+:::::::::/+ss+.        ```````````
```````````````           .:+sso+/:::::::://///:::/oo++/////////o+::::::::::::/oso:`       `````````
```````````              /ss+/:::::::::/+ooooooo+::/oo+//////++o+::::::::::::::::+ss/.        ``````
````````                 .ss:::::::::::oo+++++++o+:::/++ooooo+/::::::::::::::::::::/oso-        ````
````          `-/o/.```.:ss/:::::::::::+oo+////oo/:::::::::::::::::::::::::::::::::::/oso-       ```
```        .:osso+ossssso+::::::::::::::/+oooo++:::::::::::::::::::::::::::::::::::::::/+ss:       `
``      -/sso+/::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::/+ss`     `
`     `sso/::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::://///+++++o+++++///os:     `
`     :so///+++++++++++oooooooooooooo++++++++++++++++++++oooooooooooooooooo+++++///////////+s+      
      os+////////////////////////+++++++++++++++++++++++++++///////////////////////////////+ss      
     `ss/////////////////+++/////////////////////////+ooo+///////+oosooooo+/////////////////ss`     
     .ss/////////////+osooooosoo///////////////////+sooooos+///+soooooooooos+///////////////ss.     
     -so///////////osoooooooooooso/////////////////oo++++/oo//+soooooooooooos+//////////////ss-     
     :so//////////osoooooooooooooso////////////////+s+///+s+//+sooooooooooooso//////////////os:     
     /so/////////+s++ooooooooooooos+/////////////////+ooo+////+s++ooooooo++/so//////////////os:     
     /so/////////+s+/+oooooooooo++s+//////++ooo++//////////////+s+/////////oo///////////////os:     
     :so//////////oo////++++++///oo/////+ssoooooss+//////////////ooo++++ooo+////////////////os:     
     -so///////////os+/////////+so/////osoooooooooso////////////////+++++///////////////////os-     
     .ss////+ooooo///oooo+++oooo//////+s+oooooooooos+//////////////////////+ooooo+//////////ss.     
     `ss///osooooos/////+++++/////////+s///++++++//s+/////////////////////osoooooos+////////ss`     
      os+//so//+++s+///////////////////os/////////so//////////////////////so+oo++/s+///////+so      
`     /so//+oo++os+/////////////////////+oo+++++oo+/////////+ooooo+///////+s+///+oo////////+s/     `
`     .ss/////+++//////////////////////////+++++//////////oss/:-:/sso///////+ooo++/+++++oooss-     `
`      osoo++++++++//////////////////////////////////////os/       /so+ooooosssssssoo+//::--.      `
``     `::///+++ooosssssssssssssssssssssssssssssssssssssss+         :+//::--..``                  ``
``                       `````........................````                                       ```
````                                                                                      ``````````
`````````                                                     `````          ```````````````````````
