# ResumeMatchAi Crew

Welcome to the ResumeMatchAi Crew, a multi-agent AI system powered by [crewAI](https://crewai.com). This project is designed to help you analyze your resume, find relevant job opportunities, and get advice on how to improve your resume.

## Project Overview

The ResumeMatchAi Crew automates the process of job hunting by:

1.  **Analyzing your resume:** It extracts key information like your skills, experience, and education.
2.  **Scraping for jobs:** It searches for job listings that match your profile.
3.  **Providing advice:** It gives you suggestions on how to improve your resume to better match the job market.

## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management.

First, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

```bash
uv pip install -r requirements.txt
```

### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/resume_match_ai/config/agents.yaml` to define your agents.
- Modify `src/resume_match_ai/config/tasks.yaml` to define your tasks.
- Modify `src/resume_match_ai/crew.py` to add your own logic, tools, and specific args.
- Modify `src/resume_match_ai/main.py` to add custom inputs for your agents and tasks.

## Running the Project

To run the project, you first need to add your resume to the `src/resume_match_ai/tools` directory. Then, update the `src/resume_match_ai/main.py` file to point to your resume file.

```python
def run():
    """
    Run the crew.
    """

    inputs = {
        "resume": "src/resume_match_ai/tools/your-resume-file.pdf", # Replace with your resume file
        "current_date": str(datetime.now())
    }

    try:
        ResumeMatchAi().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
```

To kickstart your crew of AI agents, run this from the root folder of your project:

```bash
crewai run
```

This command initializes the ResumeMatchAi Crew, which will then generate the following reports in the `output` directory:
- `analyst_report.md`: A detailed analysis of your resume.
- `job_scraping_report.md`: A list of job opportunities that match your profile.
- `resume_advising_report.md`: Actionable advice on how to improve your resume.

## Understanding Your Crew

The ResumeMatchAi Crew is composed of three AI agents:

-   **Resume Analyst:** This agent parses and analyzes your resume to extract key information such as skills, experience, and education.
-   **Job Scout:** This agent identifies and collects relevant job listings that align with your resume profile and career interests.
-   **Resume Improvement Coach:** This agent provides targeted suggestions to improve your resume based on job market expectations.

These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, to provide a comprehensive analysis of your resume and the job market.

## Support

For support, questions, or feedback regarding the ResumeMatchAi Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.
