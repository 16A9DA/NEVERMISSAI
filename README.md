# NeverMiss AI

## Overview

AI personal call agent. Answers phone calls when user unavailable. Not receptionist bot, digital rep: understands user prefs, decides within set limits, detects scams, schedules appointments, translates calls, summarizes, escalates emergencies.

Covers: job interviews, recruiter calls, family emergencies, hospital calls, business opportunities, deliveries, government calls.

## Planned stack

Frontend: Next.js, TypeScript, TailwindCSS, Framer Motion, Shadcn UI.
Backend: FastAPI (Python).
Realtime: WebSockets.
Voice: Twilio Voice (or simulated for demo), Realtime LLM API, Whisper STT, TTS.
LLMs: GPT-5.5, Gemini, Claude, OpenRouter fallback.
Data: PostgreSQL, Redis, ChromaDB (long-term memory).
Auth: Clerk or Auth.js.
Deploy: Docker.

## Core capabilities

- Caller identification with confidence score (recruiter, employer, family, delivery, bank, government, hospital, school, unknown).
- Intent detection (interview, delivery, appointment, emergency, spam, fraud, sales, personal, business).
- Urgency engine, score 0 to 100, green/yellow/orange/red.
- Scam detection with explanation (fake banks, OTP requests, deepfake voices, tech support and courier scams).
- Permission engine: user-defined allow/deny rules the AI must obey.
- Personal memory: hours, calendar, languages, contacts, style, past conversations.
- Calendar integration: create/reschedule events, check availability.
- Real-time translation (English, Arabic, Urdu, French, German, Spanish).
- Emergency mode: immediate alert plus priority flag on accident, hospital, police, fire, ambulance, medical.
- Smart call summaries: action items, deadlines, people, locations, numbers, events.
- Live dashboard: waveform, streaming transcript, urgency gauge, scam score, actions, notifications.
- Analytics: calls answered, time saved, scams blocked, appointments scheduled, response time.

## Status

Spec stage only, see `plan.md`. No application code yet.

## Install

Not yet runnable. Stack and setup steps land once implementation starts.

## Usage

Pending implementation.
