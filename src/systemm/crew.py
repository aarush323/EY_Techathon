import os
import sys
import json
from typing import Optional
from datetime import datetime
import re

# ---------------- CrewAI core ---------------- #
from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# ---------------- CrewAI tools ---------------- #
from crewai_tools import FileReadTool

# ---------------- Custom system tools ---------------- #
from systemm.tools.vehicle_telematics_api import VehicleTelematicsAPI
from systemm.tools.maintenance_history_api import MaintenanceHistoryAPI
from systemm.tools.customer_notification_api import CustomerNotificationAPI
from systemm.tools.service_center_api import ServiceCenterAPI
from systemm.tools.iternio_route_optimizer import IternioRouteOptimizer

# ---------------- LLM loader utility ---------------- #
from dotenv import load_dotenv

load_dotenv()

def get_safe_llm(model_name="cerebras/llama3.1-70b", temperature=0.7, max_tokens=8000):
    """Try to load LLM with Cerebras API key; fallback to Ollama if key missing."""
    cerebras_api_key = os.getenv("CEREBRAS_API_KEY")
    
    if cerebras_api_key:
        try:
            print(f"🔹 Attempting to load {model_name} using Cerebras API...")
            return LLM(
                model=model_name,
                api_key=cerebras_api_key,
                base_url="https://api.cerebras.ai/v1",
                temperature=temperature,
                max_tokens=max_tokens
            )
        except Exception as e:
            print(f"⚠️ Cerebras load failed: {e}\nSwitching to Ollama fallback...")
    
    # Fallback to Ollama
    try:
        print(f"🔹 Attempting to load {model_name} on GPU (Ollama)...")
        os.environ.pop("OLLAMA_NO_GPU", None)
        return LLM(model=model_name, temperature=temperature, max_tokens=max_tokens)
    except Exception as e:
        print(f"⚠️ GPU load failed: {e}\nSwitching to CPU mode...")
        os.environ["OLLAMA_NO_GPU"] = "true"
        return LLM(model=model_name, temperature=temperature, max_tokens=max_tokens)


@CrewBase
class AutomotivePredictiveMaintenanceAiSystemCrew:
    """Automotive Predictive Maintenance AI System Crew"""

    def __init__(self):
        super().__init__()
        self.llm_cache = {}

    def get_llm_cached(self, model_name="ollama/llama3.2:1b"):
        """Cache LLM instances to avoid multiple reloads"""
        if model_name not in self.llm_cache:
            self.llm_cache[model_name] = get_safe_llm(model_name=model_name)
        return self.llm_cache[model_name]

    # ---------------- Agents ---------------- #

    @agent
    def master_orchestrator_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["master_orchestrator_agent"],
            tools=[],
            reasoning=False,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            llm=self.get_llm_cached(),
            output_format="json",
        )

    @agent
    def data_analysis_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["data_analysis_agent"],
            tools=[FileReadTool(), VehicleTelematicsAPI(), MaintenanceHistoryAPI()],
            reasoning=False,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            llm=self.get_llm_cached(),
            output_format="json",
        )

    @agent
    def diagnosis_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["diagnosis_agent"],
            tools=[],
            reasoning=False,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            llm=self.get_llm_cached(),
            output_format="json",
        )

    @agent
    def customer_engagement_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["customer_engagement_agent"],
            tools=[CustomerNotificationAPI()],
            reasoning=False,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            llm=self.get_llm_cached(),
            output_format="json",
        )

    @agent
    def scheduling_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["scheduling_agent"],
            tools=[ServiceCenterAPI(), IternioRouteOptimizer()],
            reasoning=False,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            llm=self.get_llm_cached(),
            output_format="json",
        )

    @agent
    def feedback_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["feedback_agent"],
            tools=[],
            reasoning=False,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            llm=self.get_llm_cached(),
            output_format="json",
        )

    @agent
    def manufacturing_quality_insights_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["manufacturing_quality_insights_agent"],
            tools=[FileReadTool()],
            reasoning=False,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            llm=self.get_llm_cached(),
            output_format="json",
        )

    @agent
    def ueba_security_monitoring_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["ueba_security_monitoring_agent"],
            tools=[],
            reasoning=False,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            llm=self.get_llm_cached(),
            output_format="json",
        )

    # ---------------- Tasks ---------------- #

    @task
    def vehicle_data_monitoring_and_analysis(self) -> Task:
        return Task(config=self.tasks_config["vehicle_data_monitoring_and_analysis"], markdown=False, output_format="json")

    @task
    def predictive_failure_diagnosis(self) -> Task:
        return Task(config=self.tasks_config["predictive_failure_diagnosis"], markdown=False, output_format="json")

    @task
    def proactive_customer_outreach(self) -> Task:
        return Task(config=self.tasks_config["proactive_customer_outreach"], markdown=False, output_format="json")

    @task
    def service_appointment_coordination(self) -> Task:
        return Task(config=self.tasks_config["service_appointment_coordination"], markdown=False, output_format="json")

    @task
    def post_service_feedback_collection(self) -> Task:
        return Task(config=self.tasks_config["post_service_feedback_collection"], markdown=False, output_format="json")

    @task
    def manufacturing_quality_analysis_and_capa_generation(self) -> Task:
        return Task(config=self.tasks_config["manufacturing_quality_analysis_and_capa_generation"], markdown=False, output_format="json")

    @task
    def security_monitoring_and_compliance(self) -> Task:
        return Task(config=self.tasks_config["security_monitoring_and_compliance"], markdown=False, output_format="json")

    @task
    def master_workflow_orchestration(self) -> Task:
        return Task(config=self.tasks_config["master_workflow_orchestration"], markdown=False, output_format="json")

    # ---------------- Crew ---------------- #

    @crew
    def crew(self) -> Crew:
        """Creates the full crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )