# asapp

Open websites in Chromium's app mode.

## Motivation

I use several GSuite apps such as Google Sheets and Google Docs, but there are not suitible 
linux clients available for these apps. Running them in [app](https://superuser.com/questions/33548/starting-google-chrome-in-application-mode) mode using the `--app` CLI option
is a good substitute for this. 

## Installation

### PyPi

```shell script
pip install asapp
```

### Git Clone

```shell script
git clone https://github.com/BlakeASmith/as_app.git
pip install . 
```

## Usage

### Open Websites

Launch a website in it's own window, without any borders or browser options. 

```shell script
asapp open https://duckduckgo.com
```

### Create a Desktop Entry

```shell script
asapp shortcut --name DuckDuckGo https://duckduckgo.com
```

This will add a `.desktop` file to the `~/.local/share/applications/` folder, causing
`DuckDuckGo` to appear in your app launcher of choice!
