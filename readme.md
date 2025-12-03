<div align="center">
  <a href="https://moonshot.hackclub.com" target="_blank">
    <img src="https://hc-cdn.hel1.your-objectstorage.com/s/v3/35ad2be8c916670f3e1ac63c1df04d76a4b337d1_moonshot.png" 
         alt="This project is part of Moonshot, a 4-day hackathon in Florida visiting Kennedy Space Center and Universal Studios!" 
         style="width: 100%;">
  </a>
</div>

It's been a while (about 4 hours), but my brother and I have the first version of our "game" with a very janky physics engine! Our code consists at about 10% AI, but we will try to lower that in the future! However, the game now supports a start screen and 3 balls: two for the two players and one for a soccer ball. How it works: One computer (player 1) hosts a local server on their respective device using the python library socket. This socket can send and recieve commands, but it is mainly used for recieving the second player's inputs (as well as the first's) and displaying them on the screen. The second player uses a minor chunk of socket code to send commands to the local server to be displayed on the main screen. This could have been fine, but we added a ball with collision detection to improve the engagingness of the game.
