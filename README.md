# NeverMiss AI


<h2 align="center">Preview</h2>

<p align="center">
  <video src="nevermiss.mp4" width="500" controls></video>
</p>


An AI that answers your phone when you can't.

Most people let calls go to voicemail and deal with them later, if at all. NeverMiss AI picks up instead. It listens to the caller, figures out who they are and what they want, and handles it the way you would: books an appointment, warns you if it smells like a scam, translates if the caller speaks another language, and gives you a clear summary the moment the call ends.

Built for [try.ka.nz](https://try.ka.nz/) AI hackathon.

## What it actually does

Say someone calls while you're in a meeting. NeverMiss AI:

1. Answers and talks to them like a real assistant would, not a phone tree.
2. Works out who's calling and why: a recruiter, a family member, a delivery driver, a scammer, whoever.
3. Follows rules you set. You decide what it's allowed to promise or agree to.
4. Books, moves, or cancels appointments on the spot if that's what the call needs.
5. Flags anything that sounds like fraud (fake bank calls, "verify your OTP," that kind of thing) and explains why.
6. Writes up a summary after the call: what was said, what needs following up, any dates or numbers mentioned.
7. If something's urgent (a hospital, an accident, an emergency), it flags that too so you notice it fast.

You see all of this on a live dashboard while the call is still happening, transcript and all.

## Tech stack

**Backend:** Python, FastAPI, PostgreSQL, Redis, ChromaDB for long-term memory of your preferences and past calls.

**Voice:** Twilio for the phone line, Groq for speech-to-text, text-to-speech, and the language model driving the conversation (Llama 3.3 70B).

**Frontend:** Next.js, TypeScript, Tailwind CSS, shadcn/ui.

**Auth:** Clerk.

**Calendar:** Own built-in scheduler by default, with optional Google Calendar sync once you connect an account.

**Deploy:** Docker Compose.

## Requirements

- Docker and Docker Compose.
- A Twilio account with a phone number.
- A Groq API key.
- A Clerk account, for dashboard login.
- A Google Cloud OAuth client, only if you want real Google Calendar sync. Skip it and the app uses its own built-in calendar instead.

## Try it

1. Copy `.env.example` to `.env` and fill in your keys (Twilio, Groq, Clerk, and optionally Google Calendar).
2. Run `docker compose up`. This builds and starts everything: PostgreSQL, Redis, ChromaDB, the backend on port 8010, and the frontend on port 3000.
3. Point your Twilio number's voice webhook at your running backend (`https://your-domain/twilio/voice`). For local testing, expose it first with something like ngrok.
4. Open `http://localhost:3000`, call your Twilio number, and watch the call show up live on the dashboard.

Prefer running things without Docker? `scripts/dev_up.sh` starts the backend and frontend directly, useful while actively developing.

No Google Calendar? No problem: bookings just get stored and shown in the dashboard's own calendar instead.

## Status

Working end to end: calls come in, get transcribed, get a real AI response, and show up live on the dashboard. Appointment booking, scam detection, and call summaries are all functional. Some pieces (analytics, multi-language polish) are still rough since this came out of a hackathon sprint, not a year of production hardening.

## Why this exists

Nobody wants to miss the call that actually mattered, a job offer, a family emergency, a doctor's office trying to reschedule you. Voicemail doesn't solve that. This tries to.

## NOTE

AI can make mistakes. Please verify important information before relying on it.