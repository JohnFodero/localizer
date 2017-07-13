from subprocess import check_output

while True:
    print(check_output('sudo iw dev wlan0 scan | egrep "signal|^BSS" | sed -e "s/\\tsignal: \(-[0-9]\{2\}\).*/\\1/" -e "s/^BSS \([0-9a-z:]\{17\}\)(on wlan0).*/\\1/" | awk \'{ORS = (NR % 2 == 0)? "\\n" : " "; print}\'', shell=True).decode())


