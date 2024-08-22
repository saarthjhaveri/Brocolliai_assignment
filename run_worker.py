import asyncio

from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker

from activities import classify_call, flag_call, tagging_classification, update_workflow_state
from workflows import CallProcessing


async def main():
    client = await Client.connect("localhost:7233", namespace="default")
    # Run the worker
    worker = Worker(
        client, task_queue="call_processing_queue", workflows=[CallProcessing], activities=[classify_call, flag_call, tagging_classification, update_workflow_state]
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())