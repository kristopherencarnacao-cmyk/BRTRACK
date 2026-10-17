# ScoreHammer — BR Tracker prototype

A functional wireframe prototype of **ScoreHammer**, a Warhammer 40K score-keeping app. Two players link their phones with a QR code, track primary, secondary and CP live through five battle rounds, and spectators can follow along on a TV or tablet.

This is a design prototype: a single HTML file with no build step and no backend. Both players and the spectator are simulated in one page, so you can play both sides of a game from one browser.

## Versions

- **`auspex.html`**: the active version. The app styled in the Auspex phosphor-terminal look shared with PhosphorDice and Dominatus Codex (cold black, phosphor green, monospace, bracketed panels, CRT scanlines). All new work happens here.
- **`index.html`**: the earlier light/dark wireframe, frozen as of the score-batching update and no longer maintained.

## Run it

Open `auspex.html` in any modern browser. Nothing to install.

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
- **Single mode:** a third option on the start screen for tracking just your own score. It skips setup and connecting and goes straight to battle round 1, with a single scoreboard in the PhosphorDice readout style (big VP on the left, Primary and Secondary totals on the right, `--` until something is scored; CP stays in the footer bar), no opponent, no spectators, and no ready syncing: Next round advances immediately. The round track is navigation: tap any round you've reached (or FS) to go back to that round's normal page and change it. The menu offers Start over and Exit to start, and results show your own round-by-round breakdown. Your game is saved in the browser after every change and restored automatically on reopen; Exit to start or New game clears it.
- **Two-player mode (hidden for now):** Host and Join are only shown with `#dev` in the URL while the app focuses on single mode. Everything below still works there.
- **Connect:** host shows a QR code and room code; opponent scans or types the code. Wrong or missing codes show a "room not found" error.
- **Setup (1 step):** your army (name required; army, up to three detachments and disposition optional), then tap Ready. Battle round 1 starts as soon as both players are ready; tap again to undo while waiting.
- **Battle rounds 1–5:**
  - Pinned scoreboard with each player's VP and CP. Tap the opponent for their army, detachments, disposition and per-round scores.
  - Primary and secondary scoring with −1 / +1 / +2 / +3 / +4 / +5. CP sits in the pinned footer with −2 / −1 / +1 / +2.
  - **Score batching:** Primary and Secondary taps gather into a pending tally (e.g. `+5`) shown on each panel. One countdown bar runs along the bottom of the scoreboard, with the running total just above it and Undo beside it. The delay is set in the menu (Instant, 3s, 5s or 10s; 3s by default). When the delay runs out after the last tap, the whole batch is added to the scoreboard as one step. Tap the tally to add it straight away. Leaving the round (Next round, jumping to another round, Finish), backgrounding the app or closing it all commit pending points first, to the round they were tapped in. CP stays instant.
  - Multi-step undo (scoring only): undo cancels the pending tally if there is one; otherwise it removes the last whole batch. CP changes are not part of undo.
  - Fix any past round from the round track (BR1–BR5, then FS for final scoring). In two-player mode this opens a fix sheet; in single mode it opens that round's page.
  - **Synced rounds:** tapping End battle round puts you in a Ready state (tap again to undo). The next round starts automatically as soon as both players are ready; there's no confirmation step.
  - **Concede:** in the menu during battle rounds. A confirmation sheet keeps the Yes button locked for a 5-second countdown; conceding ends the game for both players and goes to results.
- **End of game:** end-of-game scoring, then a results screen with a round-by-round breakdown.
- **Menu:** a bracketed dropdown under the header's MENU button with Theme (six accent colours: green, cyan, blue, violet, magenta, orange, saved per device), Score delay, Left-handed, and Start over / Exit (single mode) or invite spectators, restart, concede and leave (two-player). Tap outside, the MENU button or Escape to close.
- **Spectator:** read-only live scoreboard. When the game ends, a 5:00 countdown runs, then the link expires.

## Design notes

- Built for one-handed use at the table: information sits at the top for glancing, and the most-used controls sit at the bottom in thumb reach, with CP closest.
- Touch targets are 44px or larger; add buttons are larger and filled.
- Destructive actions sit behind a divider and a confirmation sheet.
- Works from 320px wide; big scores scale to fit their card.
- Messages like "Battle round 2 has started" float over the header as a toast instead of pushing content down.
- Follows the PhosphorDice visual spec (`DESIGN.md` in the PhosphorDice project): one phosphor accent per theme; gold and red are reserved for crit/fail meaning, so CP and the Ready state use the accent. Labels carry `// ` prefixes, hints `> `, and unscored values show `--`. Motion is stepped and brief, and off under reduced motion.
- Keeps the screen awake during rounds where the browser allows it.

## Not yet built

- Real cross-device sync (for example Supabase or WebSockets); everything currently runs in one page.
- Real QR generation and camera scanning.
- Army, detachment and disposition are free-text today; picking them from an auto-populated list is a later step.
- The general 404 page.
