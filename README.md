# Toolchain for FortiOS galaxy

This toolchain generates Galaxy collection repo and Sphinx document for FortiOS

 -   Bump galaxy version in `galaxy_version.yml` , e.g. we are going to release latest 6.2.3 as 1.0.8
```

{
    "6.0.5": {
        "1.0.6": "12.9 2019",
        "1.0.7": "2.23 2020"
    },
    "6.2.3": {
        "1.0.8": "4/24 2020"
    }
}
```
- run the generator
```
$ ./scripts/generate 1.0.8
Steps to generate Galaxy collection and Sphinx document for FortiOS:
	1). Download schema from the Fortigate device
	2). Generate raw Ansible modules
	3). Generate raw sphinx .rst documents
	4). Generate Galaxy collection repository
	5). Generate Sphinx document repository
	6). Update git repository

do you want to proceed? [yes/no]
```


### Demo
[![asciicast](https://asciinema.org/a/YYT3jb0rY3SO9zP9wp6Ig2zwG.svg)](https://asciinema.org/a/YYT3jb0rY3SO9zP9wp6Ig2zwG)


