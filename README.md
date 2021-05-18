# ConnectorTest

ss-test contains the new simulator.

Next step is to decouple the simulator into the components (Sender, Receiver, Simulator, Connector)

### Update - 180521
- Decoupled system created
-   Sender is setup to be node
-   Receiver is setup to be matcher
-   SignalSlot used to mimic connections between node and matcher
- Connector file is inactive for now. it will be used for real network tests.
