
# rmreporter

A simple tool to get reports for reported time from redmine

## Requirements:

* python3
* redminelib (python3-redminelib in Ubuntu)

## Usage

```
rmreporter [--user=USERNAME] [--password=password] [--url=site] [--project==ProjectName] [ISSUES..]
```

If not supplied, rmreporter will ask for needed details.

It will also read ~/.rmreporter if it exists, an example file is below

```
[credentials]
username = someusername
password = apassword
url = https://redmine.example.com/
```

