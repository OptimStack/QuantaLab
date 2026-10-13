# Quantum Learning & Simulation Platform — Project Masterplan
**SIH 2026 · Theme: Smart Education · Team: Egreen Quanta**
**"An AI-Powered Interactive Platform to Learn, Design, Simulate, and Visualize Quantum Algorithms"**

> Working title used throughout this document: **QuantaLab**. Rename freely — nothing in
> the architecture depends on the name. This file is the single source of truth for an
> implementation agent. Follow the milestones in Section 9 strictly in order. Do not
> write code until a milestone is reached.

---

## 0. Programming Language Decision — read this first

You asked me to think through which languages are actually needed and which aren't,
and decide. Here's the full reasoning, then the decision.

### 0.1 What the problem statement actually forces
The Expected Solution explicitly requires execution on **Qiskit Aer, PennyLane, Cirq,
and qBraid**. This is the single most architecturally decisive fact in the whole
problem statement: **all four of those are Python SDKs.** There is no JavaScript,
Java, or Go equivalent with comparable fidelity, community support, or gate-set
coverage — a few partial JS quantum-simulation libraries exist (e.g. quantum circuit
simulators written for visualization demos), but none of them *are* Qiskit, PennyLane,
Cirq, or qBraid, and the PS names those specifically. This means **the simulation/execution
core of the backend must be Python**, full stop — not a preference, a constraint.

### 0.2 Language-by-language decision

| Language | Needed? | Where / Why |
|---|---|---|
| **Python 3.11+** | **Yes — mandatory, core of the system** | The only language that gives you real Qiskit Aer / PennyLane / Cirq / qBraid execution. Also runs the backend API (FastAPI — see 0.4), the AI-tutor integration layer, the sandboxed code-execution runner, background job workers, and all data-processing/grading logic. |
| **JavaScript (ES6+), not TypeScript** | **Yes — frontend only** | Per your established preference from the last project: React + Vite + TailwindCSS frontend, plain `.jsx`, no TS. This is where the drag-and-drop circuit builder, the code editor (Monaco), the Bloch-sphere/visualization components, and all dashboards live. Nothing here needs Python. |
| **SQL** | **Yes — via the database** | For the relational schema in Section 5 (Postgres). Mostly written through an ORM (SQLAlchemy) rather than hand-written, but it's a real part of the stack — raw queries will be needed for some analytics/instructor-dashboard aggregations. |
| **OpenQASM 2.0/3.0** | **Yes — but as a data format, not an app language** | The standard interchange format for quantum circuits. Students should be able to export a circuit they built (drag-and-drop or code) as OpenQASM, and import existing `.qasm` files. All four target SDKs can parse/emit it, so it's the natural "lingua franca" between the visual builder and any backend. You don't write application logic in it — you support it as an import/export format. |
| **Bash / shell** | **Yes — ops only** | Deployment scripts, Docker entrypoints, systemd unit invocation. Not application logic. |
| **YAML / Dockerfile syntax** | **Yes — ops only** | `docker-compose.yml` for local dev (Postgres + Redis + backend + sandbox runner), Dockerfiles for the sandboxed execution image. Infrastructure config, not a programming language in the usual sense, but worth naming since it's a real part of what gets written. |
| **TypeScript** | **No** | Explicitly excluded per your stated preference. Plain JS with good component boundaries and JSDoc comments (where you want inline type hints without a build-time type checker) is sufficient for this scope. |
| **Java / C#** | **No** | No part of the Expected Solution needs a JVM or .NET runtime. None of the four required quantum SDKs are Java/C#-native. Adding either would only introduce a second backend stack to deploy and maintain, for zero functional gain. |
| **Go / Rust** | **No (for MVP)** | These are the languages you'd reach for if the sandboxed code-execution runner needed to be extremely fast or memory-safe at scale. For a 36-hour hackathon build, Python-plus-Docker-resource-limits (Section 6) is sufficient and far faster to build correctly. Flag this as a legitimate **post-hackathon optimization** if the sandbox ever needs to handle high concurrent load — not a Day 1 requirement. |
| **R** | **No** | Tempting because of its stats/plotting pedigree, but Python's scientific stack (NumPy, Matplotlib, Plotly) already covers every visualization and numerical need here. Introducing R would only fragment the stack. |
| **PHP / Ruby** | **No** | No reason to introduce either; FastAPI covers the same ground with the advantage of staying in the same language as the quantum SDKs. |
| **C/C++** | **No — but indirectly present** | Qiskit Aer's simulator core is itself implemented in C++ under the hood, and PennyLane/Cirq have some C-extension dependencies. **You never write this code** — you consume it through the Python package. Worth knowing so nobody is surprised by compiled-extension install issues (Section 10, edge cases), but it is not a language you write against.
| **Node.js as a *backend* runtime** (i.e., an Express/Nest API) | **No — build-tool only** | Exactly like the Krishi-Setu project: Node.js is needed only to run `npm run build` for the Vite frontend. It is never a second backend language. Running the real backend in Python only (not splitting "API in Node, simulation in Python") avoids a cross-language service boundary that would otherwise need its own contract, serialization, and failure-handling layer — unnecessary complexity for a 36-hour build. |

### 0.3 Net result
**Two application languages, each with one clear job:**
- **Python** — everything that touches quantum computation, AI integration, business
  logic, and the database.
- **JavaScript (not TypeScript)** — everything the user sees and interacts with in the browser.

Plus SQL (data layer), OpenQASM (circuit interchange format), and ops-only Bash/YAML/Dockerfile.
No other language earns its place in an MVP scoped to a 36-hour build.

### 0.4 Backend framework: FastAPI, not Flask — and why that's a deliberate change from last time
If you've used Flask before (e.g. on a prior project), note this is a **conscious
departure**, not an inconsistency:
- The simulation and AI-tutor endpoints are naturally **long-running and asynchronous**
  (a circuit simulation or an LLM-generated explanation can take seconds, and students
  will be running many of these concurrently in a classroom setting). FastAPI's native
  `async`/`await` support and first-class **WebSocket** support (for streaming AI-tutor
  responses token-by-token, and for live job-status updates) fit this far better than
  Flask's synchronous-by-default model.
- FastAPI auto-generates an OpenAPI schema and interactive docs from your route
  definitions and Pydantic models — valuable here because the frontend↔backend
  contract (Section 7) is larger and more varied than a typical CRUD app (circuit
  payloads, simulation job polling, AI chat streams, assessment grading).
- Everything else about the "decoupled frontend + reverse-proxied API behind Nginx"
  pattern carries over unchanged from the general architecture approach you already
  know — see Section 2.

---

## 1. Executive Summary & Goals

### 1.1 What we are building
**QuantaLab** is a web-based platform where students, researchers, and professionals
learn quantum computing by *doing*, not just reading: structured learning modules on
qubits, superposition, entanglement, and standard algorithms; a visual drag-and-drop
circuit builder alongside a real code editor; real execution of those circuits on
multiple real quantum simulation backends (Qiskit Aer, PennyLane, Cirq, qBraid);
visualization of the resulting quantum states (Bloch spheres, probability histograms,
circuit diagrams); and an AI tutor layered over all of it — explaining concepts,
generating and debugging code, and suggesting what a given student should learn next.

### 1.2 Why this problem is hard (and why most solutions fail at it)
Quantum computing education has three compounding gaps that this platform explicitly
targets:
- **Access** — real quantum hardware is scarce and expensive; most learners never get
  hands-on contact with anything beyond slides and equations.
- **Personalization** — a static course has one pace and one path; a learner stuck on
  "what does superposition actually *do* to a measurement outcome" gets the same
  content as a learner who's ready for Grover's algorithm.
- **Outcome-tracking** — without structured assessment and progress data, neither the
  learner nor an instructor can tell whether understanding actually happened, versus
  content merely being consumed.

A platform that only digitizes a textbook (static lessons + a single simulator) solves
none of these. QuantaLab is scoped specifically to address all three, which is also
exactly what the evaluator's questions (Section 1.5) will probe for.

### 1.3 Who it's for
- **Students** — structured learning paths, hands-on circuit building, instant
  feedback, AI explanations pitched at their current level.
- **Researchers / professionals** — a fast environment to prototype and test circuit
  ideas across multiple backends without separately installing and configuring four
  different SDKs locally.
- **Instructors** — cohort-level dashboards showing where learners are stuck, module
  completion rates, and assessment performance.

### 1.4 Goals for the hackathon build
- **G1 (MVP):** A learner can complete a structured module, build a circuit via
  drag-and-drop **or** code, run it on at least two of the four required backends, and
  see a Bloch sphere / measurement-probability visualization of the result.
- **G2 (MVP):** A working AI tutor — not a static FAQ, but live, context-aware
  responses: concept explanation, code generation for a stated task, and debugging
  help on a learner's actual (possibly broken) circuit code.
- **G3 (MVP):** At least one assessment type (auto-graded coding challenge or
  multiple-choice quiz) with progress tracked per learner and visible on an instructor
  dashboard.
- **G4 (MVP):** Secure execution — arbitrary learner-submitted code never runs with
  access to the host system; this is both a real security requirement and something
  evaluators will explicitly probe (Section 1.5).
- **G5 (Should-have):** A genuinely adaptive element — content or next-step
  recommendations that change based on real learner performance signals, not just a
  static curriculum tree. The PS's own opportunity analysis calls this out directly as
  the thing that separates a strong submission from a generic one.
- **G6 (Stretch):** OpenQASM import/export, multilingual UI, offline-capable lesson
  caching, qBraid live-hardware job submission (vs. simulator-only).
- **G7 (MVP):** A deployable, judge-proof demo — same "Vite static build + Python API
  behind Nginx" hosting pattern used previously, so hosting is a solved problem, not a
  last-minute scramble.

### 1.5 What the evaluator will likely ask — design for these from Day 1
These are in the official PS analysis verbatim; this masterplan's architecture exists
specifically so each has a real, truthful answer by demo day, not an improvised one:
1. **Is your data real or synthetic?** — be ready with a specific, honest answer:
   lesson content and assessment items will be authored/curated (not scraped), circuit
   execution results are **genuinely real** (actual Qiskit Aer/Cirq/PennyLane output, not
   mocked), and any "learner progress" data shown in a demo is seeded/synthetic — say so.
2. **Why this level of tech here, not overkill?** — the answer is that multi-backend
   real execution plus an AI tutor are not decoration; they are the direct response to
   the "static, theoretical, no real quantum hardware access" pain point named in the
   problem statement itself.
3. **Graceful degradation vs. breaking** — Section 10 names the specific failure modes
   (backend SDK unavailable, AI provider timeout, oversized circuit, lost connectivity)
   and what the system does instead of crashing.
4. **Production-scale behavior** — be ready to discuss what changes with 10,000
   concurrent learners vs. a demo's handful (Section 6.5, Section 10).
5. **Who benefits and how is success measured post-deployment** — module completion
   rate, assessment score improvement over attempts, time-to-concept-mastery, and
   instructor-visible cohort analytics (Section 5.10/5.11) are the concrete metrics —
   not just "page views."

---

## 2. System Architecture & Tech Stack Details

### 2.1 High-level architecture

```
                         ┌────────────┐
                         │   Browser   │  (Student / Instructor / Admin)
                         │ React SPA   │  circuit builder, code editor, visualizations
                         └──────┬──────┘
                                │ HTTPS
                         ┌──────▼──────┐
                         │  Cloudflare  │  DNS, SSL, DDoS/WAF, CDN
                         └──────┬──────┘
                                │
                   ┌────────────▼─────────────────────────────┐
                   │                 Host VM                     │
                   │  ┌──────────────────────────────────────┐  │
                   │  │                Nginx                    │  │
                   │  │  /          → frontend/dist (static)    │  │
                   │  │  /api/      → 127.0.0.1:8000 (uvicorn)  │  │
                   │  │  /ws/       → WebSocket upgrade          │  │
                   │  └───────────────┬──────────────────────┘  │
                   │                  │ proxy_pass                │
                   │          ┌───────▼────────┐                  │
                   │          │ uvicorn + FastAPI│ (systemd svc)   │
                   │          │  (Python, async) │                 │
                   │          └───┬───┬───┬───┬─┘                  │
                   └──────────────┼───┼───┼───┼──────────────────┘
                                   │   │   │   │
                 ┌─────────────────┘   │   │   └────────────────┐
                 ▼                     ▼   ▼                     ▼
        ┌─────────────────┐  ┌──────────────────┐   ┌─────────────────────┐
        │  PostgreSQL       │  │  Redis             │   │  AI Provider API      │
        │  users, courses,  │  │  Celery broker +   │   │  (LLM for tutor —     │
        │  circuits, scores,│  │  job status/cache   │   │  provider-agnostic,   │
        │  progress         │  └────────┬───────────┘   │  see Section 7)        │
        └───────────────────┘           │                └─────────────────────┘
                                         ▼
                              ┌────────────────────┐
                              │  Celery Workers      │   (Python)
                              │  simulation jobs,     │
                              │  assessment grading   │
                              └──────────┬────────────┘
                                         │ spawns, resource-limited
                              ┌──────────▼────────────┐
                              │  Sandboxed Execution    │
                              │  Container (Docker)     │
                              │  Qiskit Aer · PennyLane │
                              │  Cirq · qBraid adapters  │
                              └─────────────────────────┘

  Build-time only (never on the host VM at runtime):
  Node.js + npm → `frontend/` (React + Vite + Tailwind, JS) → `npm run build` → dist/
```

### 2.2 Tech stack (final)

| Layer | Choice | Notes |
|---|---|---|
| Frontend framework | **React 18, built with Vite** | JavaScript (`.jsx`), not TypeScript. |
| Frontend styling | **TailwindCSS** | Utility-first; dark/light theme support recommended given long study sessions. |
| Circuit builder (drag-and-drop) | **Custom React component over SVG/Canvas**, using `react-dnd` (or `@dnd-kit`) for drag interactions | No off-the-shelf "quantum circuit builder" library is mature enough to depend on — build a focused one: a gate palette, a wire/timeline grid, click-or-drag gate placement, exportable to a JSON circuit representation. |
| Code editor | **Monaco Editor** (`@monaco-editor/react`) | The same editor VS Code uses; supports Python syntax highlighting out of the box, which covers Qiskit/PennyLane/Cirq code directly. |
| Visualization | **Plotly.js** (Bloch spheres, probability histograms, statevector plots) + custom SVG for circuit diagrams | Plotly has ready-made 3D surface/sphere plotting, saving significant build time over hand-rolled WebGL. |
| Frontend routing | **React Router v6** | `/learn/*`, `/build/*`, `/assess/*`, `/instructor/*`, `/progress`. |
| Frontend data/streaming | **`fetch`/`axios`** for REST, native **WebSocket** for AI-tutor streaming and live job-status updates | Keep polling as a fallback for simulation-job status if WebSockets prove unreliable under demo conditions. |
| Backend framework | **Python 3.11+, FastAPI** | Async-first; Pydantic models double as request validation and OpenAPI docs. See Section 0.4 for why FastAPI over Flask here. |
| Backend auth | **JWT** (`fastapi-users` or hand-rolled with `python-jose`) | Roles: `student`, `instructor`, `admin`. |
| Background jobs | **Celery + Redis** | Simulation execution and auto-grading are both potentially slow — never run them in the request/response cycle; always dispatch to a worker and let the frontend poll/subscribe for the result. |
| Sandboxed code execution | **Docker container per execution, strict resource/time limits** | See Section 6 — this is the single most security-critical part of the system. |
| Quantum simulation backends | **Qiskit Aer, PennyLane, Cirq, qBraid** (all Python) | Unified behind one internal adapter interface — see Section 6.2. |
| AI tutor | **LLM API integration** (provider-agnostic — Anthropic/OpenAI/etc., configurable via env var) | See Section 7. |
| Database | **PostgreSQL** | Chosen over MongoDB here (unlike a prior project) because this domain is genuinely relational: users→courses→modules→lessons, assessments→questions→submissions→scores, instructor→cohorts→students. Foreign keys and joins are a better fit than document pooling. |
| ORM | **SQLAlchemy 2.0 + Alembic** (migrations) | |
| Reverse proxy | **Nginx** | Serves the built React app as static files, reverse-proxies `/api/` to uvicorn, and proxies `/ws/` for WebSocket upgrades. |
| App server | **uvicorn**, managed by **systemd** | |
| Hosting | **One host VM** (Azure/any Ubuntu VM) | Node.js is build-time only — same pattern as before. |
| Edge/CDN/Security | **Cloudflare** | |
| Circuit interchange format | **OpenQASM 2.0/3.0** | Export/import support — see Section 0.2. |
| Version control / methodology | **Git**, Agile iterative sprints | `frontend/` and `backend/` as clearly separated packages. |

### 2.3 Why this is the right shape for *this* problem
- Keeping **all quantum computation in Python** means every one of the four required
  SDKs is a native dependency, not something bridged across a language boundary.
- Keeping **all UI in JavaScript/React** means the circuit builder, code editor, and
  visualizations can be fast, interactive, and testable independently of backend load.
- **FastAPI's async model** is what makes "run a circuit on 2–4 different simulators
  and stream an AI explanation while that's happening" feel responsive rather than
  blocking.
- **Celery + Docker sandboxing** is what makes "let students submit arbitrary Python
  code" survivable from a security standpoint — this is non-negotiable, not optional
  polish (Section 6.3).

---

## 3. Complete Directory & File Structure Tree

```
quantalab/
├── masterplan.md
├── README.md
├── .gitignore
├── docker-compose.yml               # local dev: postgres, redis, backend, sandbox image
│
├── frontend/                        # React + Vite + Tailwind (JavaScript, no TS)
│   ├── package.json
│   ├── vite.config.js               # dev proxy: /api -> localhost:8000, /ws -> ws://localhost:8000
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── index.html
│   ├── .env.example                 # VITE_API_BASE_URL, VITE_WS_BASE_URL
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       ├── index.css
│       ├── api/
│       │   ├── client.js
│       │   ├── auth.js
│       │   ├── courses.js
│       │   ├── circuits.js
│       │   ├── simulation.js        # submit job, poll/subscribe status
│       │   ├── aiTutor.js           # WebSocket chat client
│       │   ├── assessments.js
│       │   └── progress.js
│       ├── context/
│       │   └── AuthContext.jsx
│       ├── components/
│       │   ├── layout/
│       │   │   ├── Navbar.jsx
│       │   │   └── ProtectedRoute.jsx
│       │   ├── circuit-builder/
│       │   │   ├── CircuitCanvas.jsx       # the drag-and-drop grid/timeline
│       │   │   ├── GatePalette.jsx
│       │   │   ├── GateBlock.jsx
│       │   │   └── circuitToQasm.js        # internal JSON <-> OpenQASM conversion (client-side preview)
│       │   ├── code-editor/
│       │   │   └── QuantumCodeEditor.jsx   # Monaco wrapper, Python mode
│       │   ├── visualizations/
│       │   │   ├── BlochSphere.jsx
│       │   │   ├── ProbabilityHistogram.jsx
│       │   │   ├── StatevectorView.jsx
│       │   │   └── CircuitDiagram.jsx
│       │   ├── ai-tutor/
│       │   │   ├── TutorChatPanel.jsx
│       │   │   ├── ExplanationCard.jsx
│       │   │   └── DebugSuggestionCard.jsx
│       │   ├── assessments/
│       │   │   ├── QuizRunner.jsx
│       │   │   └── CodingChallengeRunner.jsx
│       │   └── ui/                         # buttons, cards, modals (Tailwind-styled)
│       ├── pages/
│       │   ├── LoginPage.jsx
│       │   ├── RegisterPage.jsx
│       │   ├── learn/
│       │   │   ├── CourseListPage.jsx
│       │   │   └── LessonPage.jsx
│       │   ├── build/
│       │   │   └── CircuitBuilderPage.jsx   # drag-and-drop + code tabs, shared circuit state
│       │   ├── results/
│       │   │   └── SimulationResultsPage.jsx
│       │   ├── assess/
│       │   │   └── AssessmentPage.jsx
│       │   ├── progress/
│       │   │   └── ProgressPage.jsx
│       │   └── instructor/
│       │       ├── CohortDashboardPage.jsx
│       │       └── ContentManagerPage.jsx
│       └── utils/
│           └── format.js
│
├── backend/                         # FastAPI JSON API + WebSocket, Python
│   ├── requirements.txt
│   ├── run.py                       # uvicorn entry point
│   ├── config.py                    # env-driven settings (Pydantic Settings)
│   ├── .env.example
│   │
│   ├── app/
│   │   ├── __init__.py              # create_app(): CORS, routers, lifespan events
│   │   ├── db.py                    # SQLAlchemy engine/session
│   │   │
│   │   ├── models/                  # SQLAlchemy ORM models (mirrors Section 5)
│   │   │   ├── user.py
│   │   │   ├── course.py            # Course, Module, Lesson
│   │   │   ├── circuit.py
│   │   │   ├── simulation_job.py
│   │   │   ├── assessment.py        # Assessment, Question, Submission
│   │   │   ├── progress.py
│   │   │   ├── ai_tutor_session.py
│   │   │   └── instructor_cohort.py
│   │   │
│   │   ├── schemas/                 # Pydantic request/response models
│   │   │   └── ... (one per domain, mirrors models/)
│   │   │
│   │   ├── auth/
│   │   │   └── routes.py            # /api/auth/register, /login, /refresh
│   │   │
│   │   ├── courses/
│   │   │   └── routes.py            # /api/courses, /api/modules, /api/lessons
│   │   │
│   │   ├── circuits/
│   │   │   ├── routes.py            # save/load circuit designs, QASM import/export
│   │   │   └── qasm_converter.py    # internal circuit JSON <-> OpenQASM
│   │   │
│   │   ├── simulation/
│   │   │   ├── routes.py            # POST /api/simulate (enqueues job), GET /api/simulate/{job_id}
│   │   │   ├── backends/            # unified adapter interface — Section 6.2
│   │   │   │   ├── base_adapter.py
│   │   │   │   ├── qiskit_adapter.py
│   │   │   │   ├── pennylane_adapter.py
│   │   │   │   ├── cirq_adapter.py
│   │   │   │   └── qbraid_adapter.py
│   │   │   └── tasks.py             # Celery task: run_simulation_job
│   │   │
│   │   ├── sandbox/
│   │   │   ├── runner.py            # spins up the Docker sandbox, enforces limits
│   │   │   └── Dockerfile.sandbox    # the isolated execution image (also kept at repo root copy, see deployment/)
│   │   │
│   │   ├── ai_tutor/
│   │   │   ├── routes_ws.py         # WebSocket endpoint: /ws/tutor
│   │   │   ├── provider.py          # LLM provider abstraction — Section 7.2
│   │   │   ├── prompts.py           # system prompts per mode (explain/generate/debug/recommend)
│   │   │   └── context_builder.py   # assembles learner + lesson + circuit context for the LLM
│   │   │
│   │   ├── assessments/
│   │   │   ├── routes.py
│   │   │   ├── grading.py           # auto-grading: MCQ scoring + coding-challenge sandboxed test runs
│   │   │   └── tasks.py             # Celery task: grade_submission
│   │   │
│   │   ├── progress/
│   │   │   ├── routes.py
│   │   │   └── adaptive.py          # recommendation logic — Section 5.11 / Milestone 8
│   │   │
│   │   ├── instructor/
│   │   │   └── routes.py            # cohort analytics, content management
│   │   │
│   │   └── utils/
│   │       ├── decorators.py        # role_required("instructor"), etc.
│   │       └── logger.py
│   │
│   └── workers/
│       └── celery_app.py            # Celery app config, task autodiscovery
│
├── deployment/
│   ├── nginx/
│   │   └── quantalab.conf
│   ├── systemd/
│   │   ├── quantalab-api.service    # uvicorn
│   │   └── quantalab-worker.service # celery worker
│   ├── docker/
│   │   └── Dockerfile.sandbox       # canonical sandbox image definition
│   └── cloudflare/
│       └── dns_ssl_notes.md
│
├── scripts/
│   ├── seed_db.py                   # demo courses, users, sample circuits
│   └── run_simulation_cli.py        # manually trigger a simulation job for testing
│
└── tests/
    ├── backend/
    │   ├── test_auth.py
    │   ├── test_circuits.py
    │   ├── test_simulation_adapters.py
    │   ├── test_sandbox_isolation.py   # explicitly tests that malicious code cannot escape
    │   ├── test_assessments.py
    │   └── test_ai_tutor_context.py
    └── frontend/
        └── (component tests, Vitest + React Testing Library, if time allows)
```

---

## 4. Frontend ↔ Backend Contract

- **Base URL:** `VITE_API_BASE_URL` (dev: proxied via Vite to `localhost:8000`; prod:
  `/api`, same-origin through Nginx — no CORS needed in production).
- **WebSocket:** `VITE_WS_BASE_URL` for `/ws/tutor` (AI tutor streaming) and
  `/ws/simulation/{job_id}` (live job-status push, with REST polling as a fallback).
- **Auth:** `Authorization: Bearer <JWT>` on every authenticated request; silent
  refresh on `401` before forcing a re-login.
- **Response shape:** `{ "data": ..., "error": null }` / `{ "data": null, "error": { "code", "message" } }`.
- **Route inventory (keep current as routes are added):**

  | Method | Path | Purpose |
  |---|---|---|
  | POST | `/api/auth/register` \| `/login` | Account creation / JWT issuance |
  | GET | `/api/courses` | List courses/modules/lessons |
  | GET | `/api/lessons/{id}` | Lesson content |
  | POST/GET | `/api/circuits` | Save / list a learner's circuit designs |
  | GET/POST | `/api/circuits/{id}/qasm` | Export/import OpenQASM |
  | POST | `/api/simulate` | Submit a circuit + backend choice → returns `job_id` |
  | GET | `/api/simulate/{job_id}` | Poll job status/result (fallback to WS) |
  | WS | `/ws/simulation/{job_id}` | Live status push |
  | WS | `/ws/tutor` | AI tutor chat — streamed tokens, mode-tagged (explain/generate/debug/recommend) |
  | GET/POST | `/api/assessments/{id}` \| `/submit` | Fetch assessment, submit answer/code |
  | GET | `/api/progress/me` | Learner's own progress + next-step recommendation |
  | GET | `/api/instructor/cohorts/{id}` | Cohort-level analytics |
  | GET | `/api/sandbox/status` | Health of the sandbox execution layer (see Section 6.5) |

---

## 5. Core Data Models / Database Schema (PostgreSQL)

### 5.1 `users`
```
id (PK), role (student|instructor|admin), name, email (unique), password_hash,
institution (nullable), created_at, updated_at
```

### 5.2 `courses` / `modules` / `lessons`
```
courses:  id (PK), title, description, order_index
modules:  id (PK), course_id (FK), title, order_index
lessons:  id (PK), module_id (FK), title, content_markdown, concept_tags (array:
          e.g. ["superposition","qubit"]), order_index, estimated_minutes
```

### 5.3 `circuits`
```
id (PK), owner_id (FK -> users), lesson_id (FK, nullable — circuits can be
free-standing or tied to a lesson exercise), title, gate_sequence_json (the
drag-and-drop/internal representation), source_mode (visual|code), source_code
(nullable, raw Python if authored via code editor), created_at, updated_at
```

### 5.4 `simulation_jobs`
```
id (PK), circuit_id (FK), requested_by (FK -> users), backend (qiskit_aer|
pennylane|cirq|qbraid), status (queued|running|completed|failed|timeout),
result_json (statevector / counts / Bloch coordinates, nullable until completed),
error_message (nullable), started_at, completed_at
```

### 5.5 `assessments` / `questions` / `submissions`
```
assessments: id (PK), lesson_id (FK, nullable), title, type (quiz|coding_challenge),
             passing_score
questions:   id (PK), assessment_id (FK), prompt, type (mcq|coding), options_json
             (for mcq), correct_answer (mcq) / expected_output_spec (coding),
             starter_code (coding, nullable)
submissions: id (PK), user_id (FK), question_id (FK), answer_text / submitted_code,
             is_correct (nullable until graded), score, graded_at, sandbox_job_id
             (FK -> simulation_jobs-style sandbox run, for coding questions)
```

### 5.6 `progress`
```
id (PK), user_id (FK), lesson_id (FK), status (not_started|in_progress|completed),
time_spent_seconds, last_accessed_at, mastery_score (derived — see Section 5.11)
```

### 5.7 `ai_tutor_sessions` / `ai_tutor_messages`
```
ai_tutor_sessions: id (PK), user_id (FK), lesson_id (FK, nullable), circuit_id (FK,
                   nullable), started_at
ai_tutor_messages: id (PK), session_id (FK), role (user|assistant), mode
                   (explain|generate|debug|recommend), content, created_at
```

### 5.8 `instructor_cohorts`
```
id (PK), instructor_id (FK -> users), name, course_id (FK)
cohort_members: cohort_id (FK), user_id (FK)   -- join table
```

### 5.9 Indexes
- `users.email` — unique
- `circuits.owner_id`, `.lesson_id`
- `simulation_jobs.status`, `.circuit_id`
- `submissions.user_id`, `.question_id`
- `progress.user_id` + `.lesson_id` — compound unique (one progress row per learner per lesson)
- `ai_tutor_messages.session_id`

### 5.10 Instructor analytics (derived, not stored — computed on read)
Cohort-level: average module completion %, average assessment score, most-common
concept tags where learners get stuck (joined from `progress.mastery_score` and
`submissions.is_correct`), time-to-completion distribution.

### 5.11 "Adaptive loop" definition (this is what makes G5 real, not a buzzword)
`progress.mastery_score` per lesson is computed from a simple, explainable formula for
MVP (not a black-box ML model — explainability matters for an education product):
a weighted combination of assessment score on that lesson's questions, number of
attempts needed, and AI-tutor debug-mode message count on that lesson's exercises
(more debug help requested → lower initial mastery signal). `progress/adaptive.py`
uses this to recommend: review a specific prerequisite lesson (if mastery is low),
proceed to the next lesson (if mastery is high), or offer an extension/challenge
exercise (if mastery is very high). This is intentionally simple and rule-based for
the hackathon build — the PS's own text only asks for "personalized learning paths,"
not a research-grade recommender system, and a transparent rule-based version is both
buildable in time and easier to defend to an evaluator than an opaque model would be.

---

## 6. Multi-Backend Simulation & Secure Code Execution Strategy

This is the most technically and security-critical section of the whole platform —
read it before writing any simulation or code-execution code.

### 6.1 The core design principle
**No learner-submitted code — whether typed directly or generated by the AI tutor —
ever executes outside an isolated, resource-limited sandbox.** This applies even to
code the AI tutor itself wrote, because an LLM's output is still untrusted input from
the execution environment's point of view.

### 6.2 Unified backend adapter interface
Each of the four required backends is wrapped behind one common Python interface so
the rest of the system (API routes, Celery tasks, frontend) never needs to know which
specific SDK is running underneath:

```
class SimulationAdapter(Protocol):
    def run(self, circuit: CircuitSpec, shots: int) -> SimulationResult: ...
```
`backends/qiskit_adapter.py`, `pennylane_adapter.py`, `cirq_adapter.py`, and
`qbraid_adapter.py` each implement this. `SimulationResult` is a normalized shape
(statevector, measurement counts, execution time, backend name) so the frontend's
visualization components don't need backend-specific branching logic.

### 6.3 Sandbox execution design
1. A simulation or coding-challenge submission is never run in the FastAPI request
   process. It is always enqueued as a Celery task.
2. The Celery worker spins up a **single-use Docker container** (via `docker-py`,
   `sandbox/runner.py`) built from `deployment/docker/Dockerfile.sandbox` — a minimal
   image containing only Python + the four quantum SDKs, with no network access, no
   mounted host filesystem beyond a read-only copy of the submitted code, a strict CPU
   and memory limit, and a hard wall-clock timeout (e.g. 15 seconds for simple
   circuits, configurable per request type).
3. The container's only output channel is stdout/stderr, captured and parsed into the
   normalized `SimulationResult` shape; the container is destroyed immediately after,
   win or lose.
4. If the container exceeds its time or memory limit, the job is marked `timeout` or
   `failed` with a clear, learner-facing message — never a silent hang.
5. `tests/backend/test_sandbox_isolation.py` explicitly tests this boundary: submit
   code that attempts filesystem access outside its working directory, attempts a
   network call, or tries to consume unbounded memory/CPU, and assert each is blocked
   or killed within the configured limit. **This test suite is not optional** — it is
   the direct evidence you'll want on hand when an evaluator asks about security.

### 6.4 Circuit size and complexity limits
A classical simulator's resource use grows exponentially with qubit count. Cap the
maximum qubits/gates a learner-submitted circuit can request in the MVP (e.g. 12–16
qubits for statevector simulation), and return a clear, educational error — not a
crash — if a learner exceeds it ("this circuit needs more qubits than our simulator
can run live — here's why that's a general limit of classical simulation of quantum
systems," which is itself a teachable moment, not just an error state).

### 6.5 What changes at production scale (have this answer ready)
At demo scale, a handful of Celery workers and single-container-per-job is fine. At
real scale (many concurrent classrooms), the honest answer is: horizontal scaling of
Celery workers, a container pool/warm-start strategy instead of a fresh container per
job (to cut cold-start latency), and possibly routing simple/common circuit patterns
through a cached-result layer rather than re-simulating identical circuits — none of
this needs to be built for the hackathon, but having the answer ready directly
addresses the evaluator's "how would this hold up at production scale" question.

---

## 7. AI Tutor Integration Strategy

### 7.1 The four required modes
The Expected Solution names these explicitly — build each as a distinct, testable mode
rather than one generic chatbot:
1. **Concept explanation** — "explain superposition in the context of my current
   lesson," grounded in the specific lesson content the learner is on.
2. **Code generation** — "write a Qiskit circuit that creates a Bell state," producing
   code that is then **run through the same sandbox as any other submitted code**
   before being shown as "working" (never trust the AI's own claim that its code runs).
3. **Debugging** — given a learner's broken circuit code and the sandbox's actual error
   output, explain what's wrong and suggest a fix — grounded in a real error trace, not
   a guess.
4. **Personalized recommendation** — "what should I study next," informed by the
   `progress.mastery_score` data from Section 5.11, not by the chat history alone.

### 7.2 Provider abstraction
`ai_tutor/provider.py` wraps whichever LLM API is configured (Anthropic, OpenAI, or
another provider) behind one interface, so the provider can be swapped via an
environment variable without touching route or prompt logic. This also directly
supports the "what happens when [a dependency] fails" resilience question — if the
configured AI provider times out or errors, the tutor endpoint returns a clear,
learner-facing "tutor temporarily unavailable, here's the static lesson content
instead" fallback rather than hanging the request.

### 7.3 Context construction (`context_builder.py`)
Every AI-tutor request is built with explicit, bounded context — never a raw
unrestricted chat history: current lesson's content/concept tags, the learner's
current circuit (gate sequence or code), and, for debug mode, the actual sandbox error
output. This keeps responses grounded and relevant, and keeps the prompt size
predictable and cost-bounded.

### 7.4 Streaming
The `/ws/tutor` WebSocket streams the LLM response token-by-token to the frontend's
`TutorChatPanel.jsx`, so a learner sees the explanation forming in real time rather
than waiting for a complete response — meaningfully better perceived responsiveness
for what can otherwise be a multi-second wait.

### 7.5 Honesty about AI limitations (for the evaluator's "why this tech / not overkill" question)
Be explicit in the demo and in any write-up: the AI tutor is a **generation-plus-verification**
system, not an oracle — generated code is always sandbox-verified before being
presented as correct (Section 6.3, point 2), and concept explanations are grounded in
curated lesson content rather than the model's unconstrained knowledge wherever
possible. This is the honest, defensible answer to "how do you know the AI isn't just
hallucinating quantum mechanics at a nervous 17-year-old."

---

## 8. Hosting & Deployment Deep-Dive

Same proven pattern as before, adapted for this stack's extra moving pieces (Celery,
Redis, the sandbox runner).

### 8.1 What runs on the host VM at all times
- **Nginx** (static frontend + `/api` and `/ws` reverse proxy)
- **uvicorn running the FastAPI app** (systemd-managed)
- **Celery worker process(es)** (systemd-managed)
- **Redis** (Celery broker + job status cache) — can run as a local service or managed
  instance
- **PostgreSQL** — managed instance recommended (e.g. a managed Postgres offering) over
  self-hosting, to avoid babysitting database ops during a hackathon
- **Docker daemon** — required on the host so the sandbox runner (Section 6.3) can spin
  up isolated containers

**Node.js is build-time only** — exactly as in the prior project's pattern. `npm run
build` produces `frontend/dist/`, which is the only artifact that needs to reach the VM.

### 8.2 Nginx config sketch (`deployment/nginx/quantalab.conf`)
```nginx
server {
    listen 80;
    server_name your-domain.example;

    root /var/www/quantalab/frontend/dist;
    index index.html;

    location / {
        try_files $uri /index.html;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /ws/ {
        proxy_pass http://127.0.0.1:8000/ws/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### 8.3 systemd services
Three services, each `Restart=always`: `quantalab-api.service` (uvicorn),
`quantalab-worker.service` (Celery), and relying on the OS-managed `docker.service`
for the Docker daemon the sandbox runner depends on.

### 8.4 Deploy steps (in order)
1. Clone/pull the repo on the VM.
2. **Backend:** Python venv, `pip install -r backend/requirements.txt`, `.env` from
   `.env.example` (DB URL, Redis URL, JWT secret, AI provider key), run Alembic
   migrations, enable + start the `quantalab-api` and `quantalab-worker` systemd services.
3. **Sandbox image:** `docker build -f deployment/docker/Dockerfile.sandbox -t
   quantalab-sandbox .` on the VM — this must exist before any simulation/grading job
   can run.
4. **Frontend:** `npm install && npm run build` (on the VM or in CI); deploy the
   resulting `dist/` to `/var/www/quantalab/frontend/dist`.
5. Install the Nginx config, `nginx -t`, `systemctl reload nginx`.
6. Cloudflare DNS + SSL, as in the prior project's pattern.
7. **Smoke test:** load the app in a fresh browser, run a simple circuit (e.g.
   Hadamard + measure) end-to-end through at least two backends, and send one AI-tutor
   message — confirming the full Celery → sandbox → result pipeline and the WebSocket
   streaming path both work against the deployed URL.

### 8.5 Local development workflow
- Terminal 1: `docker-compose up postgres redis` (or local installs of both).
- Terminal 2: `cd backend && uvicorn run:app --reload` (port 8000).
- Terminal 3: `cd backend && celery -A workers.celery_app worker --loglevel=info`.
- Terminal 4: `cd frontend && npm run dev` (port 5173, Vite proxy to 8000).
- Build the sandbox image once locally (`docker build ...`) before testing any
  simulation/grading flow.

---

## 9. Step-by-Step Implementation Roadmap

Strictly sequential. **[MVP]** = required for the demo. **[STRETCH]** = only after all
MVP milestones are demo-stable.

### Milestone 0 — Project Scaffolding **[MVP]**
1. Create the `frontend/` + `backend/` split per Section 3.
2. **Backend:** Python venv; `requirements.txt` with `fastapi`, `uvicorn`, `sqlalchemy`,
   `alembic`, `psycopg2-binary`, `pydantic-settings`, `python-jose`, `celery`, `redis`,
   `docker` (the `docker-py` client), `qiskit`, `qiskit-aer`, `pennylane`, `cirq`,
   `qbraid` (or the relevant qBraid SDK package), `pytest`. `create_app()` with CORS
   (dev only) and a `/api/health` route.
3. **Frontend:** `npm create vite@latest frontend -- --template react`; install
   Tailwind, `react-router-dom`, `@monaco-editor/react`, `plotly.js` + `react-plotly.js`,
   `@dnd-kit/core` (or `react-dnd`). Configure the Vite dev proxy for `/api` and `/ws`.
4. `docker-compose.yml` for local Postgres + Redis.
5. **Smoke test:** `uvicorn` serves `/api/health`; `npm run dev` renders a blank
   Tailwind page that successfully calls it through the proxy.

### Milestone 1 — Database & Core Models **[MVP]**
1. Define all SQLAlchemy models from Section 5; set up Alembic; run the initial migration.
2. `scripts/seed_db.py`: demo users (one student, one instructor), two courses with a
   few modules/lessons each.
3. **Smoke test:** seed script runs clean; tables match Section 5's schema.

### Milestone 2 — Auth **[MVP]**
1. `POST /api/auth/register`, `/login` issuing JWTs; `role_required` decorator.
2. Frontend: `LoginPage.jsx`, `RegisterPage.jsx`, `AuthContext.jsx`, `ProtectedRoute.jsx`.
3. **Smoke test:** register/login as both a student and an instructor from the real UI.

### Milestone 3 — Learning Modules (content delivery) **[MVP]**
1. `GET /api/courses`, `/api/lessons/{id}`.
2. Frontend: `CourseListPage.jsx`, `LessonPage.jsx` (renders `content_markdown`).
3. **Smoke test:** a logged-in student can browse courses and open a lesson.

### Milestone 4 — Circuit Builder (visual + code) **[MVP]**
1. Build `CircuitCanvas.jsx` + `GatePalette.jsx`: place/remove gates on a qubit/timeline
   grid, producing the internal `gate_sequence_json` representation.
2. Build `QuantumCodeEditor.jsx` (Monaco, Python mode) as the alternate authoring path.
3. Backend: `POST/GET /api/circuits` to save/load a learner's circuit designs.
4. **Smoke test:** build a simple circuit both ways (drag-and-drop and code); both save
   correctly and reload identically.

### Milestone 5 — Sandbox & Multi-Backend Simulation **[MVP]**
*(Build this before AI tutor — the tutor's "generate code" and "debug" modes both
depend on the sandbox already existing and working.)*
1. Build `deployment/docker/Dockerfile.sandbox` and `sandbox/runner.py` per Section 6.3.
2. Implement the four backend adapters (Section 6.2) against the unified interface.
3. `POST /api/simulate` → Celery task → sandboxed execution → normalized result.
4. `GET /api/simulate/{job_id}` polling + `/ws/simulation/{job_id}` push.
5. Run `tests/backend/test_sandbox_isolation.py` — confirm malicious/runaway code is
   actually blocked, not just assumed to be.
6. **Smoke test:** submit a Bell-state circuit (both from the visual builder and from
   code) and run it on at least two of the four backends; confirm results are
   consistent with each other (same statevector/measurement distribution, modulo
   simulator-specific numerical formatting).

### Milestone 6 — Visualization **[MVP]**
1. `BlochSphere.jsx`, `ProbabilityHistogram.jsx`, `StatevectorView.jsx`,
   `CircuitDiagram.jsx` — all driven by the normalized `SimulationResult` shape, so they
   work identically regardless of which backend produced the result.
2. `SimulationResultsPage.jsx` ties circuit + result + visualizations together.
3. **Smoke test:** run a circuit, confirm each visualization renders correctly and
   matches the expected physics (e.g. a Hadamard on |0⟩ shows a Bloch-sphere position on
   the equator, 50/50 measurement probabilities).

### Milestone 7 — AI Tutor **[MVP]**
1. `ai_tutor/provider.py` abstraction; `prompts.py` for the four modes (Section 7.1).
2. `context_builder.py` assembling lesson + circuit + (for debug mode) sandbox error context.
3. `/ws/tutor` WebSocket streaming endpoint.
4. Frontend: `TutorChatPanel.jsx` with mode selection, streamed rendering.
5. **Critical:** wire "generate code" mode's output through the Milestone 5 sandbox
   before presenting it as working code (Section 7.1, point 2).
6. **Smoke test:** exercise all four modes; confirm debug mode references a real
   sandbox error, not a hallucinated one; confirm provider-timeout fallback works
   (simulate by misconfiguring the API key briefly).

### Milestone 8 — Assessments & Adaptive Progress **[MVP]**
1. `assessments/routes.py` + `grading.py`: MCQ auto-scoring; coding-challenge grading
   via the same sandbox, checking submitted code's output against
   `expected_output_spec`.
2. `progress/routes.py` + `adaptive.py`: compute `mastery_score`, serve next-step
   recommendations (Section 5.11).
3. Frontend: `QuizRunner.jsx`, `CodingChallengeRunner.jsx`, `ProgressPage.jsx`.
4. **Smoke test:** complete a quiz and a coding challenge; confirm scores record
   correctly and the recommendation logic visibly changes based on performance (e.g.
   deliberately fail a lesson's assessment and confirm the system recommends review
   rather than advancement).

### Milestone 9 — Instructor Dashboard **[MVP]**
1. `instructor/routes.py`: cohort creation, cohort-level analytics (Section 5.10).
2. Frontend: `CohortDashboardPage.jsx`, `ContentManagerPage.jsx` (basic lesson/course
   authoring, even if minimal for MVP).
3. **Smoke test:** as an instructor, view a cohort's aggregate completion/score data
   for the seeded demo students.

### Milestone 10 — OpenQASM Import/Export **[STRETCH]**
1. `qasm_converter.py`: internal circuit JSON ↔ OpenQASM 2.0/3.0.
2. Frontend: export button in the circuit builder; import via file upload.
3. **Smoke test:** round-trip a circuit through export → import and confirm it's identical.

### Milestone 11 — Multilingual / Offline Lesson Caching **[STRETCH]**
Only attempt after every MVP milestone is demo-stable. Scope narrowly if time allows —
e.g. a service-worker cache of already-visited lesson content for offline review,
rather than a full offline mode.

### Milestone 12 — Deployment **[MVP]**
Follow Section 8 exactly. **Smoke test:** full journey (register → lesson → build
circuit → simulate on 2+ backends → visualize → ask the AI tutor → take an assessment
→ check progress) against the deployed URL, fresh browser.

### Milestone 13 — Testing, Logging, QA Pass **[MVP]**
1. `tests/backend/`: sandbox isolation (non-negotiable — Section 6.3), adapter
   correctness (known circuits produce known results on each backend), auth, grading
   logic, AI-tutor context construction.
2. Structured logging on every job state transition (simulation + grading).
3. Run every edge case in Section 10 manually against the deployed demo.

### Milestone 14 — Demo & Pitch Readiness **[MVP]**
1. Seed a clean demo dataset (realistic course content, a couple of demo student
   accounts with varied — not uniformly perfect — progress, so the adaptive
   recommendation and instructor dashboard have something real to show).
2. Script a demo path under 5 minutes hitting: a lesson, a circuit built both ways, a
   multi-backend simulation with visualization, an AI-tutor explanation **and** a debug
   session, an assessment, and the instructor dashboard.
3. Prepare direct, specific answers to the five evaluator questions in Section 1.5 —
   the sandbox isolation test results and the adapter-consistency test results are your
   evidence, not just assertions.
4. Fallback demo plan (recorded capture or local backup) in case of live network/VM issues.

---

## 10. Potential Edge Cases & Mitigations

| # | Edge Case | Mitigation |
|---|---|---|
| 1 | **Learner submits malicious/runaway code** (infinite loop, fork bomb, filesystem/network access attempt) | Docker sandbox with no network, read-only mounts, CPU/memory caps, hard wall-clock timeout (Section 6.3) — tested explicitly, not assumed. |
| 2 | **Circuit too large for the simulator** (too many qubits/gates) | Enforce a configured max qubit/gate count; return an educational, specific error rather than a crash or an indefinite hang (Section 6.4). |
| 3 | **Backend SDK unavailable/crashes** (e.g. a qBraid API outage, or a Qiskit Aer version mismatch after an update) | Adapter-level try/except with a clear per-backend error surfaced to the frontend; if one backend is down, the others remain usable — never let one backend's failure take down the whole simulate endpoint. |
| 4 | **Simulators disagree on results for the "same" circuit** (numerical precision, differing default conventions) | Normalize results at the adapter boundary (Section 6.2) to a common representation; where genuine differences remain (e.g. basis-state ordering conventions), document them plainly rather than presenting one as "correct." |
| 5 | **AI provider times out, errors, or rate-limits** | `provider.py` wraps calls with a timeout and a clear fallback message to the learner (Section 7.2) — tutor temporarily unavailable, not a frozen chat window. |
| 6 | **AI tutor generates code that doesn't actually run** | Always sandbox-verify AI-generated code before presenting it as a working answer (Section 7.1, point 2) — never trust the model's own claim. |
| 7 | **AI tutor gives a conceptually wrong explanation (hallucination)** | Ground explanations in curated lesson content via `context_builder.py` wherever the concept maps to existing lesson material; treat free-form explanation as a known residual risk and say so honestly if asked, rather than overclaiming reliability. |
| 8 | **Celery worker crashes mid-job** | Jobs have a `status` field with a timeout fallback (a job stuck in `running` past its expected duration is marked `failed` by a periodic sweep) so the frontend never polls forever. |
| 9 | **WebSocket connection drops mid-stream** (tutor response or job-status push) | Frontend falls back to REST polling for job status; for the tutor, show a "connection lost — reconnecting" state and resume/retry rather than silently losing the in-progress response. |
| 10 | **Concurrent simulation/grading load during a classroom session** | Celery worker count is horizontally scalable; Section 6.5 documents the production-scale answer explicitly for evaluator questions. |
| 11 | **Assessment auto-grading false negative** (correct code fails grading due to an overly strict output spec) | Define `expected_output_spec` with reasonable tolerance (e.g. floating-point comparison with epsilon for probability outputs, not exact string match); allow instructor manual override on a submission. |
| 12 | **Learner loses connectivity mid-lesson** | Lesson content itself is static markdown — cache the currently-open lesson client-side so a brief connectivity drop doesn't blank the page; simulation/AI features clearly show an offline/unavailable state rather than hanging (directly answers the evaluator's "does it degrade gracefully" question). |
| 13 | **Input validation / malicious input in non-sandboxed routes** (XSS, injection via lesson titles, circuit names, etc.) | Standard practice: React's default escaping (never `dangerouslySetInnerHTML` on user content), parameterized queries via SQLAlchemy, Pydantic validation on every request body, JWT + role checks on every mutating route. |
| 14 | **Instructor dashboard shown with sparse/zero real data** (demo realism) | Seed deliberately varied demo progress (Milestone 14.1) rather than uniform/empty data, so the adaptive and analytics features have something genuine to demonstrate. |
| 15 | **Evaluator asks about real vs. synthetic data** | Honest, specific, per-component answer ready (Section 1.5, point 1) — simulation results are genuinely real computation; lesson content is authored; demo progress data is seeded and labeled as such if asked directly. |
| 16 | **Sandbox image drifts from the SDK versions pinned in `backend/requirements.txt`** | Pin exact versions in both `requirements.txt` and `Dockerfile.sandbox`; rebuild and re-run `test_simulation_adapters.py` after any dependency bump, never assume compatibility. |
| 17 | **Multiple learners editing/sharing a circuit concurrently** (if collaborative editing is ever added) | Out of scope for MVP — single-owner circuits only; flag explicitly as a Phase 2 feature if asked, rather than attempting real-time collaborative editing under hackathon time pressure. |

---

## Appendix A — Environment Variables Reference

**`backend/.env`**
```
JWT_SECRET_KEY=
DATABASE_URL=postgresql://user:pass@localhost:5432/quantalab
REDIS_URL=redis://localhost:6379/0
AI_PROVIDER=anthropic            # or openai, etc. — see provider.py
AI_PROVIDER_API_KEY=
AI_PROVIDER_MODEL=
SANDBOX_IMAGE_NAME=quantalab-sandbox
SANDBOX_CPU_LIMIT=1
SANDBOX_MEMORY_LIMIT_MB=512
SANDBOX_TIMEOUT_SECONDS=15
MAX_CIRCUIT_QUBITS=16
CORS_ALLOWED_ORIGIN=http://localhost:5173
```

**`frontend/.env`**
```
VITE_API_BASE_URL=/api
VITE_WS_BASE_URL=/ws
```

## Appendix B — Source Material
Compiled from the official SIH 2026 problem-statement analysis provided (Smart
Education theme — AI-powered quantum computing learning platform, Expected Solution's
five explicit asks, Innovation/SWOT/Evaluation scorecard, and the evaluator-question
set). Re-verify the official PS wording on sih.gov.in before final submission, as with
any third-party-compiled PS analysis.
