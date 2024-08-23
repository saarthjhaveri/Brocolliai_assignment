# Brocolliai_assignment
This project involves the workflow process for a call classification using Temporal, Openai, supabase for the following problem statement :
https://docs.google.com/document/d/17F18hjPfEt7KiSwzIiUfiM3F_VLPl65yH5niNZTZ3lc/edit

#Setup 
1) Start the temporal server using - $temporal server start-dev
   
2) To start the Worker, run this command from the project root: $python run_worker.py

  Note - You won't see any output right away, but leave the program running.

3) To start the Workflow, open a new terminal window and switch to your project root: Then run run_workflow.py from the project root to start the Workflow Execution:
   $python run_workflow.py



#TODO 
Need to make dataclasses instead of using datatypes as input to workflows.
Need to make alert trigerring functionality for flagging.
Add loggers for easy execution understanding. 
The openai function calling needs to be improved by providing better prompts to get the expected classification results. 
