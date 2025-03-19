# CMPT 371 Spring 2025 - Project by Yerkin Boranbayev, Simon Xie, Dyk kyong Do

## Project Overview
This project is to be done in groups of 4 students!

In this project, your group will build an online multiplayer game. The game itself is up to you, though a suggested game called *Deny and Conquer* is described on the next page.

## Game Requirements
- The game shall be a client-server program. Each player is a client connecting to the server from a remote machine/device.
- The server can be started by any player. All players (including the player who started the session) connect to that server as clients.
- There must be at least one shared object in the game which requires "locking" of that object for concurrency; i.e., only one player at a time can use that object. In *Deny and Conquer*, each white square is a shared object.

## Technical Rules
- You can use any programming language that you like.
- For the frontend, you can use any existing graphics or GUI library or framework. Make your life easy for the frontend as much as possible. Don’t overdo the GUI. A simple and functional GUI is enough.
- For the backend (client and server system), you cannot use any existing gaming, client-server, messaging, remote calling, or other middleware or frameworks. Everything must be written from scratch. You must use sockets programming and send application-layer messages directly.

## Deliverables
A project report which includes:

1. **Description of the game and your design**, including your application-layer messaging scheme. Please show the code snippets where you are:
   - Opening sockets
   - Handling the shared object
2. **A list of group members** and their individual contribution percentage. Each group member is expected to contribute equally; e.g., 25% for a 4-person group, or 20% for a 5-person group.
3. **Commented source code** of the client and the server. Alternatively, you can include a link to Github or other repositories, though the code still has to be commented.
4. **Video of a working demo**. Upload the video somewhere and put its link in the final report. The video must be 1 to 2 minutes and show at least 2 players playing the game, and must include the shared object in action.

## Marking Scheme
```
group project mark = 30% working demo (as seen in the video) + 70% report
individual mark (capped at 100%) = group project mark × individual contribution × size of group
```
Individual mark is the mark that is given to an individual student as the final mark for the project.

---

# Deny and Conquer
## Game Description
The game board is divided into squares of equal size. The number of squares shall be **8×8**. The game is played by multiple players, each having a pen of different color. The thickness of the pen is the same for all players.

### Objective
Deny your opponents from filling the most number of squares by taking over as many squares as you can.

### How to Take Over a Square
- A square must be **white** to be taken over.
- Click the mouse button inside the square and scribble **without lifting the pen** (hold the mouse button down) until at least **50%** of the area of the square is colored.
- Lift your pen (release the mouse button).
- If at least 50% of the square is colored, the game engine will turn the color of that square to your color.
- Otherwise, the square will turn white and another player can try taking over it.
- The game ends when all squares have been taken over.
- The player with the most number of squares wins. **Ties are possible.**

### Game Mechanics
- While a player is scribbling in a square, that square is no longer available to other players.
- If other players click in that square, they should not be able to draw anything in it.

---

