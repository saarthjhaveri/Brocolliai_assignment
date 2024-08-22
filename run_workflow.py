# @@@SNIPSTART python-project-template-run-workflow
import asyncio
import traceback

from temporalio.client import Client, WorkflowFailureError

from workflows import CallProcessing

async def main() -> None:
    # Create client connected to server at the given address
    client: Client = await Client.connect("localhost:7233")
    

    InputTranscript: str = '''Agent: Thanks for calling Armstrong Plumbing! This is Rey! How may I be of assistance?!
User: Hi. Um, I was just calling to see if I could maybe schedule an appointment with somebody to come out to our home and look at our, um, outdoor clean out.
Agent: Sure, I can help you schedule an appointment for that. Would you like to book a regular appointment during our service hours, or is this an emergency that needs immediate attention?
User: I think uh, regular service hours are fine.
Agent: Got it. I can help you with that. Could you please provide a bit more information about the issue with your outdoor clean out?
User: Sure. It's, um, basically, whenever we turn on water or anything drains from, um, you know, toilets, uh, shower, sinks, it's kind of overflowing into our yard now.
Agent: Oh no, that sounds like a real mess. Let's get this sorted out for you. Could you please provide your full name?
User: Yes. It's Alex Sandra Stavniew?
Agent: Thank you, Alex. Are you a new or existing customer with us?
User: New.
Agent: Great, welcome! Could you please provide your street name and city?
User: Yes. It's uh, 1328 Big Place in Davis, California.
Agent: Thank you. Just to confirm, that's 1-3-2-8 Big Place in Davis, California, right?
User: Yes.
Agent: Perfect. Could you also provide your zip code?
User: 95618.
Agent: Thanks! What's the best contact number to reach you at?
User: 360-561-2707.
Agent: Got it. And could you also share your email address?
User: It's, uh, rayoflightpnw@gmail.com.
Agent: Thank you. Is this a residential property?
User: Yes.
Agent: Are you the property owner?
User: Yes.
Agent: Great! Now, when would you prefer to schedule the appointment? We have slots available between 8 am and 12 pm or between 12 pm and 4 pm from Monday to Saturday.
User: It depends on the day of the week. So what's the first available, I guess?
Agent: The first available slot would be tomorrow, Monday, between 8 am and 12 pm. Does that work for you?
User: Yeah. That'll be fine.
Agent: Alright, I've scheduled you for the morning slot between 8 am and 12 pm tomorrow, Monday. Just to confirm, we're going to be visiting you at 1-3-2-8 Big Place in Davis, California, and we'll be giving you a call at 360-561-2707. Does that sound correct?
User: The phone number, sorry, uh, is 360-561-2707.
Agent: Got it, thank you for the correction. So, we'll be visiting you at 1-3-2-8 Big Place in Davis, California, and we'll be giving you a call at 360-561-2707. Does that sound correct?
User: Yes. That's yes.
Agent: Great! To send the technician out, we do have a small fee of only 85 dollars that gets waived if you choose to go ahead with the job. Does that sound good?
User: Okay.
Agent: Perfect! Is there anything else you'd like to share or any other questions you have?
User: No. That's it.
Agent: Thank you for calling Armstrong Plumbing. Hope you have a great day!'''

    workflow_id: str = 'abc123'

    try:
        result = await client.execute_workflow(
            CallProcessing.run,
            InputTranscript,
            id=workflow_id,
            task_queue='call_processing_queue',
        )

        print(f"Workflow result: {result}")

    except WorkflowFailureError:
        print("Got expected exception: ", traceback.format_exc())


if __name__ == "__main__":
    asyncio.run(main())
