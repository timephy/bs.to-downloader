# bs.to-downloader

A tool to download entire seasons from bs.to

## Requirements

- python3.6 <https://www.python.org/downloads/>
- chromedriver <https://chromedriver.chromium.org>
- beautifulsoup4 `pip3.6 install beautifulsoup4`
- selenium `pip3.6 install selenium`
- requests `pip3.6 install requests`
- wget (for downloading the videos)

## Getting started

1. Visit [bs.to](https://bs.to) and select your desired series (including season and language). Copy the URL in the top bar of your browser (Should be of this form: `http://bs.to/serie/<series>/<season>/<language>`, e.g. `https://bs.to/serie/Downton-Abbey/1/en`).
2. Run the program in the command-line: `python3.6 . -h`

## Please note

- Currently only one host ([vivo](https://vivo.sx)) is supported!

- Hosts like vivo **change** the video URLs frequently, so the links given only stay valid for about 6h.

- **Windows users**: Please user `Git Bash`/`PowerShell` instead of `cmd`!

## How it works

This tool uses selenium to parse and query html. It uses chromedriver to control a Chrome browser instance. It opens all episodes on bs.to in your own browser; Conveniently this allows **you** to solve the CAPTCHAs and copy the host-urls, this is (very sadly) necessary sinde bs.to employs CAPTCHAs to protect against browser automation.

## Disclaimer

This tool does **not** store, stream or use copyrighted material - it only handles URLs.

Use of this tool is at each users own risk. Under no circumstances shall the developer(s) be liable for and indirect, incidental, consequential, special or exemplary damages arising out of the services this tool provides.
