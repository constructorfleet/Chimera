0. Core mental model

Think of it like this:
	•	MQTT = edge devices & HA events
	•	Redis = job queues / streams / fast passing of payloads
	•	NATS = routing brain between services (orchestration bus)
	•	Router fast classifier & triage to:
		•	Jetson = heavy inference (CV, Whisper, big models)
		•	Swarm = LLMs, Qdrant, databases, MCP stuff, etc.

1. Audio pipeline (Vox): voice assistants done properly

Flow
	1.	Remote voice nodes
	•	Record audio chunks or full utterances
	•	Publish metadata over MQTT
	•	Ship raw audio over HTTP/WebSocket or chunked via Redis (Wyoming? Hermes?)
	2.	fast classification
	•	Use a tiny model to answer:
	•	“Is this real speech?”
	•	“Is wake word present?”
	•	“Is this a simple intent (lights, media controls, volume) I can map immediately?”
	•	If junk → drop
	•	If simple intent → go straight to HA via NATS/MQTT
	•	If complex → send to Whisper/ASR
	3.	Whisper / ASR
	•	Consumes audio jobs from Redis Stream:
audio:incoming
	•	Writes transcript to Redis Stream:
audio:transcribed
	4.	LLM / Intent layer (Swarm)
	•	A small router service listens to audio:transcribed
	•	Uses LLM (or rules) to produce:
	•	intent
	•	entities
	•	arguments
	•	Emits to NATS subject:
voice.intent.<type> (e.g. voice.intent.media.play)
	5.	HA / Automation
	•	Subscribes to relevant NATS subjects
	•	Performs actual actions

Concrete bus pieces

MQTT topics (from Voice Nodes):
	•	voice/<device_id>/audio_meta
	•	voice/<device_id>/wake
	•	voice/<device_id>/status

Redis streams:
	•	audio:raw – metadata + pointer to audio (file path, S3, or Redis key)
	•	audio:classified – result from classifier (speech / noise / category)
	•	audio:incoming – jobs for Whisper
	•	audio:transcribed – { text, device_id, ts, classification }

NATS subjects:
	•	audio.event.classified – classification events
	•	voice.intent.* – high-level intents to HA or other services

⸻

2. Vision pipeline (Gaze): Frigate + Coral + Jetson without stupidity

Flow
	1.	Cameras → Edge Node (Pi or similar)
	•	Edge Node ingests low-res RTSP frames or snapshots
	2.	Fast Classifier
	•	Run a tiny classifier:
	•	no motion / irrelevant (tree, light changes)
	•	simple motion
	•	“human-ish” shapes
	•	“vehicle-ish”
	•	If obviously empty → drop
	•	If interesting → forward HD frame to Jetson / Frigate
	3.	Jetson / Frigate
	•	Perform heavy object detection / tracking
	•	Emit events back via MQTT and/or NATS:
	•	person detected
	•	zones crossed
	•	object tracked IDs
	4.	Router
	•	Take Frigate’s MQTT events
	•	Push into NATS:
	•	vision.event.person_detected
	•	vision.event.package
	•	Optionally push long-term events to Redpanda / VicMet

Suggested wiring

MQTT topics (Frigate, Pi 5, HA):
	•	frigate/events
	•	cameras/<cam_id>/motion_raw
	•	cameras/<cam_id>/motion_filtered

Redis streams:
	•	vision:raw – snapshots / metadata for Classifier
	•	vision:filtered – Coral decisions
	•	vision:jobs:frigate – frames/URLs for Jetson/Frigate

NATS subjects:
	•	vision.event.motion.simple
	•	vision.event.person
	•	vision.event.vehicle
	•	vision.event.door

⸻

3. LLM routing pipeline (Mind): “send smart stuff to the right model”

Routing needs to:
	1.	Decide what kind of prompt this is
	2.	Decide if it needs:
	•	Home automation
	•	Local chat
	•	Tool use / MCP
	•	Media control
	•	“Ask a big model”
	3.	Fan it out via NATS

Flow
	1.	Prompt arrives from:
	•	Voice (post-transcription)
	•	Web UI (Chat)
	•	HA automations
	•	Some dumb script you’ll forget about in 2 weeks
	2.	Pre-classification
Coral model or small heuristic does basic routing:
	•	is this automation?
	•	is this media-related?
	•	is this general chat?
	•	is it short/simple vs long/complex?
	•	is this unsafe / blocked? (coarse filter)
	3.	Router
	•	Consumes from Redis Stream:
llm:incoming
	•	Sends job details to appropriate NATS subject:
	•	llm.route.automation
	•	llm.route.media
	•	llm.route.chat.small
	•	llm.route.chat.large
	•	llm.route.tools
	4.	Downstream workers (in swarm / Jetson)
	•	Ollama small models subscribe to llm.route.chat.small
	•	Heavier LLM infra / GPU-backed stuff subscribes to llm.route.chat.large
	•	MCP handlers subscribe to llm.route.tools
	•	HA bridge subscribes to llm.route.automation
	5.	Responses
	•	Responses published to llm.response.<origin> or llm.response.<session_id>
	•	Original client subscribes or polls via REST/WebSocket

⸻

4. How all three fit on the buses

Here’s the cheat sheet:

MQTT
	•	Entry/exit point for:
	•	Edge voice
	•	Cameras / Frigate
	•	HA
	•	Sensors
	•	MQTT is your edge device language.

Redis
	•	Short-lived job payloads:
	•	audio:*
	•	vision:*
	•	llm:incoming, llm:jobs:*
	•	Acts as the “payload staging area” between edge and Jetson/Swarm.

NATS
	•	Event + RPC fabric:
	•	voice.intent.*
	•	vision.event.*
	•	llm.route.*
	•	automation.*
	•	Basically the “brain bus” your logic talks on.
