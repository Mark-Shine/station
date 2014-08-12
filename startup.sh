source ~/.bashrc
workon station
NAME="staion"
if [ ! -n "$NAME" ];then
    echo "no arguments"
    exit;
fi

echo $NAME
ID=`ps -ef | grep "$NAME" | grep -v "$0" | grep -v "grep" | awk '{print $2}'`
echo $ID
echo "################################################"
for id in $ID
do
kill -9 $id
echo "kill $id"
done
echo  "################################################"
uwsgi --ini /root/www/station/uwsgi_station.ini --daemonize /root/www/station/station.log