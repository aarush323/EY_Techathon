from crewai.tools import BaseTool
from pydantic import BaseModel, Field, model_validator
from typing import Type, Dict, Any, List, Optional
from datetime import datetime, timedelta
import json

class ServiceCenterRequest(BaseModel):
    """Input schema for Service Center API Tool."""
    action: str = Field(..., description="The action to perform: 'check_availability', 'book_appointment', 'get_service_centers', 'cancel_appointment', or 'get_appointments'")
    service_center_id: Optional[str] = Field(None, description="ID of the service center (mumbai, delhi, bangalore, chennai, hyderabad)")
    service_type: Optional[str] = Field(None, description="Type of service needed (e.g., 'oil_change', 'brake_service', 'tire_replacement', 'battery_check', 'general_inspection')")
    date: Optional[str] = Field(None, description="Date for the service in YYYY-MM-DD format")
    time: Optional[str] = Field(None, description="Time for the service in HH:MM format")
    customer_name: Optional[str] = Field(None, description="Name of the customer for booking")
    customer_phone: Optional[str] = Field(None, description="Phone number of the customer")
    appointment_id: Optional[str] = Field(None, description="Appointment ID for cancellation or lookup")

class ServiceCenterAPI(BaseTool):
    """Tool for managing Indian service center operations, appointments, and availability."""

    name: str = "service_center_api"
    description: str = (
        "Comprehensive service center management API for Indian locations. "
        "Supports checking availability, booking appointments, retrieving service center information, "
        "cancelling appointments, and managing customer appointments across Mumbai, Delhi, Bangalore, Chennai, and Hyderabad."
    )
    args_schema: Type[BaseModel] = ServiceCenterRequest
    
    # Proper Pydantic v2 field definitions
    service_centers: Dict[str, Any] = Field(default_factory=dict, description="Service center database")
    appointments_db: Dict[str, Any] = Field(default_factory=dict, description="Appointments database")

    def model_post_init(self, __context: Any) -> None:
        """Initialize the service center database after object creation."""
        super().model_post_init(__context)
        self._initialize_service_centers()
        self._initialize_appointments_db()

    def _initialize_service_centers(self):
        """Initialize the service center database with Indian locations."""
        self.service_centers = {
            "mumbai": {
                "id": "mumbai",
                "name": "Mumbai Service Center",
                "address": "Plot No. 123, Andheri East, Mumbai, Maharashtra 400069",
                "city": "Mumbai",
                "state": "Maharashtra",
                "phone": "+91-22-2834-5678",
                "email": "mumbai@servicecenters.in",
                "working_hours": {
                    "monday": "09:00-18:00",
                    "tuesday": "09:00-18:00", 
                    "wednesday": "09:00-18:00",
                    "thursday": "09:00-18:00",
                    "friday": "09:00-18:00",
                    "saturday": "09:00-16:00",
                    "sunday": "closed"
                },
                "services": [
                    "oil_change", "brake_service", "tire_replacement", 
                    "battery_check", "general_inspection", "ac_service",
                    "engine_diagnostics", "suspension_service"
                ],
                "capacity": 15,
                "manager": "Rajesh Sharma"
            },
            "delhi": {
                "id": "delhi", 
                "name": "Delhi Service Center",
                "address": "Sector 18, Noida, Uttar Pradesh 201301",
                "city": "Delhi",
                "state": "Delhi",
                "phone": "+91-11-4567-8901",
                "email": "delhi@servicecenters.in",
                "working_hours": {
                    "monday": "08:30-19:00",
                    "tuesday": "08:30-19:00",
                    "wednesday": "08:30-19:00", 
                    "thursday": "08:30-19:00",
                    "friday": "08:30-19:00",
                    "saturday": "08:30-17:00",
                    "sunday": "10:00-15:00"
                },
                "services": [
                    "oil_change", "brake_service", "tire_replacement",
                    "battery_check", "general_inspection", "ac_service",
                    "engine_diagnostics", "transmission_service", "electrical_work"
                ],
                "capacity": 20,
                "manager": "Priya Gupta"
            },
            "bangalore": {
                "id": "bangalore",
                "name": "Bangalore Service Center", 
                "address": "Electronic City Phase 2, Bangalore, Karnataka 560100",
                "city": "Bangalore",
                "state": "Karnataka",
                "phone": "+91-80-1234-5678",
                "email": "bangalore@servicecenters.in",
                "working_hours": {
                    "monday": "09:00-18:30",
                    "tuesday": "09:00-18:30",
                    "wednesday": "09:00-18:30",
                    "thursday": "09:00-18:30", 
                    "friday": "09:00-18:30",
                    "saturday": "09:00-17:00",
                    "sunday": "closed"
                },
                "services": [
                    "oil_change", "brake_service", "tire_replacement",
                    "battery_check", "general_inspection", "ac_service", 
                    "engine_diagnostics", "hybrid_service", "software_updates"
                ],
                "capacity": 18,
                "manager": "Venkat Reddy"
            },
            "chennai": {
                "id": "chennai",
                "name": "Chennai Service Center",
                "address": "OMR Road, Thoraipakkam, Chennai, Tamil Nadu 600097",
                "city": "Chennai", 
                "state": "Tamil Nadu",
                "phone": "+91-44-9876-5432",
                "email": "chennai@servicecenters.in",
                "working_hours": {
                    "monday": "09:00-18:00",
                    "tuesday": "09:00-18:00",
                    "wednesday": "09:00-18:00",
                    "thursday": "09:00-18:00",
                    "friday": "09:00-18:00",
                    "saturday": "09:00-16:00",
                    "sunday": "10:00-14:00"
                },
                "services": [
                    "oil_change", "brake_service", "tire_replacement",
                    "battery_check", "general_inspection", "ac_service",
                    "engine_diagnostics", "paint_service", "denting_service"
                ],
                "capacity": 12,
                "manager": "Lakshmi Iyer"
            },
            "hyderabad": {
                "id": "hyderabad",
                "name": "Hyderabad Service Center",
                "address": "Gachibowli, Hyderabad, Telangana 500032",
                "city": "Hyderabad",
                "state": "Telangana", 
                "phone": "+91-40-5555-1234",
                "email": "hyderabad@servicecenters.in",
                "working_hours": {
                    "monday": "09:00-19:00",
                    "tuesday": "09:00-19:00",
                    "wednesday": "09:00-19:00",
                    "thursday": "09:00-19:00",
                    "friday": "09:00-19:00",
                    "saturday": "09:00-17:00", 
                    "sunday": "closed"
                },
                "services": [
                    "oil_change", "brake_service", "tire_replacement",
                    "battery_check", "general_inspection", "ac_service",
                    "engine_diagnostics", "wheel_alignment", "clutch_service"
                ],
                "capacity": 16,
                "manager": "Arjun Rao"
            }
        }

    def _initialize_appointments_db(self):
        """Initialize the appointments database."""
        self.appointments_db = {
            "appointments": {},
            "next_appointment_id": 1000
        }

    def _generate_appointment_id(self) -> str:
        """Generate a unique appointment ID."""
        appointment_id = f"APP{self.appointments_db['next_appointment_id']}"
        self.appointments_db['next_appointment_id'] += 1
        return appointment_id

    def _check_availability(self, service_center_id: str, date: str, time: str, service_type: str) -> Dict[str, Any]:
        """Check availability for a specific service center, date, time and service type."""
        try:
            if service_center_id not in self.service_centers:
                return {
                    "available": False,
                    "error": f"Service center '{service_center_id}' not found"
                }
            
            center = self.service_centers[service_center_id]
            
            # Check if service is offered
            if service_type not in center["services"]:
                return {
                    "available": False,
                    "error": f"Service '{service_type}' not available at {center['name']}"
                }
            
            # Parse date and check working hours
            try:
                service_date = datetime.strptime(date, "%Y-%m-%d")
                day_name = service_date.strftime("%A").lower()
                
                working_hours = center["working_hours"].get(day_name, "closed")
                if working_hours == "closed":
                    return {
                        "available": False,
                        "error": f"{center['name']} is closed on {day_name.capitalize()}"
                    }
                
                # Check if time is within working hours
                start_time, end_time = working_hours.split("-")
                service_time = datetime.strptime(time, "%H:%M").time()
                start = datetime.strptime(start_time, "%H:%M").time()
                end = datetime.strptime(end_time, "%H:%M").time()
                
                if not (start <= service_time <= end):
                    return {
                        "available": False,
                        "error": f"Requested time {time} is outside working hours ({working_hours})"
                    }
                
            except ValueError as e:
                return {
                    "available": False,
                    "error": f"Invalid date or time format: {str(e)}"
                }
            
            # Check existing appointments for capacity
            date_key = f"{service_center_id}_{date}"
            appointments_on_date = [
                apt for apt in self.appointments_db["appointments"].values()
                if apt["service_center_id"] == service_center_id and apt["date"] == date
            ]
            
            if len(appointments_on_date) >= center["capacity"]:
                return {
                    "available": False,
                    "error": f"Service center is fully booked on {date}"
                }
            
            return {
                "available": True,
                "service_center": center["name"],
                "date": date,
                "time": time,
                "service_type": service_type,
                "capacity_remaining": center["capacity"] - len(appointments_on_date)
            }
            
        except Exception as e:
            return {
                "available": False,
                "error": f"Error checking availability: {str(e)}"
            }

    def _book_appointment(self, service_center_id: str, date: str, time: str, 
                         service_type: str, customer_name: str, customer_phone: str) -> Dict[str, Any]:
        """Book an appointment at a service center."""
        try:
            # First check availability
            availability = self._check_availability(service_center_id, date, time, service_type)
            if not availability["available"]:
                return {
                    "success": False,
                    "error": availability["error"]
                }
            
            # Generate appointment ID and create appointment
            appointment_id = self._generate_appointment_id()
            appointment = {
                "id": appointment_id,
                "service_center_id": service_center_id,
                "service_center_name": self.service_centers[service_center_id]["name"],
                "date": date,
                "time": time,
                "service_type": service_type,
                "customer_name": customer_name,
                "customer_phone": customer_phone,
                "status": "confirmed",
                "created_at": datetime.now().isoformat()
            }
            
            self.appointments_db["appointments"][appointment_id] = appointment
            
            return {
                "success": True,
                "appointment_id": appointment_id,
                "appointment": appointment,
                "message": f"Appointment booked successfully at {appointment['service_center_name']}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error booking appointment: {str(e)}"
            }

    def _get_service_centers(self, service_center_id: Optional[str] = None) -> Dict[str, Any]:
        """Get information about service centers."""
        try:
            if service_center_id:
                if service_center_id not in self.service_centers:
                    return {
                        "success": False,
                        "error": f"Service center '{service_center_id}' not found"
                    }
                return {
                    "success": True,
                    "service_center": self.service_centers[service_center_id]
                }
            else:
                return {
                    "success": True,
                    "service_centers": self.service_centers,
                    "total_centers": len(self.service_centers)
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Error retrieving service centers: {str(e)}"
            }

    def _cancel_appointment(self, appointment_id: str) -> Dict[str, Any]:
        """Cancel an existing appointment."""
        try:
            if appointment_id not in self.appointments_db["appointments"]:
                return {
                    "success": False,
                    "error": f"Appointment '{appointment_id}' not found"
                }
            
            appointment = self.appointments_db["appointments"][appointment_id]
            if appointment["status"] == "cancelled":
                return {
                    "success": False,
                    "error": "Appointment is already cancelled"
                }
            
            # Update appointment status
            self.appointments_db["appointments"][appointment_id]["status"] = "cancelled"
            self.appointments_db["appointments"][appointment_id]["cancelled_at"] = datetime.now().isoformat()
            
            return {
                "success": True,
                "message": f"Appointment {appointment_id} cancelled successfully",
                "appointment": self.appointments_db["appointments"][appointment_id]
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error cancelling appointment: {str(e)}"
            }

    def _get_appointments(self, appointment_id: Optional[str] = None, 
                         service_center_id: Optional[str] = None) -> Dict[str, Any]:
        """Get appointment information."""
        try:
            if appointment_id:
                if appointment_id not in self.appointments_db["appointments"]:
                    return {
                        "success": False,
                        "error": f"Appointment '{appointment_id}' not found"
                    }
                return {
                    "success": True,
                    "appointment": self.appointments_db["appointments"][appointment_id]
                }
            
            appointments = list(self.appointments_db["appointments"].values())
            
            if service_center_id:
                appointments = [
                    apt for apt in appointments 
                    if apt["service_center_id"] == service_center_id
                ]
            
            return {
                "success": True,
                "appointments": appointments,
                "total_appointments": len(appointments)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error retrieving appointments: {str(e)}"
            }

    def _run(self, action: str, service_center_id: Optional[str] = None, 
            service_type: Optional[str] = None, date: Optional[str] = None,
            time: Optional[str] = None, customer_name: Optional[str] = None,
            customer_phone: Optional[str] = None, appointment_id: Optional[str] = None) -> str:
        """Execute the requested action."""
        try:
            if action == "check_availability":
                if not all([service_center_id, date, time, service_type]):
                    return json.dumps({
                        "error": "Missing required parameters for availability check: service_center_id, date, time, service_type"
                    })
                result = self._check_availability(service_center_id, date, time, service_type)
                
            elif action == "book_appointment":
                if not all([service_center_id, date, time, service_type, customer_name, customer_phone]):
                    return json.dumps({
                        "error": "Missing required parameters for booking: service_center_id, date, time, service_type, customer_name, customer_phone"
                    })
                result = self._book_appointment(service_center_id, date, time, service_type, customer_name, customer_phone)
                
            elif action == "get_service_centers":
                result = self._get_service_centers(service_center_id)
                
            elif action == "cancel_appointment":
                if not appointment_id:
                    return json.dumps({
                        "error": "Missing required parameter: appointment_id"
                    })
                result = self._cancel_appointment(appointment_id)
                
            elif action == "get_appointments":
                result = self._get_appointments(appointment_id, service_center_id)
                
            else:
                result = {
                    "error": f"Unknown action: {action}. Valid actions are: check_availability, book_appointment, get_service_centers, cancel_appointment, get_appointments"
                }
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            return json.dumps({
                "error": f"Unexpected error: {str(e)}"
            }, indent=2)