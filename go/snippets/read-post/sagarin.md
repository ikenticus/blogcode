# Sagarin Uploader

This repo provides a tool to scan directories and post the Sagarin ratings to a public API in order to replace the existing FTP workflow that was previously in place for USAT TODAY

## YAML Configuration
The YAML configuration file contains:

* Text to validate ratings file
* Read locations to acquire ratings file(s)
* Post settings to upload ratings data

Sample YAML layout:

```
text: Sagarin
 
read:
- relative/path/directory
- /absolute/path/location
- C:\scan\windows\example
 
post:
- url: http://domain/path/to/post/sagarin/
  query:
    - key: source
      val: gannettdigital
    - key: api_key
      val: 123456789
```

## Usage
Build executable using `go build -o sagarin main.go` and configure `sagarin.yaml` using the same output name.  Execute `./sagarin` and it should automatically scan the `Read` directories for files containing `Text` and `Post` to the specified API.

For Windows, build `go build -o sagarin.exe main.go` and execute `sagarin` using a `sagarin.yaml` with Windows directory paths.
    
## Contributing
This project uses the Go package management tool [Dep](https://github.com/golang/dep) for dependencies.
To leverage this tool to install dependencies, run the following command from the project root:

    dep ensure

Testing is done using standard go tooling, ie `go test ./...`

