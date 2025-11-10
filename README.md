### Overview
***
This is a simple python program that uses the watchdog package to monitor changes to a file where if a change is detected then the program will search the latest log addition and if the pattern matches to be the format for an alert then to send to discord.

### Requirements
- [Watchdog](https://pypi.org/project/watchdog/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [Requests](https://pypi.org/project/requests/)

### Install
Refer to C6 / Infra / Infra-Wiki -> Elastic -> Kibana -> Alerting for how it is setup currently in our environment