import os
import json
import sys
import time
from typing import TypedDict, List
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END

# Load environment variables automatically from a .env file
load_dotenv()

# --- 1. Shared State Definition ---
# Requirement: Shared state/context passing between agents
class AgentState(TypedDict):
    user_input: str
    destination: str
    duration: str
    interests: List[str]
    activities: str
    logistics: str
    final_itinerary: str

# --- 2. LLM Initialization ---
llm = None
def get_llm():
    global llm
    if llm is None:
        api_key = os.environ.get("XAI_API_KEY")
        if not api_key:
            print("\n❌ [ERROR]: XAI_API_KEY not found in environment.")
            print("Please add it to a .env file or export it in your terminal.")
            sys.exit(1)
        llm = ChatOpenAI(api_key=api_key, base_url="https://api.x.ai/v1", model="grok-4.20-reasoning", temperature=0.7)
    return llm

def simulated_typing(agent_name: str, message: str):
    """Helper formatting function specifically to make demo videos look better!"""
    print(f"\n🤖 [{agent_name}] is typing...")
    time.sleep(0.5)
    print(f"   > {message}")

# --- 3. Agent Definitions (4 Agents) ---
# Requirement: At least 3–4 agents with clear roles

def coordinator_agent(state: AgentState):
    """Agent 1: Extracts structured requirements from natural language."""
    simulated_typing("Coordinator", f"Analyzing request: '{state['user_input']}'")
    
    prompt = f"""
    You are a Senior Travel Coordinator. Extract details from this request:
    Request: {state['user_input']}
    Return ONLY a valid JSON object with: "destination" (str), "duration" (str), and "interests" (list of str).
    """
    response = get_llm().invoke([HumanMessage(content=prompt)])
    try:
        clean_json = response.content.replace("```json", "").replace("```", "").strip()
        data = json.loads(clean_json)
        return {
            "destination": data.get("destination", "Unknown"),
            "duration": data.get("duration", "3 days"),
            "interests": data.get("interests", ["sightseeing"])
        }
    except Exception:
        return {"destination": "Paris", "duration": "3 days", "interests": ["general"]}

def activity_agent(state: AgentState):
    """Agent 2: Plans daily activities based on user interests."""
    dest = state.get("destination", "Unknown")
    simulated_typing("Activity Specialist", f"Researching attractions in {dest} based on interests: {state['interests']}...")
    
    prompt = f"""
    You are an Expert Activity Planner. Suggest a set of activities for a {state['duration']} trip to {state['destination']}.
    The traveler's interests: {', '.join(state['interests'])}.
    Keep it high-quality and concise.
    """
    response = get_llm().invoke([HumanMessage(content=prompt)])
    return {"activities": response.content}

def logistics_agent(state: AgentState):
    """Agent 3: Recommends accommodations and transport options."""
    simulated_typing("Logistics Expert", f"Finding the best stays and transport for a {state['duration']} trip...")
    
    prompt = f"""
    You are a Logistics Expert. Recommend:
    1. Neighborhoods to stay in {state['destination']}
    2. Best local transportation methods for a {state['duration']} trip.
    """
    response = get_llm().invoke([HumanMessage(content=prompt)])
    return {"logistics": response.content}

def review_agent(state: AgentState):
    """Agent 4: Curates all information into a beautiful final markdown plan."""
    simulated_typing("Lead Curator", "Combining all research into a final master itinerary...")
    
    prompt = f"""
    You are the Lead Travel Curator. Combine these details into a beautiful Markdown itinerary.
    Destination: {state['destination']} for {state['duration']}
    Activities: {state['activities']}
    Logistics: {state['logistics']}
    Format it elegantly.
    """
    response = get_llm().invoke([HumanMessage(content=prompt)])
    return {"final_itinerary": response.content}

# --- 4. LangGraph Setup ---
# Requirement: Use LangGraph to define nodes and edges
def build_workflow():
    workflow = StateGraph(AgentState)

    # Define Nodes (Agents)
    workflow.add_node("coordinator", coordinator_agent)
    workflow.add_node("activity_specialist", activity_agent)
    workflow.add_node("logistics_expert", logistics_agent)
    workflow.add_node("reviewer", review_agent)

    # Define Edges (Workflow sequence)
    workflow.add_edge(START, "coordinator")
    workflow.add_edge("coordinator", "activity_specialist")
    workflow.add_edge("activity_specialist", "logistics_expert")
    workflow.add_edge("logistics_expert", "reviewer")
    workflow.add_edge("reviewer", END)

    return workflow.compile()

# --- 5. Main Execution Loop ---
# Requirement: A main() function, Accept user input dynamically
def main():
    print("="*60)
    print("🌟 AI TRAVEL STUDIO: MULTI-AGENT ORCHESTRATION 🌟")
    print("="*60)
    
    # Accept dynamic user input
    user_request = input("\nWhere do you want to go and what do you want to do? \n(e.g., 'A 5-day food and art tour in Rome')\n> ")
    
    if not user_request.strip():
        user_request = "I want to visit Switzerland for 5 days. I love mountains and chocolate."
        print(f"Using default: {user_request}")

    # Set initial context
    initial_state = {
        "user_input": user_request,
        "destination": "",
        "duration": "",
        "interests": [],
        "activities": "",
        "logistics": "",
        "final_itinerary": ""
    }

    # Compile and execute the graph
    app = build_workflow()
    
    print("\n" + "-"*30)
    print("🚀 INITIATING AGENT WORKFLOW")
    print("-"*30)
    
    # Run the orchestration
    start_time = time.time()
    result = app.invoke(initial_state)
    elapsed = time.time() - start_time

    # Output the final result
    print("\n" + "="*60)
    print("✨ YOUR MASTER ITINERARY ✨")
    print("="*60 + "\n")
    print(result["final_itinerary"])
    
    print("\n" + "="*60)
    print(f"Mission Accomplished in {elapsed:.2f} seconds.")
    print("="*60)

if __name__ == "__main__":
    main()
