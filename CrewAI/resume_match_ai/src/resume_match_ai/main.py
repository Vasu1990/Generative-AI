#!/usr/bin/env python
import sys
import warnings
import os
from datetime import datetime

from resume_match_ai.crew import ResumeMatchAi

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the crew.
    """

    inputs = {
        "resume": "<your-resume-url-file.pdf>",
        "current_date": str(datetime.now())
    }

    try:
        ResumeMatchAi().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """

    inputs = {
        'resume': "<your-resume-url-file.pdf>"
    }

    try:
        ResumeMatchAi().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
