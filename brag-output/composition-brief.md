# Hyperframes Composition Brief: NeverMiss AI

## Objective
Create a short launch-style brag video for NeverMiss AI.

## Output
- Composition directory: `brag-output/composition/`
- Rendered video: `brag-output/brag.mp4`
- Format: landscape — 1920x1080
- Duration: 20 seconds

## Source Material
- Project root: `/Users/ryn/Documents/callai`
- Primary files read: `frontend/src/app/dashboard/page.tsx`, `frontend/src/components/dashboard/{StatusCard,TranscriptStream,CallerInfoPanel,ActionFeed,RecentCalls,CalendarWidget}.tsx`, `frontend/src/app/globals.css`, `frontend/src/app/layout.tsx`, `README.md`, `UI.png`
- Product name: NeverMiss AI
- Tagline / strongest claim: "An AI that answers your phone when you can't."
- Key UI or visual moment to recreate: the live dashboard itself — status card, streaming transcript bubbles, caller-info resolution, the action feed's allowed/denied tags, and recent calls list, as shown in `UI.png`
- Copy that must appear verbatim:
  - "Agent phone number"
  - "Online"
  - "Conversation transcript"
  - "live"
  - "Caller information"
  - "Actions"
  - "allowed"
  - "Recent calls"
  - "NeverMiss AI"
  - "Never miss the call that mattered."

## Creative Direction
- Tone preset: polished
- Creative direction: a quiet, competent product film, no jokes, the calm of a screen doing its job while you're somewhere else
- Interpretation: 4 scenes, slow confident holds (4-6s each), restrained motion, soft crossfades, let the real dashboard content be the spectacle instead of typographic tricks
- Angle: no landing page exists for this product, the dashboard is the pitch. Show one real call moving through it start to finish: online → live transcript and caller ID → action taken and logged → filed into history.
- Hook: near-black frame, the agent status card alone, center screen, green dot, "Online."
- Outro / punchline: recent calls stacking up (proof of repeated use, not a single staged demo), settling into the wordmark "NeverMiss AI" / "Never miss the call that mattered."
- Avoid:
  - Generic SaaS language ("streamline," "workflow," etc.)
  - Abstract filler visuals (no particle systems, no unrelated gradients)
  - Any redesign of the actual dashboard's grayscale/near-black look, borders, or card style

## Visual Identity
- Background: oklch(0.145 0 0) — near-black, dark mode is the project's only mode
- Text: oklch(0.985 0 0) foreground; oklch(0.708 0 0) muted-foreground
- Accent: green-500 for "Online"/"live"/"allowed" states, red-500 reserved for "denied" (not needed in this cut)
- Card surface: oklch(0.205 0 0), `rounded-lg`/`rounded-xl`, `border border-border`, some panels `bg-card/60 backdrop-blur`
- Display font: Geist Sans (fallback: Inter or system sans if Geist unavailable in the renderer)
- Body font: Geist Sans; Geist Mono acceptable for the phone number / confidence percentage
- Visual references from the project: `UI.png` (ground truth screenshot of the real dashboard layout — status card top, transcript + recent calls left column, caller info + actions + calendar right column)

## Storyboard
Use the storyboard in `brag-output/brag-plan.md` as the creative contract.

Scene summary:
1. Online — 4.4s — status card alone, centered, "Agent phone number," a number, green dot, "Online"
2. The call comes in — 4.9s — transcript bubbles land one at a time (caller/agent alternating), caller-info panel resolves relation type + confidence % + intent alongside it
3. It handles it — 6.0s — action feed logs "Book appointment" tagged "allowed," call summary writes in beneath it, a calendar event appears
4. Outro — 4.9s — recent-calls rows stack in quickly, then settle into the wordmark "NeverMiss AI" / "Never miss the call that mattered."

## Audio
- Audio role: warm, steady bed under a restrained UI-sound layer
- Audio arc: one continuous low bed from open to close, three restrained accents (transcript bubbles landing, action approved, wordmark), fading out under the final logo
- Music: `happy-beats-business-moves-vol-12-by-ende-dot-app.mp3`
- Music treatment: start at 0s, volume ~0.3, gentle fade over the last ~1s under the wordmark
- Music cue guidance: bundled preset at `<skill-dir>/assets/music/cues/happy-beats-business-moves-vol-12-by-ende-dot-app.music-cues.md` / `.json` (109.96 BPM). Strong cues near 8.74s and 13.11s are good targets for the Scene 2→3 and in-scene-3 approval beat; nearby beat grid points (4.39s, 15.29s) are reasonable for the other scene cuts. Treat as hints, not requirements.
- Audio-reactive treatment: subtle; the active panel's border/glow may breathe slightly with RMS — nothing else should react
- Audio-coupled moments:
  - Scene 2 — transcript bubbles landing one by one — soft drop-style accent, softest on the first bubble, slightly more presence near the scene's strong cue
  - Scene 3 — the "allowed" tag appearing — one restrained confirm accent, timed near the 13.11s strong cue
  - Scene 4 — wordmark landing — one soft accent, then music fades
- SFX selection guidance: match the gesture — soft drop/landing sounds for bubbles and cards, one clean confirm/announcement-style cue for the approval moment, nothing per-character-typed, nothing on every recent-calls row
- SFX analysis guidance: use `<skill-dir>/assets/sfx/sfx-analysis.md` to prefer low/medium high-frequency-risk files for these repeated, polished moments
- Exact SFX choice: Hyperframes chooses filenames, timestamps, density, and volume based on the implemented animation
- Audio files: copy the chosen music into `brag-output/composition/assets/music/`; Hyperframes copies any SFX it selects into `brag-output/composition/assets/`

## Hyperframes Instructions
Load the composition-building Hyperframes domain skills — `hyperframes-core` (composition contract + `data-*` timing), `hyperframes-animation` (motion), `hyperframes-creative` (design spec, beats, audio-reactive), `hyperframes-keyframes` (seek-safe keyframes), and `hyperframes-cli` (lint/check/render). `/brag` is its own workflow: do not enter the `hyperframes` entry-point intent interview and do not route into its generic promo / launch-video workflow. Prefer native Hyperframes conventions over anything in `/brag`.

Requirements:
- Show at least one real UI, copy, or visual element from the source project (the dashboard cards, transcript layout, and copy above).
- Keep all text readable in the final render.
- Keep the video within 15-25 seconds (target 20s).
- Include the planned music/SFX layer.
- Treat `/brag` audio notes as guidance, not a fixed cue sheet. Choose SFX after the visual animation exists.
- Treat music cue metadata as optional timing hints. Ignore cues that hurt readability, scene pacing, or the product story.
- Use only 1-3 strong cue locks in this 20s video.
- Use SFX to support motion and interaction: soft drop/card sounds for reveals, one short announcement-style cue for the approval payoff, restraint elsewhere.
- Honor the planned fade-out under the final logo.
- When wiring audio-reactive treatment, follow the `hyperframes-creative` skill's own extraction workflow; if extraction is unavailable, skip it and note that in delivery rather than blocking the render.
- Use local assets for audio.
- Run `hyperframes check` before render — it is brag's single gate.
