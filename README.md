# ScoreHammer — BR Tracker prototype

A functional wireframe prototype of **ScoreHammer**, a Warhammer 40K score-keeping app. Two players link their phones with a QR code, track primary, secondary and CP live through five battle rounds, and spectators can follow along on a TV or tablet.

This is a design prototype: a single HTML file with no build step and no backend. Both players and the spectator are simulated in one page, so you can play both sides of a game from one browser.

## Run it

Open `index.html` in any modern browser. Nothing to install.

To host it, enable **GitHub Pages** for this repo (Settings → Pages → deploy from the `main` branch, root folder).

## Using the prototype

The compact row above the phone holds the dev-only controls:

- **P1 / P2 / Spectator** switch between the three simulated devices. They share one live game.
- **Skip to BR1** jumps straight to battle round 1 with both lists confirmed.
- **Reset** starts over.
- Blue dashed **Prototype** boxes stand in for things a real backend would do, such as scanning a QR code or the other player responding.

## What's covered

Mapped from the user flow in [`docs/user-flow.jpeg`](docs/user-flow.jpeg):

- **Connect:** host shows a QR code and room code; opponent scans or types the code. Wrong or missing codes show a "room not found" error.
- **Setup (3 steps):** name, army, up to three detachments and disposition; both players confirm lists; attacker/defender and first turn are set together.
- **Battle rounds 1–5:**
  - Pinned scoreboard with each player's VP and CP. Tap the opponent for their army, detachments, disposition and per-round scores.
  - Primary and secondary scoring with −10 / −5 / −1 / +1 / +5 / +10. CP uses a −/+ stepper.
  - Multi-step undo from the header.
  - Fix any past round from the round track.
  - **Synced rounds:** ending a round locks in your side. Both players move to the next round together once both have ended it.
- **End of game:** end-of-game scoring, then a results screen with a round-by-round breakdown.
- **Menu:** invite spectators, left-handed controls, restart (the opponent must agree) and leave (ends the session for everyone).
- **Spectator:** read-only live scoreboard. When the game ends, a 5:00 countdown runs, then the link expires.

## Design notes

- Built for one-handed use at the table: information sits at the top for glancing, and the most-used controls sit at the bottom in thumb reach, with CP closest.
- Touch targets are 44px or larger; add buttons are larger and filled.
- Destructive actions sit behind a divider and a confirmation sheet.
- Works from 320px wide; big scores scale to fit their card.
- Follows the system light/dark theme. Keeps the screen awake during rounds where the browser allows it.

## Not yet built

- Real cross-device sync (for example Supabase or WebSockets); everything currently runs in one page.
- Real QR generation and camera scanning.
- Auto-populated army, detachment and disposition lists (placeholders today).
- Results image export, and the general 404 page.
