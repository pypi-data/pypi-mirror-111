(this.webpackJsonpstreamlit_webrtc=this.webpackJsonpstreamlit_webrtc||[]).push([[0],{113:function(e,t,n){"use strict";n.r(t);var a=n(0),i=n.n(a),r=n(21),o=n.n(r),c=n(80),s=n(153),l=n(155),u=n(17),d=n(5),p=n.n(d),v=n(8),b=n(1),f=n(4),g=n(11),j=n(10),m=n(2),h=n(3),O=n(25),y=n(120),x=n(83),S=n(156),C=n(76),E=n(78),I=n.n(E),k=n(12),w=function(e){var t=e.theme,n=i.a.useMemo((function(){if(null!=t){var e=I.a.scale([t.textColor,t.backgroundColor]).mode("lab");return Object(c.a)({palette:{primary:{main:t.primaryColor},background:{default:t.backgroundColor,paper:t.secondaryBackgroundColor},text:{primary:t.textColor,secondary:e(.1).hex(),disabled:e(.5).hex()}},typography:{fontFamily:t.font}})}}),[t]);return null==n?Object(k.jsx)(k.Fragment,{children:e.children}):Object(k.jsx)(s.a,{theme:n,children:e.children})},D={width:"100%"},N=function(e){Object(a.useEffect)((function(){O.a.setFrameHeight()}));var t=e.stream.getVideoTracks().length>0,n=Object(a.useCallback)((function(t){t&&(t.srcObject=e.stream)}),[e.stream]),i=Object(a.useCallback)((function(){return O.a.setFrameHeight()}),[]);return t?Object(k.jsx)("video",{style:D,ref:n,autoPlay:!0,controls:!0,onCanPlay:i}):Object(k.jsx)("audio",{ref:n,autoPlay:!0,controls:!0})},T=i.a.memo(N),R=n(114),_=n(117),V=n(154),L=n(79),M=n.n(L),P=Object(R.a)((function(e){return{paper:{padding:e.spacing(4),display:"flex",justifyContent:"center",alignItems:"center"}}})),B=function(e){Object(a.useEffect)((function(){O.a.setFrameHeight()}));var t=P();return Object(k.jsx)(_.a,{className:t.paper,elevation:0,children:e.loading?Object(k.jsx)(V.a,{}):Object(k.jsx)(M.a,{fontSize:"large"})})},F=i.a.memo(B),Y=n(16);function H(e,t,n){var a=e||{};return t&&(!0===a.video?a.video={deviceId:t}:"object"!==typeof a.video&&null!=a.video||(a.video=Object(Y.a)(Object(Y.a)({},a.video),{},{deviceId:t}))),n&&(!0===a.audio?a.audio={deviceId:n}:"object"!==typeof a.audio&&null!=a.audio||(a.audio=Object(Y.a)(Object(Y.a)({},a.audio),{},{deviceId:n}))),a}var U=function(e){return"RECVONLY"===e||"SENDONLY"===e||"SENDRECV"===e},A=function(e){return e.createOffer().then((function(t){return console.log("Created offer:",t),e.setLocalDescription(t)})).then((function(){return console.log("Wait for ICE gethering..."),new Promise((function(t){if("complete"===e.iceGatheringState)t();else{e.addEventListener("icegatheringstatechange",(function n(){"complete"===e.iceGatheringState&&(e.removeEventListener("icegatheringstatechange",n),t())}))}}))})).then((function(){return e.localDescription})).catch((function(e){throw console.error(e),e}))},J=function(e){Object(m.a)(n,e);var t=Object(h.a)(n);function n(e){var a;return Object(b.a)(this,n),(a=t.call(this,e)).pc=void 0,a.processAnswerInner=function(){var e=Object(v.a)(p.a.mark((function e(t,n){var a;return p.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return a=JSON.parse(n),console.log("Receive answer sdpOffer",a),e.next=4,t.setRemoteDescription(a);case 4:console.log("Remote description is set");case 5:case"end":return e.stop()}}),e)})));return function(t,n){return e.apply(this,arguments)}}(),a.processAnswer=function(e,t){a.processAnswerInner(e,t).catch((function(e){return a.setState({error:e}),a.stop()})).finally((function(){return a.setState({signaling:!1})}))},a.startInner=Object(v.a)(p.a.mark((function e(){var t,n,i,r,o,c,s,l,d,v,b;return p.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(n=a.props.args.mode,U(n)){e.next=3;break}throw new Error("Invalid mode ".concat(n));case 3:if(a.setState({signaling:!0,stream:null,error:null}),i=(null===(t=a.props.args.settings)||void 0===t?void 0:t.rtc_configuration)||{},console.log("RTCConfiguration:",i),r=new RTCPeerConnection(i),"SENDRECV"!==n&&"RECVONLY"!==n||r.addEventListener("track",(function(e){var t=e.streams[0];a.setState({stream:t})})),"SENDRECV"!==n&&"SENDONLY"!==n){e.next=23;break}if(l=H(null===(o=a.props.args.settings)||void 0===o?void 0:o.media_stream_constraints,null===(c=a.state.videoInput)||void 0===c?void 0:c.deviceId,null===(s=a.state.audioInput)||void 0===s?void 0:s.deviceId),console.log("MediaStreamConstraints:",l),!l.audio&&!l.video){e.next=20;break}if(null!=navigator.mediaDevices){e.next=14;break}throw new Error("navigator.mediaDevices is undefined. It seems the current document is not loaded securely.");case 14:if(null!=navigator.mediaDevices.getUserMedia){e.next=16;break}throw new Error("getUserMedia is not implemented in this browser");case 16:return e.next=18,navigator.mediaDevices.getUserMedia(l);case 18:(d=e.sent).getTracks().forEach((function(e){r.addTrack(e,d)}));case 20:if("SENDONLY"===n){v=Object(u.a)(r.getTransceivers());try{for(v.s();!(b=v.n()).done;)b.value.direction="sendonly"}catch(p){v.e(p)}finally{v.f()}}e.next=24;break;case 23:"RECVONLY"===n&&(r.addTransceiver("video",{direction:"recvonly"}),r.addTransceiver("audio",{direction:"recvonly"}));case 24:return a.setState({playing:!0}),console.log("transceivers",r.getTransceivers()),a.pc=r,e.next=29,A(r).then((function(e){null!=e?(console.log("Send sdpOffer",e.toJSON()),O.a.setComponentValue({sdpOffer:e.toJSON(),playing:!0})):console.warn("Failed to create an offer SDP")}));case 29:case"end":return e.stop()}}),e)}))),a.start=function(){a.startInner().catch((function(e){return a.setState({signaling:!1,error:e})}))},a.stopInner=Object(v.a)(p.a.mark((function e(){var t;return p.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(t=a.pc,a.pc=void 0,a.setState({playing:!1},(function(){return O.a.setComponentValue({playing:!1})})),null!=t){e.next=5;break}return e.abrupt("return",Promise.resolve());case 5:return t.getTransceivers&&t.getTransceivers().forEach((function(e){e.stop&&e.stop()})),t.getSenders().forEach((function(e){var t;null===(t=e.track)||void 0===t||t.stop()})),e.abrupt("return",new Promise((function(e){setTimeout((function(){t.close(),e()}),500)})));case 8:case"end":return e.stop()}}),e)}))),a.stop=function(){a.setState({stopping:!0}),a.stopInner().catch((function(e){return a.setState({error:e})})).finally((function(){a.setState({stopping:!1,stream:null})}))},a.reconcilePlayingState=function(){var e=a.props.args.desired_playing_state;null!=e&&(!0!==e||a.state.playing||a.state.signaling?!1===e&&(a.state.playing||a.state.signaling)&&a.stop():a.start())},a.handleDeviceSelect=function(e,t){a.setState({videoInput:e,audioInput:t})},a.render=function(){var e,t,n=a.props.args.desired_playing_state,i=a.props.disabled||a.state.signaling||a.state.stopping||null!=n,r=a.props.args.mode,o={videoEnabled:!(t=null===(e=a.props.args.settings)||void 0===e?void 0:e.media_stream_constraints)||!!t.video,audioEnabled:!t||!!t.audio},c=o.videoEnabled,s=o.audioEnabled,l=U(r)&&function(e){return"SENDRECV"===e||"RECVONLY"===e}(r),u=U(r)&&function(e){return"SENDRECV"===e||"SENDONLY"===e}(r);return Object(k.jsx)(w,{theme:a.props.theme,children:Object(k.jsxs)(y.a,{children:[a.state.error&&Object(k.jsxs)(S.a,{severity:"error",children:[a.state.error.name,": ",a.state.error.message]}),Object(k.jsx)(y.a,{py:1,children:a.state.stream?Object(k.jsx)(T,{stream:a.state.stream}):l&&Object(k.jsx)(F,{loading:a.state.signaling})}),Object(k.jsxs)(y.a,{display:"flex",justifyContent:"space-between",children:[a.state.playing?Object(k.jsx)(x.a,{variant:"contained",onClick:a.stop,disabled:i,children:"Stop"}):Object(k.jsx)(x.a,{variant:"contained",color:"primary",onClick:a.start,disabled:i,children:"Start"}),u&&Object(k.jsx)(C.a,{videoEnabled:c,audioEnabled:s,onSelect:a.handleDeviceSelect,value:{video:a.state.videoInput,audio:a.state.audioInput}})]})]})})},a.state={signaling:!1,playing:!1,stopping:!1,videoInput:null,audioInput:null,stream:null,error:null},a}return Object(f.a)(n,[{key:"componentDidMount",value:function(){Object(g.a)(Object(j.a)(n.prototype),"componentDidMount",this).call(this),this.reconcilePlayingState()}},{key:"componentDidUpdate",value:function(e){if(Object(g.a)(Object(j.a)(n.prototype),"componentDidUpdate",this).call(this),this.reconcilePlayingState(),null!=this.pc){var t=this.pc;if(null==t.remoteDescription){var a=this.props.args.sdp_answer_json;a!==e.args.sdp_answer_json&&a&&this.state.signaling&&this.processAnswer(t,a)}}}}]),n}(O.b),W=Object(O.c)(J),G=Object(c.a)({overrides:{MuiCssBaseline:{"@global":{body:{backgroundColor:"initial"}}}}});o.a.render(Object(k.jsx)(i.a.StrictMode,{children:Object(k.jsxs)(s.a,{theme:G,children:[Object(k.jsx)(l.a,{}),Object(k.jsx)(W,{})]})}),document.getElementById("root"))},76:function(e,t,n){"use strict";(function(e){var a=n(17),i=n(15),r=n(0),o=n.n(r),c=n(25),s=n(120),l=n(114),u=n(83),d=n(72),p=n(85),v=n(84),b=n(122),f=n(118),g=n(117),j=n(12),m=Object(l.a)((function(e){return{paper:{padding:e.spacing(2)},formControl:{maxWidth:"80vw",margin:e.spacing(1),minWidth:120,display:"flex"},formButtonControl:{margin:e.spacing(2),marginBottom:e.spacing(1),minWidth:120,display:"flex"},selectEmpty:{marginTop:e.spacing(2)}}})),h=function(t){var n=t.labelId,a=t.value,i=t.devices,o=t.onChange,c=m(),s=Object(r.useCallback)((function(e){var t=i.find((function(t){return t.deviceId===e.target.value}));o(t||null)}),[i,o]);return 0===i.length?Object(j.jsx)(v.a,{value:"",disabled:!0,children:Object(j.jsx)("option",{"aria-label":"None",value:""})}):null==a?(e((function(){return o(i[0])})),null):Object(j.jsx)(v.a,{labelId:n,value:a.deviceId,onChange:s,className:c.selectEmpty,children:i.map((function(e){return Object(j.jsx)(b.a,{value:e.deviceId,children:e.label},e.deviceId)}))})},O=function(e){var t=e.open,n=e.anchorEl,a=e.videoEnabled,o=e.audioEnabled,s=e.value,l=e.devicesMap,v=e.onSubmit,b=Object(r.useState)(null),O=Object(i.a)(b,2),y=O[0],x=O[1],S=Object(r.useState)(null),C=Object(i.a)(S,2),E=C[0],I=C[1];Object(r.useEffect)((function(){x(l.video.find((function(e){var t;return e.deviceId===(null===(t=s.video)||void 0===t?void 0:t.deviceId)}))||null),I(l.audio.find((function(e){var t;return e.deviceId===(null===(t=s.audio)||void 0===t?void 0:t.deviceId)}))||null)}),[l,s]);var k=Object(r.useCallback)((function(e){e.preventDefault(),v(a?y:null,o?E:null)}),[v,a,o,y,E]),w=m(),D=Object(r.useRef)(),N=Object(r.useCallback)((function(e){if(e)setTimeout((function(){var t=document.getElementsByTagName("body")[0];D.current=t.style.height;var n=window.getComputedStyle(e),a=new WebKitCSSMatrix(n.transform).m42+e.getBoundingClientRect().height;a>document.body.scrollHeight&&(t.style.height="".concat(a,"px"),c.a.setFrameHeight())}),0);else{var t=document.getElementsByTagName("body")[0];null!=D.current&&(t.style.height=D.current),c.a.setFrameHeight()}}),[]);return Object(j.jsx)(f.a,{ref:N,open:t,anchorEl:n,placement:"left-end",children:Object(j.jsx)(g.a,{className:w.paper,children:Object(j.jsxs)("form",{onSubmit:k,children:[a&&Object(j.jsxs)(d.a,{className:w.formControl,children:[Object(j.jsx)(p.a,{id:"video-input-select",children:"Video input"}),Object(j.jsx)(h,{labelId:"video-input-select",devices:l.video,value:y,onChange:x})]}),o&&Object(j.jsxs)(d.a,{className:w.formControl,children:[Object(j.jsx)(p.a,{id:"audio-input-select",children:"Audio input"}),Object(j.jsx)(h,{labelId:"audio-input-select",devices:l.audio,value:E,onChange:I})]}),Object(j.jsx)(d.a,{className:w.formButtonControl,children:Object(j.jsx)(u.a,{type:"submit",variant:"contained",color:"primary",children:"OK"})})]})})})},y=function(e){var t=e.videoEnabled,n=e.audioEnabled,c=e.value,l=e.onSelect,d=Object(r.useState)(!1),p=Object(i.a)(d,2),v=p[0],b=p[1],f=o.a.useState(null),g=Object(i.a)(f,2),m=g[0],h=g[1],y=Object(r.useState)(),x=Object(i.a)(y,2),S=x[0],C=x[1],E=Object(r.useState)(!1),I=Object(i.a)(E,2),k=I[0],w=I[1],D=Object(r.useCallback)((function(e){var t,n;if(h(e.currentTarget),"function"!==typeof(null===(t=navigator)||void 0===t||null===(n=t.mediaDevices)||void 0===n?void 0:n.enumerateDevices))return C(void 0),void w(!0);navigator.mediaDevices.enumerateDevices().then((function(e){var t,n=[],i=[],r=Object(a.a)(e);try{for(r.s();!(t=r.n()).done;){var o=t.value;"videoinput"===o.kind?n.push(o):"audioinput"===o.kind&&i.push(o)}}catch(c){r.e(c)}finally{r.f()}C({video:n,audio:i}),b(!0)}))}),[]),N=Object(r.useCallback)((function(){return b(!1)}),[]),T=Object(r.useCallback)((function(e,t){C(void 0),b(!1),l(e,t)}),[l]);return Object(j.jsxs)(s.a,{children:[k&&Object(j.jsx)("p",{children:"Unavailable"}),S&&Object(j.jsx)(O,{open:v,anchorEl:m,videoEnabled:t,audioEnabled:n,value:c,devicesMap:S,onSubmit:T}),Object(j.jsx)(u.a,{onClick:v?N:D,children:"Select device"})]})};t.a=o.a.memo(y)}).call(this,n(102).setImmediate)}},[[113,1,2]]]);
//# sourceMappingURL=main.3f98995c.chunk.js.map