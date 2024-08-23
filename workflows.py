from temporalio import workflow

from datetime import timedelta
from typing import Dict

with workflow.unsafe.imports_passed_through():
    from activities import classify_call, flag_call, tagging_classification, update_workflow_state

##todo take input as an object which has 2 things workflowid and transcript instead of just sending transcript as str

from shared import TranscriptData

@workflow.defn
class CallProcessing:
    @workflow.run
    async def run(self, transcript_data: TranscriptData) ->  Dict[str, str]:

        params = ("WORKFLOW_STARTED", transcript_data.workflow_id)

        await workflow.execute_activity(
            update_workflow_state,
            params,
            start_to_close_timeout=timedelta(seconds=10)
        )

        #Classification [Emergency, Regular Job, Cancel Service, Note down msg, Other]
        classification = await workflow.execute_activity(
            classify_call,
            transcript_data.transcript,
            start_to_close_timeout=timedelta(seconds=10)
        )

        params = ("CALL_CLASSIFICATION_COMPLETED", transcript_data.workflow_id)

        await workflow.execute_activity(
            update_workflow_state,
            params,
            start_to_close_timeout=timedelta(seconds=10)
        )

        #Flag the call if necessary [Verbal loop, incomplete call, Hallucinate, Reading prompt, None]
        flagged = await workflow.execute_activity(
            flag_call,
            transcript_data.transcript,
            start_to_close_timeout=timedelta(seconds=10)
        )

        params= ("CALL_FLAGGING_COMPLETED", transcript_data.workflow_id)


         # Update state: CALL_FLAGGING_COMPLETED
        await workflow.execute_activity(
            update_workflow_state,
            params,
            start_to_close_timeout=timedelta(seconds=10)
        )


        #Tag the call for customers [Job booked, Spam, Estimate required, Empty call , Callback required]
        tag = await workflow.execute_activity(
            tagging_classification,
            transcript_data.transcript,
            start_to_close_timeout=timedelta(seconds=10)
        )

        params= ("CALL_TAGGING_COMPLETED", transcript_data.workflow_id)


        await workflow.execute_activity(
            update_workflow_state,
            params,
            start_to_close_timeout=timedelta(seconds=10)
        )

        # Return the final results
        return {
            "classification": classification,
            "flagged": flagged,
            "tag": tag
        }




