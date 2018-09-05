read N
if [ $[N % 2] -eq 1 -o $N -ge 6 -a $N -le 20 ]; then
    echo 'Weird'
else
    echo 'Not Weird'
fi
