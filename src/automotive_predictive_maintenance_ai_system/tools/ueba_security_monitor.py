from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Dict, Any, List, Optional
import json
import time
from datetime import datetime, timedelta

class SecurityMonitorRequest(BaseModel):
    """Input schema for UEBA Security Monitor Tool."""
    action: str = Field(..., description="Action to perform: 'establish_baseline', 'detect_anomaly', 'log_event', 'get_threat_score', 'analyze_behavior', 'get_security_report'")
    agent_id: str = Field(..., description="Unique identifier for the agent being monitored")
    event_data: Optional[Dict[str, Any]] = Field(default=None, description="Event data for logging and analysis")
    time_window: Optional[int] = Field(default=24, description="Time window in hours for analysis")
    threshold: Optional[float] = Field(default=0.7, description="Anomaly detection threshold (0.0-1.0)")

class UEBASecurityMonitor(BaseTool):
    """User and Entity Behavior Analytics monitoring tool for CrewAI agents.
    
    This tool provides comprehensive security monitoring capabilities including:
    - Establishing baseline behaviors for agents
    - Detecting anomalous activities and behaviors
    - Security threat scoring and risk assessment
    - Event logging and analysis
    - Behavioral pattern analysis
    - Security reporting and alerts
    """

    name: str = "ueba_security_monitor"
    description: str = (
        "Monitor and analyze agent behavior for security threats. Establishes baselines, "
        "detects anomalies, scores threats, and maintains security event logs. "
        "Use this tool to ensure agent activities remain within expected security parameters."
    )
    args_schema: Type[BaseModel] = SecurityMonitorRequest
    
    # Pydantic v2 compatible field definitions with proper defaults
    agent_baselines: Dict[str, Any] = Field(default_factory=dict, description="Baseline behavior data for each agent")
    security_events: List[Dict[str, Any]] = Field(default_factory=list, description="Log of security events")
    threat_scores: Dict[str, float] = Field(default_factory=dict, description="Current threat scores for agents")
    behavioral_patterns: Dict[str, List[Dict[str, Any]]] = Field(default_factory=dict, description="Behavioral patterns for each agent")
    anomaly_thresholds: Dict[str, float] = Field(default_factory=dict, description="Anomaly detection thresholds per agent")
    last_analysis_time: Dict[str, datetime] = Field(default_factory=dict, description="Last analysis timestamp for each agent")
    security_alerts: List[Dict[str, Any]] = Field(default_factory=list, description="Active security alerts")
    risk_metrics: Dict[str, Dict[str, float]] = Field(default_factory=dict, description="Risk metrics for each agent")

    def model_post_init(self, __context: Any) -> None:
        """Initialize security monitoring data after Pydantic model creation."""
        # Initialize default security parameters
        self.default_metrics = {
            'activity_frequency': 0.0,
            'resource_access_pattern': 0.0,
            'communication_frequency': 0.0,
            'execution_time_variance': 0.0,
            'error_rate': 0.0,
            'permission_escalations': 0.0
        }
        
        # Initialize threat detection rules
        self.threat_rules = {
            'high_frequency_activity': {'threshold': 10.0, 'weight': 0.3},
            'unusual_resource_access': {'threshold': 0.8, 'weight': 0.4},
            'permission_escalation': {'threshold': 1.0, 'weight': 0.5},
            'abnormal_execution_time': {'threshold': 2.0, 'weight': 0.2},
            'elevated_error_rate': {'threshold': 0.15, 'weight': 0.3}
        }

    def _run(self, action: str, agent_id: str, event_data: Optional[Dict[str, Any]] = None, 
             time_window: int = 24, threshold: float = 0.7) -> str:
        """Execute UEBA security monitoring actions."""
        try:
            if action == "establish_baseline":
                return self._establish_baseline(agent_id, event_data or {})
            elif action == "detect_anomaly":
                return self._detect_anomaly(agent_id, event_data or {}, threshold)
            elif action == "log_event":
                return self._log_security_event(agent_id, event_data or {})
            elif action == "get_threat_score":
                return self._get_threat_score(agent_id)
            elif action == "analyze_behavior":
                return self._analyze_behavior(agent_id, time_window)
            elif action == "get_security_report":
                return self._generate_security_report(agent_id, time_window)
            else:
                return f"Error: Unknown action '{action}'. Available actions: establish_baseline, detect_anomaly, log_event, get_threat_score, analyze_behavior, get_security_report"
                
        except Exception as e:
            return f"Error in UEBA Security Monitor: {str(e)}"

    def _establish_baseline(self, agent_id: str, behavior_data: Dict[str, Any]) -> str:
        """Establish baseline behavior for an agent."""
        try:
            current_time = datetime.now()
            
            # Initialize baseline if not exists
            if agent_id not in self.agent_baselines:
                self.agent_baselines[agent_id] = {
                    'created_at': current_time.isoformat(),
                    'last_updated': current_time.isoformat(),
                    'metrics': self.default_metrics.copy(),
                    'sample_count': 0,
                    'behavior_profile': {}
                }
            
            baseline = self.agent_baselines[agent_id]
            
            # Update baseline with new behavior data
            for metric, value in behavior_data.items():
                if isinstance(value, (int, float)):
                    # Calculate running average
                    current_avg = baseline['metrics'].get(metric, 0.0)
                    sample_count = baseline['sample_count']
                    new_avg = (current_avg * sample_count + value) / (sample_count + 1)
                    baseline['metrics'][metric] = new_avg
                else:
                    baseline['behavior_profile'][metric] = value
            
            baseline['sample_count'] += 1
            baseline['last_updated'] = current_time.isoformat()
            
            # Set initial anomaly threshold
            self.anomaly_thresholds[agent_id] = 0.7
            self.threat_scores[agent_id] = 0.0
            
            return json.dumps({
                "status": "success",
                "message": f"Baseline established for agent {agent_id}",
                "baseline_metrics": baseline['metrics'],
                "sample_count": baseline['sample_count']
            })
            
        except Exception as e:
            return f"Error establishing baseline: {str(e)}"

    def _detect_anomaly(self, agent_id: str, current_behavior: Dict[str, Any], threshold: float) -> str:
        """Detect anomalies in agent behavior compared to baseline."""
        try:
            if agent_id not in self.agent_baselines:
                return json.dumps({
                    "status": "error",
                    "message": f"No baseline established for agent {agent_id}. Please establish baseline first."
                })
            
            baseline = self.agent_baselines[agent_id]
            anomalies = []
            total_anomaly_score = 0.0
            
            # Check each metric for anomalies
            for metric, current_value in current_behavior.items():
                if isinstance(current_value, (int, float)) and metric in baseline['metrics']:
                    baseline_value = baseline['metrics'][metric]
                    
                    if baseline_value > 0:
                        deviation = abs(current_value - baseline_value) / baseline_value
                        
                        if deviation > threshold:
                            anomaly = {
                                'metric': metric,
                                'baseline_value': baseline_value,
                                'current_value': current_value,
                                'deviation': deviation,
                                'severity': self._calculate_severity(deviation)
                            }
                            anomalies.append(anomaly)
                            total_anomaly_score += deviation
            
            # Update threat score
            if anomalies:
                new_threat_score = min(total_anomaly_score / len(anomalies), 1.0)
                self.threat_scores[agent_id] = max(self.threat_scores.get(agent_id, 0.0), new_threat_score)
                
                # Log security event for high anomaly scores
                if new_threat_score > 0.8:
                    self._log_security_event(agent_id, {
                        'event_type': 'high_anomaly_detected',
                        'threat_score': new_threat_score,
                        'anomalies': anomalies
                    })
            
            return json.dumps({
                "status": "success",
                "agent_id": agent_id,
                "anomalies_detected": len(anomalies),
                "anomalies": anomalies,
                "threat_score": self.threat_scores.get(agent_id, 0.0),
                "analysis_timestamp": datetime.now().isoformat()
            })
            
        except Exception as e:
            return f"Error detecting anomalies: {str(e)}"

    def _log_security_event(self, agent_id: str, event_data: Dict[str, Any]) -> str:
        """Log a security event for analysis."""
        try:
            security_event = {
                'agent_id': agent_id,
                'timestamp': datetime.now().isoformat(),
                'event_data': event_data,
                'threat_level': self._determine_threat_level(event_data),
                'requires_attention': False
            }
            
            # Determine if event requires immediate attention
            if security_event['threat_level'] in ['high', 'critical']:
                security_event['requires_attention'] = True
                
                # Add to security alerts
                alert = {
                    'alert_id': f"alert_{len(self.security_alerts) + 1}",
                    'agent_id': agent_id,
                    'timestamp': security_event['timestamp'],
                    'threat_level': security_event['threat_level'],
                    'description': event_data.get('event_type', 'Unknown security event'),
                    'status': 'active'
                }
                self.security_alerts.append(alert)
            
            self.security_events.append(security_event)
            
            # Update last analysis time
            self.last_analysis_time[agent_id] = datetime.now()
            
            return json.dumps({
                "status": "success",
                "message": "Security event logged",
                "event_id": len(self.security_events),
                "threat_level": security_event['threat_level'],
                "requires_attention": security_event['requires_attention']
            })
            
        except Exception as e:
            return f"Error logging security event: {str(e)}"

    def _get_threat_score(self, agent_id: str) -> str:
        """Get current threat score for an agent."""
        try:
            threat_score = self.threat_scores.get(agent_id, 0.0)
            risk_level = self._get_risk_level(threat_score)
            
            # Get recent security events
            recent_events = [
                event for event in self.security_events
                if event['agent_id'] == agent_id and 
                datetime.fromisoformat(event['timestamp']) > datetime.now() - timedelta(hours=24)
            ]
            
            return json.dumps({
                "status": "success",
                "agent_id": agent_id,
                "threat_score": threat_score,
                "risk_level": risk_level,
                "recent_events_count": len(recent_events),
                "last_analysis": self.last_analysis_time.get(agent_id, "Never").isoformat() if isinstance(self.last_analysis_time.get(agent_id), datetime) else "Never"
            })
            
        except Exception as e:
            return f"Error getting threat score: {str(e)}"

    def _analyze_behavior(self, agent_id: str, time_window: int) -> str:
        """Analyze agent behavior patterns over specified time window."""
        try:
            cutoff_time = datetime.now() - timedelta(hours=time_window)
            
            # Get events within time window
            relevant_events = [
                event for event in self.security_events
                if event['agent_id'] == agent_id and 
                datetime.fromisoformat(event['timestamp']) > cutoff_time
            ]
            
            # Analyze patterns
            analysis = {
                'agent_id': agent_id,
                'time_window_hours': time_window,
                'total_events': len(relevant_events),
                'threat_levels': {},
                'common_event_types': {},
                'behavior_trends': {},
                'recommendations': []
            }
            
            # Analyze threat levels
            for event in relevant_events:
                threat_level = event.get('threat_level', 'unknown')
                analysis['threat_levels'][threat_level] = analysis['threat_levels'].get(threat_level, 0) + 1
            
            # Analyze event types
            for event in relevant_events:
                event_type = event.get('event_data', {}).get('event_type', 'unknown')
                analysis['common_event_types'][event_type] = analysis['common_event_types'].get(event_type, 0) + 1
            
            # Generate recommendations
            if analysis['threat_levels'].get('high', 0) > 0:
                analysis['recommendations'].append("High threat events detected - review agent permissions and activities")
            
            if analysis['total_events'] > 50:
                analysis['recommendations'].append("High activity volume - consider adjusting monitoring sensitivity")
            
            if not analysis['recommendations']:
                analysis['recommendations'].append("Behavior appears normal within acceptable parameters")
            
            return json.dumps({
                "status": "success",
                "analysis": analysis,
                "analysis_timestamp": datetime.now().isoformat()
            })
            
        except Exception as e:
            return f"Error analyzing behavior: {str(e)}"

    def _generate_security_report(self, agent_id: str, time_window: int) -> str:
        """Generate comprehensive security report for an agent."""
        try:
            cutoff_time = datetime.now() - timedelta(hours=time_window)
            
            # Get agent data
            baseline = self.agent_baselines.get(agent_id, {})
            threat_score = self.threat_scores.get(agent_id, 0.0)
            
            # Get recent events and alerts
            recent_events = [
                event for event in self.security_events
                if event['agent_id'] == agent_id and 
                datetime.fromisoformat(event['timestamp']) > cutoff_time
            ]
            
            active_alerts = [
                alert for alert in self.security_alerts
                if alert['agent_id'] == agent_id and alert['status'] == 'active'
            ]
            
            report = {
                'agent_id': agent_id,
                'report_generated': datetime.now().isoformat(),
                'time_window_hours': time_window,
                'summary': {
                    'current_threat_score': threat_score,
                    'risk_level': self._get_risk_level(threat_score),
                    'total_events': len(recent_events),
                    'active_alerts': len(active_alerts),
                    'baseline_established': bool(baseline)
                },
                'threat_analysis': {
                    'high_risk_events': len([e for e in recent_events if e.get('threat_level') == 'high']),
                    'medium_risk_events': len([e for e in recent_events if e.get('threat_level') == 'medium']),
                    'low_risk_events': len([e for e in recent_events if e.get('threat_level') == 'low'])
                },
                'recommendations': self._generate_security_recommendations(agent_id, recent_events, threat_score),
                'alerts': active_alerts[:5]  # Show recent 5 alerts
            }
            
            return json.dumps({
                "status": "success",
                "security_report": report
            })
            
        except Exception as e:
            return f"Error generating security report: {str(e)}"

    def _calculate_severity(self, deviation: float) -> str:
        """Calculate severity level based on deviation."""
        if deviation > 2.0:
            return "critical"
        elif deviation > 1.5:
            return "high"
        elif deviation > 1.0:
            return "medium"
        else:
            return "low"

    def _determine_threat_level(self, event_data: Dict[str, Any]) -> str:
        """Determine threat level based on event data."""
        event_type = event_data.get('event_type', '')
        threat_score = event_data.get('threat_score', 0.0)
        
        if 'critical' in event_type.lower() or threat_score > 0.9:
            return 'critical'
        elif 'high' in event_type.lower() or threat_score > 0.7:
            return 'high'
        elif 'medium' in event_type.lower() or threat_score > 0.4:
            return 'medium'
        else:
            return 'low'

    def _get_risk_level(self, threat_score: float) -> str:
        """Get risk level based on threat score."""
        if threat_score >= 0.8:
            return "critical"
        elif threat_score >= 0.6:
            return "high"
        elif threat_score >= 0.3:
            return "medium"
        else:
            return "low"

    def _generate_security_recommendations(self, agent_id: str, recent_events: List[Dict], threat_score: float) -> List[str]:
        """Generate security recommendations based on analysis."""
        recommendations = []
        
        if threat_score > 0.7:
            recommendations.append("Consider implementing additional access controls for this agent")
            recommendations.append("Review and audit recent agent activities")
        
        high_risk_events = [e for e in recent_events if e.get('threat_level') == 'high']
        if len(high_risk_events) > 3:
            recommendations.append("Multiple high-risk events detected - investigate potential security breach")
        
        if len(recent_events) > 100:
            recommendations.append("Unusually high activity volume - review for potential automation or misuse")
        
        if not recommendations:
            recommendations.append("Security posture appears normal - continue regular monitoring")
        
        return recommendations