from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Dict, Any, Optional
import json
import random
from datetime import datetime

class IternioRouteOptimizerInput(BaseModel):
    """Input schema for Iternio Route Optimizer Tool."""
    action: str = Field(
        ..., 
        description="Action to perform: 'optimize_route', 'find_charging_stations', 'calculate_energy', or 'get_charging_time'"
    )
    start_location: Optional[str] = Field(
        None, 
        description="Starting location (address or coordinates) for route optimization"
    )
    end_location: Optional[str] = Field(
        None, 
        description="Destination location (address or coordinates) for route optimization"
    )
    vehicle_type: Optional[str] = Field(
        "Model S", 
        description="Electric vehicle model for route planning"
    )
    max_range_km: Optional[int] = Field(
        500, 
        description="Maximum range of the vehicle in kilometers"
    )
    latitude: Optional[float] = Field(
        None, 
        description="Latitude coordinate for finding nearby charging stations"
    )
    longitude: Optional[float] = Field(
        None, 
        description="Longitude coordinate for finding nearby charging stations"
    )
    radius_km: Optional[int] = Field(
        50, 
        description="Search radius in kilometers for charging stations"
    )
    battery_level: Optional[int] = Field(
        None, 
        description="Current battery level percentage for charging time calculation"
    )
    target_level: Optional[int] = Field(
        None, 
        description="Target battery level percentage for charging time calculation"
    )
    charging_power: Optional[int] = Field(
        None, 
        description="Charging power in kW for charging time calculation"
    )
    route_data: Optional[str] = Field(
        None, 
        description="JSON string containing route data for energy consumption calculation"
    )
    vehicle_specs: Optional[str] = Field(
        None, 
        description="JSON string containing vehicle specifications for energy consumption calculation"
    )

class IternioRouteOptimizer(BaseTool):
    """Tool for electric vehicle route planning and charging station optimization (Synthetic)."""

    name: str = "iternio_route_optimizer"
    description: str = (
        "Simulates Iternio API for electric vehicle route planning, charging station optimization, "
        "and energy consumption calculations. Supports route optimization, charging station finding, "
        "energy consumption estimation, and charging time calculations for electric service vehicle fleets."
    )
    args_schema: Type[BaseModel] = IternioRouteOptimizerInput

    def _optimize_service_route(self, start_location: str, end_location: str, 
                               vehicle_type: str, max_range_km: int) -> Dict[str, Any]:
        """Simulate optimal route planning."""
        distance = random.randint(50, 300)
        duration = int(distance * 1.5)  # Rough estimate
        
        return {
            "route_optimized": True,
            "start_location": start_location,
            "end_location": end_location,
            "vehicle_type": vehicle_type,
            "total_distance_km": distance,
            "total_time_minutes": duration,
            "charging_stops": [
                {
                    "name": "SuperCharger Station A",
                    "distance_from_start_km": int(distance * 0.4),
                    "duration_minutes": 20
                }
            ] if distance > max_range_km * 0.6 else [],
            "energy_consumption_kwh": int(distance * 0.2),
            "route_polyline": "encoded_polyline_string_placeholder",
            "warnings": []
        }

    def _find_charging_stations(self, latitude: float, longitude: float, 
                               radius_km: int) -> Dict[str, Any]:
        """Simulate finding charging stations."""
        stations = []
        for i in range(random.randint(2, 5)):
            stations.append({
                "name": f"Charging Station {chr(65+i)}",
                "address": f"{random.randint(1, 999)} EV Lane",
                "latitude": latitude + random.uniform(-0.1, 0.1),
                "longitude": longitude + random.uniform(-0.1, 0.1),
                "distance_km": round(random.uniform(1, radius_km), 1),
                "power_kw": random.choice([50, 150, 250]),
                "connector_types": ["CCS", "Type 2"],
                "availability": "Available",
                "network": "EVNet",
                "cost_per_kwh": 0.35
            })
        
        return {
            "search_location": {"latitude": latitude, "longitude": longitude},
            "search_radius_km": radius_km,
            "stations_found": len(stations),
            "charging_stations": stations
        }

    def _calculate_energy_consumption(self, route_data: str, vehicle_specs: str) -> Dict[str, Any]:
        """Simulate energy consumption calculation."""
        try:
            # Parse JSON strings just to validate, but generate synthetic result
            route_info = json.loads(route_data) if isinstance(route_data, str) else route_data
            distance_km = route_info.get("distance_km", 100)
            
            consumption = distance_km * 0.2
            
            return {
                "route_distance_km": distance_km,
                "estimated_consumption_kwh": round(consumption, 2),
                "consumption_per_100km": 20.0,
                "battery_usage_percent": round((consumption / 75) * 100, 1),
                "remaining_range_km": int((75 - consumption) / 0.2),
                "factors_applied": {
                    "elevation_factor": 1.02,
                    "temperature_factor": 1.0,
                    "speed_factor": 1.05
                }
            }
        except Exception:
            return {"error": True, "message": "Invalid input data"}

    def _get_charging_time(self, battery_level: int, target_level: int, 
                          charging_power: int) -> Dict[str, Any]:
        """Calculate charging duration."""
        if battery_level >= target_level:
            return {"message": "Battery already sufficient"}
            
        needed_kwh = (target_level - battery_level) * 0.75  # Assuming 75kWh battery
        time_hours = needed_kwh / charging_power
        
        return {
            "current_battery_level": battery_level,
            "target_battery_level": target_level,
            "charging_power_kw": charging_power,
            "energy_needed_kwh": round(needed_kwh, 2),
            "charging_time_minutes": int(time_hours * 60),
            "charging_time_hours": round(time_hours, 1),
            "estimated_cost": round(needed_kwh * 0.30, 2),
            "battery_capacity_assumed_kwh": 75
        }

    def _run(self, action: str, start_location: Optional[str] = None, 
             end_location: Optional[str] = None, vehicle_type: str = "Model S", 
             max_range_km: int = 500, latitude: Optional[float] = None, 
             longitude: Optional[float] = None, radius_km: int = 50, 
             battery_level: Optional[int] = None, target_level: Optional[int] = None, 
             charging_power: Optional[int] = None, route_data: Optional[str] = None, 
             vehicle_specs: Optional[str] = None) -> str:
        """Execute the specified action."""
        
        try:
            if action == "optimize_route":
                result = self._optimize_service_route(start_location, end_location, 
                                                    vehicle_type, max_range_km)
            
            elif action == "find_charging_stations":
                result = self._find_charging_stations(latitude or 0.0, longitude or 0.0, radius_km)
            
            elif action == "calculate_energy":
                result = self._calculate_energy_consumption(route_data or "{}", vehicle_specs or "{}")
            
            elif action == "get_charging_time":
                result = self._get_charging_time(battery_level or 0, target_level or 80, charging_power or 50)
            
            else:
                return json.dumps({
                    "error": True,
                    "message": f"Unknown action: {action}"
                })
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            return json.dumps({
                "error": True,
                "message": f"Tool execution error: {str(e)}"
            })