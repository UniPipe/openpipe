# Local Multi Threaded Workflow engine

This engine provides concurrent processing of pipelines, this is achieved by running each segment on it's own thread.

## Pipeline Manager

The pipeline manager is responsible for the functions described in the next sections.

### Segment Controllers Creation

The engine client document loader invokes `create_segment(...)` for each segment found in the pipeline. This method will create a `SegmentController` thread, which is only started if `start_controller(...)` is called later.

The created controller is returned to the document loader, its `add_action(...)` method will be called later, for each action set in the segment sequence.

#### Pipeline Start

When the engine client invokes `start(...)` to start the pipeline, this method  invokes the `start_controller(...)` with the _start_ segment controller.

Put a _"provide input"_ to the _start_ segment controller `from_manager` queue.
Fetch the input link item from the request reply queue, store it as `start_input_link` .

##### Segment Controller Start

The `start_controller(...)` method starts the specified controller thread.

Loop fetching items from the controller's `to_manager` queue:

- If a _"request input"_ request is received:
    - If the controller for the requested segment name was not started, start it by calling `start_controller(...)`
    - put a _"provide input"_ to the requested segment controller `from_manager` queue.
- Until a _"started"_ or _"failed"_ is received

Fetch the "activation_item" from the `from_manager` queue

#### Pipeline Activation

When the engine client invokes `activate(...)`.

Loop the started controllers list:
- Put _"activate"_ into the controller's `from_manager` queue

Put the activation item into the `start_input_link` queue.
Put `None` into the `start_input_link` queue.

Loop the started controllers list:
- Fetch termination item (must be _"terminated"_) from the controller's `to_manager` queue

## Segment Controller

The segment controller is responsible for the functions described in the next sections.

### Segment Runner Creation

When a segment controller is started it creates a `SegmentRunner` thread, it invokes the _runner's_ `add_action(...)` for each action container in the _controller's_ action list. It starts the `runner` thread.

Looping fetching items from the runners's `to_controller` queue:

- Send it to the `to_manager` queue
- Until a _"started"_ or _"failed"_ is received

Loop fetching items from the `from_manager` queue:

- if a _"provide input"_ is received:
    - increase _input_link_count_
    - put the input link to the _provide_ reply queue
- until an _"activate"_ is received

Looping fetching items from the runners's `to_controller` queue:

- if a `None` is received:
    - decrease _input_link_count_
    - if _input_link_count_ is zero:
        - put `False` to the runners's `from_controller` queue
    - else:
        - put `True` to the runners's `from_controller` queue
- until _input_link_count_ is zero

- put _"terminated"_ into the `to_manager` queue

## Segment Runner

When a segment runner is started.

Loop the runner actions list:
- Call the action `on_start(...)`
- If it fails, abort loop and put "failed" into the `to_controller` queue

Put _"started"_ into the `to_controller` queue

Loop fetching items from the `input_queue`:
- If item is `None`:
    - Put `None` into `to_controller` queue
    - Fetch item from the `from_controller` queue
        - If is `False` break loop
        - If is `True` continue loop
- Call first's action `_on_input_` method
