
from pathlib import Path

from custom_command import YoutubeClicker
from openwpm.command_sequence import CommandSequence
from openwpm.commands.browser_commands import GetCommand, DumpPageSourceCommand, ScreenshotFullPageCommand
from openwpm.config import BrowserParams, ManagerParams
from openwpm.storage.sql_provider import SQLiteStorageProvider
from openwpm.task_manager import TaskManager


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

file_list = ["beautysites.txt","fashionsites.txt","gamesites.txt","interiordesignsites.txt","recipesites.txt","techsites.txt","travelsites.txt"]
path = "site_listings/"
sites = []
for file_name in file_list:
    sites = sites + get_pages(path+file_name)


print("Site count: " + str(len(sites)))



#sites = ["https://www.youtube.com/redirect?event=video_description&redir_token=QUFFLUhqbHNKYVlxS0pfR040X3JsOTM0bjVKSnJoNzNid3xBQ3Jtc0tuNkxsaklYdDJXLXg1SEx0MmlTTUNBLTQyOUlqeVNEa3RCc2pmR1doYnhoZHFMSWlDS2trUTZXemVEWmptM0x6cmlvXzM2QXBHaE9uRmhWbEE3UkVHMDQ2OWktVks4djdMRkxqN3BXZGVSSlBDUDR4OA&q=https%3A"+"%"+"2F"+"%"+"2Fsbird.co"+"%"+"2F3ucMihX&v=pP4BMKEu5Ss","https://www.the-atlantic-pacific.com/2023/08/21/end-of-summer-sets-from-saks/"]
#visit_id is associated with redirect url in crawl-data.http_redirects

# Loads the default ManagerParams
# and NUM_BROWSERS copies of the default BrowserParams
NUM_BROWSERS = 6
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
    # Record DNS resolution
    browser_param.dns_instrument = False
    browser_param.bot_mitigation = True

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
        command_sequence.append_command(DumpPageSourceCommand(""))
        #command_sequence.append_command(ScreenshotFullPageCommand(""))
        #command_sequence.append_command(YoutubeClicker())
        # Run commands across all browsers (simple parallelization)
        manager.execute_command_sequence(command_sequence)
