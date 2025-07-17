"""
Example: Demonstrating how to use the Scrapeless SDK profile module
Filename: profile_example.py
"""
from scrapeless import Scrapeless, Logger
from scrapeless.types import ProfilePaginationParams

log = Logger().with_prefix('Scraping Example')

def run_example():
    client = Scrapeless()
    create_resp = client.profile.create(name="py_name")
    print('Profile created: ', create_resp)

    params = ProfilePaginationParams(
        page=1,
        page_size=10,
    )
    profiles = client.profile.list(params=params)
    print('Profiles: ', profiles)

    profile = client.profile.get(create_resp['profileId'])
    print('Profile detail: ', profile)

    delete_resp = client.profile.delete(create_resp['profileId'])
    print('Profile deleted: ', delete_resp)

    log.info('Example completed successfully')

run_example()