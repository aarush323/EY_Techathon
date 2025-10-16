from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Dict, Any, Optional
import requests
import json
import os

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
    """Tool for electric vehicle route planning and charging station optimization using Iternio API."""

    name: str = "iternio_route_optimizer"
    description: str = (
        "Integrates with Iternio API for electric vehicle route planning, charging station optimization, "
        "and energy consumption calculations. Supports route optimization, charging station finding, "
        "energy consumption estimation, and charging time calculations for electric service vehicle fleets."
    )
    args_schema: Type[BaseModel] = IternioRouteOptimizerInput

    def _get_api_key(self) -> str:
        """Get the Iternio API key from environment variables."""
        api_key = os.getenv("ITERNIO_API_KEY")
        if not api_key:
            raise ValueError("ITERNIO_API_KEY environment variable is required")
        return api_key

    def _make_api_request(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Make a request to the Iternio API with proper headers and error handling."""
        try:
            api_key = self._get_api_key()
            base_url = "https://api.iternio.com/1"
            url = f"{base_url}/{endpoint}"
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
                "User-Agent": "CrewAI-IternioRouteOptimizer/1.0"
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            
            return response.json()
        
        except requests.exceptions.RequestException as e:
            return {
                "error": True,
                "message": f"API request failed: {str(e)}",
                "status_code": getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None
            }
        except Exception as e:
            return {
                "error": True,
                "message": f"Unexpected error: {str(e)}"
            }

    def _optimize_service_route(self, start_location: str, end_location: str, 
                               vehicle_type: str, max_range_km: int) -> Dict[str, Any]:
        """Plan optimal route for service vehicles considering EV range and charging needs."""
        params = {
            "start": start_location,
            "destination": end_location,
            "vehicle": vehicle_type,
            "max_range": max_range_km,
            "fast_chargers_only": "true",
            "units": "km"
        }
        
        result = self._make_api_request("tlm/route", params)
        
        if result.get("error"):
            return result
        
        # Process and structure the route data
        processed_result = {
            "route_optimized": True,
            "start_location": start_location,
            "end_location": end_location,
            "vehicle_type": vehicle_type,
            "total_distance_km": result.get("distance", 0),
            "total_time_minutes": result.get("duration", 0),
            "charging_stops": result.get("chargers", []),
            "energy_consumption_kwh": result.get("consumption", 0),
            "route_polyline": result.get("polyline", ""),
            "warnings": result.get("warnings", [])
        }
        
        return processed_result

    def _find_charging_stations(self, latitude: float, longitude: float, 
                               radius_km: int) -> Dict[str, Any]:
        """Find charging stations near service centers."""
        params = {
            "lat": latitude,
            "lng": longitude,
            "radius": radius_km,
            "fast_charging": "true",
            "available": "true"
        }
        
        result = self._make_api_request("tlm/chargers", params)
        
        if result.get("error"):
            return result
        
        # Process charging station data
        charging_stations = []
        for station in result.get("chargers", []):
            charging_stations.append({
                "name": station.get("name", "Unknown"),
                "address": station.get("address", ""),
                "latitude": station.get("lat", 0),
                "longitude": station.get("lng", 0),
                "distance_km": station.get("distance", 0),
                "power_kw": station.get("power", 0),
                "connector_types": station.get("connectors", []),
                "availability": station.get("status", "unknown"),
                "network": station.get("network", ""),
                "cost_per_kwh": station.get("cost", 0)
            })
        
        return {
            "search_location": {"latitude": latitude, "longitude": longitude},
            "search_radius_km": radius_km,
            "stations_found": len(charging_stations),
            "charging_stations": charging_stations
        }

    def _calculate_energy_consumption(self, route_data: str, vehicle_specs: str) -> Dict[str, Any]:
        """Estimate energy needs for routes based on vehicle specifications."""
        try:
            # Parse JSON strings
            route_info = json.loads(route_data) if isinstance(route_data, str) else route_data
            vehicle_info = json.loads(vehicle_specs) if isinstance(vehicle_specs, str) else vehicle_specs
            
            # Extract route parameters
            distance_km = route_info.get("distance_km", 0)
            elevation_gain_m = route_info.get("elevation_gain_m", 0)
            average_speed_kmh = route_info.get("average_speed_kmh", 50)
            temperature_celsius = route_info.get("temperature_celsius", 20)
            
            # Extract vehicle parameters
            efficiency_kwh_per_100km = vehicle_info.get("efficiency_kwh_per_100km", 20)
            battery_capacity_kwh = vehicle_info.get("battery_capacity_kwh", 75)
            weight_kg = vehicle_info.get("weight_kg", 2000)
            
            # Basic energy consumption calculation
            base_consumption = (distance_km / 100) * efficiency_kwh_per_100km
            
            # Adjust for elevation (simplified calculation)
            elevation_factor = 1 + (elevation_gain_m / 10000)  # 1% increase per 100m elevation gain
            
            # Adjust for temperature (simplified)
            temp_factor = 1.0
            if temperature_celsius < 0:
                temp_factor = 1.2  # 20% increase in cold weather
            elif temperature_celsius > 30:
                temp_factor = 1.1  # 10% increase in hot weather
            
            # Adjust for speed (simplified)
            speed_factor = 1.0
            if average_speed_kmh > 80:
                speed_factor = 1 + ((average_speed_kmh - 80) * 0.01)  # 1% per km/h over 80
            
            total_consumption = base_consumption * elevation_factor * temp_factor * speed_factor
            
            return {
                "route_distance_km": distance_km,
                "estimated_consumption_kwh": round(total_consumption, 2),
                "consumption_per_100km": round((total_consumption / distance_km) * 100, 2),
                "battery_usage_percent": round((total_consumption / battery_capacity_kwh) * 100, 1),
                "remaining_range_km": round(((battery_capacity_kwh - total_consumption) / efficiency_kwh_per_100km) * 100, 0),
                "factors_applied": {
                    "elevation_factor": round(elevation_factor, 2),
                    "temperature_factor": round(temp_factor, 2),
                    "speed_factor": round(speed_factor, 2)
                }
            }
            
        except json.JSONDecodeError as e:
            return {
                "error": True,
                "message": f"Invalid JSON data provided: {str(e)}"
            }
        except Exception as e:
            return {
                "error": True,
                "message": f"Error calculating energy consumption: {str(e)}"
            }

    def _get_charging_time(self, battery_level: int, target_level: int, 
                          charging_power: int) -> Dict[str, Any]:
        """Calculate charging duration for electric service vehicles."""
        try:
            if not all([battery_level, target_level, charging_power]):
                return {
                    "error": True,
                    "message": "Battery level, target level, and charging power are required"
                }
            
            if battery_level >= target_level:
                return {
                    "error": True,
                    "message": "Current battery level is already at or above target level"
                }
            
            # Assume a typical EV battery capacity (can be made configurable)
            battery_capacity_kwh = 75  # Default capacity
            
            # Calculate energy needed
            energy_needed_kwh = ((target_level - battery_level) / 100) * battery_capacity_kwh
            
            # Calculate charging time (simplified - doesn't account for charging curve)
            charging_time_hours = energy_needed_kwh / charging_power
            charging_time_minutes = charging_time_hours * 60
            
            # Estimate cost (assuming average electricity cost)
            cost_per_kwh = 0.30  # Default cost per kWh
            estimated_cost = energy_needed_kwh * cost_per_kwh
            
            return {
                "current_battery_level": battery_level,
                "target_battery_level": target_level,
                "charging_power_kw": charging_power,
                "energy_needed_kwh": round(energy_needed_kwh, 2),
                "charging_time_minutes": round(charging_time_minutes, 0),
                "charging_time_hours": round(charging_time_hours, 1),
                "estimated_cost": round(estimated_cost, 2),
                "battery_capacity_assumed_kwh": battery_capacity_kwh
            }
            
        except Exception as e:
            return {
                "error": True,
                "message": f"Error calculating charging time: {str(e)}"
            }

    def _run(self, action: str, start_location: Optional[str] = None, 
             end_location: Optional[str] = None, vehicle_type: str = "Model S", 
             max_range_km: int = 500, latitude: Optional[float] = None, 
             longitude: Optional[float] = None, radius_km: int = 50, 
             battery_level: Optional[int] = None, target_level: Optional[int] = None, 
             charging_power: Optional[int] = None, route_data: Optional[str] = None, 
             vehicle_specs: Optional[str] = None) -> str:
        """Execute the specified action for EV route optimization and charging management."""
        
        try:
            if action == "optimize_route":
                if not start_location or not end_location:
                    return json.dumps({
                        "error": True,
                        "message": "Start location and end location are required for route optimization"
                    })
                result = self._optimize_service_route(start_location, end_location, 
                                                    vehicle_type, max_range_km)
            
            elif action == "find_charging_stations":
                if latitude is None or longitude is None:
                    return json.dumps({
                        "error": True,
                        "message": "Latitude and longitude are required for finding charging stations"
                    })
                result = self._find_charging_stations(latitude, longitude, radius_km)
            
            elif action == "calculate_energy":
                if not route_data or not vehicle_specs:
                    return json.dumps({
                        "error": True,
                        "message": "Route data and vehicle specifications are required for energy calculation"
                    })
                result = self._calculate_energy_consumption(route_data, vehicle_specs)
            
            elif action == "get_charging_time":
                if battery_level is None or target_level is None or charging_power is None:
                    return json.dumps({
                        "error": True,
                        "message": "Battery level, target level, and charging power are required for charging time calculation"
                    })
                result = self._get_charging_time(battery_level, target_level, charging_power)
            
            else:
                return json.dumps({
                    "error": True,
                    "message": f"Unknown action: {action}. Available actions: optimize_route, find_charging_stations, calculate_energy, get_charging_time"
                })
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            return json.dumps({
                "error": True,
                "message": f"Tool execution error: {str(e)}"
            })