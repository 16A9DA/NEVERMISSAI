# NeverMiss AI

## Overview

AI personal call agent. Answers phone calls when user unavailable. Not receptionist bot, digital rep: understands user prefs, decides within set limits, detects scams, schedules appointments, translates calls, summarizes, escalates emergencies.

Covers: job interviews, recruiter calls, family emergencies, hospital calls, business opportunities, deliveries, government calls.

## Stack

Frontend: Next.js, TypeScript, TailwindCSS, Framer Motion, Shadcn UI.
Backend: FastAPI (Python).
Realtime: WebSockets.
Voice: Twilio Voice (mock transport for demo), Groq STT and TTS.
LLM: Groq (llama 3.3 70b versatile).
Data: PostgreSQL, Redis, ChromaDB (long term memory).
Auth: Clerk.
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

In active development. Backend (FastAPI) covers voice pipeline, calendar, memory, permissions, and WebSocket routers. Frontend (Next.js) app scaffolded with components, hooks, and API proxy. Full spec in `plan.md`.

## Install

Backend: Python virtualenv, install `backend/requirements.txt` (or equivalent), configure `.env` from `.env.example`, run `uvicorn app.main:app`.
Frontend: `npm install` in `frontend/`, then `npm run dev`.
See `scripts/dev_up.sh` for a combined startup path.

## Usage

Start backend and frontend as above, then call the configured Twilio number (or use the mock transport for local demo) to exercise the call pipeline.
