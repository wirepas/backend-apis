# API between a Gateway and Wirepas Backends

<!--- Version: v1.1A
API Version {#api-version .ListParagraph}
===========

+-----------------------+-----------------------+-----------------------+
| **Version**           | **WP-RM-128 version** | **Description**       |
+=======================+=======================+=======================+
| **1**                 | This document (v1.1A) | Changes:              |
|                       |                       |                       |
|                       |                       | -   *is\_fast\_transm |
|                       |                       | ission*               |
|                       |                       |     field from        |
|                       |                       |     [SendPacketReq](# |
|                       |                       | protocol-buffers-form |
|                       |                       | at-3)                 |
|                       |                       |     structure is      |
|                       |                       |     renamed           |
|                       |                       |     *is\_unack\_csma\ |
|                       |                       | _ca*                  |
|                       |                       |     to reflect        |
|                       |                       |     official feature  |
|                       |                       |     name.             |
|                       |                       |                       |
|                       |                       | -   New [gateway info |
|                       |                       |     services](#get-ga |
|                       |                       | teway-info)           |
|                       |                       |     added in API.     |
+-----------------------+-----------------------+-----------------------+
| **0**                 | v1.0A                 | Initial released      |
|                       |                       | version               |
+-----------------------+-----------------------+-----------------------+
--->

<!-- MarkdownTOC levels="1,2,3" autolink="true"  -->

- [Introduction](#introduction)
- [Overview of gateway features](#overview-of-gateway-features)
- [Unique identifier](#unique-identifier)
    - [Gateway and sinks](#gateway-and-sinks)
    - [Request unique identifier](#request-unique-identifier)
- [API description](#api-description)
    - [Gateway status module](#gateway-status-module)
    - [Config module](#config-module)
    - [Data module](#data-module)
    - [OTAP module](#otap-module)
- [API extension](#api-extension)
- [Implementation and workflow example for backends](#implementation-and-workflow-example-for-backends)
    - [General remarks](#general-remarks)
    - [Backend for network configuration](#backend-for-network-configuration)
    - [Backend for data exchanges](#backend-for-data-exchanges)
- [List of all MQTT topics](#list-of-all-mqtt-topics)

<!-- /MarkdownTOC -->

## Introduction

A Wirepas network contains nodes (router nodes and non-routers nodes)
and one or more gateways that can have multiple sinks attached.

The gateway's objective is to transfer data between Wirepas network and
backends (servers) upstream and downstream. A network can be connected through
its gateways to multiple backends.

Wirepas has developed its own backends and especially the Wirepas
Network Tool (WNT) to monitor the network behavior. To send data from a
gateway to a Wirepas Backends, the gateway must be compliant with the
API described in this document and from now on known as backend to gateway API.

The backend to gateway API is based on a set of MQTT topics where messages are encoded as [Protocol Buffers (syntax 2)][protobuf_homepage]. All the messages in the MQTT topics have the same
[root message][message_GenericMessage].

The following diagram describes the topology of a full Wirepas solution
network. There are several gateways with multiple sinks and multiple
backends running in parallel.

![](./media/image2.png)


## Overview of gateway features

A gateway is an interface between a Wirepas Mesh network and cloud services.
The gateway exposes local capabilities that allow the cloud services to
configure and operate a Wirepas Mesh network.

The gateway services are classified in the following groups:

-   **Gateway status**: Services for monitoring the gateway itself and mainly the status of the connection with the MQTT broker;
-   **Config**: Services to configure the local sinks attached to the gateway;
-   **Data**: Services to send and receive data to/from a Wirepas network;
-   **OTAP**: Services to manage the local OTAP operation.

## Unique identifier

As a Wirepas system solution can contain multiple gateways (with
multiple sinks) connected to multiple backends as described in the
introduction each element must have its unique identifier.

### Gateway and sinks

A gateway must generate a unique id that remains the same all along the
product life. This id must be encodable in ASCII as it is used inside
MQTT topics. This id is referred as *\<gw-id>* in this document.

The uniqueness must be ensured between all gateways registered to the
**same MQTT broker**. A good id could be made with the gateway model as a
prefix followed by a generated random suffix with enough values to
ensure its uniqueness.

As a gateway can have multiple sinks attached, it is the gateway's
responsibility to identify the different sinks. This id must also be
encodable as ASCII for the same reason. This id is referred as
*\<sink-id>* in this document: sink0, sink1, sink2, ... is often used
to identify the different sinks.

The combination of *\<gw-id>/\<sink-id>* allows to unambiguously
identify a sink.

### Request unique identifier

Multiple backends can simultaneously send requests to the same gateway
(on same topic). To correlate the answers to the requests, each request
must have a unique id.

This id is referred as *\<req-id>* in this document, a 64 bits field.

At least 48 bits must be randomly generated by the backend to guarantee
the uniqueness of the request id between backends.

This request identifier is reported by the gateways in all response header. The only exception is for asynchronous responses generated by a gateway
without a prior request by the backend. The reason for such exception
is to avoid having further topics to subscribe and publish to.

## API description

This section introduces the API's MQTT topics and its contents and is
split in several subsections, one for each module:

1. [Gateway status module](#gateway-status-module)
1. [Config module](#config-module)
1. [Data module](#data-module)
1. [OTAP module](#otap-module)

Each subsection contains the relevant topic and the payload carried
by it. This sections point out the specific protocol buffer message
that must be implemented within the common
[Generic Message][message_GenericMessage]. Please refer to
[API extension](#api-extension) for further details.

In MQTT, the QoS is an important concept. Most of the gateway to broker
communication should happen with QoS2 to be sure the messages are
received or published one and only one time. However, as many packets
can be received from a network and multiple gateways can publish on the
same broker, message received event should be published with QoS1.
Depending on the quality of the connection between gateway and Backends,
it can create duplicates that will have to be filtered by the backends.
To ease this filtering, each event contains a unique identifier (random
64 bits value) in its header.

### Gateway status module

---

This module oversees the discovery of gateways for the different
backends. It also allows the backends to monitor the gateways status.

#### Status message

> **topic:**
> gw-event/status/*\<gw_id\>*
>
> **content:**
> [GenericMessage][message_GenericMessage].[WirepasMessage][message_WirepasMessage].[StatusEvent][message_StatusEvent]

The message must have the retained flag set to true to allow a new
backend to immediately be noticed of all the available gateways when
subscribing to this topic.

Once connected to the MQTT broker, status must be set to *ONLINE*.

#### Last will message

Same message with a status set to *OFFLINE* must be set by the gateway as
a **last will message**.

It will allow backends to easily see which gateway is offline.

#### Keep alive message

This API doesn't enforce the usage of a keep alive message by a gateway
to avoid additional constraints on the gateway implementation. In fact,
it implies the generation of a PING request to the broker if there is no
message generated within a keep alive interval.

Nevertheless, it is recommended to use the keep alive mechanism of MQTT
to overcome the half-open connection issue of a TCP connection.

The broker will disconnect a client if no message is received within one
and a half times of the keep alive interval and the last will message
will be sent. It allows the backends to be notified in a really short
period of a problem with a gateway connection.

60s is a good value for the keep alive interval.

### Config module

---

This module oversees configuration of the different sinks attached to
the gateway.

#### Get configs message

- **Request:**

    > **topic:** gw-request/get_configs/*\<gw-id\>*
    >
    > **content:** [GenericMessage][message_GenericMessage].[WirepasMessage][message_WirepasMessage].[GetConfigsReq][message_GetConfigsReq]

- **Response:**

    > **topics:** gw-response/get_configs/*\<gw-id\>*
    >
    > **content:** [GenericMessage][message_GenericMessage].[WirepasMessage][message_WirepasMessage].[GetConfigsResp][message_GetConfigsResp]

:warning:

_A gateway must generate a [GetConfigsResp][message_GetConfigsResp]
with a request id set to 0 in its header when its configuration change.
When a sink is added or removed for example.
It is the only way for a backend to monitor this change without
having to frequently poll for such event._

#### Set config message

-  **Request:**

    > **topic:** gw-request/set_config/*\<gw-id\>/\<sink-id\>*
    >
    > **content:** [GenericMessage][message_GenericMessage].[WirepasMessage][message_WirepasMessage].[SetConfigReq ][message_SetConfigReq]

- **Response:**

    > **topics:** gw-response/set_config/*\<gw-id\>/\<sink-id\>*
    >
    > **content:** [GenericMessage][message_GenericMessage].[WirepasMessage][message_WirepasMessage].[SetConfigResp][message_SetConfigResp]

:warning:

_A gateway must generate a [SetConfigResp][message_SetConfigResp]
with a request id set to 0 in its header when a sink state
change, especially if it reboots. In fact, if sink configuration
is changed through remote api, it is the only way for a backend
to monitor this change._

#### Get gateway info

- **Request:**

    > **topic:** gw-request/get_gw_info/*\<gw-id\>*
    >
    > **content:** [GenericMessage][message_GenericMessage].[WirepasMessage][message_WirepasMessage].[GetGwInfoReq][message_GetGwInfoReq]

- **Response:**

    > **topics:** gw-response/get_gw_info/*\<gw-id\>/\<sink-id\>*
    >
    > **content:** [GenericMessage][message_GenericMessage].[WirepasMessage][message_WirepasMessage].[GetGwInfoResp][message_GetGwInfoResp]

:warning:

_The API field should not be explicitly set from code and default value
must be kept. Default value is incremented by Wirepas for each release._

_Even if this version is increased, the API remains backward compatible.
It just help backends development to identify if new features are
present in a gateway._

#### Set configuration data item

Only processed if CONFIGURATION_DATA_V1 feature flag is set on the gateway.

- **Request:**

    > **topic:** gw-request/set_configuration_data_item/*\<gw-id\>/\<sink-id\>*
    >
    > **content:** [GenericMessage][message_GenericMessage].[WirepasMessage][message_WirepasMessage].[message_SetConfigurationDataItemReq]

- **Response:**

    > **topics:** gw-response/set_configuration_data_item/*\<gw-id\>/\<sink-id\>*
    >
    > **content:** [GenericMessage][message_GenericMessage].[WirepasMessage][message_WirepasMessage].[message_SetConfigurationDataItemResp]
    >
    > **possible errors:**
    > - INVALID_ROLE: Node is not a sink.
    > - SINK_OUT_OF_MEMORY: Payload is too large or maximum number of items is reached.
    > - INVALID_DEST_ENDPOINT: Endpoint is too large (it should be a 16 bit unsigned integer).
    > - INVALID_DATA_PAYLOAD: Payload is rejected for this endpoint by the sink.
    > - INVALID_SINK_ID: Invalid sink id in the request header.

:warning:

_Successfully setting an item must be treated as a configuration change on the
sink, meaning that the gateway must report the new complete configuration data
content by generating a new [StatusEvent][message_StatusEvent] message._

#### Get configuration data item

Only processed if CONFIGURATION_DATA_V1 feature flag is set on the gateway.

- **Request:**

    > **topic:** gw-request/get_configuration_data_item/*\<gw-id\>/\<sink-id\>*
    >
    > **content:** [GenericMessage][message_GenericMessage].[WirepasMessage][message_WirepasMessage].[message_GetConfigurationDataItemReq]

- **Response:**

    > **topics:** gw-response/get_configuration_data_item/*\<gw-id\>/\<sink-id\>*
    >
    > **content:** [GenericMessage][message_GenericMessage].[WirepasMessage][message_WirepasMessage].[message_GetConfigurationDataItemResp]
    >
    > **possible errors:**
    > - INVALID_DEST_ENDPOINT: Endpoint is too large (it should be a 16 bit unsigned integer).
    > - INVALID_PARAM: No item found with the given endpoint.
    > - INVALID_SINK_ID: Invalid sink id in the request header.

### Data module

---

#### Send packet message

- **Request:**

    > **topic:** gw-request/send_data/*\<gw-id\>/\<sink-id\>*
    >
    > **content:** [GenericMessage][message_GenericMessage].[WirepasMessage][message_WirepasMessage].[SendPacketReq][message_SendPacketReq]

- **Response:**

    > **topics:** gw-response/send_data/*\<gw-id\>/\<sink-id\>*
    >
    > **content:** [GenericMessage][message_GenericMessage].[WirepasMessage][message_WirepasMessage].[SendPacketResp][message_SendPacketResp]

#### Packet received event

> **topic:** gw-event/received_data/*\<gw-id\>/\<sink-id\>/\<net_id\>/\<src_ep\>/\<dst_ep\>*
>
> **content:** [GenericMessage][message_GenericMessage].[WirepasMessage][message_WirepasMessage].[PacketReceivedEvent][message_PacketReceivedEvent]

##### QoS

As described in the beginning of this chapter, it is recommended to
publish this event with a QoS1 to avoid loading too much the broker.

:warning:

_To take full advantage of WNT Wirepas backend and have the correct
visualization of network activity, all received messages must be
published on this topic._

_But for security reason in some use cases, it may be required that
application payload is sent through a different channel without passing
through the MQTT broker._

_This is the main reason for the "payload" and "payload size" fields to
be optional. In fact, WNT doesn't need the application payload content
to work properly, headers are enough._

_If payload is not published, setting the payload size is a good
information for WNT. And if payload is published, payload_size can be
omitted as already available from payload field._

_Even if WNT Wirepas backend can operate without the payload, it may not
be the case for other backends implementing this API._

_Consequently, it is highly recommended to keep this field._

### OTAP module

---

#### Get local scratchpad status

- **Request:**

    > **topic:** gw-request/otap_status/*\<gw-id\>/\<sink-id\>*
    >
    > **content:** [GenericMessage][message_GenericMessage].[WirepasMessage][message_WirepasMessage].[GetScratchpadStatusReq][message_GetScratchpadStatusReq]

- **Response:**

    > **topics:** gw-response/otap_status/*\<gw-id\>/\<sink-id\>*
    >
    > **content:** [GenericMessage][message_GenericMessage].[WirepasMessage][message_WirepasMessage].[GetScratchpadStatusRes][message_GetScratchpadStatusRes]

#### Upload local scratchpad

- **Request:**

    > **topic:** gw-request/otap_load_scratchpad/*\<gw-id\>/\<sink-id\>*
    >
    > **content:** [GenericMessage][message_GenericMessage].[WirepasMessage][message_WirepasMessage].[UploadScratchpadReq][message_UploadScratchpadReq]

- **Response:**

    > **topics:** gw-response/otap_load_scratchpad/*\<gw-id\>/\<sink-id\>*
    >
    > **content:** [GenericMessage][message_GenericMessage].[WirepasMessage][message_WirepasMessage].[UploadScratchpadResp][message_UploadScratchpadResp]

#### Process local scratchpad

- **Request:**

    > **topic:** gw-request/otap_process_scratchpad/*\<gw-id\>/\<sink-id\>*
    >
    > **content:** [GenericMessage][message_GenericMessage].[WirepasMessage][message_WirepasMessage].[ProcessScratchpadReq][message_ProcessScratchpadReq]

- **Response:**

    > **topics:** gw-response/otap_process_scratchpad/*\<gw-id\>/\<sink-id\>*
    >
    > **content:** [GenericMessage][message_GenericMessage].[WirepasMessage][message_WirepasMessage].[ProcessScratchpadResp][message_ProcessScratchpadResp]

#### Set target scratchpad and action

- **Request:**

    > **topic:** gw-request/otap_set_target_scratchpad/*\<gw-id\>/\<sink-id\>*
    >
    > **content:** [GenericMessage][message_GenericMessage].[WirepasMessage][message_WirepasMessage].[SetScratchpadTargetAndActionReq][message_SetScratchpadTargetAndActionReq]

- **Response:**

    > **topics:** gw-response/otap_set_target_scratchpad/*\<gw-id\>/\<sink-id\>*
    >
    > **content:** [GenericMessage][message_GenericMessage].[WirepasMessage][message_WirepasMessage].[SetScratchpadTargetAndActionResp][message_SetScratchpadTargetAndActionResp]

## API extension

This API is the minimal set of services to be integrated to be
compatible with Wirepas backends.

Any payload format can be extended to feat specific gateway needs. And
new topics can be added on top of those ones.

To ease API extension by every gateway manufacturer without breaking
compatibility with different backends provider, every message has the
same [GenericMessage][message_GenericMessage] root type
that contains an optional [CustomerMessage][message_CustomerMessage],
such as:

```protobuf
    message WirepasMessage {
        optional StatusEvent status_event = 1;
        optional GetConfigsReq get_configs_req = 2;
        ... // All possible specific payloads
    }

    message CustomerMessage {
        // Customer name is needed to avoid any collision between
        different customer implementation
        required string customer_name = 1;
        // Can be freely used for enhancing API by customers
    }

    message GenericMessage {
        optional WirepasMessage wirepas = 1;
        optional CustomerMessage customer = 2;
    }
```

As the customer field is optional, it will not affect the Wirepas
backends that will not have the knowledge of such field.

For example, the status message can be extended with more information on
the gateway itself for gateway specific information like the model and
any useful information.

## Implementation and workflow example for backends

### General remarks

-   A backend must know the MQTT broker that is used by the gateway(s)
    in the network;

-   There is relevant information present in both the MQTT topic and Protocol
    Buffers payload. Reason is to allow more flexibility in implementation.
    Filtering can be done on topics or by parsing the payload format.

### Backend for network configuration

This section describes the workflow for a backend that oversees the
network configuration. Usually, only one backend has this function in a
full product to avoid any mismatch configuration that cannot be avoided
by the gateway itself. WNT developed by Wirepas can be used for this
function.

#### Initialization

Once connected to the broker, the backend must subscribe to the
*gw-event/status/+* topic to discover the different gateways registered
to that broker.

As all gateways post a retained message on that topic with their status,
the backend will immediately know the list of gateways connected to this
broker.

Backend can ask each gateway, its list of attached sinks by publishing a
message on *gw-request/get_configs/\<gw-id\>* topic and the backend
should subscribe to *gw-response/get_configs/\<gw-id\>* topic to
receive the answer from a specific gateway or
*gw-response/get_configs/+* topic for all gateways.

#### Sink(s) configuration

Each sink can be configured and started/stopped by publishing a message
on *gw-request/set_config/\<gw-id>/\<sink-id\>*.

The gateway will publish back a message on
*gw-response/set_config/\<gw-id\>/\<sink-id\>* topic with the result of
configuration and the full new configuration.

#### OTAP

A new scratchpad can be loaded and processed by sinks attached to the
gateway with messages described in the OTAP section.

All the remote procedure is managed by the dedicated remote API.

### Backend for data exchanges

This section describes the work flow for a backend that just want to
send/receive application data to/from a Wirepas network.

In a simple use case, a backend waiting for messages on endpoint 10 from
network 12345 must only subscribe to topic
*gw-event/received_data/+/+/12345/10/+*

And messages can be sent to the network from a given sink by publishing
on topic: *gw-request/send_data/\<gw-id\>/\<sink-id\>*

## List of all MQTT topics

Here is a list of the different MQTT topics for a global view of the
interface between a backend and a gateway (without the payload
definition)

*Request* from a backend to a gateway:

```mqtt
    gw-request/get_configs/<gw-id>

    gw-request/get_gw_info/<gw-id>

    gw-request/set_config/<gw-id>/<sink-id>

    gw-request/send_data/<gw-id>/<sink-id>

    gw-request/otap_status/<gw-id>/<sink-id>

    gw-request/otap_load_scratchpad/<gw-id>/<sink-id>

    gw-request/otap_process_scratchpad/<gw-id>/<sink-id>

    gw-request/otap_set_target_scratchpad/<gw-id>/<sink-id>

    gw-request/set_configuration_data_item/<gw-id>/<sink-id>

    gw-request/get_configuration_data_item/<gw-id>/<sink-id>
```

*Response* from a gateway to a backend:

```mqtt
    gw-response/get_configs/<gw-id>

    gw-response/get_gw_info/<gw-id>

    gw-response/set_config/<gw-id>/<sink-id>

    gw-response/send_data/<gw-id>/<sink-id>

    gw-response/otap_status/<gw-id>/<sink-id>

    gw-response/otap_load_scratchpad/<gw-id>/<sink-id>

    gw-response/otap_process_scratchpad/<gw-id>/<sink-id>

    gw-response/otap_set_target_scratchpad/<gw-id>/<sink-id>

    gw-response/set_configuration_data_item/<gw-id>/<sink-id>

    gw-response/get_configuration_data_item/<gw-id>/<sink-id>
```

*Asynchronous* event from a gateway:

```mqtt
    gw-event/status/<gw_id>

    gw-event/received_data/<gw-id>/<sink-id>/<net_id>/<src_ep>/<dst_ep>
```


[message_StatusEvent]: https://github.com/wirepas/backend-apis/blob/85a6ffd5168f42ac18561e25cc2cf334cd8ded17/gateway_to_backend/protocol_buffers_files/config_message.proto#L136

[message_GetConfigsReq]: https://github.com/wirepas/backend-apis/blob/85a6ffd5168f42ac18561e25cc2cf334cd8ded17/gateway_to_backend/protocol_buffers_files/config_message.proto#L163

[message_GetConfigsResp]: https://github.com/wirepas/backend-apis/blob/85a6ffd5168f42ac18561e25cc2cf334cd8ded17/gateway_to_backend/protocol_buffers_files/config_message.proto#L167

[message_SetConfigReq]: https://github.com/wirepas/backend-apis/blob/85a6ffd5168f42ac18561e25cc2cf334cd8ded17/gateway_to_backend/protocol_buffers_files/config_message.proto#L173

[message_SetConfigResp]: https://github.com/wirepas/backend-apis/blob/85a6ffd5168f42ac18561e25cc2cf334cd8ded17/gateway_to_backend/protocol_buffers_files/config_message.proto#L179

[message_GetGwInfoReq]: https://github.com/wirepas/backend-apis/blob/85a6ffd5168f42ac18561e25cc2cf334cd8ded17/gateway_to_backend/protocol_buffers_files/config_message.proto#L186

[message_GetGwInfoResp]: https://github.com/wirepas/backend-apis/blob/85a6ffd5168f42ac18561e25cc2cf334cd8ded17/gateway_to_backend/protocol_buffers_files/config_message.proto#L190

[message_SendPacketReq]: https://github.com/wirepas/backend-apis/blob/85a6ffd5168f42ac18561e25cc2cf334cd8ded17/gateway_to_backend/protocol_buffers_files/data_message.proto#L10

[message_SendPacketResp]: https://github.com/wirepas/backend-apis/blob/85a6ffd5168f42ac18561e25cc2cf334cd8ded17/gateway_to_backend/protocol_buffers_files/data_message.proto#L27

[message_PacketReceivedEvent]: https://github.com/wirepas/backend-apis/blob/85a6ffd5168f42ac18561e25cc2cf334cd8ded17/gateway_to_backend/protocol_buffers_files/data_message.proto#L34

[message_GetScratchpadStatusReq]: https://github.com/wirepas/backend-apis/blob/85a6ffd5168f42ac18561e25cc2cf334cd8ded17/gateway_to_backend/protocol_buffers_files/otap_message.proto#L10

[message_GetScratchpadStatusRes]: https://github.com/wirepas/backend-apis/blob/85a6ffd5168f42ac18561e25cc2cf334cd8ded17/gateway_to_backend/protocol_buffers_files/otap_message.proto#L14

[message_UploadScratchpadReq]: https://github.com/wirepas/backend-apis/blob/85a6ffd5168f42ac18561e25cc2cf334cd8ded17/gateway_to_backend/protocol_buffers_files/otap_message.proto#L26

[message_UploadScratchpadResp]: https://github.com/wirepas/backend-apis/blob/85a6ffd5168f42ac18561e25cc2cf334cd8ded17/gateway_to_backend/protocol_buffers_files/otap_message.proto#L44

[message_ProcessScratchpadReq]: https://github.com/wirepas/backend-apis/blob/85a6ffd5168f42ac18561e25cc2cf334cd8ded17/gateway_to_backend/protocol_buffers_files/otap_message.proto#L48

[message_ProcessScratchpadResp]: https://github.com/wirepas/backend-apis/blob/85a6ffd5168f42ac18561e25cc2cf334cd8ded17/gateway_to_backend/protocol_buffers_files/otap_message.proto#L52

[message_GenericMessage]: https://github.com/wirepas/backend-apis/blob/85a6ffd5168f42ac18561e25cc2cf334cd8ded17/gateway_to_backend/protocol_buffers_files/generic_message.proto#L40

[message_CustomerMessage]: https://github.com/wirepas/backend-apis/blob/85a6ffd5168f42ac18561e25cc2cf334cd8ded17/gateway_to_backend/protocol_buffers_files/generic_message.proto#L34

[message_WirepasMessage]: https://github.com/wirepas/backend-apis/blob/85a6ffd5168f42ac18561e25cc2cf334cd8ded17/gateway_to_backend/protocol_buffers_files/generic_message.proto#L9

[message_SetScratchpadTargetAndActionReq]: https://github.com/wirepas/backend-apis/blob/85a6ffd5168f42ac18561e25cc2cf334cd8ded17/gateway_to_backend/protocol_buffers_files/otap_message.proto#L56

[message_SetScratchpadTargetAndActionResp]: https://github.com/wirepas/backend-apis/blob/85a6ffd5168f42ac18561e25cc2cf334cd8ded17/gateway_to_backend/protocol_buffers_files/otap_message.proto#L62

[message_SetConfigurationDataItemReq]: https://github.com/wirepas/backend-apis/blob/85a6ffd5168f42ac18561e25cc2cf334cd8ded17/gateway_to_backend/protocol_buffers_files/config_message.proto#L196

[message_SetConfigurationDataItemResp]: https://github.com/wirepas/backend-apis/blob/85a6ffd5168f42ac18561e25cc2cf334cd8ded17/gateway_to_backend/protocol_buffers_files/config_message.proto#L203

[message_GetConfigurationDataItemReq]: https://github.com/wirepas/backend-apis/blob/85a6ffd5168f42ac18561e25cc2cf334cd8ded17/gateway_to_backend/protocol_buffers_files/config_message.proto#L207

[message_GetConfigurationDataItemResp]: https://github.com/wirepas/backend-apis/blob/85a6ffd5168f42ac18561e25cc2cf334cd8ded17/gateway_to_backend/protocol_buffers_files/config_message.proto#L213

[protobuf_homepage]: https://developers.google.com/protocol-buffers
