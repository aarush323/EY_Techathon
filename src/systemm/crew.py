import os

from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from systemm.tools.vehicle_telematics_api import VehicleTelematicsAPI
from systemm.tools.maintenance_history_api import MaintenanceHistoryAPI
from systemm.tools.customer_notification_api import CustomerNotificationAPI
from systemm.tools.service_center_api import ServiceCenterAPI
from systemm.tools.iternio_route_optimizer import IternioRouteOptimizer

@CrewBase
class AutomotivePredictiveMaintenanceAiSystemCrew:
    """AutomotivePredictiveMaintenanceAiSystem crew"""

    llm_models = {
    "data_analysis_agent": "perplexity/sonar-pro",
    "diagnosis_agent": "perplexity/sonar-pro",
    "customer_engagement_agent": "perplexity/sonar-pro",
    "scheduling_agent": "perplexity/sonar-pro",
    "feedback_agent": "perplexity/sonar-pro",
    "manufacturing_quality_insights_agent": "perplexity/sonar-pro",
    "master_orchestrator_agent": "perplexity/sonar-pro",
}
    # Rest of your code remains unchanged


    @agent
    def data_analysis_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["data_analysis_agent"],
            tools=[VehicleTelematicsAPI(), MaintenanceHistoryAPI()],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(model=self.llm_models["data_analysis_agent"], temperature=0.7),
        )

    @agent
    def diagnosis_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["diagnosis_agent"],
            tools=[MaintenanceHistoryAPI()],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(model=self.llm_models["diagnosis_agent"], temperature=0.7),
        )

    @agent
    def customer_engagement_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["customer_engagement_agent"],
            tools=[CustomerNotificationAPI()],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(model=self.llm_models["customer_engagement_agent"], temperature=0.7),
        )

    @agent
    def scheduling_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["scheduling_agent"],
            tools=[ServiceCenterAPI(), IternioRouteOptimizer()],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(model=self.llm_models["scheduling_agent"], temperature=0.7),
        )

    @agent
    def feedback_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["feedback_agent"],
            tools=[CustomerNotificationAPI(), MaintenanceHistoryAPI()],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(model=self.llm_models["feedback_agent"], temperature=0.7),
        )

    @agent
    def manufacturing_quality_insights_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["manufacturing_quality_insights_agent"],
            tools=[MaintenanceHistoryAPI()],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(model=self.llm_models["manufacturing_quality_insights_agent"], temperature=0.7),
        )

    @agent
    def master_orchestrator_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["master_orchestrator_agent"],
            tools=[],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(model=self.llm_models["master_orchestrator_agent"], temperature=0.7),
        )

    @task
    def monitor_vehicle_fleet_data(self) -> Task:
        return Task(
            config=self.tasks_config["monitor_vehicle_fleet_data"],
            markdown=False,
        )

    @task
    def predict_component_failures(self) -> Task:
        return Task(
            config=self.tasks_config["predict_component_failures"],
            markdown=False,
        )

    @task
    def engage_customers_with_maintenance_alerts(self) -> Task:
        return Task(
            config=self.tasks_config["engage_customers_with_maintenance_alerts"],
            markdown=False,
        )

    @task
    def schedule_maintenance_appointments(self) -> Task:
        return Task(
            config=self.tasks_config["schedule_maintenance_appointments"],
            markdown=False,
        )

    @task
    def collect_service_feedback_and_update_records(self) -> Task:
        return Task(
            config=self.tasks_config["collect_service_feedback_and_update_records"],
            markdown=False,
        )

    @task
    def generate_manufacturing_quality_insights(self) -> Task:
        return Task(
            config=self.tasks_config["generate_manufacturing_quality_insights"],
            markdown=False,
        )

    @task
    def generate_comprehensive_business_intelligence_dashboard(self) -> Task:
        return Task(
            config=self.tasks_config["generate_comprehensive_business_intelligence_dashboard"],
            markdown=False,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the AutomotivePredictiveMaintenanceAiSystem crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

    def _load_response_format(self, name):
        with open(os.path.join(self.base_directory, "config", f"{name}.json")) as f:
            json_schema = json.loads(f.read())

        return SchemaConverter.build(json_schema)
