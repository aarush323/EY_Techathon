from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Dict, Any, List, Optional
import json
import hashlib
import math
from datetime import datetime, timedelta

class VehicleTelematicsRequest(BaseModel):
    """Input schema for Vehicle Telematics API Tool."""
    vehicle_id: str = Field(..., description="The unique vehicle identifier (e.g., VEH001)")

class VehicleTelematicsAPI(BaseTool):
    """Tool for simulating real-time vehicle telematics data for automotive predictive maintenance."""

    name: str = "Vehicle Telematics API"
    description: str = (
        "Simulates realistic vehicle telematics data including engine metrics, brake condition, "
        "battery status, tire pressure, GPS coordinates, diagnostic trouble codes, maintenance history, "
        "and usage patterns. Returns consistent data based on vehicle ID for testing and analysis."
    )
    args_schema: Type[BaseModel] = VehicleTelematicsRequest

    def _generate_seed(self, vehicle_id: str) -> int:
        """Generate a consistent seed based on vehicle ID."""
        return int(hashlib.md5(vehicle_id.encode()).hexdigest()[:8], 16)

    def _seeded_random(self, seed: int, min_val: float, max_val: float) -> float:
        """Generate a pseudo-random number between min_val and max_val using seed."""
        # Simple linear congruential generator
        seed = (seed * 1103515245 + 12345) & 0x7fffffff
        normalized = seed / 0x7fffffff
        return min_val + normalized * (max_val - min_val)

    def _get_maintenance_status(self, seed: int, vehicle_num: int) -> Dict[str, Any]:
        """Determine maintenance status and warning conditions."""
        # Some vehicles have issues based on their number
        has_issues = vehicle_num in [2, 4, 6, 8, 10]  # Even numbered vehicles have issues
        
        if has_issues:
            return {
                "has_warnings": True,
                "warning_level": "high" if vehicle_num in [4, 8] else "medium",
                "maintenance_due": True
            }
        else:
            return {
                "has_warnings": vehicle_num in [3, 7],  # Some vehicles have minor warnings
                "warning_level": "low" if vehicle_num in [3, 7] else "none",
                "maintenance_due": False
            }

    def _generate_dtcs(self, vehicle_id: str, maintenance_status: Dict) -> List[str]:
        """Generate diagnostic trouble codes based on maintenance status."""
        dtcs = []
        vehicle_num = int(vehicle_id[-3:]) if vehicle_id[-3:].isdigit() else 1
        
        if maintenance_status["has_warnings"]:
            if vehicle_num == 2:
                dtcs = ["P0300", "P0171"]  # Engine misfire, lean mixture
            elif vehicle_num == 4:
                dtcs = ["P0128", "P0420", "P0171"]  # Coolant thermostat, catalytic converter, lean mixture
            elif vehicle_num == 6:
                dtcs = ["P0562", "P0118"]  # Low battery voltage, coolant temp sensor
            elif vehicle_num == 8:
                dtcs = ["P0420", "P0300", "P0128"]  # Catalytic converter, misfire, thermostat
            elif vehicle_num == 10:
                dtcs = ["P0171", "P0562"]  # Lean mixture, low battery voltage
            elif vehicle_num in [3, 7]:
                dtcs = ["P0420"] if vehicle_num == 3 else ["P0171"]  # Minor issues
                
        return dtcs

    def _run(self, vehicle_id: str) -> str:
        """Generate comprehensive vehicle telematics data."""
        try:
            # Generate consistent seed and vehicle number
            base_seed = self._generate_seed(vehicle_id)
            vehicle_num = int(vehicle_id[-3:]) if vehicle_id[-3:].isdigit() else 1
            
            # Get maintenance status
            maintenance_status = self._get_maintenance_status(base_seed, vehicle_num)
            
            # Generate base coordinates (simulate fleet in different regions)
            base_lat = 40.7128 + (vehicle_num * 0.1) - 0.5  # Around NYC area
            base_lng = -74.0060 + (vehicle_num * 0.1) - 0.5
            
            # Generate sensor data with realistic ranges
            current_seed = base_seed
            
            # Engine metrics
            rpm_base = 800 if maintenance_status["warning_level"] == "none" else 850
            current_seed = (current_seed * 1103515245 + 12345) & 0x7fffffff
            engine_rpm = rpm_base + self._seeded_random(current_seed, 0, 200)
            
            current_seed = (current_seed * 1103515245 + 12345) & 0x7fffffff
            temp_base = 195 if maintenance_status["warning_level"] == "none" else 210
            engine_temp = temp_base + self._seeded_random(current_seed, -5, 15)
            
            current_seed = (current_seed * 1103515245 + 12345) & 0x7fffffff
            oil_pressure_base = 40 if maintenance_status["warning_level"] in ["none", "low"] else 25
            oil_pressure = oil_pressure_base + self._seeded_random(current_seed, -5, 10)
            
            # Brake and battery
            current_seed = (current_seed * 1103515245 + 12345) & 0x7fffffff
            brake_thickness_base = 8 if maintenance_status["warning_level"] == "none" else 3
            brake_pad_thickness = brake_thickness_base + self._seeded_random(current_seed, -1, 2)
            
            current_seed = (current_seed * 1103515245 + 12345) & 0x7fffffff
            battery_base = 12.6 if maintenance_status["warning_level"] == "none" else 11.8
            battery_voltage = battery_base + self._seeded_random(current_seed, -0.3, 0.4)
            
            # Transmission and coolant
            current_seed = (current_seed * 1103515245 + 12345) & 0x7fffffff
            trans_temp = 175 + self._seeded_random(current_seed, -10, 25)
            
            current_seed = (current_seed * 1103515245 + 12345) & 0x7fffffff
            coolant_level = 85 + self._seeded_random(current_seed, -10, 15)
            if maintenance_status["warning_level"] in ["high", "medium"]:
                coolant_level -= 20
            
            # Tire pressures
            tire_pressures = []
            base_pressure = 32
            for i in range(4):
                current_seed = (current_seed * 1103515245 + 12345) & 0x7fffffff
                pressure = base_pressure + self._seeded_random(current_seed, -3, 3)
                if maintenance_status["warning_level"] == "high" and i == vehicle_num % 4:
                    pressure -= 8  # One tire low on high warning vehicles
                tire_pressures.append(round(pressure, 1))
            
            # Odometer and fuel
            current_seed = (current_seed * 1103515245 + 12345) & 0x7fffffff
            odometer = int(25000 + vehicle_num * 5000 + self._seeded_random(current_seed, 0, 15000))
            
            current_seed = (current_seed * 1103515245 + 12345) & 0x7fffffff
            fuel_level = 25 + self._seeded_random(current_seed, 0, 70)
            
            # GPS coordinates with small variation
            current_seed = (current_seed * 1103515245 + 12345) & 0x7fffffff
            gps_lat = base_lat + self._seeded_random(current_seed, -0.01, 0.01)
            current_seed = (current_seed * 1103515245 + 12345) & 0x7fffffff
            gps_lng = base_lng + self._seeded_random(current_seed, -0.01, 0.01)
            
            # Usage patterns
            current_seed = (current_seed * 1103515245 + 12345) & 0x7fffffff
            daily_miles = int(30 + self._seeded_random(current_seed, 0, 120))
            
            current_seed = (current_seed * 1103515245 + 12345) & 0x7fffffff
            driving_style_base = 85 if maintenance_status["warning_level"] == "none" else 65
            driving_style_score = int(driving_style_base + self._seeded_random(current_seed, -15, 15))
            
            # Last maintenance date
            days_ago = 30 if maintenance_status["maintenance_due"] else 15
            last_maintenance = (datetime.now() - timedelta(days=days_ago + vehicle_num * 5)).strftime("%Y-%m-%d")
            
            # Generate DTCs
            dtcs = self._generate_dtcs(vehicle_id, maintenance_status)
            
            # Compile all data
            telematics_data = {
                "vehicle_id": vehicle_id,
                "timestamp": datetime.now().isoformat(),
                "engine_data": {
                    "rpm": round(engine_rpm, 0),
                    "temperature_f": round(engine_temp, 1),
                    "oil_pressure_psi": round(oil_pressure, 1)
                },
                "brake_system": {
                    "front_pad_thickness_mm": round(brake_pad_thickness, 1),
                    "rear_pad_thickness_mm": round(brake_pad_thickness + self._seeded_random(current_seed, -1, 1), 1)
                },
                "electrical_system": {
                    "battery_voltage": round(battery_voltage, 2)
                },
                "transmission": {
                    "temperature_f": round(trans_temp, 1)
                },
                "cooling_system": {
                    "coolant_level_percent": round(max(0, min(100, coolant_level)), 1)
                },
                "tire_pressure_psi": {
                    "front_left": tire_pressures[0],
                    "front_right": tire_pressures[1],
                    "rear_left": tire_pressures[2],
                    "rear_right": tire_pressures[3]
                },
                "vehicle_status": {
                    "odometer_miles": odometer,
                    "fuel_level_percent": round(fuel_level, 1)
                },
                "gps_location": {
                    "latitude": round(gps_lat, 6),
                    "longitude": round(gps_lng, 6)
                },
                "diagnostic_codes": dtcs,
                "maintenance_info": {
                    "last_service_date": last_maintenance,
                    "maintenance_due": maintenance_status["maintenance_due"],
                    "warning_level": maintenance_status["warning_level"]
                },
                "usage_patterns": {
                    "daily_average_miles": daily_miles,
                    "driving_style_score": driving_style_score,
                    "driving_style_description": self._get_driving_style_description(driving_style_score)
                },
                "alerts": self._generate_alerts(maintenance_status, oil_pressure, brake_pad_thickness, 
                                              battery_voltage, tire_pressures, coolant_level)
            }
            
            return json.dumps(telematics_data, indent=2)
            
        except Exception as e:
            return f"Error generating vehicle telematics data: {str(e)}"
    
    def _get_driving_style_description(self, score: int) -> str:
        """Get driving style description based on score."""
        if score >= 90:
            return "Excellent - Smooth and efficient driving"
        elif score >= 80:
            return "Good - Generally safe driving habits"
        elif score >= 70:
            return "Fair - Some aggressive acceleration/braking"
        elif score >= 60:
            return "Poor - Frequent harsh driving events"
        else:
            return "Critical - Dangerous driving patterns detected"
    
    def _generate_alerts(self, maintenance_status: Dict, oil_pressure: float, 
                        brake_thickness: float, battery_voltage: float, 
                        tire_pressures: List[float], coolant_level: float) -> List[str]:
        """Generate maintenance alerts based on sensor readings."""
        alerts = []
        
        if oil_pressure < 30:
            alerts.append("LOW OIL PRESSURE - Check engine oil level immediately")
        
        if brake_thickness < 4:
            alerts.append("BRAKE PADS WORN - Schedule brake service soon")
        
        if battery_voltage < 12.0:
            alerts.append("LOW BATTERY VOLTAGE - Battery may need replacement")
        
        if any(pressure < 28 for pressure in tire_pressures):
            alerts.append("LOW TIRE PRESSURE - Check tire inflation")
        
        if coolant_level < 70:
            alerts.append("LOW COOLANT LEVEL - Check for leaks and refill")
        
        if maintenance_status["maintenance_due"]:
            alerts.append("SCHEDULED MAINTENANCE DUE - Contact service department")
        
        return alerts