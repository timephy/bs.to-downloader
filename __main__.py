import os
import pathlib
import argparse
import webbrowser
from pprint import pformat

from objects import Season
import utils


supported_hosts = ["vivo"]


# PARSER
parser = argparse.ArgumentParser(
    prog="bs.to-downloader",
    description="A tool to download entire seasons on bs.to")


parser.add_argument("url", help="the url of the season")
parser.add_argument("host", help="the video host (currently only 'vivo')",
                    default="vivo", nargs="?")

parser.add_argument("--start", help="first episode number",
                    default=0, type=int)
parser.add_argument("--end", help="last episode number",
                    default=9999, type=int)

parser.add_argument("--out", help="output directory",
                    default="output")
parser.add_argument("--flat", help="put all seasons into the base directory",
                    action="store_true")
# parser.add_argument("--script",
#                     help="instead of downloading, generate a download script",
#                     action="store_true")

parser.add_argument("--dry", help="should what could have been downloaded",
                    action="store_true")
parser.add_argument("--json", help="output json data",
                    action="store_true")
parser.add_argument("-v", "--verbose", help="verbose",
                    action="store_true")


args = parser.parse_args()
print("args:", args)

# LOAD EPISODE LIST
if args.verbose:
    print(f"Extracting data from {args.url}...")
s = Season(args.url)

print("Title:", pformat(s.title))
print("Season:", pformat(s.season))
print("Language:", pformat(s.language))

print(f"All episodes ({len(s.episodes)}):")
for ep in s.episodes:
    print(" ", str(ep).ljust(60), list(ep.hosts.keys()))

print("Available hosts:", s.all_hosts)

host_select = supported_hosts[0]  # args.host
print(f"Currently the only supported host is '{supported_hosts[0]}'")
print("Selected host:", pformat(host_select))

episodes_select = [ep for ep in s.episodes if host_select in ep.hosts]
episodes_select = [ep for ep in episodes_select
                   if args.start <= ep.id <= args.end]

if not episodes_select:  # no episodes selected
    print("no episodes selected.")
    quit()

print(f"Selected episodes ({len(episodes_select)}):")
for ep in episodes_select:
    print(" ", ep)


# dry run exit
if args.dry:
    print("dry run complete.")
    quit()


print(("Please solve CAPTCHAs if needed and copy-paste the host-url, "
       "then press enter:"))
for ep in episodes_select:
    webbrowser.open(s.base + "/" + ep.hosts[host_select])
    ep.host_url = input(f"  {ep}: ").strip()
    # ep.host_url = "https://vivo.sx/bfac151056"


# CRAWL HOST SITES
if host_select == "vivo":
    import host.vivo
    for ep, url in zip(episodes_select, host.vivo.resolve([ep.host_url for ep in episodes_select])):
        ep.video_url = url[0]
        ep.filetype = url[1].split("/")[1]

else:
    print("ERROR")
    quit()


# OUTPUT
outpath = pathlib.Path(args.out).joinpath(utils.safe_filename(s.series_str))
print(f"Output directory: '{outpath.absolute()}'")
outpath.mkdir(parents=True, exist_ok=True)

if args.json:
    # data file
    import json
    data = {
        "title": s.title,
        "season": s.season,
        "language": s.language,
        "host_select": host_select,
        "episodes_select": [{"title": ep.title, "id": ep.id,
                             "host_url": ep.host_url,
                             "video_url": ep.video_url}
                            for ep in episodes_select]
    }
    filepath = outpath.joinpath(utils.safe_filename(f"{s.id_str}.json"))
    with filepath.open("w") as file:
        file.write(json.dumps(data, indent=4))


# DOWNLOAD
# downloadpath = pathlib.Path(args.dir)
# eppath = outpath  # downloadpath.joinpath(utils.safe_filename(s.series_str))
eppath = pathlib.Path()
if not args.flat:  # put into season-directory
    eppath = eppath.joinpath(utils.safe_filename(s.season_str))
# print(f"Download directory: '{downloadpath.absolute()}'")

downloads = [(ep.video_url, eppath.joinpath(utils.safe_filename(
    f"{s.id_str}.{ep.id_str}.{ep.filetype}")))
    for ep in episodes_select]

# SCRIPT
scriptpath = outpath.joinpath(utils.safe_filename(f"Download {s.id_str}.sh"))
with scriptpath.open("w") as file:
    if not args.flat:
        file.write(f"mkdir -p \"{eppath}\"\n")
    for d in downloads:
        file.write(
            f"wget --no-check-certificate {d[0]} -O \"{d[1]}\"\n")
scriptpath.chmod(0o775)  # make download script executable
print(f"Generated download script '{scriptpath.name}'")

# RUN DOWNLOAD SCRIPT
print("Downloading...")
cmds = [
    f"cd \"{outpath}\"",
    f"\"./{scriptpath.relative_to(outpath)}\""
]

if args.verbose:
    for cmd in cmds:
        print(f"$ {cmd}")
os.system(" && ".join(cmds))

print("done.")
