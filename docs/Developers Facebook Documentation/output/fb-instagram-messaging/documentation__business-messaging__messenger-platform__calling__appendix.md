# Appendix | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling/appendix_

---

# Appendix

Updated: Mar 16, 2026

This appendix shows the SDP structures involved when using the Messenger Calling API.

### Sample SDP offer structure

This is an example SDP offer structure that your application provides when calling the accept API.

```json
v=0
o=- 8436422327585670287 2 IN IP4 127.0.0.1
s=-
t=0 0
a=group:BUNDLE 0
a=extmap-allow-mixed
a=msid-semantic: WMS a7299aa1-1469-48ed-b99f-30e5ebc5fd14
m=audio 9 UDP/TLS/RTP/SAVPF 111 63 9 0 8 110 126
c=IN IP4 0.0.0.0
a=rtcp:9 IN IP4 0.0.0.0
a=ice-ufrag:GVWP
a=ice-pwd:GoQbqNzclssPK7hZfTHBAZK3
a=ice-options:trickle
a=fingerprint:sha-256 F3:A4:D1:09:55:4A:73:84:21:4C:46:56:E1:05:E7:8B:47:45:5B:A0:0E:3F:30:14:D8:5F:36:95:A2:06:AA:48
a=setup:actpass
a=mid:0
a=sendrecv
a=msid:a7299aa1-1469-48ed-b99f-30e5ebc5fd14 9d4611fa-fe03-4cad-81f1-63e4f764f358
a=rtcp-mux
a=rtpmap:111 opus/48000/2
a=rtcp-fb:111 transport-cc
a=fmtp:111 minptime=10;useinbandfec=1
a=rtpmap:63 red/48000/2
a=fmtp:63 111/111
a=rtpmap:9 G722/8000
a=rtpmap:0 PCMU/8000
a=rtpmap:8 PCMA/8000
a=rtpmap:110 telephone-event/48000
a=rtpmap:126 telephone-event/8000
a=ssrc:2607947206 cname:z8aoN2l/L7oiSqrJ
a=ssrc:2607947206 msid:a7299aa1-1469-48ed-b99f-30e5ebc5fd14 9d4611fa-fe03-4cad-81f1-63e4f764f358
```

### Sample SDP answer structure

This is an example SDP answer structure that Meta returns to your application when calling the accept API.

```json
v=0
o=- 8436422327585670287 3 IN IP4 127.0.0.1
s=-
t=0 0
a=group:BUNDLE 0
a=msid-semantic: WMS
a=ice-lite
m=audio 40007 UDP/TLS/RTP/SAVPF 111
c=IN IP4 157.240.22.131
a=rtcp:9 IN IP4 0.0.0.0
a=candidate:2958823651 1 udp 2122260224 157.240.22.131 40007 typ host generation 1
a=candidate:716810591 1 udp 2122262784 2a03:2880:f231:d2:face:b00c:0:8c2 40007 typ host generation 1
a=candidate:4276087827 1 tcp 1518280448 157.240.22.131 3478 typ host tcptype passive generation 1
a=candidate:1681544623 1 tcp 1518283008 2a03:2880:f231:d2:face:b00c:0:8c2 3478 typ host tcptype passive generation 1
a=ice-ufrag:EbT4cXksCyVKQMC/103
a=ice-pwd:74O3IvX6AV9ulmb9udAmimux
a=fingerprint:sha-256 4F:6E:0A:C8:9B:A5:E5:1B:25:C2:30:2C:F0:93:E3:99:5D:00:56:C3:1D:4E:45:26:38:00:88:87:CF:91:3B:57
a=setup:passive
a=mid:0
a=extmap:1 urn:ietf:params:rtp-hdrext:ssrc-audio-level
a=extmap:4 urn:ietf:params:rtp-hdrext:sdes:mid
a=sendrecv
a=msid:- 9d4611fa-fe03-4cad-81f1-63e4f764f358
a=rtcp-mux
a=rtpmap:111 opus/48000/2
a=fmtp:111 maxaveragebitrate=20000;maxplaybackrate=16000;minptime=10;usedtx=1;useinbandfec=1
```

### Sample SDP renegotiation structure

This is an example SDP renegotiation structure that Meta returns to your application when calling the accept API.

```json
v=0
o=- 8436422327585670287 3 IN IP4 127.0.0.1
s=-
t=0 0
a=group:BUNDLE 0 1
a=msid-semantic: WMS 499556708:yxYSY4D3OsewsKgu:DEFAULT
a=ice-lite
a=x-fb-feature:pqc-0
m=audio 40007 UDP/TLS/RTP/SAVPF 111
c=IN IP4 157.240.22.131
a=rtcp:9 IN IP4 0.0.0.0
a=candidate:2958823651 1 udp 2122260224 157.240.22.131 40007 typ host generation 1
a=candidate:716810591 1 udp 2122262784 2a03:2880:f231:d2:face:b00c:0:8c2 40007 typ host generation 1
a=candidate:4276087827 1 tcp 1518280448 157.240.22.131 3478 typ host tcptype passive generation 1
a=candidate:1681544623 1 tcp 1518283008 2a03:2880:f231:d2:face:b00c:0:8c2 3478 typ host tcptype passive generation 1
a=ice-ufrag:EbT4cXksCyVKQMC//103
a=ice-pwd:74O3IvX6AV9ulmb9udAmimux
a=ice-options:fb-force-5245
a=fingerprint:sha-256 4F:6E:0A:C8:9B:A5:E5:1B:25:C2:30:2C:F0:93:E3:99:5D:00:56:C3:1D:4E:45:26:38:00:88:87:CF:91:3B:57
a=setup:passive
a=mid:0
a=extmap:1 urn:ietf:params:rtp-hdrext:ssrc-audio-level
a=extmap:4 urn:ietf:params:rtp-hdrext:sdes:mid
a=recvonly
a=msid:- 9d4611fa-fe03-4cad-81f1-63e4f764f358
a=rtcp-mux
a=x-google-flag:conference
a=rtpmap:111 opus/48000/2
a=fmtp:111 maxaveragebitrate=20000;maxplaybackrate=16000;minptime=10;usedtx=1;useinbandfec=1
m=audio 40007 UDP/TLS/RTP/SAVPF 111
c=IN IP4 157.240.22.131
a=rtcp:9 IN IP4 0.0.0.0
a=candidate:2958823651 1 udp 2122260224 157.240.22.131 40007 typ host generation 1
a=candidate:716810591 1 udp 2122262784 2a03:2880:f231:d2:face:b00c:0:8c2 40007 typ host generation 1
a=candidate:4276087827 1 tcp 1518280448 157.240.22.131 3478 typ host tcptype passive generation 1
a=candidate:1681544623 1 tcp 1518283008 2a03:2880:f231:d2:face:b00c:0:8c2 3478 typ host tcptype passive generation 1
a=ice-ufrag:EbT4cXksCyVKQMC//103
a=ice-pwd:74O3IvX6AV9ulmb9udAmimux
a=ice-options:fb-force-5245
a=fingerprint:sha-256 4F:6E:0A:C8:9B:A5:E5:1B:25:C2:30:2C:F0:93:E3:99:5D:00:56:C3:1D:4E:45:26:38:00:88:87:CF:91:3B:57
a=setup:passive
a=mid:1
a=extmap:1 urn:ietf:params:rtp-hdrext:ssrc-audio-level
a=extmap:4 urn:ietf:params:rtp-hdrext:sdes:mid
a=sendonly
a=msid:499556708:yxYSY4D3OsewsKgu:DEFAULT 1116955618675631925
a=rtcp-mux
a=x-google-flag:conference
a=rtpmap:111 opus/48000/2
a=fmtp:111 maxaveragebitrate=20000;maxplaybackrate=16000;minptime=10;usedtx=1;useinbandfec=1
a=ssrc:1379106125 cname:499556708:yxYSY4D3OsewsKgu
```

### Sample client SDP offer structure for `media_update`

This is an example SDP offer structure that Meta sends to your application when a consumer turns on their video during a call.

```json
v=0
o=- 6632004562319072770 3 IN IP4 127.0.0.1
s=-
t=0 0
a=group:BUNDLE 0 1 2 3
a=msid-semantic: WMS 1628954254:a71PRewqztualmqc:DEFAULT
a=ice-lite
m=audio 40008 UDP/TLS/RTP/SAVPF 111 110
c=IN IP4 157.240.22.60
a=rtcp:9 IN IP4 0.0.0.0
a=candidate:501682339 1 udp 2122260224 157.240.22.60 40008 typ host generation 1
a=candidate:383361191 1 udp 2122262784 2a03:2880:f231:cd:face:b00c:0:6443 40008 typ host generation 1
a=candidate:1399123027 1 tcp 1518280448 157.240.22.60 3479 typ host tcptype passive generation 1
a=candidate:1482316887 1 tcp 1518283008 2a03:2880:f231:cd:face:b00c:0:6443 3479 typ host tcptype passive generation 1
a=ice-ufrag:OJGX1CblNaGgpRIF/4
a=ice-pwd:74N8ugT4vaZbJFVcwkpf9PDP
a=ice-options:fb-force-5245
a=fingerprint:sha-256 2C:5F:8F:CB:06:D5:75:36:FB:B3:0A:AA:A1:56:64:7A:6C:2F:81:D9:DD:A5:B6:D7:89:85:60:4C:D4:B2:9D:95
a=setup:passive
a=mid:0
a=extmap:1 urn:ietf:params:rtp-hdrext:ssrc-audio-level
a=extmap:4 urn:ietf:params:rtp-hdrext:sdes:mid
a=recvonly
a=msid:- ce699e0a-4f3b-4f3e-a4bc-2e434173b5d8
a=rtcp-mux
a=rtcp-rsize
a=x-google-flag:conference
a=rtpmap:111 opus/48000/2
a=fmtp:111 maxaveragebitrate=20000;maxplaybackrate=16000;minptime=10;usedtx=1;useinbandfec=1
a=rtpmap:110 telephone-event/48000
m=video 40008 UDP/TLS/RTP/SAVPF 109
c=IN IP4 157.240.22.60
a=rtcp:9 IN IP4 0.0.0.0
a=candidate:501682339 1 udp 2122260224 157.240.22.60 40008 typ host generation 1
a=candidate:383361191 1 udp 2122262784 2a03:2880:f231:cd:face:b00c:0:6443 40008 typ host generation 1
a=candidate:1399123027 1 tcp 1518280448 157.240.22.60 3479 typ host tcptype passive generation 1
a=candidate:1482316887 1 tcp 1518283008 2a03:2880:f231:cd:face:b00c:0:6443 3479 typ host tcptype passive generation 1
a=ice-ufrag:OJGX1CblNaGgpRIF/4
a=ice-pwd:74N8ugT4vaZbJFVcwkpf9PDP
a=ice-options:fb-force-5245
a=fingerprint:sha-256 2C:5F:8F:CB:06:D5:75:36:FB:B3:0A:AA:A1:56:64:7A:6C:2F:81:D9:DD:A5:B6:D7:89:85:60:4C:D4:B2:9D:95
a=setup:passive
a=mid:1
a=extmap:3 http://www.ietf.org/id/draft-holmer-rmcat-transport-wide-cc-extensions-01
a=extmap:6 http://www.webrtc.org/experiments/rtp-hdrext/video-content-type
a=extmap:4 urn:ietf:params:rtp-hdrext:sdes:mid
a=sendonly
a=msid:- D3F4U1T_F8_TR4CK
a=rtcp-mux
a=rtcp-rsize
a=x-google-flag:conference
a=rtpmap:109 H264/90000
a=rtcp-fb:109 ccm fir
a=rtcp-fb:109 nack
a=rtcp-fb:109 nack pli
a=rtcp-fb:109 goog-remb
a=rtcp-fb:109 transport-cc
a=fmtp:109 level-asymmetry-allowed=1;packetization-mode=1;profile-level-id=42e01f
m=video 40008 UDP/TLS/RTP/SAVPF 109
c=IN IP4 157.240.22.60
a=rtcp:9 IN IP4 0.0.0.0
a=candidate:501682339 1 udp 2122260224 157.240.22.60 40008 typ host generation 1
a=candidate:383361191 1 udp 2122262784 2a03:2880:f231:cd:face:b00c:0:6443 40008 typ host generation 1
a=candidate:1399123027 1 tcp 1518280448 157.240.22.60 3479 typ host tcptype passive generation 1
a=candidate:1482316887 1 tcp 1518283008 2a03:2880:f231:cd:face:b00c:0:6443 3479 typ host tcptype passive generation 1
a=ice-ufrag:OJGX1CblNaGgpRIF/4
a=ice-pwd:74N8ugT4vaZbJFVcwkpf9PDP
a=ice-options:fb-force-5245
a=fingerprint:sha-256 2C:5F:8F:CB:06:D5:75:36:FB:B3:0A:AA:A1:56:64:7A:6C:2F:81:D9:DD:A5:B6:D7:89:85:60:4C:D4:B2:9D:95
a=setup:passive
a=mid:2
a=extmap:3 http://www.ietf.org/id/draft-holmer-rmcat-transport-wide-cc-extensions-01
a=extmap:6 http://www.webrtc.org/experiments/rtp-hdrext/video-content-type
a=extmap:4 urn:ietf:params:rtp-hdrext:sdes:mid
a=sendonly
a=msid:1628954254:a71PRewqztualmqc:DEFAULT 12713505002384555584
a=rtcp-mux
a=rtcp-rsize
a=x-google-flag:conference
a=rtpmap:109 H264/90000
a=rtcp-fb:109 ccm fir
a=rtcp-fb:109 nack
a=rtcp-fb:109 nack pli
a=rtcp-fb:109 goog-remb
a=rtcp-fb:109 transport-cc
a=fmtp:109 level-asymmetry-allowed=1;packetization-mode=1;profile-level-id=42e01f
a=ssrc:2699573882 cname:1628954254:a71PRewqztualmqc
m=audio 40008 UDP/TLS/RTP/SAVPF 111 110
c=IN IP4 157.240.22.60
a=rtcp:9 IN IP4 0.0.0.0
a=candidate:501682339 1 udp 2122260224 157.240.22.60 40008 typ host generation 1
a=candidate:383361191 1 udp 2122262784 2a03:2880:f231:cd:face:b00c:0:6443 40008 typ host generation 1
a=candidate:1399123027 1 tcp 1518280448 157.240.22.60 3479 typ host tcptype passive generation 1
a=candidate:1482316887 1 tcp 1518283008 2a03:2880:f231:cd:face:b00c:0:6443 3479 typ host tcptype passive generation 1
a=ice-ufrag:OJGX1CblNaGgpRIF/4
a=ice-pwd:74N8ugT4vaZbJFVcwkpf9PDP
a=ice-options:fb-force-5245
a=fingerprint:sha-256 2C:5F:8F:CB:06:D5:75:36:FB:B3:0A:AA:A1:56:64:7A:6C:2F:81:D9:DD:A5:B6:D7:89:85:60:4C:D4:B2:9D:95
a=setup:passive
a=mid:3
a=extmap:1 urn:ietf:params:rtp-hdrext:ssrc-audio-level
a=extmap:4 urn:ietf:params:rtp-hdrext:sdes:mid
a=sendonly
a=msid:1628954254:a71PRewqztualmqc:DEFAULT 9519166913317126035
a=rtcp-mux
a=rtcp-rsize
a=x-google-flag:conference
a=rtpmap:111 opus/48000/2
a=fmtp:111 maxaveragebitrate=20000;maxplaybackrate=16000;minptime=10;usedtx=1;useinbandfec=1
a=rtpmap:110 telephone-event/48000
a=ssrc:2475174920 cname:1628954254:a71PRewqztualmqc
```

### Sample business SDP offer structure for `media_update`

This is an example SDP offer structure that you send to Meta when a business turns on their video during a call.

```json
v=0
o=- 6238703880104695329 4 IN IP4 127.0.0.1
s=-
t=0 0
a=group:BUNDLE 0 1 2
a=extmap-allow-mixed
a=msid-semantic: WMS
m=audio 57585 UDP/TLS/RTP/SAVPF 111 63 9 0 8 13 110 126
c=IN IP4 163.114.132.128
a=rtcp:9 IN IP4 0.0.0.0
a=candidate:3164814847 1 udp 2122194687 172.24.234.214 52518 typ host generation 0 network-id 1 network-cost 10
a=candidate:1301697869 1 udp 2122063615 100.108.66.72 57574 typ host generation 0 network-id 3 network-cost 50
a=candidate:1883922133 1 udp 2122262783 2a03:83e0:1151:15::154 64439 typ host generation 0 network-id 2 network-cost 10
a=candidate:3293623034 1 udp 2122131711 2620:10d:c085:21cf::103d 60006 typ host generation 0 network-id 4 network-cost 50
a=candidate:3522357606 1 udp 1686055167 2620:10d:c090:500::5:72ac 64439 typ srflx raddr 2a03:83e0:1151:15::154 rport 64439 generation 0 network-id 2 network-cost 10
a=candidate:2104322741 1 udp 1685987071 163.114.132.128 57585 typ srflx raddr 172.24.234.214 rport 52518 generation 0 network-id 1 network-cost 10
a=candidate:3261914983 1 tcp 1518214911 172.24.234.214 9 typ host tcptype active generation 0 network-id 1 network-cost 10
a=candidate:861517781 1 tcp 1518083839 100.108.66.72 9 typ host tcptype active generation 0 network-id 3 network-cost 50
a=candidate:243645517 1 tcp 1518283007 2a03:83e0:1151:15::154 9 typ host tcptype active generation 0 network-id 2 network-cost 10
a=candidate:3131002978 1 tcp 1518151935 2620:10d:c085:21cf::103d 9 typ host tcptype active generation 0 network-id 4 network-cost 50
a=ice-ufrag:Txee
a=ice-pwd:VNIFqZIEdn4Grt2PcAAOVFRt
a=ice-options:trickle
a=fingerprint:sha-256 F2:CD:C8:BA:E3:5E:99:B5:91:BA:49:94:8E:ED:BC:16:12:14:7B:EB:C6:B4:6B:FC:99:71:24:91:6D:D6:1C:BC
a=setup:actpass
a=mid:0
a=extmap:1 urn:ietf:params:rtp-hdrext:ssrc-audio-level
a=extmap:4 urn:ietf:params:rtp-hdrext:sdes:mid
a=extmap:2 http://www.webrtc.org/experiments/rtp-hdrext/abs-send-time
a=extmap:3 http://www.ietf.org/id/draft-holmer-rmcat-transport-wide-cc-extensions-01
a=sendrecv
a=msid:- 84a3b65a-e6fc-4e06-8a10-59202ce3c968
a=rtcp-mux
a=rtcp-rsize
a=rtpmap:111 opus/48000/2
a=fmtp:111 minptime=10;useinbandfec=1
a=rtpmap:63 red/48000/2
a=fmtp:63 111/111
a=rtpmap:9 G722/8000
a=rtpmap:0 PCMU/8000
a=rtpmap:8 PCMA/8000
a=rtpmap:13 CN/8000
a=rtpmap:110 telephone-event/48000
a=rtpmap:126 telephone-event/8000
a=ssrc:1745453179 cname:RjFfzNPobxWehiyS
a=ssrc:1745453179 msid:- 84a3b65a-e6fc-4e06-8a10-59202ce3c968
m=audio 9 UDP/TLS/RTP/SAVPF 111 63 9 0 8 13 110 126
c=IN IP4 0.0.0.0
a=rtcp:9 IN IP4 0.0.0.0
a=ice-ufrag:Txee
a=ice-pwd:VNIFqZIEdn4Grt2PcAAOVFRt
a=ice-options:trickle
a=fingerprint:sha-256 F2:CD:C8:BA:E3:5E:99:B5:91:BA:49:94:8E:ED:BC:16:12:14:7B:EB:C6:B4:6B:FC:99:71:24:91:6D:D6:1C:BC
a=setup:actpass
a=mid:1
a=extmap:1 urn:ietf:params:rtp-hdrext:ssrc-audio-level
a=extmap:4 urn:ietf:params:rtp-hdrext:sdes:mid
a=extmap:2 http://www.webrtc.org/experiments/rtp-hdrext/abs-send-time
a=extmap:3 http://www.ietf.org/id/draft-holmer-rmcat-transport-wide-cc-extensions-01
a=recvonly
a=rtcp-mux
a=rtcp-rsize
a=rtpmap:111 opus/48000/2
a=fmtp:111 minptime=10;useinbandfec=1
a=rtpmap:63 red/48000/2
a=fmtp:63 111/111
a=rtpmap:9 G722/8000
a=rtpmap:0 PCMU/8000
a=rtpmap:8 PCMA/8000
a=rtpmap:13 CN/8000
a=rtpmap:110 telephone-event/48000
a=rtpmap:126 telephone-event/8000
m=video 9 UDP/TLS/RTP/SAVPF 96 97 103 104 107 108 109 114 115 116 117 118 39 40 45 46 98 99 100 101 119 120 123 124 125
c=IN IP4 0.0.0.0
a=rtcp:9 IN IP4 0.0.0.0
a=ice-ufrag:Txee
a=ice-pwd:VNIFqZIEdn4Grt2PcAAOVFRt
a=ice-options:trickle
a=fingerprint:sha-256 F2:CD:C8:BA:E3:5E:99:B5:91:BA:49:94:8E:ED:BC:16:12:14:7B:EB:C6:B4:6B:FC:99:71:24:91:6D:D6:1C:BC
a=setup:actpass
a=mid:2
a=extmap:14 urn:ietf:params:rtp-hdrext:toffset
a=extmap:2 http://www.webrtc.org/experiments/rtp-hdrext/abs-send-time
a=extmap:13 urn:3gpp:video-orientation
a=extmap:3 http://www.ietf.org/id/draft-holmer-rmcat-transport-wide-cc-extensions-01
a=extmap:5 http://www.webrtc.org/experiments/rtp-hdrext/playout-delay
a=extmap:6 http://www.webrtc.org/experiments/rtp-hdrext/video-content-type
a=extmap:7 http://www.webrtc.org/experiments/rtp-hdrext/video-timing
a=extmap:8 http://www.webrtc.org/experiments/rtp-hdrext/color-space
a=extmap:4 urn:ietf:params:rtp-hdrext:sdes:mid
a=extmap:10 urn:ietf:params:rtp-hdrext:sdes:rtp-stream-id
a=extmap:11 urn:ietf:params:rtp-hdrext:sdes:repaired-rtp-stream-id
a=sendrecv
a=msid:- d7957d20-51c9-4373-81bb-68c2569e856a
a=rtcp-mux
a=rtcp-rsize
a=rtpmap:96 VP8/90000
a=rtcp-fb:96 goog-remb
a=rtcp-fb:96 transport-cc
a=rtcp-fb:96 ccm fir
a=rtcp-fb:96 nack
a=rtcp-fb:96 nack pli
a=rtpmap:97 rtx/90000
a=fmtp:97 apt=96
a=rtpmap:103 H264/90000
a=rtcp-fb:103 goog-remb
a=rtcp-fb:103 transport-cc
a=rtcp-fb:103 ccm fir
a=rtcp-fb:103 nack
a=rtcp-fb:103 nack pli
a=fmtp:103 level-asymmetry-allowed=1;packetization-mode=1;profile-level-id=42001f
a=rtpmap:104 rtx/90000
a=fmtp:104 apt=103
a=rtpmap:107 H264/90000
a=rtcp-fb:107 goog-remb
a=rtcp-fb:107 transport-cc
a=rtcp-fb:107 ccm fir
a=rtcp-fb:107 nack
a=rtcp-fb:107 nack pli
a=fmtp:107 level-asymmetry-allowed=1;packetization-mode=0;profile-level-id=42001f
a=rtpmap:108 rtx/90000
a=fmtp:108 apt=107
a=rtpmap:109 H264/90000
a=rtcp-fb:109 goog-remb
a=rtcp-fb:109 transport-cc
a=rtcp-fb:109 ccm fir
a=rtcp-fb:109 nack
a=rtcp-fb:109 nack pli
a=fmtp:109 level-asymmetry-allowed=1;packetization-mode=1;profile-level-id=42e01f
a=rtpmap:114 rtx/90000
a=fmtp:114 apt=109
a=rtpmap:115 H264/90000
a=rtcp-fb:115 goog-remb
a=rtcp-fb:115 transport-cc
a=rtcp-fb:115 ccm fir
a=rtcp-fb:115 nack
a=rtcp-fb:115 nack pli
a=fmtp:115 level-asymmetry-allowed=1;packetization-mode=0;profile-level-id=42e01f
a=rtpmap:116 rtx/90000
a=fmtp:116 apt=115
a=rtpmap:117 H264/90000
a=rtcp-fb:117 goog-remb
a=rtcp-fb:117 transport-cc
a=rtcp-fb:117 ccm fir
a=rtcp-fb:117 nack
a=rtcp-fb:117 nack pli
a=fmtp:117 level-asymmetry-allowed=1;packetization-mode=1;profile-level-id=4d001f
a=rtpmap:118 rtx/90000
a=fmtp:118 apt=117
a=rtpmap:39 H264/90000
a=rtcp-fb:39 goog-remb
a=rtcp-fb:39 transport-cc
a=rtcp-fb:39 ccm fir
a=rtcp-fb:39 nack
a=rtcp-fb:39 nack pli
a=fmtp:39 level-asymmetry-allowed=1;packetization-mode=0;profile-level-id=4d001f
a=rtpmap:40 rtx/90000
a=fmtp:40 apt=39
a=rtpmap:45 AV1/90000
a=rtcp-fb:45 goog-remb
a=rtcp-fb:45 transport-cc
a=rtcp-fb:45 ccm fir
a=rtcp-fb:45 nack
a=rtcp-fb:45 nack pli
a=fmtp:45 level-idx=5;profile=0;tier=0
a=rtpmap:46 rtx/90000
a=fmtp:46 apt=45
a=rtpmap:98 VP9/90000
a=rtcp-fb:98 goog-remb
a=rtcp-fb:98 transport-cc
a=rtcp-fb:98 ccm fir
a=rtcp-fb:98 nack
a=rtcp-fb:98 nack pli
a=fmtp:98 profile-id=0
a=rtpmap:99 rtx/90000
a=fmtp:99 apt=98
a=rtpmap:100 VP9/90000
a=rtcp-fb:100 goog-remb
a=rtcp-fb:100 transport-cc
a=rtcp-fb:100 ccm fir
a=rtcp-fb:100 nack
a=rtcp-fb:100 nack pli
a=fmtp:100 profile-id=2
a=rtpmap:101 rtx/90000
a=fmtp:101 apt=100
a=rtpmap:119 H264/90000
a=rtcp-fb:119 goog-remb
a=rtcp-fb:119 transport-cc
a=rtcp-fb:119 ccm fir
a=rtcp-fb:119 nack
a=rtcp-fb:119 nack pli
a=fmtp:119 level-asymmetry-allowed=1;packetization-mode=1;profile-level-id=64001f
a=rtpmap:120 rtx/90000
a=fmtp:120 apt=119
a=rtpmap:123 red/90000
a=rtpmap:124 rtx/90000
a=fmtp:124 apt=123
a=rtpmap:125 ulpfec/90000
a=ssrc-group:FID 3573058693 2436256575
a=ssrc:3573058693 cname:RjFfzNPobxWehiyS
a=ssrc:3573058693 msid:- d7957d20-51c9-4373-81bb-68c2569e856a
a=ssrc:2436256575 cname:RjFfzNPobxWehiyS
a=ssrc:2436256575 msid:- d7957d20-51c9-4373-81bb-68c2569e856a
```
