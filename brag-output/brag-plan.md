# Brag Plan: NeverMiss AI

## What is this app?
An AI that answers your phone when you can't, figures out who's calling and what they want, books or reschedules appointments on the spot, and flags anything that smells like a scam, all visible live on a dashboard.

## The angle
No landing page, no marketing fluff, this product's whole pitch is the dashboard itself: a dark, quiet screen that watches a real phone call happen and handles it. The video is a single call moving through that dashboard, start to finish, letting the actual UI (live transcript, caller ID with confidence score, action approvals, calendar booking) carry the story.

## Hook (first 2-3 seconds)
Near-black frame. The agent's status card, alone, center screen: "Agent phone number" over a number, a green dot, "Online." No other chrome yet. Restraint first, then the dashboard fills in around it.

## Key moments (the middle)
- Live transcript fills with real turns, caller then agent, bubbles landing one at a time.
- Caller info resolves: relation type, a confidence percentage, the detected intent.
- The action feed logs the call's outcome: an action row lands marked "allowed," the call summary writes itself underneath, and a new event appears in the calendar.

## Outro / punchline
Recent calls stacks up, row after row, quiet proof this isn't a one-off demo. Cut to the wordmark: "NeverMiss AI" over "Never miss the call that mattered."

## User flow worth showing
1. Entry: phone rings in, dashboard status flips online, transcript starts streaming live.
2. Key action: caller gets identified (who, why) and the agent takes an action against that intent.
3. Result: action logged as allowed, summary written, calendar updated, call filed into recent calls.

## Tone
- Preset: polished
- Creative direction: a quiet, competent product film, no jokes, the calm of a screen doing its job while you're somewhere else
- Interpretation: few scenes, slow confident holds, restrained motion, let the real UI content be the spectacle instead of typography tricks

## Format: landscape — 1920x1080
## Duration: 20s

## Visual identity (from the project)
- Background: oklch(0.145 0 0) (near-black, dark mode is the only mode, forced via `dark` class on `<html>`)
- Card surface: oklch(0.205 0 0)
- Accent (live/allowed states): green-500; (denied): red-500
- Text: oklch(0.985 0 0) foreground, oklch(0.708 0 0) muted
- Display font: Geist Sans
- Body font: Geist Sans (Geist Mono available for numeric/mono accents)
- Strongest visual element: the rounded, border-hairline card grid of the actual dashboard (`rounded-lg`/`rounded-xl border border-border bg-card/60 backdrop-blur`), and the transcript's chat-bubble layout (agent bubbles right-aligned/tinted, caller bubbles left-aligned/muted)

## Share copy (draft)
Built an AI that picks up when you can't, figures out who's calling and why, books the appointment, and catches the scam call before you do.

## Audio direction
- Role: warm, steady bed under a restrained UI-sound layer
- Music: `happy-beats-business-moves-vol-12-by-ende-dot-app.mp3` (109.96 BPM, steady/clean, suited to polished)
- Music treatment: start at 0s, volume 0.3, gentle fade out over the last ~1s of the outro
- Music cue guidance: preset read from bundled cues. Target strong cues near 8.74s (transcript/caller-ID resolves) and 13.11s (action approved). Scene cuts at 4.4s and 15.3s ride the nearby beat grid (4.39s, 15.29s) rather than forcing an exact strong-cue lock.
- Audio-reactive treatment: subtle; card border/glow on the currently-active panel may breathe slightly with RMS, nothing else reacts
- SFX posture: minimal but present, 2-3 cues total, nothing louder than the music bed
- Audio-coupled moments: transcript bubbles land with a very soft drop; the "allowed" action row and calendar event get one quiet confirn accent; recent-calls rows in the outro are not individually scored, only the wordmark gets a last soft accent
- Restraint rule: no per-character typing sound, no click on every hover, at most one accent per scene

## Storyboard

### Scene 1 — Online — 4.4s
Near-black frame. The StatusCard alone, centered: "Agent phone number" label, the number, green pulse dot, "Online." Nothing else on screen yet.
Sequential/interaction: none
Audio intent: quiet open, let the bed establish before anything happens on screen
Audio-coupled idea: none
Music: steady bed enters at low presence
Transition mood: soft crossfade → Scene 2

### Scene 2 — The call comes in — 4.9s (4.4s → 9.3s)
Dashboard frame builds around the status card: transcript panel and caller-info panel appear. Transcript bubbles land one at a time (caller bubble muted/left, agent bubble tinted/right), 2-3 turns. Caller info resolves alongside it: relation type label, confidence percentage ticking to its final value, detected intent line.
Sequential/interaction: yes, transcript bubbles arrive one by one in sync with caller info fields resolving
Audio intent: attentive, something is actively happening
Audio-coupled idea: soft drop sound on each transcript bubble landing, softest on the first, slightly more presence on the last as it nears the scene's strong cue
Music: bed continues, lift in presence toward the strong cue at 8.74s
Transition mood: clean → Scene 3

### Scene 3 — It handles it — 6.0s (9.3s → 15.3s)
Action feed panel: an action row lands ("Book appointment," tagged "allowed" in green). Call summary text writes in underneath. Calendar widget gets a new event card appearing beside it.
Sequential/interaction: yes, action row lands, then summary text, then the calendar event, in that order
Audio intent: quiet payoff, the moment the product proves its claim
Audio-coupled idea: one restrained confirm accent when the "allowed" tag appears, timed near the 13.11s strong cue
Music: bed holds near its fullest presence for this scene
Transition mood: clean → Scene 4

### Scene 4 — Outro — 4.9s (15.3s → 20.2s)
Recent calls list builds, row after row stacking in quickly, implying volume and repetition, not a single lucky demo. Cut to the wordmark on near-black: "NeverMiss AI" then, smaller beneath, "Never miss the call that mattered."
Sequential/interaction: yes, recent-call rows stack in quickly (unscored individually), then a hard settle into the wordmark
Audio intent: confident close
Audio-coupled idea: one soft accent under the wordmark landing, then music fades
Music: bed begins its fade under the wordmark, silent by 20.2s
Transition mood: soft → end

**Music mood for this video:** polished, steady, clean corporate-adjacent bed (vol-12)
**Audio summary:** one continuous low bed from open to close, three restrained accents (transcript bubbles, action approval, wordmark), fading out under the final logo, nothing in the mix competes with the real UI content it's scoring.
