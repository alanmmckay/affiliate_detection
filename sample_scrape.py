
from pathlib import Path

from custom_command import YoutubeClicker
from openwpm.command_sequence import CommandSequence
from openwpm.commands.browser_commands import GetCommand, DumpPageSourceCommand, ScreenshotFullPageCommand
from openwpm.config import BrowserParams, ManagerParams
from openwpm.storage.sql_provider import SQLiteStorageProvider
from openwpm.task_manager import TaskManager


# ----- Collecting pages to scrape ---- #
def get_pages(file_name):
    f = open(file_name,"r")
    data = f.readlines()
    f.close()
    sites = []
    for line in data:
        if line != "\n":
            entry = line.split(' , ')
            if entry[1].strip() == 'yes':
                sites.append(entry[0].strip())
    return sites

file_list = ["affiliate_sample.txt","non-affiliate_sample.txt"]
path = "analysis_files/sample/"

sites = []
for file_name in file_list:
    sites = sites + get_pages(path+file_name)
print("Site count: " + str(len(sites)))

#visit_id is associated with redirect url in crawl-data.http_redirects
# ----------------------------------------#


# Loads the default ManagerParams
# and NUM_BROWSERS copies of the default BrowserParams
NUM_BROWSERS = 3
manager_params = ManagerParams(num_browsers=NUM_BROWSERS)
browser_params = [BrowserParams(display_mode="xvfb") for _ in range(NUM_BROWSERS)]

# Update browser configuration (use this for per-browser settings)
for browser_param in browser_params:

    # Record HTTP Requests and Responses
    browser_param.http_instrument = True

    # Record cookie changes
    browser_param.cookie_instrument = False

    # Record Navigations
    browser_param.navigation_instrument = True

    # Record JS Web API calls
    browser_param.js_instrument = False

    # Record the callstack of all WebRequests made
    # browser_param.callstack_instrument = True

    # Record DNS resolution3
    browser_param.dns_instrument = False

    # Enable bot mitigation
    browser_param.bot_mitigation = True
# End for-loop

# Update TaskManager configuration (use this for crawl-wide settings)
manager_params.data_directory = Path("./datadir/")
manager_params.log_path = Path("./datadir/openwpm.log")


# memory_watchdog and process_watchdog are useful for large scale cloud crawls.
# Please refer to docs/Configuration.md#platform-configuration-options for more information
# manager_params.memory_watchdog = True
# manager_params.process_watchdog = True


# Commands time out by default after 60 seconds
with TaskManager(
    manager_params,
    browser_params,
    SQLiteStorageProvider(Path("./datadir/crawl-data.sqlite")),
    None,
) as manager:
    # Visits the sites
    for index, site in enumerate(sites):

        def callback(success: bool, val: str = site) -> None:
            print(
                f"CommandSequence for {val} ran {'successfully' if success else 'unsuccessfully'}"
            )

        # Parallelize sites over all number of browsers set above.
        command_sequence = CommandSequence(
            site,
            site_rank=index,
            callback=callback,
        )

        # Start by visiting the page
        command_sequence.append_command(GetCommand(url=site, sleep=3), timeout=60)

        # Grab Full-page screenshot ensuring a scroll effort
        command_sequence.append_command(SaveScreenshotCommand(""))

        # Dump the generated source
        #command_sequence.append_command(DumpPageSourceCommand(""))

        #Test custom command:
        #command_sequence.append_command(YoutubeClicker())

        # Run commands across all browsers (simple parallelization)
        manager.execute_command_sequence(command_sequence)

# End command-execution wrapper



