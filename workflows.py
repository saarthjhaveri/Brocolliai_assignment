from temporalio import workflow

from datetime import timedelta
from typing import Dict

with workflow.unsafe.imports_passed_through():
    from activities import classify_call, flag_call, tagging_classification, update_workflow_state

##todo take input as an object which has 2 things workflowid and transcript instead of just sending transcript as str



@workflow.defn
class CallProcessing:
    @workflow.run
    async def run(self, transcript: str) ->  Dict[str, str]:

        await workflow.execute_activity(
            update_workflow_state,
            # workflow_id
            "WORKFLOW_STARTED",
            start_to_close_timeout=timedelta(seconds=10)
        )

        #Classification [Emergency, Regular Job, Cancel Service, Note down msg, Other]
        classification = await workflow.execute_activity(
            classify_call,
            transcript,
            start_to_close_timeout=timedelta(seconds=10)
        )

        await workflow.execute_activity(
            update_workflow_state,
            # workflow_id,
            "CALL_CLASSIFICATION_COMPLETED",
            start_to_close_timeout=timedelta(seconds=10)
        )

        #Flag the call if necessary [Verbal loop, incomplete call, Hallucinate, Reading prompt, None]
        flagged = await workflow.execute_activity(
            flag_call,
            transcript,
            start_to_close_timeout=timedelta(seconds=10)
        )

         # Update state: CALL_FLAGGING_COMPLETED
        await workflow.execute_activity(
            update_workflow_state,
            # workflow_id,
            "CALL_FLAGGING_COMPLETED",
            start_to_close_timeout=timedelta(seconds=10)
        )


        #Tag the call for customers [Job booked, Spam, Estimate required, Empty call , Callback required]
        tag = await workflow.execute_activity(
            tagging_classification,
            transcript,
            start_to_close_timeout=timedelta(seconds=10)
        )

        await workflow.execute_activity(
            update_workflow_state,
            # workflow_id,
            "CALL_TAGGING_COMPLETED",
            start_to_close_timeout=timedelta(seconds=10)
        )

        # Return the final results
        return {
            "classification": classification,
            "flagged": flagged,
            "tag": tag
        }




