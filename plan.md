MASTER PROMPT — NeverMiss AI

You are an elite team of AI engineers, backend developers, frontend engineers, UX designers, product managers, and hackathon winners.

Your task is to build a production-quality AI application called NeverMiss AI.

Mission

Build an AI Personal Call Agent that can answer phone calls on behalf of the user when they are unavailable.

This is NOT an AI receptionist.

This is a digital representative that understands the user’s preferences, makes decisions within defined limits, detects scams, schedules appointments, translates conversations, summarizes calls, and escalates emergencies.

The demo should leave judges thinking:

“This feels like the future of phone calls.”

⸻

Core Value Proposition

Never miss:

* Job interview calls
* Recruiter calls
* Family emergencies
* Hospital calls
* Business opportunities
* Delivery calls
* Government calls

The AI acts like the user—not a generic chatbot.

⸻

Tech Stack

Frontend:

* Next.js
* TypeScript
* TailwindCSS
* Framer Motion
* Shadcn UI

Backend:

* FastAPI (Python)

Realtime:

* WebSockets

Voice(ARABIC AND ENGLISH):

LLMs:


* STS: nvidia
parakeet-1.1b-rnnt-multilingual-asr
* TTS nvidia chatterbox-multilingual-tts


Database:

* PostgreSQL
* Redis
* ChromaDB (long-term memory)

Authentication:

* Clerk 

Deployment:

* Docker

⸻

Main Dashboard

Create a futuristic dashboard.

Sections:

• Live Incoming Calls

• AI Status

• Conversation Transcript

• Caller Information

• Urgency Score

• Scam Detection Score

• Calendar

• Follow-up Tasks

• AI Memory

• Call History

• Analytics

Dark theme with Apple-quality UI.

⸻

Main Workflow

Incoming Call

↓

Identify Caller

↓

Check Contact Database

↓

Detect Intent

↓

Estimate Urgency

↓

Run Scam Detection

↓

Consult Personal Memory

↓

Consult Permission Rules

↓

Generate Response

↓

Speak Naturally

↓

Take Actions

↓

Create Summary

↓

Notify User

Everything streams live.

⸻

AI Capabilities

Caller Identification

Identify:

* Recruiter
* Employer
* Family
* Delivery
* Friend
* Unknown
* Bank
* Government
* Hospital
* School

Display confidence score.

⸻

Intent Detection

Examples:

Interview

Delivery

Appointment

Emergency

Spam

Support

Sales

Fraud

Personal

Business

⸻

Urgency Engine

Assign score 0–100.

Green

Yellow

Orange

Red

Emergency calls trigger immediate notifications.

⸻

Scam Detection

Detect:

* Fake banks
* Investment scams
* OTP requests
* Deepfake voices (prototype)
* Tech support scams
* Fake courier scams

Explain WHY a call is suspicious.

⸻

Permission Engine (Key Differentiator)

The user defines rules.

Examples:

✔ Schedule meetings

✔ Confirm interview times

✔ Reschedule appointments

✔ Accept deliveries

✔ Translate conversations

✔ Take messages

✘ Never reveal passwords

✘ Never reveal personal ID

✘ Never accept payments

✘ Never agree to legal contracts

The AI must obey these rules.

⸻

Personal Memory

Remember:

Preferred working hours

Calendar availability

Languages(AR/EN)

Frequently contacted people

Preferred meeting locations

Communication style

Common answers

Previous conversations

⸻

Calendar Integration

The AI can:

Create events

Reschedule meetings

Check availability

Avoid conflicts

⸻

Translation

Support:

English

Arabic


Translate conversations in real time.

⸻

Emergency Mode

If the AI detects:

Accident

Hospital

Police

Fire

Ambulance

Medical emergency

It should:

Notify the user immediately

Call emergency contacts if configured

Highlight the transcript

Create a priority alert

⸻

Smart Summaries

Generate:

Summary

Action Items

Meeting Details

Deadlines

People Mentioned

Locations

Important Numbers

Calendar Events

⸻

Live Dashboard

Show:

Incoming waveform

Transcript streaming

Thinking indicator

Current AI reasoning

Urgency gauge

Scam probability

Actions being executed

Calendar updates

Notifications

Memory lookup

Everything updates live.

⸻

Demo Script

Demo 1

Recruiter calls.

AI:

Recognizes recruiter.

Checks calendar.

Schedules interview.

Creates event.

Sends confirmation.

Summarizes call.

⸻

Demo 2

Delivery driver calls.

AI confirms preferred delivery instructions.

Updates notes.

⸻

Demo 3

Scammer calls.

AI detects phishing language.

Politely refuses.

Flags the number.

Notifies the user.

Explains why it was suspicious.

⸻

Demo 4

Hospital calls.

AI detects emergency.

Immediately alerts the user.

Highlights urgency.

⸻

Analytics

Display:

Calls answered

Time saved

Scams blocked

Appointments scheduled

Missed opportunities prevented

Average response time

Languages used

Urgency distribution

⸻

UI Requirements

Use glassmorphism.

Animated cards.

Live graphs.

Typing indicators.

Voice waveform.

Smooth transitions.

Professional spacing.

Modern typography.

Responsive design.

⸻

Stretch Features

* Voice cloning (ethical demo only with consent)
* AI mood detection
* Follow-up email drafting
* WhatsApp summary generation
* CRM integration
* Company mode for small businesses
* Offline fallback
* Multi-agent architecture (Conversation Agent, Safety Agent, Scheduler, Memory Agent)

⸻

Code Quality

Use clean architecture.

Modular code.

Production-level components.

Environment variables.

Docker support.

Comprehensive README.

Setup guide.

API documentation.

No placeholder code unless explicitly marked.

Generate the complete project from folder structure to deployment, ensuring the application is runnable and demo-ready for a hackathon.