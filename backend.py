import os
import json
import sys
from typing import TypedDict, List
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END

load_dotenv()

# --- 1. Define Shared State ---
class AgentState(TypedDict):
    user_input: str
    destination: str
    duration: str
    interests: List[str]
    activities: str
    logistics: str
    final_itinerary: str

# --- 2. Agent Logic ---

def get_llm(api_key: str):
    return ChatOpenAI(api_key=api_key, base_url="https://api.x.ai/v1", model="grok-4.20-reasoning", temperature=0.7)

def coordinator_agent(state: AgentState, llm):
    prompt = f"""
    Senior Travel Coordinator. Extract from: {state['user_input']}
    Return ONLY JSON: "destination", "duration", "interests" (list).
    """
    response = llm.invoke([HumanMessage(content=prompt)])
    try:
        clean_content = response.content.replace("```json", "").replace("```", "").strip()
        data = json.loads(clean_content)
        return {
            "destination": data.get("destination", "Unknown"),
            "duration": data.get("duration", "3 days"),
            "interests": data.get("interests", ["general sightseeing"])
        }
    except:
        return {"destination": "Paris", "duration": "3 days", "interests": ["sightseeing"]}

def activity_agent(state: AgentState, llm):
    prompt = f"Expert Activity Planner. Trip to {state['destination']} ({state['duration']}). Interests: {', '.join(state['interests'])}. Plan it."
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"activities": response.content}

def logistics_agent(state: AgentState, llm):
    prompt = f"Logistics Expert. Stays and transport in {state['destination']} for {state['duration']}."
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"logistics": response.content}

def review_agent(state: AgentState, llm):
    prompt = f"Lead Travel Curator. Consolidate into Markdown Itinerary. Destination: {state['destination']} for {state['duration']}. activities: {state['activities']} logistics: {state['logistics']}"
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"final_itinerary": response.content}

# --- 3. Graph Builder ---

def build_workflow(llm):
    workflow = StateGraph(AgentState)
    
    # Passing llm via lambda to nodes
    workflow.add_node("coordinator", lambda state: coordinator_agent(state, llm))
    workflow.add_node("activity_specialist", lambda state: activity_agent(state, llm))
    workflow.add_node("logistics_expert", lambda state: logistics_agent(state, llm))
    workflow.add_node("reviewer", lambda state: review_agent(state, llm))

    workflow.add_edge(START, "coordinator")
    workflow.add_edge("coordinator", "activity_specialist")
    workflow.add_edge("activity_specialist", "logistics_expert")
    workflow.add_edge("logistics_expert", "reviewer")
    workflow.add_edge("reviewer", END)

    return workflow.compile()

# --- 4. FastAPI Setup ---

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PlanRequest(BaseModel):
    user_input: str

@app.get("/")
async def get_index():
    return FileResponse("index.html")

@app.post("/api/plan")
async def create_plan(req: PlanRequest):
    api_key = os.environ.get("XAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="XAI_API_KEY not configured on the server.")
    
    try:
        llm = get_llm(api_key)
        graph = build_workflow(llm)
        
        initial_state = {
            "user_input": req.user_input,
            "destination": "",
            "duration": "",
            "interests": [],
            "activities": "",
            "logistics": "",
            "final_itinerary": ""
        }
        
        # In a real app we might stream, but for now we run to completion
        final_state = graph.invoke(initial_state)
        return final_state
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
