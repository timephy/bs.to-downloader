import utils
import bs_to
import itertools


class Season:
    def __init__(self, url):
        url_parts = url.split("/")
        self.path = url_parts[3:7]
        self.base = "/".join(url_parts[:3])

        html = utils.get(url)
        self.title = bs_to.get_series_title(html)

        self.all_languages = bs_to.get_languages(html)
        self.all_seasons = bs_to.get_seasons(html)

        self.episodes = [Episode(*ep) for ep in bs_to.get_episodes(html)]  #

    @property
    def all_hosts(self):
        return set(itertools.chain(*[ep.hosts.keys() for ep in self.episodes]))

    @property
    def language(self):
        return self.all_languages[self.path[-1]]

    @property
    def season(self):
        return self.all_seasons["/".join(self.path)]

    def __repr__(self):
        return f"Season({self.season}, {self.title}, {self.language})"

    def __str__(self):
        return f"{self.season} - {self.title}"

    @property
    def series_str(self):
        return f"{self.title}"

    @property
    def season_str(self):
        id = self.season
        id = f"S{id.zfill(2)}" if id.isdigit() else id
        return f"{id}.{self.language}"

    @property
    def id_str(self):
        return f"{self.series_str}.{self.season_str}"

    def obj(self):
        return {
            "title": self.title,
            "season": self.season,
            "language": self.language,
            "episodes": self.episodes
        }


class Episode:
    def __init__(self, id, title, hosts):
        print(id, type(id))
        self.id = id
        self.title = title
        self.hosts = {host[0]: host[1] for host in hosts}
        self.host_url = None
        self.video_url = None

    @property
    def filename(self):
        return ""

    def __repr__(self):
        return f"Episode({self.id}, {self.title}, {self.hosts})"

    def __str__(self):
        return f"{str(self.id).zfill(2)} {self.title}"

    @property
    def episode_str(self):
        return f"E{str(self.id).zfill(2)}"

    @property
    def id_str(self):
        return f"{self.episode_str}.{self.title}"


class Host:
    def __init__(self, name, url):
        self.name = name
        self.url = url
