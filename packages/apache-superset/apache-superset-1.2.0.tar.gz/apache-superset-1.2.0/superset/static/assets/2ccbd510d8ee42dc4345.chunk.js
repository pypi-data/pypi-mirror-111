(window.webpackJsonp=window.webpackJsonp||[]).push([[76],{4525:function(t,e,a){"use strict";a.d(e,"b",(function(){return c})),a.d(e,"a",(function(){return r}));var n=a(47),u=a(17);const c=n.j.div`
  height: ${({height:t})=>t};
  width: ${({width:t})=>t};
`,r=Object(n.j)(u.s)`
  width: 100%;
`},4883:function(t,e,a){"use strict";a.r(e),a.d(e,"default",(function(){return o}));a(40);var n=a(47),u=a(0),c=a(783),r=a(4525),i=a(1);const s=Object(n.j)(r.b)`
  overflow-x: scroll;
`;function o(t){const{formData:e,setDataMask:a,width:n,filterState:r}=t,{defaultValue:o}=e,[l,f]=Object(u.useState)(null!=o?o:"Last week"),w=t=>{f(t),a({extraFormData:{time_range:t},filterState:{value:t}})};return Object(u.useEffect)(()=>{var t;w(null!=(t=r.value)?t:"Last week")},[r.value]),Object(u.useEffect)(()=>{w(null!=o?o:"Last week")},[o]),Object(i.h)(s,{width:n},Object(i.h)(c.a,{value:l,name:"time_range",onChange:w}))}}}]);