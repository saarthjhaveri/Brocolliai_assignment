from temporalio import activity
import asyncio
from supabase import create_client
# import newrelic.agent 

# Initialize the New Relic agent using the config file you generated using your license key
# newrelic.agent.initialize('newrelic.ini')

from openai_api_functions.call_classification import classify_call_via_openai
from openai_api_functions.call_tagging import tag_call_via_openai
from openai_api_functions.call_flagging import flag_call_via_openai
from shared import TranscriptData
from secret_key import supabase_api_key, supabase_url

supabase = create_client(supabase_url, supabase_api_key)

from shared import TranscriptData


@activity.defn
async def classify_call(transcript: str) -> str:
    return await asyncio.to_thread(classify_call_via_openai,transcript)

@activity.defn
async def flag_call(transcript: str) -> str:
    return await  asyncio.to_thread(flag_call_via_openai,transcript)

@activity.defn
async def tagging_classification(transcript:str) -> str:
    return await asyncio.to_thread(tag_call_via_openai,transcript)
    ## todo : make use of classification and flagged value also to appropriately tag the call


##Update the supabase table with each state
@activity.defn
async def update_workflow_state(params) -> None:
    state,workflow_id = params
    # Insert the workflow state into Supabase
    supabase.table("call_processing_statetable").insert({
        "workflow_id": workflow_id,
        "state": state,
    }).execute()

