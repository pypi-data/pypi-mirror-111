(window.webpackJsonp=window.webpackJsonp||[]).push([[4],{195:function(e,t,a){"use strict";a.d(t,"a",(function(){return u}));var l=a(26),n=a.n(l),o=a(117),i=(a(0),a(17)),r=a(47),c=a(48),s=a(174),d=a(1);function u(e){const{type:t="info",description:a,showIcon:l=!0,closable:u=!0,children:g}=e,p=Object(r.l)(),{colors:h,typography:b}=p,{alert:m,error:f,info:j,success:v}=h;let O=j,x=s.a.InfoSolid;return"error"===t?(O=f,x=s.a.ErrorSolid):"warning"===t?(O=m,x=s.a.AlertSolid):"success"===t&&(O=v,x=s.a.CircleCheckSolid),Object(d.h)(i.a,n()({role:"alert",showIcon:l,icon:Object(d.h)(x,{"aria-label":`${t} icon`}),closeText:u&&Object(d.h)(c.a,{name:"x-small","aria-label":"close icon"}),css:Object(o.a)({padding:"6px 10px",alignItems:"flex-start",border:0,backgroundColor:O.light2,"& .ant-alert-icon":{marginRight:10},"& .ant-alert-message":{color:O.dark2,fontSize:b.sizes.m,fontWeight:a?b.weights.bold:b.weights.normal},"& .ant-alert-description":{color:O.dark2,fontSize:b.sizes.m}},";label:Alert;")},e),g)}},4526:function(e,t,a){"use strict";a.d(t,"a",(function(){return ze})),a.d(t,"b",(function(){return Ee}));var l=a(11),n=a.n(l),o=a(28),i=a.n(o),r=a(49),c=a.n(r),s=a(26),d=a.n(s),u=a(47),g=a(14),p=a(0),h=a.n(p),b=a(17),m=a(195);function f(){return(f=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var a=arguments[t];for(var l in a)Object.prototype.hasOwnProperty.call(a,l)&&(e[l]=a[l])}return e}).apply(this,arguments)}var j=p.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M83.195 1.366L103 24v38a4 4 0 01-4 4H20a4 4 0 01-4-4V24L35.805 1.366A4 4 0 0138.815 0h41.37a4 4 0 013.01 1.366zM101 26v36a2 2 0 01-2 2H20a2 2 0 01-2-2V26h17.25A4.75 4.75 0 0140 30.75a6.75 6.75 0 006.75 6.75h25.5A6.75 6.75 0 0079 30.75 4.75 4.75 0 0183.75 26H101zm-.658-2L81.69 2.683A2 2 0 0080.185 2h-41.37a2 2 0 00-1.505.683L18.657 24H35.25A6.75 6.75 0 0142 30.75a4.75 4.75 0 004.75 4.75h25.5A4.75 4.75 0 0077 30.75 6.75 6.75 0 0183.75 24h16.592z",fill:"#D1D1D1"}),v=p.createElement("path",{d:"M16 53.29C6.074 55.7 0 58.94 0 62.5 0 69.956 26.64 76 59.5 76S119 69.956 119 62.5c0-3.56-6.074-6.799-16-9.21V62a4 4 0 01-4 4H20a4 4 0 01-4-4v-8.71z",fill:"#F2F2F2"});function O(e){return p.createElement("svg",f({width:119,height:76,fill:"none"},e),j,v)}a.p;var x=a(5),y=a.n(x),w=a(44),S=a(48),C=a(4688),k=a(667),$=(a(40),a(1));const I=u.j.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(459px, 1fr));
  grid-gap: ${({theme:e})=>8*e.gridUnit}px;
`,F=u.j.div`
  border: 2px solid transparent;
  &.card-selected {
    border: 2px solid ${({theme:e})=>e.colors.primary.base};
  }
  &.bulk-select {
    cursor: pointer;
  }
`;function R({bulkSelectEnabled:e,loading:t,prepareRow:a,renderCard:l,rows:o}){var i;return l?Object($.h)(I,null,t&&0===o.length&&n()(i=[...new Array(25)]).call(i,(e,a)=>Object($.h)("div",{key:a},l({loading:t}))),o.length>0&&n()(o).call(o,n=>l?(a(n),Object($.h)(F,{className:y()({"card-selected":e&&n.isSelected,"bulk-select":e}),key:n.id,onClick:t=>{return a=t,l=n.toggleRowSelected,void(e&&(a.preventDefault(),a.stopPropagation(),l()));var a,l},role:"none"},l({...n.original,loading:t}))):null)):null}var z=a(171);const E=u.j.div`
  position: relative;
`,P=u.j.input`
  width: 200px;
  height: ${({theme:e})=>8*e.gridUnit}px;
  background-image: none;
  border: 1px solid ${({theme:e})=>e.colors.secondary.light2};
  border-radius: 4px;
  box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.075);
  padding: 4px 28px;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
  &:focus {
    outline: none;
  }
`,M="\n  position: absolute;\n  z-index: 2;\n  display: block;\n  cursor: pointer;\n",_=Object(u.j)(S.a)`
  ${M};
  top: 4px;
  left: 2px;
`,T=Object(u.j)(S.a)`
  ${M};
  right: 0px;
  top: 4px;
`;function A({onChange:e,onClear:t,onSubmit:a,placeholder:l="Search",name:n,value:o}){return Object($.h)(E,null,Object($.h)(_,{role:"button",name:"search",onClick:()=>a()}),Object($.h)(P,{onKeyDown:e=>{"Enter"===e.key&&a()},onBlur:()=>a(),placeholder:l,onChange:e,value:o,name:n}),o&&Object($.h)(T,{role:"button",name:"cancel-x",onClick:()=>t()}))}const V=u.j.div`
  display: inline-flex;
  margin-right: 2em;
  font-size: ${({theme:e})=>e.typography.sizes.s}px;
  align-items: center;
`,N=u.j.label`
  font-weight: bold;
  margin: 0 0.4em 0 0;
`;function U({Header:e,name:t,initialValue:a,onSubmit:l}){const[n,o]=Object(p.useState)(a||"");return Object($.h)(V,null,Object($.h)(A,{placeholder:e,name:t,value:n,onChange:e=>{o(e.currentTarget.value)},onSubmit:()=>{n&&l(n)},onClear:()=>{o(""),l("")}}))}var B=a(59),L=a.n(B),D=a(58),H=a(43),W=a.n(H),q=a(1406),G=a.n(q),J=a(54),K=a.n(J),X=a(33),Q=a.n(X),Y=a(55),Z=a.n(Y),ee=a(250),te=a.n(ee),ae=a(380),le=a(2094),ne=a(96),oe=a.n(ne);const ie={encode:e=>void 0===e?void 0:oe.a.encode(e),decode:e=>void 0===e||Z()(e)?void 0:oe.a.decode(e)};class re extends Error{constructor(){super(...arguments),this.name="ListViewError"}}function ce(e,t){return n()(e).call(e,({id:e,urlDisplay:a,operator:l})=>({id:e,urlDisplay:a,operator:l,value:t[a||e]}))}function se(e,t){var a;const l=[],n={};return i()(a=W()(e)).call(a,t=>{const a={id:t,value:e[t]};n[t]=a,l.push(a)}),i()(t).call(t,e=>{const t=e.urlDisplay||e.id,a=n[t];a&&(a.operator=e.operator,a.id=e.id)}),l}function de({fetchData:e,columns:t,data:a,count:l,initialPageSize:o,initialFilters:r=[],initialSort:c=[],bulkSelectMode:s=!1,bulkSelectColumnConfig:d,renderCard:u=!1,defaultViewMode:g="card"}){const[h,b]=Object(le.d)({filters:ie,pageIndex:le.a,sortColumn:le.c,sortOrder:le.c,viewMode:le.c}),m=Object(p.useMemo)(()=>h.sortColumn&&h.sortOrder?[{id:h.sortColumn,desc:"desc"===h.sortOrder}]:c,[h.sortColumn,h.sortOrder]),f={filters:h.filters?se(h.filters,r):[],pageIndex:h.pageIndex||0,pageSize:o,sortBy:m},[j,v]=Object(p.useState)(h.viewMode||(u?g:"table")),O=Object(p.useMemo)(()=>{const e=n()(t).call(t,e=>({...e,filter:"exact"}));return s?[d,...e]:e},[s,t]),{getTableProps:x,getTableBodyProps:y,headerGroups:w,rows:S,prepareRow:C,canPreviousPage:k,canNextPage:$,pageCount:I,gotoPage:F,setAllFilters:R,selectedFlatRows:z,toggleAllRowsSelected:E,state:{pageIndex:P,pageSize:M,sortBy:_,filters:T}}=Object(ae.useTable)({columns:O,count:l,data:a,disableFilters:!0,disableSortRemove:!0,initialState:f,manualFilters:!0,manualPagination:!0,manualSortBy:!0,autoResetFilters:!1,pageCount:Math.ceil(l/o)},ae.useFilters,ae.useSortBy,ae.usePagination,ae.useRowState,ae.useRowSelect),[A,V]=Object(p.useState)(h.filters&&r.length?ce(r,h.filters):[]);Object(p.useEffect)(()=>{r.length&&V(ce(r,h.filters?h.filters:{}))},[r]),Object(p.useEffect)(()=>{const t={};i()(A).call(A,e=>{if(void 0!==e.value&&("string"!=typeof e.value||e.value.length>0)){const a=e.urlDisplay||e.id;t[a]=e.value}});const a={filters:W()(t).length?t:void 0,pageIndex:P};_[0]&&(a.sortColumn=_[0].id,a.sortOrder=_[0].desc?"desc":"asc"),u&&(a.viewMode=j);const l=void 0!==h.pageIndex&&a.pageIndex!==h.pageIndex?"push":"replace";b(a,l),e({pageIndex:P,pageSize:M,sortBy:_,filters:T})},[e,P,M,_,T]),Object(p.useEffect)(()=>{te()(f.pageIndex,P)||F(f.pageIndex)},[h]);return{canNextPage:$,canPreviousPage:k,getTableBodyProps:y,getTableProps:x,gotoPage:F,headerGroups:w,pageCount:I,prepareRow:C,rows:S,selectedFlatRows:z,setAllFilters:R,state:{pageIndex:P,pageSize:M,sortBy:_,filters:T,internalFilters:A,viewMode:j},toggleAllRowsSelected:E,applyFilterValue:(e,t)=>{V(a=>{if(a[e].value===t)return a;const l={...a[e],value:t},o=function(e,t,a){const l=L()(e).call(e,(e,a)=>t===a);return[...K()(e).call(e,0,t),{...l,...a},...K()(e).call(e,t+1)]}(a,e,l);var i,r,c;return R((i=o,G()(r=n()(c=Q()(i).call(i,e=>!(void 0===e.value||Z()(e.value)&&!e.value.length))).call(c,({value:e,operator:t,id:a})=>"between"===t&&Z()(e)?[{value:e[0],operator:"gt",id:a},{value:e[1],operator:"lt",id:a}]:{value:e,operator:t,id:a})).call(r))),F(0),o})},setViewMode:v}}const ue={container:(e,{getValue:t})=>({...e,minWidth:`${Math.min(12,Math.max(5,3+t()[0].label.length/2))}em`}),control:e=>({...e,borderWidth:0,boxShadow:"none",cursor:"pointer",backgroundColor:"transparent"})};var ge=Object(z.c)((function({Header:e,emptyLabel:t="None",fetchSelects:a,initialValue:l,onSelect:n,paginate:o=!1,selects:i=[],theme:r}){const c={spacing:{baseUnit:2,fontSize:r.typography.sizes.s,minWidth:"5em"}},s={label:t,value:"CLEAR_SELECT_FILTER_VALUE"},d=[s,...i];let u=s;if(!a){const e=L()(d).call(d,e=>e.value===l);e&&(u=e)}const[g,h]=Object(p.useState)(u),b=e=>{null!==e&&(n("CLEAR_SELECT_FILTER_VALUE"===e.value?void 0:e.value),h(e))};return Object($.h)(V,null,Object($.h)(N,null,e,":"),a?Object($.h)(D.g,{defaultOptions:!0,themeConfig:c,stylesConfig:ue,value:g,onChange:b,loadOptions:async(e,t,{page:n})=>{let i=e||n>0?[]:[s],r=o;if(a){const t=await a(e,n);t.length||(r=!1),i=[...i,...t];const o=L()(i).call(i,e=>e.value===l);o&&h(o)}return{options:i,hasMore:r,additional:{page:n+1}}},placeholder:t,clearable:!1,additional:{page:0}}):Object($.h)(D.h,{themeConfig:c,stylesConfig:ue,value:g,options:d,onChange:b,clearable:!1}))})),pe=a(38),he=a.n(pe),be=a(989);const me=Object(u.j)(be.b)`
  padding: 0 11px;
  transform: translateX(-7px);
`,fe=Object(u.j)(V)`
  margin-right: 1em;
`;function je({Header:e,initialValue:t,onSubmit:a}){const[l,n]=Object(p.useState)(null!=t?t:null),o=Object(p.useMemo)(()=>!l||Z()(l)&&!l.length?null:[he()(l[0]),he()(l[1])],[l]);return Object($.h)(fe,null,Object($.h)(N,null,e,":"),Object($.h)(me,{showTime:!0,bordered:!1,value:o,onChange:e=>{var t,l,o,i;if(!e)return n(null),void a([]);const r=[null!=(t=null==(l=e[0])?void 0:l.valueOf())?t:0,null!=(o=null==(i=e[1])?void 0:i.valueOf())?o:0];n(r),a(r)}}))}const ve=u.j.div`
  display: inline-block;
`;var Oe=Object(z.c)((function({filters:e,internalFilters:t=[],updateFilterValue:a}){return Object($.h)(ve,null,n()(e).call(e,({Header:e,fetchSelects:l,id:n,input:o,paginate:i,selects:r,unfilteredLabel:c},s)=>{const d=t[s]&&t[s].value;return"select"===o?Object($.h)(ge,{Header:e,emptyLabel:c,fetchSelects:l,initialValue:d,key:n,name:n,onSelect:e=>a(s,e),paginate:i,selects:r}):"search"===o&&"string"==typeof e?Object($.h)(U,{Header:e,initialValue:d,key:n,name:n,onSubmit:e=>a(s,e)}):"datetime_range"===o?Object($.h)(je,{Header:e,initialValue:d,key:n,name:n,onSubmit:e=>a(s,e)}):null}))}));const xe=u.j.label`
  font-weight: bold;
  line-height: 27px;
  margin: 0 0.4em 0 0;
`,ye=u.j.div`
  display: inline-flex;
  font-size: ${({theme:e})=>e.typography.sizes.s}px;
  padding-top: ${({theme:e})=>e.gridUnit}px;
  text-align: left;
`;const we=Object(z.c)((function({onChange:e,options:t,selectStyles:a,theme:l,value:n}){const o={spacing:{baseUnit:1,fontSize:l.typography.sizes.s,minWidth:"5em"}};return Object($.h)(D.h,{clearable:!1,onChange:e,options:t,stylesConfig:a,themeConfig:o,value:n})})),Se=({initialSort:e,onChange:t,options:a,pageIndex:l,pageSize:n})=>{const o=e&&L()(a).call(a,({id:t})=>t===e[0].id),[i,r]=Object(p.useState)(o||a[0]);return Object($.h)(ye,null,Object($.h)(xe,null,Object(g.e)("Sort:")),Object($.h)(we,{onChange:e=>(e=>{r(e);const a=[{id:e.id,desc:e.desc}];t({pageIndex:l,pageSize:n,sortBy:a,filters:[]})})(e),options:a,selectStyles:ue,value:i}))},Ce=u.j.div`
  text-align: center;

  .superset-list-view {
    text-align: left;
    border-radius: 4px 0;
    margin: 0 ${({theme:e})=>4*e.gridUnit}px;

    .header {
      display: flex;
      padding-bottom: ${({theme:e})=>4*e.gridUnit}px;

      .header-left {
        display: flex;
        flex: 5;
      }
      .header-right {
        flex: 1;
        text-align: right;
      }
    }

    .body.empty table {
      margin-bottom: 0;
    }

    .body {
      overflow-x: auto;
    }

    .ant-empty {
      .ant-empty-image {
        height: auto;
      }
    }
  }

  .pagination-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    margin-bottom: ${({theme:e})=>4*e.gridUnit}px;
  }

  .row-count-container {
    margin-top: ${({theme:e})=>2*e.gridUnit}px;
    color: ${({theme:e})=>e.colors.grayscale.base};
  }
`,ke=Object(u.j)(m.a)`
  border-radius: 0;
  margin-bottom: 0;
  color: #3d3d3d;
  background-color: ${({theme:e})=>e.colors.primary.light4};

  .selectedCopy {
    display: inline-block;
    padding: ${({theme:e})=>2*e.gridUnit}px 0;
  }

  .deselect-all {
    color: #1985a0;
    margin-left: ${({theme:e})=>4*e.gridUnit}px;
  }

  .divider {
    margin: ${({theme:{gridUnit:e}})=>`${2*-e}px 0 ${2*-e}px ${4*e}px`};
    width: 1px;
    height: ${({theme:e})=>8*e.gridUnit}px;
    box-shadow: inset -1px 0px 0px #dadada;
    display: inline-flex;
    vertical-align: middle;
    position: relative;
  }
`,$e={Cell:({row:e})=>Object($.h)(C.a,d()({},e.getToggleRowSelectedProps(),{id:e.id})),Header:({getToggleAllRowsSelectedProps:e})=>Object($.h)(C.a,d()({},e(),{id:"header-toggle-all"})),id:"selection",size:"sm"},Ie=u.j.div`
  padding-right: ${({theme:e})=>4*e.gridUnit}px;
  display: inline-block;

  .toggle-button {
    display: inline-block;
    border-radius: ${({theme:e})=>e.gridUnit/2}px;
    padding: ${({theme:e})=>e.gridUnit}px;
    padding-bottom: 0;

    &:first-of-type {
      margin-right: ${({theme:e})=>2*e.gridUnit}px;
    }
  }

  .active {
    background-color: ${({theme:e})=>e.colors.grayscale.base};
    svg {
      color: ${({theme:e})=>e.colors.grayscale.light5};
    }
  }
`,Fe=u.j.div`
  padding: ${({theme:e})=>40*e.gridUnit}px 0;

  &.table {
    background: ${({theme:e})=>e.colors.grayscale.light5};
  }
`,Re=({mode:e,setMode:t})=>Object($.h)(Ie,null,Object($.h)("div",{role:"button",tabIndex:0,onClick:e=>{e.currentTarget.blur(),t("card")},className:y()("toggle-button",{active:"card"===e})},Object($.h)(S.a,{name:"card-view"})),Object($.h)("div",{role:"button",tabIndex:0,onClick:e=>{e.currentTarget.blur(),t("table")},className:y()("toggle-button",{active:"table"===e})},Object($.h)(S.a,{name:"list-view"})));var ze,Ee=function({columns:e,data:t,count:a,pageSize:l,fetchData:o,loading:r,initialSort:s=[],className:d="",filters:u=[],bulkActions:m=[],bulkSelectEnabled:f=!1,disableBulkSelect:j=(()=>{}),renderBulkSelectCopy:v=(e=>Object(g.e)("%s Selected",e.length)),renderCard:x,cardSortSelectOptions:y,defaultViewMode:S="card",highlightRowId:C,emptyState:I={}}){const{getTableProps:F,getTableBodyProps:z,headerGroups:E,rows:P,prepareRow:M,pageCount:_=1,gotoPage:T,applyFilterValue:A,selectedFlatRows:V,toggleAllRowsSelected:N,setViewMode:U,state:{pageIndex:B,pageSize:L,internalFilters:D,viewMode:H}}=de({bulkSelectColumnConfig:$e,bulkSelectMode:f&&Boolean(m.length),columns:e,count:a,data:t,fetchData:o,initialPageSize:l,initialSort:s,initialFilters:u,renderCard:Boolean(x),defaultViewMode:S}),W=Boolean(u.length);if(W){const t=c()(e).call(e,(e,t)=>({...e,[t.id||t.accessor]:!0}),{});i()(u).call(u,e=>{if(!t[e.id])throw new re(`Invalid filter config, ${e.id} is not present in columns`)})}const q=Boolean(x);return Object(p.useEffect)(()=>{f||N(!1)},[f,N]),Object($.h)(Ce,null,Object($.h)("div",{className:`superset-list-view ${d}`},Object($.h)("div",{className:"header"},Object($.h)("div",{className:"header-left"},q&&Object($.h)(Re,{mode:H,setMode:U}),W&&Object($.h)(Oe,{filters:u,internalFilters:D,updateFilterValue:A})),Object($.h)("div",{className:"header-right"},"card"===H&&y&&Object($.h)(Se,{initialSort:s,onChange:o,options:y,pageIndex:B,pageSize:L}))),Object($.h)("div",{className:`body ${0===P.length?"empty":""}`},f&&Object($.h)(ke,{type:"info",closable:!0,showIcon:!1,onClose:j,message:Object($.h)(h.a.Fragment,null,Object($.h)("div",{className:"selectedCopy"},v(V)),Boolean(V.length)&&Object($.h)(h.a.Fragment,null,Object($.h)("span",{role:"button",tabIndex:0,className:"deselect-all",onClick:()=>N(!1)},Object(g.e)("Deselect all")),Object($.h)("div",{className:"divider"}),n()(m).call(m,e=>Object($.h)(w.a,{key:e.key,buttonStyle:e.type,cta:!0,onClick:()=>e.onSelect(n()(V).call(V,e=>e.original))},e.name))))}),"card"===H&&Object($.h)(R,{bulkSelectEnabled:f,prepareRow:M,renderCard:x,rows:P,loading:r}),"table"===H&&Object($.h)(k.b,{getTableProps:F,getTableBodyProps:z,prepareRow:M,headerGroups:E,rows:P,columns:e,loading:r,highlightRowId:C}),!r&&0===P.length&&Object($.h)(Fe,{className:H},Object($.h)(b.j,{image:Object($.h)(O,null),description:I.message||Object(g.e)("No Data")},I.slot||null)))),P.length>0&&Object($.h)("div",{className:"pagination-container"},Object($.h)(k.a,{totalPages:_||0,currentPage:_?B+1:0,onChange:e=>T(e-1),hideFirstAndLastPageLinks:!0}),Object($.h)("div",{className:"row-count-container"},!r&&Object(g.e)("%s-%s of %s",L*B+(P.length&&1),L*B+P.length,a))))};!function(e){e.startsWith="sw",e.endsWith="ew",e.contains="ct",e.equals="eq",e.notStartsWith="nsw",e.notEndsWith="new",e.notContains="nct",e.notEquals="neq",e.greaterThan="gt",e.lessThan="lt",e.relationManyMany="rel_m_m",e.relationOneMany="rel_o_m",e.titleOrSlug="title_or_slug",e.nameOrDescription="name_or_description",e.allText="all_text",e.chartAllText="chart_all_text",e.datasetIsNullOrEmpty="dataset_is_null_or_empty",e.between="between",e.dashboardIsFav="dashboard_is_favorite",e.chartIsFav="chart_is_favorite"}(ze||(ze={}))},4688:function(e,t,a){"use strict";var l=a(0),n=a.n(l),o=a(47),i=a(48),r=a(1);const c=o.j.label`
  cursor: pointer;
  display: inline-block;
  margin-bottom: 0;
`,s=Object(o.j)(i.a)`
  color: ${({theme:e})=>e.colors.primary.dark1};
  cursor: pointer;
`,d=o.j.input`
  &[type='checkbox'] {
    cursor: pointer;
    opacity: 0;
    position: absolute;
    left: 3px;
    margin: 0;
    top: 4px;
  }
`,u=o.j.div`
  cursor: pointer;
  display: inline-block;
  position: relative;
`,g=n.a.forwardRef(({indeterminate:e,id:t,checked:a,onChange:l,title:o="",labelText:g=""},p)=>{const h=n.a.useRef(),b=p||h;return n.a.useEffect(()=>{b.current.indeterminate=e},[b,e]),Object(r.h)(n.a.Fragment,null,Object(r.h)(u,null,e&&Object(r.h)(s,{name:"checkbox-half"}),!e&&a&&Object(r.h)(s,{name:"checkbox-on"}),!e&&!a&&Object(r.h)(i.a,{name:"checkbox-off"}),Object(r.h)(d,{name:t,id:t,type:"checkbox",ref:b,checked:a,onChange:l})),Object(r.h)(c,{title:o,htmlFor:t},g))});t.a=g}}]);