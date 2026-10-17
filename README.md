# ScoreHammer — BR Tracker prototype

A functional wireframe prototype of **ScoreHammer**, a Warhammer 40K score-keeping app. Two players link their phones with a QR code, track primary, secondary and CP live through five battle rounds, and spectators can follow along on a TV or tablet.

This is a design prototype: a single HTML file with no build step and no backend. Both players and the spectator are simulated in one page, so you can play both sides of a game from one browser.

## Versions

- **`index.html`**: the wireframe prototype (light/dark, system fonts).
- **`auspex.html`**: the same app restyled in the Auspex phosphor-terminal look shared with PhosphorDice and Dominatus Codex (cold black, phosphor green, monospace, bracketed panels, CRT scanlines). Both are kept in sync for visual design testing.

## Run it

Open `index.html` in any modern browser. Nothing to install.

To host it, enable **GitHub Pages** for this repo (Settings → Pages → deploy from the `main` branch, root folder).

## Using the prototype

The dev-only controls are hidden by default. Add `#dev` to the end of the URL (for example `auspex.html#dev`) to show the compact row above the phone:

- **P1 / P2 / Spectator** switch between the three simulated devices. They share one live game.
- **Skip to BR1** jumps straight to battle round 1 with both players set up.
- **Reset** starts over.
- **Force advance (dev)**, below End battle round, readies both players and moves straight to the next round (or final scoring after BR5).
- Blue dashed **Prototype** boxes stand in for things a real backend would do, such as scanning a QR code or the other player responding.

## What's covered

Mapped from the user flow in [`docs/user-flow.jpeg`](docs/user-flow.jpeg):

- **How it works:** a single page with a simple diagram explaining solo scoring (VP, +1–5 buttons, round track, CP). It opens only from "How it works" on the start screen.
- **Single mode:** a third option on the start screen for tracking just your own score. It skips setup and connecting and goes straight to battle round 1, with a single scoreboard (your VP and CP), no opponent, no spectators, and no ready syncing: End battle round advances immediately. The menu offers Start over and Exit to start, and results show your own round-by-round breakdown.
- **Two-player mode (hidden for now):** Host and Join are only shown with `#dev` in the URL while the app focuses on single mode. Everything below still works there.
- **Connect:** host shows a QR code and room code; opponent scans or types the code. Wrong or missing codes show a "room not found" error.
- **Setup (1 step):** your army (name required; army, up to three detachments and disposition optional), then tap Ready. Battle round 1 starts as soon as both players are ready; tap again to undo while waiting.
- **Battle rounds 1–5:**
  - Pinned scoreboard with each player's VP and CP. Tap the opponent for their army, detachments, disposition and per-round scores.
  - Primary and secondary scoring with −1 / +1 / +2 / +3 / +4 / +5. CP sits in the pinned footer with −2 / −1 / +1 / +2.
  - Multi-step undo from the header.
  - Fix any past round from the round track (BR1–BR5, then FS for final scoring).
  - **Synced rounds:** tapping End battle round puts you in a Ready state (tap again to undo). The next round starts automatically as soon as both players are ready; there's no confirmation step.
  - **Concede:** in the menu during battle rounds. A confirmation sheet keeps the Yes button locked for a 5-second countdown; conceding ends the game for both players and goes to results.
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
- Army, detachment and disposition are free-text today; picking them from an auto-populated list is a later step.
- The general 404 page.
