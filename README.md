# Study Planner Agent

Study Planner Agent is an AI agent that creates personalized study plans for any subject, not only DSA or DBMS. Its two main tools are `analyze_subjects(subjects)`, which analyzes the student's subjects and recommends study phases, and `build_schedule(subjects, days, daily_hours, session_minutes, priority_subject)`, which converts those decisions into a concrete multi-day schedule. The agent also has supporting tools to save plans, retrieve saved plans, and remember student preferences.

The agent's memory is stored persistently in `study_memory.json`. It remembers recent conversation turns, saved study plans, and useful preferences such as available study time and preferred session length. This allows the agent to use information from earlier turns and retrieve a previously saved plan instead of starting from zero each time.

One honest failure during development was an OpenRouter free-tier rate-limit error, so the project was moved to Gemini. I then hit a Gemini SDK compatibility error because `Part.from_function_response()` did not accept an `id` argument in the installed SDK version; I removed that unsupported argument and retested the tool loop successfully. Group note: Solo submission, so I completed the agent, tools, memory, UI, and demo.
