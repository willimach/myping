# myping
ping different server with raspberry pi to check whether internet at home works or not.
server are pinged every second. information about status is written in a logfile.
Once every hour the Date, Start and end time of offline times get extracted in a seperate file. 
Via matplotlib a plot of the offline times is generated and loadet on a webserver via ftp to view plot.
