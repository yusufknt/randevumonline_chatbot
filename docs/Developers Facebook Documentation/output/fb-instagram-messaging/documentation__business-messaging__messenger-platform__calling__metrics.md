# Metrics | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling/metrics_

---

# Metrics

Updated: Mar 16, 2026

Send detailed network metrics to Meta after each call. This API allows a business using your app to submit call metrics data to Meta after a call completes. These metrics help Meta debug issues and improve call quality for businesses.

| Property | Description |
| --- | --- |
| `Page-ID` string | This is the Page ID connected to the app |
| `platform` string | The platform this call took place on. `messenger` is the only possible value for now. |
| `call_id` string | The unique id for the call whose data is being submitted |
| `end_call_reason` enum | The reason the call was ended. See [End Call Reason Values](https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling/metrics#end-call). |
| `end_call_subreason` string | Freeform input field for the business to include any additional details on the reason for the call ending; guidance will be to include specific error information |
| `call_ended_time` Unix Timestamp | Timestamp for when the business received the hangup webhook or when they received a success response for the terminate API request |
| `first_audio_packet_received_time` Unix Timestamp | Timestamp for when the first audio packet was received from the consumer |
| `audio_stats` Dictionary of string to mixed values | This field will contain a dictionary with the fields requested from that RTC stats report. A script is provided that takes the RTC status report and returns the dictionary of requested values. You can then populate this field using the returned dictionary.<br>The dictionary will be required to have the following values<br>1) `call_ended_time` (Unix Timestamp)<br>2) `jitter` (float)<br>3) `packets_lost` (int)<br>4) `packets_received` (int)<br>5) `round_trip_time_ms` (float)<br>6) `jitter_buffer_delay_ms` (float)<br>7) `concealed_samples` (int)<br>8) `silent_concealed_samples` (int)<br>9) `total_samples_duration_ms` (float) |

```curl
POST /<PAGE_ID>/call_metrics
{
  "platform": "messenger",
  "call_id": "c_M5YPhGE5jm0L_PMQdScLlYJlR7tU_f0rgXinCqnTQ",
  "end_call_reason": "Hangup_Call",
  "end_call_subreason": "Conversation was finished",
  "call_ended_time": 123456,
  "first_audio_packet_received_time": 12345,
  "audio_stats": {
    "jitter_sec": 0.01,
    "packets_lost": 0,
    "packets_received": 1000,
    "round_trip_time_sec": 10.5,
    "jitter_buffer_delay_sec": 4000.5,
    "concealed_samples": 2000,
    "silent_concealed_samples": 16000,
    "total_samples_duration_sec": 316.5
  },
}
```

### Example response

| Property | Description |
| --- | --- |
| `success` boolean | `true` if data was successfully submitted; `false` otherwise |

```json
{
  "success": true
}
```

### Error response

The following errors can happen:

- Invalid call id
- Invalid page-id
- Metrics submitted outside of 24-hour submission window
- Call is still in progress
- Metrics have already been submitted
- Invalid permissions. The app will be required to have the calling capability and the Page will be required to be eligible for calling

For more details on these errors, see the [Messenger Platform error codes reference](https://developers.facebook.com/documentation/business-messaging/messenger-platform/error-codes).

### End call reason values

The list below contains the possible enum values that the business can submit when calling the API.

- `Call_End_Accept_After_Hang_Up`
- `Caller_Not_Visible`
- `Camera_Permission_Denied`
- `Client_Error`
- `Client_Interrupted`
- `Connection_Dropped`
- `Hangup_Call`
- `Ignore_Call`
- `In_Another_Call`
- `Inactive_Timeout`
- `Incoming_Timeout`
- `Max_Allowed_Participants_Reached`
- `Microphone_Permission_Denied`
- `No_Answer_Timeout`
- `No_Permission`
- `Removed_By_Participant`
- `Ring_Muted`
- `Signaling_Message_Failed`
- `Unexpected_End_Of_Call`
- `Unknown`
- `Version_Unsupported`
- `WebRTC_Error`

### Generating metrics

At the end of each call, generate metrics from the peer connection object using the following code sample:

```js
function transformRtcStats(stats) {
  const apiSpec = {
    platform: 'messenger',
    call_id: '', // You need to provide this value
    end_call_reason: 'HangupCall', // You need to provide this value
    end_call_subreason: 'Conversation was finished', // You need to provide this value
    call_ended_time: 0, // You need to provide this value
    first_audio_packet_received_time: 0, // You need to provide this value
    audio_stats: {},
  };

  let inboundRtpReport;
  let remoteInboundRtpReport;

  stats.forEach((report) => {
    if (report.type === 'inbound-rtp' && report.kind === 'audio') {
      inboundRtpReport = report;
    } else if (report.type === 'remote-inbound-rtp' && report.kind === 'audio') {
      remoteInboundRtpReport = report;
    }
  });

  if (inboundRtpReport) {
    apiSpec.audio_stats.jitter_sec = inboundRtpReport.jitter;
    apiSpec.audio_stats.packets_lost = inboundRtpReport.packetsLost;
    apiSpec.audio_stats.packets_received = inboundRtpReport.packetsReceived;
    apiSpec.audio_stats.jitter_buffer_delay_sec = inboundRtpReport.jitterBufferDelay;
    apiSpec.audio_stats.concealed_samples = inboundRtpReport.concealedSamples;
    apiSpec.audio_stats.silent_concealed_samples = inboundRtpReport.silentConcealedSamples;
    apiSpec.audio_stats.total_samples_duration_sec = inboundRtpReport.totalSamplesDuration;
  }
  if (remoteInboundRtpReport) {
    apiSpec.audio_stats.round_trip_time_sec = remoteInboundRtpReport.totalRoundTripTime;
  }

  return apiSpec;
}

const stats = await pc.getStats(); // pc is the peer connection object for the call
const apiSpec = transformRtcStats(stats);
console.log(apiSpec);
```
