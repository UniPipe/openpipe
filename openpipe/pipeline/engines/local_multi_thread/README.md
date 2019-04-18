# Local Multi Threaded Workflow engine

This engine provides concurrent processing of pipelines, this is achieved by running each segment on it's own thread.

## Architecture

### Pipeline Manager

The pipeline manager is responsible for:

    needs_segment_manager = [start_segment]
    for segment_manager in needs_segment_manager
        segment_manager.start()
        input_link = segment_manager.control_out.read()
        needs_more = segment_manager.get()
        while needs_more:
            needs_segment_manager.append[needs_more]
            needs_more = segment_manager.get()



- For each segment in the pipeline:
    - Create a pipeline manager, providing him a "control_in" and "control_out" queue

load()
- For each segment manager:
    - Send to the "control_in" the segment content

start()
    - For each segment manager:
        Get status from "control_in"
    
- Add the (self, sm "start") o the needs_started list:
- Send "start", to the sm start

- while needs_started or needs_links:
    for request, link in needs_links:

    clear needs_started
    Send "Get Link" to the sm contol_in
    Read "Reply" from sm control_ouy
    if reply == ("Link", link object)
        if requester == self:
            break
        to the requester control in send:

    if reply == ("Requests Link", link name)
        needed_links.append(sm, sm link name)

- For each segment manager in the "links_needed" list:

    - Read messages from the control_out which may be:
        - "Get link", segment_name  - Add segment name to the "links_needed"
        - "Start completed", (number of actions)) - Remove from "links_needed"
        - "Start failed", reason    - Remove from "not stated"

- Validate for any cross-link requests (avoid dead lock)

- For each "Get link to segment name":
    - Send "Request link" to the control_in of the "names" segment manager:
    - Read the response from the control_out
    - Send the response to the "Get link to segment" manager


activate()
    - "
    - For each segment manager (not started):

#### Bootstraping segment managers

- For each segment found in the pipeline:
    - Create a segment manager instance

- For each segment manager:
    - Send the list of additional libraries to the segment manager instance [PM->SM]#a1

- For each segment manager:
    - Wait for the load result, interrupt if there was an error[SM->PM]#a2

- For each segment manager:
    - Send the list of actions to the segment manager instance[PM->SM]#a3

- For each segment manager:
    - Wait for the load result, interrupt if there was an error[SM->PM]#a4

- For each segment manager:
    - Send the "start" request[PM->SM]#a5

- For each segment manager:
    - Wait for the start result, interrupt if there was an error[SM->PM]#a6

- For each segment manager:
    - Read the list of resource offers ["segment", {'name': 'x'}, offer_queue] [SM->PM]#a7

- For each segment manager:
    - Send all the offers[PM->SM]#a8

- For each segment manager:
    - Wait for the run result, interrupt if there was an error

- For each segment manager:

#### Segment manager start
- Create a segment runner instance
- Wait for the list of additional libraries[PM->SM]#a1
- Send the list of additional libraries to the segment runner[SM->SR]#b1
- Wait for result[SR->SM]#b2
- send the result back[SM->PM#]#a2

- Wait for the list of actions[PM->SM]#a3
- Send the list of actions to the segment runner[SM->SR]#b3
- Wait for result[SR->SM]#b4
- send the result back[SM->PM]#a4

- Wait for the "start" request[PM->SM]#a5
- Send the "start" request to the segment runner[SM->SR]#b5
- Wait for the result[SR->SM]#b6
- Send the result back[SM->PM]#a6
- Send the list of offers[SM->PM]#a7
- Wait for the list of claims from the segment runner[SR->SM]#b7
- Wait for list of offers[PM->SM]#a8
- Match claims with offers






#### Activating the pipeline
- With the `start` segment manager:
    - Send a _"get link"_ instruction
    - Send the "activate" item to the received link
    - Send "None"" item to the received link
- For each segment manager:
    - Send the _"run"_ instruction «to get segments in the wait for input loop»
- For each segment manager:
    - Wait for run result, which may be "completed", "failed" or "aborted"


### Segment manager

The segment managers are responsible for:

#### Bootstraping segment runners
- Creating a segment runner instance
- Wait for the list of additional libraries
- Send the list of additional libraries to the segment runner
- Wait for the result and send it back, interrupt on failure
- Wait for the list of actions
- Send the list of actions to the segment runner
- Wait for the result and send it back, interrupt on failure
- Wait for the "start" request
- Run the `on_start()` method for all actions in the segment
- Wait for control requests:
    - "get link"
    - "run"

- Wait for control instructions from the pipeline manager:
    - "start:
        - Run the `on_start()` method for all actions in the segment
        - Waits for the result, wich may be _"started"_ or _"failed"_
        - Send the result back to the pipeline manager

# Segment Manager
The segment manager is responsible for creating the segment (threads), it will also create a control queue for each segment, this control queue will be used to managed the segment threads.

# Segment Manager Algorithm (Main Thread)
The segment manager `start()` method  will `start()` all segment threads.

For each segment thread it will get items from the control which may be:

- "link segment_name"
    - segment manager will create a queue
    - add it to the target segment input que list
    - send it to the control queue
- "started"
- "failed"

For each segment thread it will put in the control queue:
- "True": Segment thread should enter the wait for input loop
- "False": Segment thread should terminate (there was a start error)

If there was a start error, stop here.

For each segment, get the pipeline execution result (None or an error).


# Segment Thread Algorithm

Run the `on_start()` method, get boolean "should enter input loop ?" fromc ontrol queue, if False, exit.

If input queue lengh size is 0, report "No references" and exit.

Loop waiting for input:

- Loop:
    - If input queue list is empty, quit loop
    - Get an input_queue from input_queue_list (using round robin)
    - Get and item from input queue
    - If item is None remove queue from input queue list
- Run the `on_finish()`
- Put _None_ or _Error_ in the control queue


Send to controlo queue None or Error

