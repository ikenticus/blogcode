auth=$1
hash=$2
len=$(echo $hash | wc -c)
for i in $(seq $[len-1] -1 $[len/2]); do
    key=$(echo $hash | cut -c$i-)
    echo -e "\n\n\n--- $key"
    go run main.go $auth read SMGWPBlog $key
done
