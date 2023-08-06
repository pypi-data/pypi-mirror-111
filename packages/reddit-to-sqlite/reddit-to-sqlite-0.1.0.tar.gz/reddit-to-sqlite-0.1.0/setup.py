# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['reddit_to_sqlite']

package_data = \
{'': ['*']}

install_requires = \
['praw>=7.2.0,<8.0.0', 'sqlite-utils>=3.6,<4.0', 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['reddit-to-sqlite = reddit_to_sqlite.main:app']}

setup_kwargs = {
    'name': 'reddit-to-sqlite',
    'version': '0.1.0',
    'description': '',
    'long_description': "# reddit-to-sqlite\nSave data from Reddit to SQLite. Dogsheep-based.\n\nInserts records of posts and comments into a SQLite database.  Can \nbe run repeatedly safely; will refresh already-saved results (see Reload, below).\nCreates `posts` and `comments` tables, plus an `items` view with a unified \nview.\n\n## Usage\n\n\n    reddit-to-sqlite r/python\n    reddit-to-sqlite u/catherinedevlin \n    reddit-to-sqlite --help \n\nBy default, writes to a local `reddit.db` database (change with `--db`).\n\n## Authorizing\n\nreddit-to-sqlite will look for a file of authorization info (location determined \nby --auth, defaults to `~/.config/reddit-to-sqlite.json`) and, if not found, will \nquery the user and then save the info there.  You will need a Reddit username and \npassword, and you will need to \n[register your app with Reddit](https://www.reddit.com/wiki/api) to get a client_id \nand client_secret.  ([More instructions](https://www.geeksforgeeks.org/how-to-get-client_id-and-client_secret-for-python-reddit-api-registration/))\n\n## Limits\n\nWhether used for users or for subreddits, can't guarantee getting all \nposts or comments, because\n\n- Reddit's API only supplies the last 1000 items for each API call, and does \nnot support pagination; \n- Comments nested under a single post won't be retrieved if they are deeply \nnested in long comment chains \n(see [replace_more](https://praw.readthedocs.io/en/latest/tutorials/comments.html#the-replace-more-method)) \n\n## Reload \n\nreddit_to_sql can be run repeatedly for a given user or subreddit, replacing previously saved \nresults each time.  However, to save excessive API use, it works backward through time and \nstops after it reaches the timestamp of the last saved post, plus an overlap period (default \n7 days).  That way, recent changes (scores, new comments) will be recorded, but older ones\nwon't unless `--post_reload` is increased.  If posts keep getting comments of interest long \nafter they are posted, you can increase `--post_reload`. \n\nWhen loading an individual user's comments, by default reddit_to_sql stops just 1 day after \nreaching the most recent comment that is already recorded in the database.  However, if you're \ninterested in comment scores, you may want to impose a longer `--comment_reload`, since scores \nmay keep changing for longer than a single day after the comment is posted.\n\n## Notes\n\n- `author` is saved in case-sensitive form, so case-insensitive searching with `LIKE` \nmay be helpful.\n",
    'author': 'Catherine Devlin',
    'author_email': 'catherine.devlin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
