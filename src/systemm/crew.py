import os
from dotenv import load_dotenv
import json

from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from systemm.tools.vehicle_telematics_api import VehicleTelematicsAPI
from systemm.tools.maintenance_history_api import MaintenanceHistoryAPI
from systemm.tools.customer_notification_api import CustomerNotificationAPI
from systemm.tools.service_center_api import ServiceCenterAPI
from systemm.tools.iternio_route_optimizer import IternioRouteOptimizer

# Load environment variables from .env file
load_dotenv()


@CrewBase
class AutomotivePredictiveMaintenanceAiSystemCrew:
    """AutomotivePredictiveMaintenanceAiSystem crew"""

    # LLM provider selection
    llm_provider = os.getenv("LLM_PROVIDER", "perplexity").lower()

    # Model routing
    llm_models = {
        # Perplexity = ONLY for high-level reasoning
        "master_orchestrator_agent": "perplexity/sonar-pro",
        "data_analysis_agent": "perplexity/sonar-pro",

        # Cerebras = fast + free
        "diagnosis_agent": "perplexity/sonar-pro",
        "manufacturing_quality_insights_agent": "perplexity/sonar-pro",
        "scheduling_agent": "perplexity/sonar-pro",

        # Ollama = local + free
        "customer_engagement_agent": "perplexity/sonar-pro",
        "feedback_agent": "perplexity/sonar-pro",
    }

    # Proper LLM builder (CrewAI ignores token caps inside LLM, so kept minimal)
    def llm_config(self, model_key):
        return LLM(
            model=self.llm_models[model_key],
            temperature=0.5,
        )

    # -------------------- AGENTS ----------------------

    @agent
    def data_analysis_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["data_analysis_agent"],
            tools=[VehicleTelematicsAPI(), MaintenanceHistoryAPI()],
            reasoning=False,
            inject_date=True,
            allow_delegation=False,
            max_iter=3,
            max_input_tokens=1200,
            max_output_tokens=300,
            max_total_tokens=1500,
            constraints=["Return short anomaly summary only. No raw tables or telemetry logs."],
            llm=self.llm_config("data_analysis_agent"),
        )

    @agent
    def diagnosis_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["diagnosis_agent"],
            tools=[MaintenanceHistoryAPI()],
            reasoning=False,
            inject_date=True,
            allow_delegation=False,
            max_iter=3,
            max_input_tokens=1000,
            max_output_tokens=250,
            max_total_tokens=1300,
            context_filters=[
            {
                "filter_type": "include_keys",
                "keys": [
              "vehicles.vehicle_id",
                "vehicles.priority_rank",
                "vehicles.health_score",
                "vehicles.predicted_failures",
                 "vehicles.diagnostic_trouble_codes",
                "vehicles.sensor_readings.engine_metrics.anomalies",
                "vehicles.sensor_readings.brake_condition.anomalies",
                "vehicles.sensor_readings.battery_status.anomalies",
                "vehicles.sensor_readings.transmission_health.anomalies"
        ]
    }
],
            constraints=["Return compact failure predictions only. No tables."],
            llm=self.llm_config("diagnosis_agent"),
        )

    @agent
    def customer_engagement_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["customer_engagement_agent"],
            tools=[CustomerNotificationAPI()],
            reasoning=False,
            inject_date=True,
            allow_delegation=False,
            max_iter=2,
            max_input_tokens=700,
            max_output_tokens=200,
            max_total_tokens=900,
            constraints=["Write short, friendly customer messages only."],
            llm=self.llm_config("customer_engagement_agent"),
        )

    @agent
    def scheduling_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["scheduling_agent"],
            tools=[ServiceCenterAPI(), IternioRouteOptimizer()],
            reasoning=False,
            inject_date=True,
            allow_delegation=False,
            max_iter=3,
            max_input_tokens=900,
            max_output_tokens=250,
            max_total_tokens=1200,
            constraints=["Return only appointment summary. Do not print center lists or route details."],
            llm=self.llm_config("scheduling_agent"),
        )

    @agent
    def feedback_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["feedback_agent"],
            tools=[CustomerNotificationAPI(), MaintenanceHistoryAPI()],
            reasoning=False,
            inject_date=True,
            allow_delegation=False,
            max_iter=2,
            max_input_tokens=700,
            max_output_tokens=200,
            max_total_tokens=900,
            constraints=["Summarize customer feedback briefly."],
            llm=self.llm_config("feedback_agent"),
        )

    @agent
    def manufacturing_quality_insights_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["manufacturing_quality_insights_agent"],
            tools=[MaintenanceHistoryAPI()],
            reasoning=False,
            inject_date=True,
            allow_delegation=False,
            max_iter=3,
            max_input_tokens=900,
            max_output_tokens=300,
            max_total_tokens=1200,
            constraints=["Return short RCA/CAPA insights only."],
            llm=self.llm_config("manufacturing_quality_insights_agent"),
        )

    @agent
    def master_orchestrator_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["master_orchestrator_agent"],
            tools=[],
            reasoning=False,
            inject_date=True,
            allow_delegation=False,
            max_iter=3,
            max_input_tokens=1200,
            max_output_tokens=400,
            max_total_tokens=1600,
            constraints=["Return compact dashboard summary. No raw data or tables."],
            llm=self.llm_config("master_orchestrator_agent"),
        )

    # -------------------- TASKS ----------------------

    @task
    def monitor_vehicle_fleet_data(self) -> Task:
        return Task(config=self.tasks_config["monitor_vehicle_fleet_data"], markdown=False)

    @task
    def predict_component_failures(self) -> Task:
        return Task(
            config=self.tasks_config["predict_component_failures"],
            markdown=False,
            context_filters=[
                {
                    "filter_type": "include_keys",
                    "keys": [
                        "vehicles.vehicle_id",
                        "vehicles.priority_rank",
                        "vehicles.health_score",
                        "vehicles.predicted_failures",
                        "vehicles.sensor_readings.engine_metrics.anomalies",
                        "vehicles.sensor_readings.brake_condition.anomalies",
                        "vehicles.sensor_readings.battery_status.anomalies",
                        "vehicles.sensor_readings.transmission_health.anomalies",
                        "vehicles.diagnostic_trouble_codes",
                    ]
                }
            ]
              
              )

    @task
    def engage_customers_with_maintenance_alerts(self) -> Task:
        return Task(config=self.tasks_config["engage_customers_with_maintenance_alerts"], markdown=False)

    @task
    def schedule_maintenance_appointments(self) -> Task:
        return Task(config=self.tasks_config["schedule_maintenance_appointments"], markdown=False)

    @task
    def collect_service_feedback_and_update_records(self) -> Task:
        return Task(config=self.tasks_config["collect_service_feedback_and_update_records"], markdown=False)

    @task
    def generate_manufacturing_quality_insights(self) -> Task:
        return Task(config=self.tasks_config["generate_manufacturing_quality_insights"], markdown=False)

    @task
    def generate_comprehensive_business_intelligence_dashboard(self) -> Task:
        return Task(config=self.tasks_config["generate_comprehensive_business_intelligence_dashboard"], markdown=False)

    # -------------------- CREW ----------------------

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

    # -------------------- JSON FORMAT LOADER ----------------------

    def _load_response_format(self, name):
        with open(os.path.join(self.base_directory, "config", f"{name}.json")) as f:
            json_schema = json.loads(f.read())
        return SchemaConverter.build(json_schema)
