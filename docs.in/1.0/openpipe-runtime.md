
## Runtime Engine (openpipe)
Once you are familiar with the pipeline format as described on the previous sections, it is important to understand the purpose of the OPL runtime engine.

An OPL runtime engine is the software responsible for:

1. Loading, parsing and validating pipeline documents
1. Mapping action names to computer functions (code)
1. Validating action config versus the specific action requirements
1. Allocate instances for each action of the pipeline
1. Establishing the "connections" between steps
1. Delivering the system current time to the first action of the 'start' segment
1. Scheduling the action code execution when input data becomes available


