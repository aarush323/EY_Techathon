#!/usr/bin/env python
import sys
import os
from systemm.crew import AutomotivePredictiveMaintenanceAiSystemCrew
from datetime import datetime

import json
import os
from datetime import datetime

def format_json_as_report(json_text):
    """Convert JSON output to a readable Markdown report format"""
    try:
        # Try to parse the JSON
        if isinstance(json_text, str):
            data = json.loads(json_text)
        else:
            data = json_text
            
        report_lines = []
        
        def format_section(title, content, level=2):
            """Format a section with proper indentation"""
            # Markdown headers
            header_prefix = "#" * level
            report_lines.append(f"{header_prefix} {title.upper()}")
            report_lines.append("")
            
            if isinstance(content, dict):
                for key, value in content.items():
                    if isinstance(value, (dict, list)):
                        format_section(key.replace("_", " ").title(), value, level + 1)
                    else:
                        report_lines.append(f"- **{key.replace('_', ' ').title()}**: {value}")
                report_lines.append("")
            elif isinstance(content, list):
                for i, item in enumerate(content, 1):
                    if isinstance(item, dict):
                        report_lines.append(f"**{i}. Item {i}:**")
                        for sub_key, sub_value in item.items():
                            report_lines.append(f"  - **{sub_key.replace('_', ' ').title()}**: {sub_value}")
                    else:
                        report_lines.append(f"{i}. {item}")
                report_lines.append("")
            else:
                report_lines.append(f"{content}")
                report_lines.append("")
        
        # Format the main report
        if isinstance(data, dict):
            for key, value in data.items():
                format_section(key.replace("_", " ").title(), value)
        else:
            report_lines.append(str(data))
            
        return "\n".join(report_lines)
        
    except Exception as e:
        # If JSON parsing fails, return formatted text
        return f"Report Content:\n{json_text}"

# Set Perplexity API key if not already set
if not os.getenv("PERPLEXITY_API_KEY"):
    os.environ["PERPLEXITY_API_KEY"] = "key"

# This main file is intended to run your crew locally
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew safely and generate a JSON report for the frontend.
    """
    inputs = {
        'oem_name': 'Sample OEM',
        'customer_name': 'John Doe',
        'vehicle_id': 'VH12345',
        'vehicle_count': '10'
    }

    result = AutomotivePredictiveMaintenanceAiSystemCrew().crew().kickoff(inputs=inputs)

    # Safely get full_report if it exists, else fallback to string representation
    report_text = getattr(result, 'full_report', None)
    if not report_text:
        # If full_report is missing, try to convert result to dict and format nicely
        try:
            report_text = json.dumps(result.dict(), indent=2)
        except Exception:
            report_text = str(result)

    # Save to JSON for Flask
    import json, os
    report_file = os.path.join(os.path.dirname(__file__), 'crew_report.json')
    formatted_report = format_json_as_report(report_text)
    
    # New schema as requested
    output_data = {
        "title": "Automotive Maintenance Report",
        "format": "markdown",
        "content": formatted_report,
        "timestamp": datetime.now().isoformat(),
        "raw_json": report_text
    }
    
    with open(report_file, 'w') as f:
        json.dump(output_data, f, indent=2)

    # Format and print as readable report
    print("=== AUTOMOTIVE PREDICTIVE MAINTENANCE REPORT ===")
    print(formatted_report)



def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'oem_name': 'sample_value'
    }
    try:
        AutomotivePredictiveMaintenanceAiSystemCrew().crew().train(
            n_iterations=int(sys.argv[2]),
            filename=sys.argv[3],
            inputs=inputs
        )
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        AutomotivePredictiveMaintenanceAiSystemCrew().crew().replay(task_id=sys.argv[2])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'oem_name': 'sample_value'
    }
    try:
        AutomotivePredictiveMaintenanceAiSystemCrew().crew().test(
            n_iterations=int(sys.argv[2]),
            inputs=inputs
        )
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: main.py <command> [<args>]")
        sys.exit(1)

    command = sys.argv[1]
    if command == "run":
        run()
    elif command == "train":
        train()
    elif command == "replay":
        replay()
    elif command == "test":
        test()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
