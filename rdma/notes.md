# RDMA
- Hardware data path via async submission and completion queues. 
- Direct HW access via kernel bypass
- One-sided operations -> Remove Direct Memory Access (RDMA)

## RDMA Design Goals
- Decouple the network from software
- These are overhead
- - Software assisted packet ordering, retransmission
- - Software assisted message framing
- - Software assisted virtualization of the network card
- - Software assisted memory management and buffer copies

### How overheads are solved
- Every connection must only use one path through network.
- If a packet is ever lost the network will treat it as a connection fatal error.
- Basic message frame.
- User space polling loops (no interrupts)
- Batching (multiple Work Requests, one write)
- Coalescing (do more per notification)
- Hardware assisted virtualization (per-connection memory mapping)

### Zero Copy Networking
- I want to request that data into this buffer. (memory copy across network)
- Remotly identify a a resource such that network card can read or write data.


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
RoCE -> RDMA over Converged Ethernet
Provide IB API on top of Ethernet network. Lossless Ethernet via ECN - Congestion Notification
Pause - Flow Control
Xon,Xoff - Flow control signals
RoCE 1 uses raw Ethernet frames
RoCE2 uses Ethernet frames carrying IP packets

Multiple implementations of RDMA. 
- Physical & link layers -> InfiniBand and Ethernet
| Protocol       | Transport                   | Typical Use         |
| -------------- | --------------------------- | ------------------- |
| **InfiniBand** | Dedicated InfiniBand fabric | HPC clusters        |
| **RoCE v1**    | Ethernet (same L2 subnet)   | Data centers        |
| **RoCE v2**    | UDP/IP (routable)           | Cloud & DC networks |
| **iWARP**      | TCP/IP                      | General Ethernet    |

## RDMA Programming
RDMA apps are developed using libibverbs and librdmacm.
https://github.com/linux-rdma/rdma-core
- librdmacm provides connection establishment with IP addressing
- libibverbs provides an API for other control and data path operations

ibv_pd -> Protection Domain - high level container for other objects.
ibv_qp_ex -> Queue Pair - queue for posting receive work requests and queue for posting send work requests.
ibv_cq_ex -> Completion queue - queue that recevies completion notifications for receive and send work requests. Attached to one or more work queues.
ibv_mr -> Memory region - memory buffer that is targeted by work requests.

## Learning RDMA Examples in Repo

1. ibv_rc_pingpong (understand verbs fundamentals)
2. ibv_asyncwatch (learn about async events)
3. ibv_ud_pingpong (learn datagram mode)
4. ibv_uc_pingpong ()
4. rdma_server/rdma_client (learn connection management)
5. rping (learn production patterns)
6. ibv_devices (list available RDMA devices)
7. ibv_devinfo (query device capabilities)
8. mckey (learn about multicast operations)


### Blog Post Read
- https://davekilian.com/rdma-design.html?utm_source=chatgpt.com

### Blog posts to Read
- https://blog.enfabrica.net/software-defined-rdma-networks-for-large-scale-ai-infrastructure-7ad0fe6d3910
- https://linbit.com/blog/rdma-what-it-means-for-data-transfer-replication/?utm_source=chatgpt.com