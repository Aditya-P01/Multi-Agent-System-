# 🎥 Demo Presentation Script: Kyoto Trip

Use this script to guide your 5-8 minute demo video!

## 1. Introduction (0:00 - 1:00)
**Action**: Have `multi_agent_system.py` open on screen.
>**Script**: "Hello! For my assignment, I built a Multi-Agent AI System called 'AI Travel Studio' using LangChain and LangGraph. The objective of this project is to take a complex natural language request and orchestrate it through a team of 4 specialized AI agents working together to build a master travel itinerary."

## 2. Code Requirements Walkthrough (1:00 - 3:30)
**Action**: Scroll through the code and point to the following sections:
> **Script**: "To satisfy the code constraints, my system is contained completely within this single `multi_agent_system.py` file.
> 
> *   **Shared State**: At the top (line 10), I defined `AgentState` using a `TypedDict`. This is the shared context that gets passed between all agents.
> *   **4 Agent Roles**: I have 4 clear agents:
>     1.  The **Coordinator** (line 35) structure's the natural language into JSON.
>     2.  The **Activity Specialist** (line 64) curates the day-to-day plan.
>     3.  The **Logistics Expert** (line 76) handles transportation and stays.
>     4.  The **Lead Curator** (line 90) compiles everything.
> *   **LangGraph Orchestration**: Down here in `build_workflow` (line 112), you can see I define the nodes and edges, creating a linear directed graph from Start to Finish.
> *   **Dynamic Input**: Finally, in the `main()` function, I use Python's `input()` to prompt the user dynamically at runtime."

## 3. The Live Demo (3:30 - 6:00)
**Action**: Open your terminal window and run `python3 multi_agent_system.py`.

At the prompt, *copy and paste the following exactly*:
**`"I'm taking my family to Kyoto for 6 days. We really want to focus on traditional Japanese tea ceremonies, ancient temples, and finding the best street food."`**

**Action**: As the terminal logs text, narrate the agent process:
> **Script**: "Let's run it. I'm providing a complex prompt about a 6 day family trip to Kyoto focusing on tea, temples, and street food.
> Notice how the **Coordinator** isolates the core criteria. 
> Now, the **Activity Specialist** has taken over, utilizing LangChain to talk to the Groq Llama-3 model to specifically map out the tea ceremonies and temples.
> Next, the **Logistics Expert** maps out neighborhoods and the transit system.
> And finally, the **Lead Reviewer** is combining the context state into a markdown output."

**Action**: Scroll up slightly to show the final generated Markdown Itinerary.
> **Script**: "As you can see, the final itinerary perfectly incorporates all 6 days, maps out the street food like Nishiki Market, and explains the Japan transit system. This proves the agents successfully communicated their individual outputs through the shared state."

## 4. Key Learnings & Conclusion (6:00 - End)
> **Script**: "My biggest takeaway from this assignment is the power of **Prompt Specialization**. By breaking a massive task into 4 specialized prompts via LangGraph, rather than a single massive AI request, the results are much more accurate, structured, and easier to debug. Thank you!"
