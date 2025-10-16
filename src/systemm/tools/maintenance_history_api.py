from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Dict, Any, List, Optional
import json
import math
from datetime import datetime, timedelta
import random

class MaintenanceHistoryAPIInput(BaseModel):
    """Input schema for MaintenanceHistoryAPI Tool."""
    vehicle_id: str = Field(..., description="Vehicle ID (e.g., VEH001-VEH010)")
    action_type: str = Field(..., description="Action type: get_history, predict_failures, get_rca_data, add_service_record, get_pattern_analysis")
    filters: Optional[Dict[str, Any]] = Field(default=None, description="Optional filters for data retrieval")

class MaintenanceHistoryAPI(BaseTool):
    """Tool for simulating comprehensive vehicle maintenance history and failure prediction system."""

    name: str = "MaintenanceHistoryAPI"
    description: str = (
        "Simulates a comprehensive vehicle maintenance history and failure prediction system. "
        "Provides ML-like failure predictions, RCA/CAPA analysis, maintenance history tracking, "
        "and predictive maintenance recommendations for vehicles VEH001-VEH010."
    )
    args_schema: Type[BaseModel] = MaintenanceHistoryAPIInput

    def _generate_vehicle_data(self, vehicle_id: str) -> Dict[str, Any]:
        """Generate comprehensive vehicle data based on vehicle_id."""
        # Vehicle fleet data (VEH001-VEH010)
        vehicles = {
            f"VEH{str(i).zfill(3)}": {
                "year": 2020 + (i % 4),
                "make": ["Toyota", "Honda", "Ford", "Chevrolet"][i % 4],
                "model": ["Camry", "Accord", "F-150", "Silverado"][i % 4],
                "mileage": 15000 + (i * 5000) + random.randint(-2000, 8000),
                "usage_pattern": ["city", "highway", "mixed", "heavy_duty"][i % 4],
                "climate": ["temperate", "hot", "cold", "humid"][i % 4],
                "manufacturing_batch": f"BATCH_{2020 + (i % 2)}_{chr(65 + (i % 3))}"
            }
            for i in range(1, 11)
        }
        
        return vehicles.get(vehicle_id, vehicles["VEH001"])

    def _generate_service_history(self, vehicle_id: str, vehicle_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate realistic service history for a vehicle."""
        base_date = datetime.now() - timedelta(days=365 * (datetime.now().year - vehicle_data["year"]))
        history = []
        
        service_types = [
            {"type": "Oil Change", "cost_range": (40, 80), "interval_days": 90},
            {"type": "Brake Inspection", "cost_range": (100, 300), "interval_days": 180},
            {"type": "Tire Rotation", "cost_range": (50, 100), "interval_days": 120},
            {"type": "Air Filter Replacement", "cost_range": (30, 60), "interval_days": 365},
            {"type": "Transmission Service", "cost_range": (150, 400), "interval_days": 365},
            {"type": "Coolant Flush", "cost_range": (80, 150), "interval_days": 730}
        ]
        
        service_centers = ["QuickLube Pro", "AutoCare Plus", "MasterTech", "ServiceFirst"]
        
        current_date = base_date
        while current_date <= datetime.now():
            for service in service_types:
                if random.random() < 0.7:  # 70% chance of service being performed
                    history.append({
                        "date": current_date.strftime("%Y-%m-%d"),
                        "service_type": service["type"],
                        "cost": random.randint(*service["cost_range"]),
                        "service_center": random.choice(service_centers),
                        "mileage_at_service": vehicle_data["mileage"] - random.randint(0, 5000),
                        "technician": f"TECH_{random.randint(1001, 1099)}",
                        "notes": f"Routine {service['type'].lower()} completed successfully"
                    })
            current_date += timedelta(days=random.randint(60, 120))
        
        return sorted(history, key=lambda x: x["date"])

    def _predict_failures(self, vehicle_id: str, vehicle_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate ML-like failure predictions based on vehicle data."""
        components = [
            {"name": "Brake Pads", "base_failure_rate": 0.15, "mileage_factor": 0.000008},
            {"name": "Battery", "base_failure_rate": 0.12, "age_factor": 0.05},
            {"name": "Alternator", "base_failure_rate": 0.08, "mileage_factor": 0.000005},
            {"name": "Transmission", "base_failure_rate": 0.06, "usage_factor": 0.03},
            {"name": "Air Conditioning", "base_failure_rate": 0.10, "climate_factor": 0.04},
            {"name": "Water Pump", "base_failure_rate": 0.07, "age_factor": 0.02},
            {"name": "Starter Motor", "base_failure_rate": 0.05, "mileage_factor": 0.000003}
        ]
        
        predictions = []
        current_year = datetime.now().year
        vehicle_age = current_year - vehicle_data["year"]
        
        for component in components:
            # Calculate failure probability
            base_prob = component["base_failure_rate"]
            
            # Age factor
            age_multiplier = component.get("age_factor", 0) * vehicle_age
            
            # Mileage factor
            mileage_multiplier = component.get("mileage_factor", 0) * vehicle_data["mileage"]
            
            # Usage pattern factor
            usage_multipliers = {"city": 1.2, "highway": 0.9, "mixed": 1.0, "heavy_duty": 1.4}
            usage_multiplier = component.get("usage_factor", 0) * usage_multipliers.get(vehicle_data["usage_pattern"], 1.0)
            
            # Climate factor
            climate_multipliers = {"temperate": 1.0, "hot": 1.3, "cold": 1.1, "humid": 1.2}
            climate_multiplier = component.get("climate_factor", 0) * climate_multipliers.get(vehicle_data["climate"], 1.0)
            
            total_probability = min(base_prob + age_multiplier + mileage_multiplier + usage_multiplier + climate_multiplier, 0.95)
            
            # Time to failure estimation (days)
            time_to_failure = int(365 * (1 - total_probability) * random.uniform(0.5, 2.0))
            
            # Confidence level based on data quality
            confidence = min(0.85 + random.uniform(-0.15, 0.10), 0.95)
            
            predictions.append({
                "component": component["name"],
                "failure_probability": round(total_probability, 3),
                "confidence_level": round(confidence, 3),
                "estimated_days_to_failure": time_to_failure,
                "estimated_failure_date": (datetime.now() + timedelta(days=time_to_failure)).strftime("%Y-%m-%d"),
                "severity": "High" if total_probability > 0.7 else "Medium" if total_probability > 0.4 else "Low",
                "recommended_action": "Immediate inspection required" if total_probability > 0.7 else "Schedule maintenance" if total_probability > 0.4 else "Continue monitoring"
            })
        
        return sorted(predictions, key=lambda x: x["failure_probability"], reverse=True)

    def _generate_rca_data(self, vehicle_id: str, vehicle_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Root Cause Analysis data for manufacturing feedback."""
        failure_patterns = [
            {
                "issue": "Premature Brake Pad Wear",
                "affected_batches": ["BATCH_2020_A", "BATCH_2021_A"],
                "root_cause": "Substandard brake pad material from Supplier ABC",
                "occurrence_rate": 0.23,
                "corrective_action": "Switch to Supplier XYZ for brake pad materials"
            },
            {
                "issue": "Alternator Bearing Failure",
                "affected_batches": ["BATCH_2020_B"],
                "root_cause": "Inadequate bearing lubrication during assembly",
                "occurrence_rate": 0.18,
                "corrective_action": "Revised assembly procedures and lubrication protocols"
            },
            {
                "issue": "Transmission Fluid Leak",
                "affected_batches": ["BATCH_2021_C"],
                "root_cause": "Defective seal gaskets from manufacturing batch",
                "occurrence_rate": 0.15,
                "corrective_action": "Quality inspection enhancement for seal components"
            }
        ]
        
        batch_analysis = {
            "vehicle_batch": vehicle_data["manufacturing_batch"],
            "total_vehicles_in_batch": random.randint(500, 1500),
            "reported_issues": random.randint(5, 50),
            "defect_rate": round(random.uniform(0.01, 0.08), 4)
        }
        
        supplier_quality = [
            {"supplier": "ABC Components", "quality_score": 7.2, "trend": "declining"},
            {"supplier": "XYZ Manufacturing", "quality_score": 8.9, "trend": "stable"},
            {"supplier": "DEF Industries", "quality_score": 8.1, "trend": "improving"}
        ]
        
        return {
            "batch_analysis": batch_analysis,
            "failure_patterns": failure_patterns,
            "supplier_quality_trends": supplier_quality,
            "recommended_actions": [
                "Implement enhanced quality controls for Supplier ABC",
                "Increase inspection frequency for BATCH_2020_A components",
                "Develop predictive maintenance program for identified failure patterns"
            ]
        }

    def _generate_pattern_analysis(self, vehicle_id: str, vehicle_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate usage pattern analysis for predictive maintenance."""
        usage_stats = {
            "avg_daily_miles": round(vehicle_data["mileage"] / ((datetime.now().year - vehicle_data["year"]) * 365), 1),
            "driving_pattern": vehicle_data["usage_pattern"],
            "seasonal_variation": {
                "spring": random.randint(80, 120),
                "summer": random.randint(90, 140),
                "fall": random.randint(70, 110),
                "winter": random.randint(60, 100)
            }
        }
        
        maintenance_adherence = {
            "on_time_services": random.randint(70, 95),
            "overdue_services": random.randint(5, 30),
            "adherence_score": round(random.uniform(0.75, 0.95), 2)
        }
        
        predictive_intervals = {
            "oil_change": f"Every {random.randint(3000, 5000)} miles or {random.randint(3, 6)} months",
            "brake_inspection": f"Every {random.randint(10000, 15000)} miles",
            "tire_rotation": f"Every {random.randint(5000, 8000)} miles",
            "comprehensive_inspection": "Every 12 months"
        }
        
        return {
            "usage_statistics": usage_stats,
            "maintenance_adherence": maintenance_adherence,
            "recommended_intervals": predictive_intervals,
            "cost_optimization": {
                "potential_annual_savings": random.randint(200, 800),
                "preventive_vs_reactive_ratio": f"{random.randint(70, 85)}:{random.randint(15, 30)}"
            }
        }

    def _add_service_record(self, vehicle_id: str, service_data: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate adding a new service record."""
        new_record = {
            "record_id": f"SVC_{vehicle_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "vehicle_id": vehicle_id,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "service_type": service_data.get("service_type", "General Maintenance"),
            "cost": service_data.get("cost", random.randint(50, 300)),
            "service_center": service_data.get("service_center", "AutoCare Plus"),
            "technician": service_data.get("technician", f"TECH_{random.randint(1001, 1099)}"),
            "status": "Completed"
        }
        
        return {
            "status": "success",
            "message": "Service record added successfully",
            "record": new_record
        }

    def _run(self, vehicle_id: str, action_type: str, filters: Optional[Dict[str, Any]] = None) -> str:
        """Execute the maintenance history API request."""
        try:
            # Validate vehicle ID
            if not vehicle_id.startswith("VEH") or not vehicle_id[3:].isdigit():
                return json.dumps({
                    "error": "Invalid vehicle_id format. Use VEH001-VEH010",
                    "status": "error"
                })
            
            vehicle_data = self._generate_vehicle_data(vehicle_id)
            
            if action_type == "get_history":
                service_history = self._generate_service_history(vehicle_id, vehicle_data)
                result = {
                    "vehicle_id": vehicle_id,
                    "vehicle_info": vehicle_data,
                    "service_history": service_history,
                    "total_records": len(service_history),
                    "total_maintenance_cost": sum(record["cost"] for record in service_history)
                }
                
            elif action_type == "predict_failures":
                predictions = self._predict_failures(vehicle_id, vehicle_data)
                result = {
                    "vehicle_id": vehicle_id,
                    "prediction_date": datetime.now().strftime("%Y-%m-%d"),
                    "failure_predictions": predictions,
                    "summary": {
                        "high_risk_components": len([p for p in predictions if p["severity"] == "High"]),
                        "medium_risk_components": len([p for p in predictions if p["severity"] == "Medium"]),
                        "low_risk_components": len([p for p in predictions if p["severity"] == "Low"])
                    }
                }
                
            elif action_type == "get_rca_data":
                rca_data = self._generate_rca_data(vehicle_id, vehicle_data)
                result = {
                    "vehicle_id": vehicle_id,
                    "analysis_date": datetime.now().strftime("%Y-%m-%d"),
                    "rca_analysis": rca_data
                }
                
            elif action_type == "add_service_record":
                service_data = filters or {}
                record_result = self._add_service_record(vehicle_id, service_data)
                result = record_result
                
            elif action_type == "get_pattern_analysis":
                pattern_analysis = self._generate_pattern_analysis(vehicle_id, vehicle_data)
                result = {
                    "vehicle_id": vehicle_id,
                    "analysis_date": datetime.now().strftime("%Y-%m-%d"),
                    "pattern_analysis": pattern_analysis
                }
                
            else:
                result = {
                    "error": f"Invalid action_type: {action_type}",
                    "valid_actions": ["get_history", "predict_failures", "get_rca_data", "add_service_record", "get_pattern_analysis"],
                    "status": "error"
                }
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            return json.dumps({
                "error": f"Tool execution failed: {str(e)}",
                "status": "error"
            }, indent=2)