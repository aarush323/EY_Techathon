from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Dict, Any, List, Optional
from datetime import datetime
import json

class CustomerNotificationRequest(BaseModel):
    """Input schema for Customer Notification API Tool."""
    action: str = Field(..., description="Action to perform: send_notification, get_customer_preferences, update_notification_status")
    customer_id: Optional[str] = Field(None, description="Customer ID (VEH001-VEH010)")
    notification_type: Optional[str] = Field(None, description="Type of notification: email, sms, app_push")
    message: Optional[str] = Field(None, description="Notification message content")
    subject: Optional[str] = Field(None, description="Subject for email notifications")
    notification_id: Optional[str] = Field(None, description="Notification ID for status updates")
    status: Optional[str] = Field(None, description="New status for notification: pending, sent, delivered, failed")

class CustomerNotificationAPI(BaseTool):
    """Tool for managing customer notifications via multiple channels."""

    name: str = "Customer Notification API"
    description: str = (
        "Manages customer notifications through email, SMS, and app push channels. "
        "Handles customer preferences, notification tracking, and status updates for customers VEH001-VEH010."
    )
    args_schema: Type[BaseModel] = CustomerNotificationRequest
    
    # Proper Pydantic v2 field definition
    customer_db: Dict[str, Dict[str, Any]] = Field(default_factory=dict, description="Customer database with profiles and preferences")
    notification_history: List[Dict[str, Any]] = Field(default_factory=list, description="History of all notifications sent")

    def model_post_init(self, __context: Any) -> None:
        """Initialize the customer database after object creation."""
        super().model_post_init(__context)
        self._initialize_customer_database()

    def _initialize_customer_database(self):
        """Initialize the customer database with 10 customers (VEH001-VEH010)."""
        customers = [
            {
                "id": "VEH001",
                "name": "John Smith",
                "email": "john.smith@email.com",
                "phone": "+1234567890",
                "preferences": {
                    "email": True,
                    "sms": True,
                    "app_push": True,
                    "preferred_time": "09:00-17:00",
                    "language": "en"
                },
                "notification_history": []
            },
            {
                "id": "VEH002",
                "name": "Sarah Johnson",
                "email": "sarah.johnson@email.com",
                "phone": "+1234567891",
                "preferences": {
                    "email": True,
                    "sms": False,
                    "app_push": True,
                    "preferred_time": "10:00-18:00",
                    "language": "en"
                },
                "notification_history": []
            },
            {
                "id": "VEH003",
                "name": "Mike Davis",
                "email": "mike.davis@email.com",
                "phone": "+1234567892",
                "preferences": {
                    "email": False,
                    "sms": True,
                    "app_push": True,
                    "preferred_time": "08:00-16:00",
                    "language": "en"
                },
                "notification_history": []
            },
            {
                "id": "VEH004",
                "name": "Emily Wilson",
                "email": "emily.wilson@email.com",
                "phone": "+1234567893",
                "preferences": {
                    "email": True,
                    "sms": True,
                    "app_push": False,
                    "preferred_time": "11:00-19:00",
                    "language": "es"
                },
                "notification_history": []
            },
            {
                "id": "VEH005",
                "name": "Robert Brown",
                "email": "robert.brown@email.com",
                "phone": "+1234567894",
                "preferences": {
                    "email": True,
                    "sms": True,
                    "app_push": True,
                    "preferred_time": "07:00-15:00",
                    "language": "en"
                },
                "notification_history": []
            },
            {
                "id": "VEH006",
                "name": "Lisa Garcia",
                "email": "lisa.garcia@email.com",
                "phone": "+1234567895",
                "preferences": {
                    "email": True,
                    "sms": False,
                    "app_push": True,
                    "preferred_time": "12:00-20:00",
                    "language": "es"
                },
                "notification_history": []
            },
            {
                "id": "VEH007",
                "name": "David Miller",
                "email": "david.miller@email.com",
                "phone": "+1234567896",
                "preferences": {
                    "email": False,
                    "sms": True,
                    "app_push": True,
                    "preferred_time": "06:00-14:00",
                    "language": "en"
                },
                "notification_history": []
            },
            {
                "id": "VEH008",
                "name": "Jennifer Taylor",
                "email": "jennifer.taylor@email.com",
                "phone": "+1234567897",
                "preferences": {
                    "email": True,
                    "sms": True,
                    "app_push": True,
                    "preferred_time": "13:00-21:00",
                    "language": "fr"
                },
                "notification_history": []
            },
            {
                "id": "VEH009",
                "name": "Christopher Anderson",
                "email": "chris.anderson@email.com",
                "phone": "+1234567898",
                "preferences": {
                    "email": True,
                    "sms": False,
                    "app_push": False,
                    "preferred_time": "09:00-17:00",
                    "language": "en"
                },
                "notification_history": []
            },
            {
                "id": "VEH010",
                "name": "Amanda White",
                "email": "amanda.white@email.com",
                "phone": "+1234567899",
                "preferences": {
                    "email": True,
                    "sms": True,
                    "app_push": True,
                    "preferred_time": "14:00-22:00",
                    "language": "de"
                },
                "notification_history": []
            }
        ]
        
        # Populate the customer database
        self.customer_db = {customer["id"]: customer for customer in customers}

    def _send_notification(self, customer_id: str, notification_type: str, message: str, subject: str = None) -> Dict[str, Any]:
        """Send a notification to a specific customer."""
        try:
            if customer_id not in self.customer_db:
                return {
                    "success": False,
                    "error": f"Customer {customer_id} not found",
                    "notification_id": None
                }

            customer = self.customer_db[customer_id]
            preferences = customer["preferences"]

            # Check if customer has enabled this notification type
            if not preferences.get(notification_type, False):
                return {
                    "success": False,
                    "error": f"Customer {customer_id} has disabled {notification_type} notifications",
                    "notification_id": None
                }

            # Generate notification ID
            notification_id = f"NOTIF_{customer_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # Create notification record
            notification = {
                "notification_id": notification_id,
                "customer_id": customer_id,
                "type": notification_type,
                "message": message,
                "subject": subject if notification_type == "email" else None,
                "status": "sent",
                "timestamp": datetime.now().isoformat(),
                "recipient": {
                    "email": customer["email"] if notification_type == "email" else None,
                    "phone": customer["phone"] if notification_type == "sms" else None,
                    "device": "app" if notification_type == "app_push" else None
                }
            }

            # Add to notification history
            self.notification_history.append(notification)
            self.customer_db[customer_id]["notification_history"].append(notification)

            return {
                "success": True,
                "notification_id": notification_id,
                "customer_id": customer_id,
                "type": notification_type,
                "status": "sent",
                "timestamp": notification["timestamp"],
                "message": "Notification sent successfully"
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to send notification: {str(e)}",
                "notification_id": None
            }

    def _get_customer_preferences(self, customer_id: str) -> Dict[str, Any]:
        """Get customer notification preferences."""
        try:
            if customer_id not in self.customer_db:
                return {
                    "success": False,
                    "error": f"Customer {customer_id} not found"
                }

            customer = self.customer_db[customer_id]
            return {
                "success": True,
                "customer_id": customer_id,
                "customer_name": customer["name"],
                "contact_info": {
                    "email": customer["email"],
                    "phone": customer["phone"]
                },
                "preferences": customer["preferences"],
                "total_notifications": len(customer["notification_history"])
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get customer preferences: {str(e)}"
            }

    def _update_notification_status(self, notification_id: str, status: str) -> Dict[str, Any]:
        """Update the status of a notification."""
        try:
            valid_statuses = ["pending", "sent", "delivered", "failed", "read"]
            if status not in valid_statuses:
                return {
                    "success": False,
                    "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                }

            # Find notification in history
            notification_found = False
            for notification in self.notification_history:
                if notification["notification_id"] == notification_id:
                    old_status = notification["status"]
                    notification["status"] = status
                    notification["status_updated"] = datetime.now().isoformat()
                    notification_found = True

                    # Also update in customer's history
                    customer_id = notification["customer_id"]
                    if customer_id in self.customer_db:
                        for customer_notif in self.customer_db[customer_id]["notification_history"]:
                            if customer_notif["notification_id"] == notification_id:
                                customer_notif["status"] = status
                                customer_notif["status_updated"] = notification["status_updated"]
                                break

                    return {
                        "success": True,
                        "notification_id": notification_id,
                        "old_status": old_status,
                        "new_status": status,
                        "updated_at": notification["status_updated"],
                        "message": "Notification status updated successfully"
                    }

            if not notification_found:
                return {
                    "success": False,
                    "error": f"Notification {notification_id} not found"
                }

        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to update notification status: {str(e)}"
            }

    def _run(self, action: str, customer_id: str = None, notification_type: str = None, 
            message: str = None, subject: str = None, notification_id: str = None, 
            status: str = None) -> str:
        """Execute the requested action."""
        try:
            if action == "send_notification":
                if not all([customer_id, notification_type, message]):
                    return json.dumps({
                        "success": False,
                        "error": "Missing required parameters: customer_id, notification_type, and message are required"
                    })

                if notification_type not in ["email", "sms", "app_push"]:
                    return json.dumps({
                        "success": False,
                        "error": "Invalid notification_type. Must be: email, sms, or app_push"
                    })

                result = self._send_notification(customer_id, notification_type, message, subject)
                return json.dumps(result, indent=2)

            elif action == "get_customer_preferences":
                if not customer_id:
                    return json.dumps({
                        "success": False,
                        "error": "Missing required parameter: customer_id"
                    })

                result = self._get_customer_preferences(customer_id)
                return json.dumps(result, indent=2)

            elif action == "update_notification_status":
                if not all([notification_id, status]):
                    return json.dumps({
                        "success": False,
                        "error": "Missing required parameters: notification_id and status are required"
                    })

                result = self._update_notification_status(notification_id, status)
                return json.dumps(result, indent=2)

            else:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid action: {action}. Valid actions: send_notification, get_customer_preferences, update_notification_status"
                })

        except Exception as e:
            return json.dumps({
                "success": False,
                "error": f"Tool execution failed: {str(e)}"
            })