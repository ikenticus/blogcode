
for i in $(cat sport_181210); do
    go run main.go ~/repos/tasks/GoogleKeys/datastore-write-staging.json delete sport $i
done

