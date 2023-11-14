# AoC Private Leaderboard Stats Updater Script for Reddit

## Required Environment Variables 

    
1.  `REDDIT_CLIENT_ID`: Reddit API client ID.
2.  `REDDIT_CLIENT_SECRET`: Reddit API client secret.
3.  `REDDIT_PASSWORD`: Reddit account password.
4.  `REDDIT_USERNAME`: Reddit account username.
5.  `AOC_SESSION_COOKIE`: Session cookie for the Advent of Code website.
6.  `AOC_LEADERBOARD_CODE`: Code for the Advent of Code leaderboard.
7.  `REDDIT_POST_ID`: ID of Reddit post which is used as leaderboard.

----
## Instructions on how to get `AOC_SESSION_COOKIE`
1. **Create an Advent of Code Account:**
   - If you don't have an Advent of Code account, go to the [Advent of Code website](https://adventofcode.com/), and sign up for an account.

2. **Log into Your AoC Account & open the leaderboard**
   - After creating an account, log into the AoC website using your credentials. Make sure you have joined the private leaderboard which's ID you have set in `AOC_LEADERBOARD_CODE`. Now navigate to the leaderboard page.
   
3. **Open Developer Tools in Your Browser:**
   - Open the browser's developer tools. You can usually do this by right-clicking on the web page, selecting "Inspect" or "Inspect Element," and then navigating to the "Network" tab.
    
4. **Go to the Network Tab:**
   - In the developer tools, go to the "Network" tab. This tab will show all network requests made by the website.

5. **Refresh the Page:**
   - Refresh the Advent of Code website. This will trigger various network requests, including the one that authenticates your session.

6. **Look for the Request with the Cookie:**
   - In the "Network" tab, look for a network request that is related to the Advent of Code website. It might be named something like "session" or "authenticate."
   - Click on this request to view its details.

7. **Find the Cookie Information:**
   - In the details of the network request, look for a section named "Request Headers" or "Cookies." You are interested in the value of the `session` cookie.

8. **Copy the Session Cookie Value:**
   - Copy the value of the `session` cookie. It is usually a long hex string of letters and numbers.

9. **Use the Session Cookie:**
   - Paste the copied session cookie value into the appropriate environment variable (`AOC_SESSION_COOKIE` in this case) in your code or set it as an environment variable. 

![session-cookie](https://github.com/ni5arga/deviras/blob/main/aoc/cookie.png?raw=true)




