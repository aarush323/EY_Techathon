
import sys
import os
from systemm.crew import AutomotivePredictiveMaintenanceAiSystemCrew
from datetime import datetime

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
        'vehicle_id': 'VH12345'
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
    with open(report_file, 'w') as f:
        json.dump({
            'report_text': report_text,
            'timestamp': datetime.now().isoformat()
        }, f)

    # Also print to terminal
    print(report_text)



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