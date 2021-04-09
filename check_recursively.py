import linkcheck
from linkcheck import director
from linkcheck.cmdline import aggregate_url
from linkcheck.director import get_aggregate, console

import pathlib


def check_recursively(base_url, **kwargs):
    """ Check broken link recursively and run selenium plugins
    export to csv file

    :param base_url:
    :return:
    """
    config = linkcheck.configuration.Configuration()
    config.set_status_logger(console.StatusLogger())
    config["checkextern"] = True

    config["pluginfolders"] = [f'{pathlib.Path(__file__).parent.absolute()}/selenium_plugins']

    csv_logger = config.logger_new("csv", filename='result/check_result.csv', fileoutput=1)
    config["fileoutput"].append(csv_logger)

    # if use selenium plugin, decrease it
    config["threads"] = 10

    if "config" in kwargs:
        config.update(kwargs["config"])

    config.sanitize()
    aggregate = get_aggregate(config)
    aggregate_url(aggregate, base_url)

    director.check_urls(aggregate)
