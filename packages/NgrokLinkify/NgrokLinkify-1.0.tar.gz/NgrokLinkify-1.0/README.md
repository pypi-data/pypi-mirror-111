# NgrokLinkify

A tool to expose your Ngrok URLs in an easy-to-access way. This tool uses the Ngrok free plan to get public URLs for your internal services and expose them. You can either use a telegram bot to get the public URLs or use redirection on Github pages to get a permanent URL to access your tunnels.


- Expose your tunnels public URL conveniently for your friends
- No need for setting up port forwarding on your system
- Relatively safe, no hardening needed
- Two choices to expose URLs: Telegram bot and Github pages
- Setup as a systemd service to do this on boot

## Related Libraries

- [Ngrok](https://ngrok.com/)
- [PyGitHub](https://github.com/PyGithub/PyGithub)

## Installation
### Dependencies

1. You'll have to install Ngrok by downloading it from [here](https://ngrok.com/download). For ease of use you can create a config file similar to the one below
```yaml
authtoken: TOKEN_ID 
region: in # Set the region to closest one from your location
log_level: info
log_format: json
log: /var/log/ngrok.log
tunnels:
        jupyter: # Name of the tunnel
                proto: http
                addr: 1234 # Port number of the service
                bind_tls: true
        file-download:
                proto: http
                addr: 5678
                bind_tls: true
        heimdall:
                proto: http
                addr: 1111
                bind_tls: true
```
The name of your tunnel will be the path to the redirect link on Github pages. For ex. to visit the jupyter service you need to visit `https://<github-username>.github.io/jupyter`. You'll be redirected to the tunnel and should be able access your service. 

2. You'll also need to install these dependencies
```sh
pip install PyGithub python-telegram-bot
```
### Install NgrokLinkify
```sh
pip install NgrokLinkify
```
Once you install the tool you'll need to create a config file. The basic structure of the config file is available in the package as example-cfg.ini. You can copy the file and edit it according to your system. 
```ini
[Default]
NgrokUrl = http://127.0.0.1:4040/api/tunnels #API endpoint for Ngrok, this is the default value
LogFile = /var/log/NgrokLinkify.log #Location of the Log File
[Git]
RepoPath = /path/to/github-pages/repo #Change this to the path to your local git pages repo
CommitComment = Committed URL at {0} # Commit Message when committing Github Pages
PagesContent = ---\ntitle: {0}\nredirect_to: {1}\n---\n #The content of the redirect file, I use https://github.com/jekyll/jekyll-redirect-from. You can use raw HTML by following https://stackoverflow.com/questions/5411538/redirect-from-an-html-page and replacing the URL by {0} 
[Telegram]
FailureMsg = The server is not running currently! Ping @username #The Failure message to return when Ngrok isn't running
SuccessMsg = The public urls are \n ---------------------- \n{0} #The success message, {0} here contains tunnel name and public url
BotToken = 123123123 #The Bot token for telegram bot
```

### Setup github repo
To ensure that you can update githuba pages without entering username or password. Enable ssh login to github by following this [guide](https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh). Once done create and pull your github pages repo to the location mentioned in the config file. 

Once you've enabled ssh access to your repo, set the upstream branch with ssh using the following command in the repo directory. Note the URL has to be a ssh url. 
 ```bash
git remote set-url origin git@github.com:bagdeabhishek/bagdeabhishek.github.io.git 
```

## Usage
You can directly run the utility by using linkify command
### Simple command line usage

```sh
linkify -config /path/to/config/file
```
You can choose to enable telegram bot or update the github page with redirection. use the `-h` flag to get help
### Use it programmatically inside python script

```python
from NgrokLinkify.linkify import Linkify 
Linkify(start_telegram_bot=False ,update_github_pages=True,config_file="/home/abhishek/linkify.ini")
```
## Options
The command line utility accepts the following arguments
###  --config CONFIG_FILE_LOCATION
Path to the configuration file

### --exclude-telegram  
Don't run telegram bot 

### --exclude-gh-pages 
Do not update github pages

## Persist the services using systemd
The package contains example service file for both NgrokLinkify and Ngrok. You can copy them to `/etc/systemd/system/` location.

### Ngrok systemd service file
```ini
[Unit]                                                                                                                  Description=Ngrok                                                                                                       After=network.service                                                                                                                                                                                                                           [Service]                                                                                                               Type=simple                                                                                                             User=user-name                                                                                                           WorkingDirectory=/home/abhishek                                                                                         ExecStart=/path/to/ngrok start --all --config=".ngrok2/ngrok.yml"                                       Restart=on-failure                                                                                                                                                                                                                              [Install]                                                                                                               WantedBy=multi-user.target 
```
### Enable at boot
Create save this file as `ngrok.service` in `/etc/systemd/system/` location. Run the following commands to enable Ngrok at boot
```sh
sudo systemctl daemon-reload;
sudo systemctl enable ngrok.service; 
```

### NgrokLinkify systemd service
You can run NgrokLinkify as a service using the following example 
```ini
[Unit]                                                                                                                  Description=Telegram bot to return URLs                                                                                 After=ngrok.service network.target network-online.target                                                                PartOf=ngrok.service                                                                                                                                                                                                                            [Service]                                                                                                               Type=simple                                                                                                             User=username                                                                                                           ExecStart=/home/username/miniconda3/bin/linkify --config /home/username/linkify.ini                Restart=on-failure                                                                                                                                                                                                                              [Install]                                                                                                               WantedBy=multi-user.target 
```
Save this file as `NgrokLinkify.service` in `/etc/systemd/system/` location. Enable the service at boot using the follwing commands
```sh
sudo systemctl daemon-reload;
sudo systemctl enable ngrok.service; 
```
