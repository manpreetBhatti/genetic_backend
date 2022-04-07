## TODO
- [x] Genetic program run that on different thread
- [x] Post req params to send: File (csv), emailId
- [x] File save on server
- [x] Train method should invoke and then invoke result (same thread)
- [ ] Start train() for email whose status is 'done'
- [ ] Post req params to send: number of input neurons, number of output neurons, train-test-split(int) [Save in variable]
- [ ] Send email to the user in result

## Testing
```bash
$ curl -X POST http://127.0.01:5000/data -F "file=@/tmp/1.csv" -F "emailId=test7@gmail.com"
```
