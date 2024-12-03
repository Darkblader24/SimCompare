import argparse
import datetime
import sys
import time

from src.modules.crawler import crawl_sites

sim_urls = [
    "https://www.sim24.de",
    "https://www.blacksim.de",
    "https://www.cybersim.de",
    "https://www.winsim.de",
    "https://www.sim.de",
    "https://www.deutschlandsim.de",
    "https://www.premiumsim.de",
    "https://www.handyvertrag.de",
    "https://www.simplytel.de",
    "https://www.smartmobil.de",
    # "https://www.maxxim.de/allnet-flats",  # These don't work for some reason
    # "https://www.yourfone.de/allnet-flat",
]


def main(argv: list[str] | str) -> None:
    """
    The main function of the script.
    :param argv: The arguments passed to the script.
    :return: None
    """
    start_time = time.time()

    # Parse arguments
    print(f"Starting ... with arguments: {' '.join(argv)}\n")
    if argv and argv[0].endswith(".py"):
        argv = argv[1:]
    parser = argparse.ArgumentParser(description="This is such a cool app!")
    parser.add_argument("--clean", action="store_true", help="Start a new clean crawl")
    args = parser.parse_args(args=argv)

    # Do cool stuff
    crawl_sites(sim_urls, args.clean)

    # Finish script
    total_time = int(time.time() - start_time)
    print(f"\n-> Finished in {datetime.timedelta(seconds=total_time)}")


if __name__ == "__main__":
    """ This block is executed when the script is run from the command line. """
    main(sys.argv)
