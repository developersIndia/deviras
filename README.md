# deviras

> Bunch of scripts to automate stuff in r/developersIndia.

[![Discord](https://img.shields.io/discord/669880381649977354?color=%237289da&label=Discord&logo=Discord)](https://discordapp.com/invite/MKXMSNC)
[![Subreddit subscribers](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fdevelopersindia.github.io%2Fmetrics%2Fdata%2F&query=%24.totalMembers&suffix=%20members&style=flat&logo=reddit&label=r%2FdevelopersIndia&color=orange&link=https%3A%2F%2Fwww.reddit.com%2Fr%2FdevelopersIndia
)](https://www.reddit.com/r/developersIndia/)
[![All Contributors](https://img.shields.io/badge/all_contributors-3-orange.svg)](#contributors-)

## Scripts

### [idcard_update](https://github.com/developersIndia/deviras/blob/main/idcard_update/main.py)
 
- Used for changing the text below _total members_ & _live members_ count on the Subreddit.
- ![action build](https://github.com/developersIndia/deviras/actions/workflows/titles-updater.yml/badge.svg)

### [aoc](https://github.com/developersIndia/deviras/blob/main/aoc/main.py)

- Used for updating the Advent of Code User Scores in the [leaderboard post](https://www.reddit.com/r/developersIndia/comments/1889ar3/advent_of_code_rdevelopersindia_leaderboard_year/).
- ![action build](https://github.com/developersIndia/deviras/actions/workflows/aoc.yml/badge.svg)

### [community-threads](https://github.com/developersIndia/deviras/blob/main/community-threads/main.py)

- Used for grabbing the posts from [community threads collection](https://www.reddit.com/r/developersIndia/collection/958aef35-f9cb-414d-ab33-08bc639e47de/) and adding it to the [wiki](https://www.reddit.com/r/developersIndia/wiki/community-threads/).
- ![action build](https://github.com/developersIndia/deviras/actions/workflows/collection-thread-updater.yml/badge.svg)

### [job-thread](https://github.com/developersIndia/deviras/blob/main/job-thread/main.py)

- Used for creating [hiring threads](https://www.reddit.com/r/developersIndia/?f=flair_name%3A%22Hiring%22) in the subreddit that gets the job from our [job board](https://developersindia.in/job-board/).

### [showcase-sunday](https://github.com/developersIndia/deviras/blob/main/showcase-sunday/main.py)

- Used for creating [Showcase Sunday Megathreads](https://www.reddit.com/r/developersIndia/search/?q=flair%3A%20Showcase%20Sunday&restrict_sr=1) posts in the subreddit.
- ![action build](https://github.com/developersIndia/deviras/actions/workflows/showcase-sunday.yml/badge.svg)

### [ama-summarizer](https://github.com/developersIndia/deviras/blob/main/ama-summarizer/main.py/)
- The Python script to help during AMAs. It generates a markdown file of questions and links of the questions the AMA guest has answered. 



## Setup

1. Clone the repo

   ```bash
   git clone https://github.com/developersIndia/deviras.git
   ```
2. Initialise a virtual environment.

   ```bash
   cd deviras
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```
4. To run the tests, use the following command in a python virtual environment:

   ```bash
   python -m unittest
   ```


## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/SameerSahu007"><img src="https://avatars.githubusercontent.com/u/29480670?v=4?s=100" width="100px;" alt="Sameer Sahu"/><br /><sub><b>Sameer Sahu</b></sub></a><br /><a href="https://github.com/developersIndia/deviras/commits?author=SameerSahu007" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://pavanjadhaw.me"><img src="https://avatars.githubusercontent.com/u/26551780?v=4?s=100" width="100px;" alt="Pavan Jadhaw"/><br /><sub><b>Pavan Jadhaw</b></sub></a><br /><a href="#ideas-pavanjadhaw" title="Ideas, Planning, & Feedback">🤔</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://animesh-ghosh.github.io/"><img src="https://avatars.githubusercontent.com/u/34956994?v=4?s=100" width="100px;" alt="MaDDogx"/><br /><sub><b>MaDDogx</b></sub></a><br /><a href="https://github.com/developersIndia/deviras/commits?author=Animesh-Ghosh" title="Code">💻</a> <a href="https://github.com/developersIndia/deviras/commits?author=Animesh-Ghosh" title="Tests">⚠️</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://pratham.cc"><img src="https://avatars.githubusercontent.com/u/67585967?v=4?s=100" width="100px;" alt="Pratham"/><br /><sub><b>Pratham</b></sub></a><br /><a href="https://github.com/developersIndia/deviras/commits?author=git-bruh" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://nisarga.me/"><img src="https://avatars.githubusercontent.com/u/45588772?v=4?s=100" width="100px;" alt="Nisarga Adhikary"/><br /><sub><b>Nisarga Adhikary</b></sub></a><br /><a href="https://github.com/developersIndia/deviras/commits?author=ni5arga" title="Code">💻</a></td>
     <td align="center" valign="top" width="14.28%"><a href="https://lineararray.nekoweb.org"><img src="https://github.com/lineararray.png" width="100px;" alt="LinearArray"/><br /><sub><b>LinearArray</b></sub></a><br /><a href="https://github.com/developersIndia/deviras/commits?author=LinearArray" title="Code">💻</a></td>
    </tr>
  </tbody>
 
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
