<h1>DevAgent - AI Code Auditor</h1>
<p>An AI-powered multi-agent system built with LangGraph that analyzes source code for security vulnerabilities, generates potential fixes, requests user approval before applying code changes, and runs tests to validate the fixes.</p>
<h3>Overview</h3>
<p>The system uses multiple AI agents to automate the code security review process while keeping the developer in control of code modifications.
The workflow identifies potential security issues, proposes fixes, waits for user approval, and executes tests to verify the changes.</p>
<h3>Features</h3>
<ul>
<li>Security Analysis: Scans source code to identify potential security vulnerabilities. </li>
<li>Multi-Agent Architecture: Uses LangGraph to orchestrate specialized AI agents. </li>
<li>Automated Fix Generation: Generates code fixes for identified vulnerabilities. </li>
<li>Human-in-the-Loop Approval: Requests user approval before generating or applying approved code changes. </li>
<li>Automated Testing: Runs tests to help validate proposed fixes. </li>
<li>Stateful Workflow: Manages agent execution and workflow transitions using LangGraph. </li>
</ul>
<h3>Architecture</h3>
<p>The application uses a multi-layer architecture to connect the user interface, backend services, and AI agent workflow.</p>

```bash

                ┌──────────────────────┐
                │     React.js UI      │
                │  User Interaction    │
                └──────────┬───────────┘
                           │
                ┌──────────▼───────────┐
                │ Node.js + Express.js │
                │    Backend API       │
                └──────────┬───────────┘
                           │ HTTP API
                ┌──────────▼───────────┐
                │      FastAPI         │
                │    Python Service    │
                └──────────┬───────────┘
                           │
                ┌──────────▼───────────┐
                │      LangGraph       │
                │ Multi-Agent Workflow │
                └──────────┬───────────┘
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
   │Code Security│  │ Fix         │  │ Test        │
   │Analysis     │  │ Generation  │  │ Execution   │
   │Agent        │  │ Agent       │  │             │
   └─────────────┘  └─────────────┘  └─────────────┘
```
<h3>Workflow</h3>
<ul>
  <li>Code Input: The user provides source code for analysis.</li>
  <li>Security Analysis: The security analysis agent examines the code for potential vulnerabilities. </li>
  <li>Fix Generation: The system prepares suggested fixes for the identified issues. </li>
  <li>User Approval: The workflow pauses and asks the user to approve the proposed changes. </li>
  <li>Code Modification: After approval, the system generates or applies the approved fixes. </li>
  <li>Testing: The testing stage runs relevant tests to evaluate the changes. </li>
  <li>Results: The user receives the analysis findings and test results. </li>
</ul>
<h3>Tech Stack</h3>
<ul>
  <li>Python — AI agent implementation and backend service logic  </li>
  <li>LangGraph — Multi-agent orchestration and stateful workflows  </li>
  <li>FastAPI — REST API for exposing the AI agent  </li>
  <li>Node.js — JavaScript runtime for the application backend </li>
  <li>Express.js — Backend routing and API integration  </li>
  <li>React.js — Interactive user interface  </li>
  <li>Large Language Models (LLMs) — Code analysis and fix generation  </li>
</ul>
<h3>Project Structure</h3>

```bash
project-root/
├── devagent/
│   └── src/
│       ├── App.jsx
│       ├── App.css
│       ├── index.jsx
│       └── index.css
├── backend/
│   └── schema/
│   │   └──code.js
│   └── app.js
├── fastapi/
│   ├── graph/
│   ├── main.py
│   └── requirements.txt
├── .gitignore
└── README.md
```
