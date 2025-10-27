# RDMA
- Hardware data path via async submission and completion queues. 
- Direct HW access via kernel bypass
- One-sided operations -> Remove Direct Memory Access (RDMA)

## Async Queues
- Submitting work requests to send and receive queues and collecting completions for completion queues.
- Parallel applications via per-CPU or per-thread queues. 

## Kernel Bypass
- Transport is offloaded from CPUs handling packetization, reliability and retransmission.

One sided operation -> One host moves data directly to or from memory of its communication peer without involving CPU. 
Assumption -> Memory is pre-registered.
Two-sided operation -> Receive work, Send work request. 
Can mix one-sided (RDMA) and two-sided (send/receive)

## Transports
Multiple implementations of RDMA. 
- Physical & link layers -> InfiniBand and Ethernet
| Protocol       | Transport                   | Typical Use         |
| -------------- | --------------------------- | ------------------- |
| **InfiniBand** | Dedicated InfiniBand fabric | HPC clusters        |
| **RoCE v1**    | Ethernet (same L2 subnet)   | Data centers        |
| **RoCE v2**    | UDP/IP (routable)           | Cloud & DC networks |
| **iWARP**      | TCP/IP                      | General Ethernet    |
