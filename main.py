from check_recursively import check_recursively
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("url")
parser.add_argument("-p", "--plugins", help="run selenium plugins separate by colon. Ex: "
                                            "ModalCheck. Number threads will decrease to 1. Don't set threads too much, "
                                            "browser will kill your computer")
parser.add_argument("-t", "--threads",
                    help="run selenium plugins separate by colon. Default = 10")

args = parser.parse_args()


def main():
    config = dict()
    if args.threads:
        config["threads"] = int(args.threads)
    else:
        config["threads"] = 10
    # add selenium plugins
    if args.plugins:
        plugins = []
        for p in args.plugins.split(","):
            plugins.append(p)
            config[p] = dict()

        config["enabledplugins"] = plugins

        # auto decrease number thread when use selenium plugins
        config["threads"] = 1

    check_recursively(args.url, config=config)


if __name__ == "__main__":
    main()
