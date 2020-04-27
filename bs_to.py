import utils


def get_series_title(html):
    soup = utils.soup(html)

    serie = soup.find("section", {"class": "serie"})
    return list(serie.h2.children)[0].strip()  # evade <small> season


def get_language(html):
    soup = utils.soup(html)

    return soup.find("span", {"class": "current"}).text


def get_languages(html):
    soup = utils.soup(html)

    options = (soup
               .find("div", {"class": "language"})
               .find_all("option"))

    return {op["value"].strip(): op.text.strip() for op in options}


def get_seasons(html):
    soup = utils.soup(html)

    options = (soup
               .find("div", {"id": "seasons"})
               .find_all("a"))

    return {op["href"].strip(): op.text.strip() for op in options}


def get_episodes(html):
    soup = utils.soup(html)
    episodes = soup.find("table", {"class": "episodes"}).find_all("tr")

    def episode(tr):
        id = int(tr.find("a").text.strip())
        title = tr.find("strong").text.strip()
        hosts = list(tr.children)[5]
        hosts = hosts.find_all("a")
        hosts = list(map(
            lambda host: (host["title"], host["href"]), hosts))

        return (id, title, hosts)

    return list(map(episode, episodes))


# def get_host_url(html):
#     soup = utils.soup(html)
#     player = soup.find("div", {"class": "hoster-player"})
#     a = player.find("a")
#     return a["href"]
