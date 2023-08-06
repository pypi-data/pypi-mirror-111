(window.webpackJsonp=window.webpackJsonp||[]).push([[28],{1004:function(e,t,a){"use strict";a(0);var n=a(47),s=a(473),o=a(174),c=a(50),l=a(1);t.a=function({warningMarkdown:e}){const t=Object(n.l)();return Object(l.h)(c.a,{id:"warning-tooltip",title:Object(l.h)(s.a,{source:e})},Object(l.h)(o.a.AlertSolid,{iconColor:t.colors.alert.base}))}},1265:function(e,t,a){"use strict";a(40);var n=a(11),s=a.n(n),o=a(78),c=a.n(o),l=a(0),r=a.n(l),i=a(195),d=a(44),b=a(47),u=a(91),h=a(14),p=a(101),m=a(400),j=a(42),O=a(73),g=a(129),f=a(1);const y=Object(m.a)(()=>Promise.all([a.e(0),a.e(48)]).then(a.bind(null,2135))),v=Object(b.j)(p.b)`
  .modal-content {
    height: 900px;
    display: flex;
    flex-direction: column;
    align-items: stretch;
  }

  .modal-header {
    flex: 0 1 auto;
  }
  .modal-body {
    flex: 1 1 auto;
    overflow: auto;
  }

  .modal-footer {
    flex: 0 1 auto;
  }

  .ant-modal-body {
    overflow: visible;
  }
`;function w(e){const t=null!=e&&e.certified_by||null!=e&&e.certification_details?{certified_by:null==e?void 0:e.certified_by,details:null==e?void 0:e.certification_details}:void 0;return c()({certification:t,warning_markdown:null==e?void 0:e.warning_markdown})}t.a=Object(g.a)(({addSuccessToast:e,datasource:t,onDatasourceSave:a,onHide:n,show:o})=>{const[c,b]=Object(l.useState)(t),[m,g]=Object(l.useState)([]),[S,x]=Object(l.useState)(!1),C=Object(l.useRef)(null),[_,k]=p.b.useModal(),N=()=>{var t,o,l;const r=(null==(t=c.tableSelector)?void 0:t.schema)||(null==(o=c.databaseSelector)?void 0:o.schema)||c.schema;x(!0),u.a.post({endpoint:"/datasource/save/",postPayload:{data:{...c,schema:r,metrics:null==c?void 0:null==(l=c.metrics)?void 0:s()(l).call(l,e=>({...e,extra:w(e)})),type:c.type||c.datasource_type}}}).then(({json:t})=>{e(Object(h.e)("The dataset has been saved")),a(t),n()}).catch(e=>{x(!1),Object(O.a)(e).then(({error:e})=>{_.error({title:"Error",content:e||Object(h.e)("An error has occurred"),okButtonProps:{danger:!0,className:"btn-danger"}})})})};return Object(f.h)(v,{show:o,onHide:n,title:Object(f.h)("span",null,Object(h.e)("Edit Dataset "),Object(f.h)("strong",null,c.table_name)),footer:Object(f.h)(r.a.Fragment,null,Object(j.c)(j.a.ENABLE_REACT_CRUD_VIEWS)&&Object(f.h)(d.a,{buttonSize:"small",buttonStyle:"default",className:"m-r-5",onClick:()=>{window.location.href=c.edit_url||c.url}},Object(h.e)("Use legacy datasource editor")),Object(f.h)(d.a,{buttonSize:"small",className:"m-r-5",onClick:n},Object(h.e)("Cancel")),Object(f.h)(d.a,{buttonSize:"small",buttonStyle:"primary",onClick:()=>{C.current=_.confirm({title:Object(h.e)("Confirm save"),content:Object(f.h)("div",null,Object(f.h)(i.a,{css:e=>({marginTop:4*e.gridUnit,marginBottom:4*e.gridUnit}),type:"warning",showIcon:!0,message:Object(h.e)("The dataset configuration exposed here\n                affects all the charts using this dataset.\n                Be mindful that changing settings\n                here may affect other charts\n                in undesirable ways.")}),Object(h.e)("Are you sure you want to save and apply changes?")),onOk:N,icon:null})},disabled:S||m.length>0},Object(h.e)("Save"))),responsive:!0},Object(f.h)(y,{showLoadingForImport:!0,height:500,datasource:c,onChange:(e,t)=>{var a;b({...e,metrics:null==e?void 0:s()(a=e.metrics).call(a,e=>({...e,is_certified:(null==e?void 0:e.certified_by)||(null==e?void 0:e.certification_details)}))}),g(t)}}),k)})},1369:function(e,t,a){"use strict";var n=a(0),s=a.n(n),o=a(50),c=a(48),l=a(1);t.a=({onClick:e,tooltipContent:t})=>{const a=s.a.forwardRef((e,t)=>Object(l.h)(c.a,e));return Object(l.h)(o.a,{title:t},Object(l.h)(a,{role:"button",onClick:e,name:"refresh",css:e=>({cursor:"pointer",color:e.colors.grayscale.base,"&:hover":{color:e.colors.primary.base}})}))}},1861:function(e,t,a){"use strict";var n=a(0),s=a.n(n),o=a(14),c=a(47),l=a(48),r=a(50),i=a(1);t.a=function({certifiedBy:e,details:t,size:a=24}){return Object(i.h)(r.a,{id:"certified-details-tooltip",title:Object(i.h)(s.a.Fragment,null,e&&Object(i.h)("div",null,Object(i.h)("strong",null,Object(o.e)("Certified by %s",e))),Object(i.h)("div",null,t))},Object(i.h)(l.a,{color:c.k.colors.primary.base,height:a,width:a,name:"certified"}))}},1862:function(e,t,a){"use strict";a.d(t,"a",(function(){return S}));a(40);var n=a(33),s=a.n(n),o=a(69),c=a.n(o),l=a(11),r=a.n(l),i=a(0),d=a(47),b=a(91),u=a(14),h=a(96),p=a.n(h),m=a(58),j=a(136),O=a(1369),g=a(738),f=a(1);const y=d.j.p`
  color: ${({theme:e})=>e.colors.secondary.light2};
  font-size: ${({theme:e})=>e.typography.sizes.s}px;
  margin: 20px 0 10px 0;
  text-transform: uppercase;
`,v=d.j.div`
  .fa-refresh {
    padding-left: 9px;
  }

  .refresh-col {
    display: flex;
    align-items: center;
    width: 30px;
    margin-left: ${({theme:e})=>e.gridUnit}px;
  }

  .section {
    padding-bottom: 5px;
    display: flex;
    flex-direction: row;
  }

  .select {
    flex-grow: 1;
  }
`,w=d.j.span`
  display: inline-flex;
  align-items: center;
`;function S({dbId:e,formMode:t=!1,getDbList:a,getTableList:n,handleError:o,isDatabaseSelectEnabled:l=!0,onChange:d,onDbChange:h,onSchemaChange:S,onSchemasLoad:x,readOnly:C=!1,schema:_,sqlLabMode:k=!1}){const[N,$]=Object(i.useState)(e),[D,E]=Object(i.useState)(_),[I,R]=Object(i.useState)(!1),[T,A]=Object(i.useState)([]);function z(t,a=!1){const n=t||e;if(n){R(!0);const e=`/api/v1/database/${n}/schemas/?q=${p.a.encode({force:Boolean(a)})}`;return b.a.get({endpoint:e}).then(({json:e})=>{var t;const a=r()(t=e.result).call(t,e=>({value:e,label:e,title:e}));A(a),R(!1),x&&x(a)}).catch(()=>{A([]),R(!1),o(Object(u.e)("Error while fetching schema list"))})}return c.a.resolve()}function L({dbId:e,schema:t}){$(e),E(t),d&&d({dbId:e,schema:t,tableName:void 0})}function U(e){var t;return a&&a(e.result),0===e.result.length&&o(Object(u.e)("It seems you don't have access to any database")),r()(t=e.result).call(t,e=>({...e,label:`${e.backend} ${e.database_name}`}))}function M(e,t=!1){const a=e?e.id:null;A([]),S&&S(null),h&&h(e),z(a,t),L({dbId:a,schema:void 0})}function H(e){return Object(f.h)(w,{title:e.database_name},Object(f.h)(j.a,{type:"default"},e.backend)," ",e.database_name)}function B(e,t){return Object(f.h)("div",{className:"section"},Object(f.h)("span",{className:"select"},e),Object(f.h)("span",{className:"refresh-col"},t))}return Object(i.useEffect)(()=>{N&&z(N)},[N]),Object(f.h)(v,null,t&&Object(f.h)(y,null,Object(u.e)("datasource")),function(){const e=p.a.encode({order_columns:"database_name",order_direction:"asc",page:0,page_size:-1,...t||!k?{}:{filters:[{col:"expose_in_sqllab",opr:"eq",value:!0}]}});return B(Object(f.h)(g.a,{dataEndpoint:`/api/v1/database/?q=${e}`,onChange:e=>M(e),onAsyncError:()=>o(Object(u.e)("Error while fetching database list")),clearable:!1,value:N,valueKey:"id",valueRenderer:e=>Object(f.h)("div",null,Object(f.h)("span",{className:"text-muted m-r-5"},Object(u.e)("Database:")),H(e)),optionRenderer:H,mutator:U,placeholder:Object(u.e)("Select a database"),autoSelect:!0,isDisabled:!l||C}),null)}(),t&&Object(f.h)(y,null,Object(u.e)("schema")),function(){const a=s()(T).call(T,({value:e})=>D===e),o=!t&&!C&&Object(f.h)(O.a,{onClick:()=>M({id:e},!0),tooltipContent:Object(u.e)("Force refresh schema list")});return B(Object(f.h)(m.h,{name:"select-schema",placeholder:Object(u.e)("Select a schema (%s)",T.length),options:T,value:a,valueRenderer:e=>Object(f.h)("div",null,Object(f.h)("span",{className:"text-muted"},Object(u.e)("Schema:"))," ",e.label),isLoading:I,autosize:!1,onChange:e=>function(e,t=!1){const a=e?e.value:null;S&&S(a),E(a),L({dbId:N,schema:a}),n&&n(N,a,t)}(e),isDisabled:C}),o)}())}},1866:function(e,t,a){"use strict";a(40);var n=a(69),s=a.n(n),o=a(11),c=a.n(o),l=a(0),r=a(47),i=a(91),d=a(14),b=a(58),u=a(95),h=a(1862),p=a(1369),m=a(1861),j=a(1004),O=a(1);const g=r.j.p`
  color: ${({theme:e})=>e.colors.secondary.light2};
  font-size: ${({theme:e})=>e.typography.sizes.s}px;
  margin: 20px 0 10px 0;
  text-transform: uppercase;
`,f=r.j.div`
  .fa-refresh {
    padding-left: 9px;
  }

  .refresh-col {
    display: flex;
    align-items: center;
    width: 30px;
    margin-left: ${({theme:e})=>e.gridUnit}px;
  }

  .section {
    padding-bottom: 5px;
    display: flex;
    flex-direction: row;
  }

  .select {
    flex-grow: 1;
  }

  .divider {
    border-bottom: 1px solid ${({theme:e})=>e.colors.secondary.light5};
    margin: 15px 0;
  }
`,y=r.j.span`
  align-items: center;
  display: flex;
  white-space: nowrap;

  > svg,
  > small {
    margin-right: ${({theme:e})=>e.gridUnit}px;
  }
`;t.a=({database:e,dbId:t,formMode:a=!1,getDbList:n,handleError:o,isDatabaseSelectEnabled:r=!0,onChange:v,onDbChange:w,onSchemaChange:S,onSchemasLoad:x,onTableChange:C,onTablesLoad:_,readOnly:k=!1,schema:N,sqlLabMode:$=!0,tableName:D,tableNameSticky:E=!0})=>{const[I,R]=Object(l.useState)(N),[T,A]=Object(l.useState)(D),[z,L]=Object(l.useState)(!1),[U,M]=Object(l.useState)([]);function H(e,a,n=!1,l="undefined"){const r=a||I,b=e||t;if(b&&r){const e=encodeURIComponent(r),t=encodeURIComponent(l);L(!0),M([]);const a=encodeURI(`/superset/tables/${b}/${e}/${t}/${!!n}/`);return i.a.get({endpoint:a}).then(({json:e})=>{var t;const a=c()(t=e.options).call(t,e=>({value:e.value,schema:e.schema,label:e.label,title:e.title,type:e.type,extra:null==e?void 0:e.extra}));L(!1),M(a),_&&_(e.options)}).catch(()=>{L(!1),M([]),o(Object(d.e)("Error while fetching table list"))})}return L(!1),M([]),s.a.resolve()}function B({dbId:e,schema:t,tableName:a}){A(a),R(t),v&&v({dbId:e,schema:t,tableName:a})}function q(e="undefined"){if(!t||!e){const e=[];return s.a.resolve({options:e})}const a=encodeURIComponent(N||""),n=encodeURIComponent(e);return i.a.get({endpoint:encodeURI(`/superset/tables/${t}/${a}/${n}`)}).then(({json:e})=>{var t;return{options:c()(t=e.options).call(t,e=>({value:e.value,schema:e.schema,label:e.label,title:e.title,type:e.type}))}})}function P(e){if(!e)return void A("");const a=e.schema,n=e.value;E&&B({dbId:t,schema:a,tableName:n}),C&&C(n,a)}function F(e){var t,a;return Object(O.h)(y,{title:e.label},Object(O.h)("small",{className:"text-muted"},Object(O.h)("i",{className:`fa fa-${"view"===e.type?"eye":"table"}`})),(null==(t=e.extra)?void 0:t.certification)&&Object(O.h)(m.a,{certifiedBy:e.extra.certification.certified_by,details:e.extra.certification.details,size:20}),(null==(a=e.extra)?void 0:a.warning_markdown)&&Object(O.h)(j.a,{warningMarkdown:e.extra.warning_markdown,size:20}),e.label)}return Object(l.useEffect)(()=>{t&&N&&H()},[t,N]),Object(O.h)(f,null,Object(O.h)(h.a,{dbId:t,formMode:a,getDbList:n,getTableList:H,handleError:o,onChange:B,onDbChange:k?void 0:w,onSchemaChange:k?void 0:S,onSchemasLoad:x,schema:I,sqlLabMode:$,isDatabaseSelectEnabled:r&&!k,readOnly:k}),!a&&Object(O.h)("div",{className:"divider"}),$&&Object(O.h)("div",{className:"section"},Object(O.h)(u.a,null,Object(d.e)("See table schema")," ",N&&Object(O.h)("small",null,U.length," in",Object(O.h)("i",null,N)))),a&&Object(O.h)(g,null,Object(d.e)("Table")),function(){const n=U;let s=null;if(I&&!a)s=Object(O.h)(b.h,{name:"select-table",isLoading:z,ignoreAccents:!1,placeholder:Object(d.e)("Select table or type table name"),autosize:!1,onChange:P,options:n,value:T,optionRenderer:F,valueRenderer:F,isDisabled:k});else if(a)s=Object(O.h)(b.c,{name:"select-table",isLoading:z,ignoreAccents:!1,placeholder:Object(d.e)("Select table or type table name"),autosize:!1,onChange:P,options:n,value:T,optionRenderer:F});else{let t,a=!1;e&&e.allow_multi_schema_metadata_fetch?t=Object(d.e)("Type to search ..."):(t=Object(d.e)("Select table "),a=!0),s=Object(O.h)(b.b,{name:"async-select-table",placeholder:t,isDisabled:a,autosize:!1,onChange:P,value:T,loadOptions:q,optionRenderer:F})}return function(e,t){return Object(O.h)("div",{className:"section"},Object(O.h)("span",{className:"select"},e),Object(O.h)("span",{className:"refresh-col"},t))}(s,!a&&!k&&Object(O.h)(p.a,{onClick:()=>function(e,a=!1){const n=e?e.value:null;S&&S(n),B({dbId:t,schema:n,tableName:void 0}),H(t,I,a)}({value:N},!0),tooltipContent:Object(d.e)("Force refresh table list")}))}())}},4532:function(e,t,a){"use strict";a(40);var n=a(11),s=a.n(n),o=a(0),c=a.n(o),l=a(47),r=a(14),i=a(48),d=a(101),b=a(445),u=a(1);Object(l.j)(i.a)`
  margin: auto ${({theme:e})=>2*e.gridUnit}px auto 0;
`;const h=l.j.div`
  display: block;
  color: ${({theme:e})=>e.colors.grayscale.base};
  font-size: ${({theme:e})=>e.typography.sizes.s-1}px;
`,p=l.j.div`
  padding-bottom: ${({theme:e})=>2*e.gridUnit}px;
  padding-top: ${({theme:e})=>2*e.gridUnit}px;

  & > div {
    margin: ${({theme:e})=>e.gridUnit}px 0;
  }

  &.extra-container {
    padding-top: 8px;
  }

  .confirm-overwrite {
    margin-bottom: ${({theme:e})=>2*e.gridUnit}px;
  }

  .input-container {
    display: flex;
    align-items: center;

    label {
      display: flex;
      margin-right: ${({theme:e})=>2*e.gridUnit}px;
    }

    i {
      margin: 0 ${({theme:e})=>e.gridUnit}px;
    }
  }

  input,
  textarea {
    flex: 1 1 auto;
  }

  textarea {
    height: 160px;
    resize: none;
  }

  input::placeholder,
  textarea::placeholder {
    color: ${({theme:e})=>e.colors.grayscale.light1};
  }

  textarea,
  input[type='text'],
  input[type='number'] {
    padding: ${({theme:e})=>1.5*e.gridUnit}px
      ${({theme:e})=>2*e.gridUnit}px;
    border-style: none;
    border: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
    border-radius: ${({theme:e})=>e.gridUnit}px;

    &[name='name'] {
      flex: 0 1 auto;
      width: 40%;
    }

    &[name='sqlalchemy_uri'] {
      margin-right: ${({theme:e})=>3*e.gridUnit}px;
    }
  }
`;t.a=({resourceName:e,resourceLabel:t,passwordsNeededMessage:a,confirmOverwriteMessage:n,addDangerToast:l,addSuccessToast:i,onModelImport:m,show:j,onHide:O,passwordFields:g=[],setPasswordFields:f=(()=>{})})=>{const[y,v]=Object(o.useState)(!0),[w,S]=Object(o.useState)(null),[x,C]=Object(o.useState)({}),[_,k]=Object(o.useState)(!1),[N,$]=Object(o.useState)(!1),D=Object(o.useRef)(null),E=()=>{S(null),f([]),C({}),k(!1),$(!1),D&&D.current&&(D.current.value="")},{state:{alreadyExists:I,passwordsNeeded:R},importResource:T}=Object(b.e)(e,t,e=>{E(),l(e)});Object(o.useEffect)(()=>{f(R)},[R,f]),Object(o.useEffect)(()=>{k(I.length>0)},[I,k]);const A=e=>{var t,a;const n=null!=(t=null==(a=e.currentTarget)?void 0:a.value)?t:"";$(n.toUpperCase()===Object(r.e)("OVERWRITE"))};return y&&j&&v(!1),Object(u.h)(d.b,{name:"model",className:"import-model-modal",disablePrimaryButton:null===w||_&&!N,onHandledPrimaryAction:()=>{null!==w&&T(w,x,N).then(e=>{e&&(i(Object(r.e)("The import was successful")),E(),m())})},onHide:()=>{v(!0),O(),E()},primaryButtonName:_?Object(r.e)("Overwrite"):Object(r.e)("Import"),primaryButtonType:_?"danger":"primary",width:"750px",show:j,title:Object(u.h)("h4",null,Object(r.e)("Import %s",t))},Object(u.h)(p,null,Object(u.h)("div",{className:"control-label"},Object(u.h)("label",{htmlFor:"modelFile"},Object(r.e)("File"),Object(u.h)("span",{className:"required"},"*"))),Object(u.h)("input",{ref:D,name:"modelFile",id:"modelFile",type:"file",accept:".yaml,.json,.yml,.zip",onChange:e=>{const{files:t}=e.target;S(t&&t[0]||null)}})),0===g.length?null:Object(u.h)(c.a.Fragment,null,Object(u.h)("h5",null,"Database passwords"),Object(u.h)(h,null,a),s()(g).call(g,e=>Object(u.h)(p,{key:`password-for-${e}`},Object(u.h)("div",{className:"control-label"},e,Object(u.h)("span",{className:"required"},"*")),Object(u.h)("input",{name:`password-${e}`,autoComplete:`password-${e}`,type:"password",value:x[e],onChange:t=>C({...x,[e]:t.target.value})})))),_?Object(u.h)(c.a.Fragment,null,Object(u.h)(p,null,Object(u.h)("div",{className:"confirm-overwrite"},n),Object(u.h)("div",{className:"control-label"},Object(r.e)('Type "%s" to confirm',Object(r.e)("OVERWRITE"))),Object(u.h)("input",{id:"overwrite",type:"text",onChange:A}))):null)}},4541:function(e,t,a){"use strict";a.d(t,"a",(function(){return s}));var n=a(14);const s={name:Object(n.e)("Data"),tabs:[{name:"Databases",label:Object(n.e)("Databases"),url:"/databaseview/list/",usesRouter:!0},{name:"Datasets",label:Object(n.e)("Datasets"),url:"/tablemodelview/list/",usesRouter:!0},{name:"Saved queries",label:Object(n.e)("Saved queries"),url:"/savedqueryview/list/",usesRouter:!0},{name:"Query history",label:Object(n.e)("Query history"),url:"/superset/sqllab/history/",usesRouter:!0}]}},4931:function(e,t,a){"use strict";a.r(t);a(40);var n=a(49),s=a.n(n),o=a(54),c=a.n(o),l=a(11),r=a.n(l),i=a(14),d=a(47),b=a(91),u=a(0),h=a.n(u),p=a(96),m=a.n(p),j=a(125),O=a(445),g=a(1367),f=a(1265),y=a(1368),v=a(4526),w=a(1e3),S=a(4541),x=a(129),C=a(50),_=a(174),k=a(1372),N=a(1861),$=a(4532),D=a(42),E=a(1004),I=a(730),R=a.n(I),T=a(439),A=a.n(T),z=a(48),L=a(101),U=a(1866),M=a(1);const H=Object(d.j)(z.a)`
  margin: auto ${({theme:e})=>2*e.gridUnit}px auto 0;
`,B=d.j.div`
  padding-bottom: 340px;
  width: 65%;
`;var q=Object(x.a)(({addDangerToast:e,addSuccessToast:t,onDatasetAdd:a,onHide:n,show:s})=>{const[o,c]=Object(u.useState)(""),[l,r]=Object(u.useState)(""),[d,b]=Object(u.useState)(0),[p,m]=Object(u.useState)(!0),{createResource:j}=Object(O.g)("dataset",Object(i.e)("dataset"),e);return Object(M.h)(L.b,{disablePrimaryButton:p,onHandledPrimaryAction:()=>{const e={database:d,...o?{schema:o}:{},table_name:l};j(e).then(e=>{e&&(a&&a({id:e.id,...e}),t(Object(i.e)("The dataset has been saved")),n())})},onHide:n,primaryButtonName:Object(i.e)("Add"),show:s,title:Object(M.h)(h.a.Fragment,null,Object(M.h)(H,{name:"warning-solid"}),Object(i.e)("Add dataset"))},Object(M.h)(B,null,Object(M.h)(U.a,{clearable:!1,dbId:d,formMode:!0,handleError:e,onChange:({dbId:e,schema:t,tableName:a})=>{b(e),m(R()(e)||A()(a)),c(t),r(a)},schema:o,tableName:l})))});const P=Object(i.e)('The passwords for the databases below are needed in order to import them together with the datasets. Please note that the "Secure Extra" and "Certificate" sections of the database configuration are not present in export files, and should be added manually after the import if they are needed.'),F=Object(i.e)("You are importing one or more datasets that already exist. Overwriting might cause you to lose some of your work. Are you sure you want to overwrite?"),V=d.j.div`
  align-items: center;
  display: flex;

  > svg {
    margin-right: ${({theme:e})=>e.gridUnit}px;
  }
`,J=d.j.div`
  color: ${({theme:e})=>e.colors.grayscale.base};
`;t.default=Object(x.a)(({addDangerToast:e,addSuccessToast:t,user:a})=>{const{state:{loading:n,resourceCount:o,resourceCollection:l,bulkSelectEnabled:d},hasPerm:p,fetchData:x,toggleBulkSelect:I,refreshData:R}=Object(O.f)("dataset",Object(i.e)("dataset"),e),[T,A]=Object(u.useState)(!1),[z,L]=Object(u.useState)(null),[U,H]=Object(u.useState)(null),[B,W]=Object(u.useState)(!1),[Q,K]=Object(u.useState)([]),X=()=>{W(!0)},Y=p("can_write"),G=p("can_write"),Z=p("can_write"),ee=p("can_read"),te=[{id:"changed_on_delta_humanized",desc:!0}],ae=Object(u.useCallback)(({id:t})=>{b.a.get({endpoint:`/api/v1/dataset/${t}`}).then(({json:e={}})=>{var t;const a=r()(t=e.result.owners).call(t,e=>e.id);H({...e.result,owners:a})}).catch(()=>{e(Object(i.e)("An error occurred while fetching dataset related data"))})},[e]),ne=Object(u.useMemo)(()=>[{Cell:({row:{original:{kind:e}}})=>"physical"===e?Object(M.h)(C.a,{id:"physical-dataset-tooltip",title:Object(i.e)("Physical dataset")},Object(M.h)(_.a.DatasetPhysical,null)):Object(M.h)(C.a,{id:"virtual-dataset-tooltip",title:Object(i.e)("Virtual dataset")},Object(M.h)(_.a.DatasetVirtual,null)),accessor:"kind_icon",disableSortBy:!0,size:"xs"},{Cell:({row:{original:{extra:e,table_name:t,explore_url:a}}})=>{const n=Object(M.h)("a",{href:a},t);try{const t=JSON.parse(e);return Object(M.h)(V,null,(null==t?void 0:t.certification)&&Object(M.h)(N.a,{certifiedBy:t.certification.certified_by,details:t.certification.details}),(null==t?void 0:t.warning_markdown)&&Object(M.h)(E.a,{warningMarkdown:t.warning_markdown}),n)}catch{return n}},Header:Object(i.e)("Name"),accessor:"table_name"},{Cell:({row:{original:{kind:e}}})=>{var t;return(null==(t=e[0])?void 0:t.toUpperCase())+c()(e).call(e,1)},Header:Object(i.e)("Type"),accessor:"kind",disableSortBy:!0,size:"md"},{Header:Object(i.e)("Source"),accessor:"database.database_name",size:"lg"},{Header:Object(i.e)("Schema"),accessor:"schema",size:"lg"},{Cell:({row:{original:{changed_on_delta_humanized:e}}})=>Object(M.h)("span",{className:"no-wrap"},e),Header:Object(i.e)("Modified"),accessor:"changed_on_delta_humanized",size:"xl"},{Cell:({row:{original:{changed_by_name:e}}})=>e,Header:Object(i.e)("Modified by"),accessor:"changed_by.first_name",size:"xl"},{accessor:"database",disableSortBy:!0,hidden:!0},{Cell:({row:{original:{owners:e=[]}}})=>Object(M.h)(k.a,{users:e}),Header:Object(i.e)("Owners"),id:"owners",disableSortBy:!0,size:"lg"},{accessor:"sql",hidden:!0,disableSortBy:!0},{Cell:({row:{original:e}})=>Y||G||ee?Object(M.h)(J,{className:"actions"},G&&Object(M.h)(C.a,{id:"delete-action-tooltip",title:Object(i.e)("Delete"),placement:"bottom"},Object(M.h)("span",{role:"button",tabIndex:0,className:"action-button",onClick:()=>{return t=e,b.a.get({endpoint:`/api/v1/dataset/${t.id}/related_objects`}).then(({json:e={}})=>{L({...t,chart_count:e.charts.count,dashboard_count:e.dashboards.count})}).catch(Object(j.c)(e=>Object(i.e)("An error occurred while fetching dataset related data: %s",e)));var t}},Object(M.h)(_.a.Trash,null))),ee&&Object(M.h)(C.a,{id:"export-action-tooltip",title:Object(i.e)("Export"),placement:"bottom"},Object(M.h)("span",{role:"button",tabIndex:0,className:"action-button",onClick:()=>le([e])},Object(M.h)(_.a.Share,null))),Y&&Object(M.h)(C.a,{id:"edit-action-tooltip",title:Object(i.e)("Edit"),placement:"bottom"},Object(M.h)("span",{role:"button",tabIndex:0,className:"action-button",onClick:()=>ae(e)},Object(M.h)(_.a.EditAlt,null)))):null,Header:Object(i.e)("Actions"),id:"actions",hidden:!Y&&!G,disableSortBy:!0}],[Y,G,ee,ae]),se=Object(u.useMemo)(()=>[{Header:Object(i.e)("Owner"),id:"owners",input:"select",operator:v.a.relationManyMany,unfilteredLabel:"All",fetchSelects:Object(j.e)("dataset","owners",Object(j.c)(e=>Object(i.e)("An error occurred while fetching dataset owner values: %s",e)),a.userId),paginate:!0},{Header:Object(i.e)("Database"),id:"database",input:"select",operator:v.a.relationManyMany,unfilteredLabel:"All",fetchSelects:Object(j.e)("dataset","database",Object(j.c)(e=>Object(i.e)("An error occurred while fetching datasets: %s",e))),paginate:!0},{Header:Object(i.e)("Schema"),id:"schema",input:"select",operator:v.a.equals,unfilteredLabel:"All",fetchSelects:Object(j.d)("dataset","schema",Object(j.c)(e=>Object(i.e)("An error occurred while fetching schema values: %s",e))),paginate:!0},{Header:Object(i.e)("Type"),id:"sql",input:"select",operator:v.a.datasetIsNullOrEmpty,unfilteredLabel:"All",selects:[{label:"Virtual",value:!1},{label:"Physical",value:!0}]},{Header:Object(i.e)("Search"),id:"table_name",input:"search",operator:v.a.contains}],[]),oe={activeChild:"Datasets",...S.a},ce=[];(G||ee)&&ce.push({name:Object(i.e)("Bulk select"),onClick:I,buttonStyle:"secondary"}),Z&&ce.push({name:Object(M.h)(h.a.Fragment,null,Object(M.h)("i",{className:"fa fa-plus"})," ",Object(i.e)("Dataset")," "),onClick:()=>A(!0),buttonStyle:"primary"}),Object(D.c)(D.a.VERSIONED_EXPORT)&&ce.push({name:Object(M.h)(C.a,{id:"import-tooltip",title:Object(i.e)("Import datasets"),placement:"bottomRight"},Object(M.h)(_.a.Import,null)),buttonStyle:"link",onClick:X}),oe.buttons=ce;const le=e=>window.location.assign(`/api/v1/dataset/export/?q=${m.a.encode(r()(e).call(e,({id:e})=>e))}`);return Object(M.h)(h.a.Fragment,null,Object(M.h)(w.a,oe),Object(M.h)(q,{show:T,onHide:()=>A(!1),onDatasetAdd:R}),z&&Object(M.h)(y.a,{description:Object(i.e)("The dataset %s is linked to %s charts that appear on %s dashboards. Are you sure you want to continue? Deleting the dataset will break those objects.",z.table_name,z.chart_count,z.dashboard_count),onConfirm:()=>{z&&(({id:a,table_name:n})=>{b.a.delete({endpoint:`/api/v1/dataset/${a}`}).then(()=>{R(),L(null),t(Object(i.e)("Deleted: %s",n))},Object(j.c)(t=>e(Object(i.e)("There was an issue deleting %s: %s",n,t))))})(z)},onHide:()=>{L(null)},open:!0,title:Object(i.e)("Delete Dataset?")}),U&&Object(M.h)(f.a,{datasource:U,onDatasourceSave:R,onHide:()=>{H(null)},show:!0}),Object(M.h)(g.a,{title:Object(i.e)("Please confirm"),description:Object(i.e)("Are you sure you want to delete the selected datasets?"),onConfirm:a=>{b.a.delete({endpoint:`/api/v1/dataset/?q=${m.a.encode(r()(a).call(a,({id:e})=>e))}`}).then(({json:e={}})=>{R(),t(e.message)},Object(j.c)(t=>e(Object(i.e)("There was an issue deleting the selected datasets: %s",t))))}},e=>{const t=[];return G&&t.push({key:"delete",name:Object(i.e)("Delete"),onSelect:e,type:"danger"}),ee&&t.push({key:"export",name:Object(i.e)("Export"),type:"primary",onSelect:le}),Object(M.h)(v.b,{className:"dataset-list-view",columns:ne,data:l,count:o,pageSize:25,fetchData:x,filters:se,loading:n,initialSort:te,bulkActions:t,bulkSelectEnabled:d,disableBulkSelect:I,renderBulkSelectCopy:e=>{const{virtualCount:t,physicalCount:a}=s()(e).call(e,(e,t)=>("physical"===t.original.kind?e.physicalCount+=1:"virtual"===t.original.kind&&(e.virtualCount+=1),e),{virtualCount:0,physicalCount:0});return e.length?t&&!a?Object(i.e)("%s Selected (Virtual)",e.length,t):a&&!t?Object(i.e)("%s Selected (Physical)",e.length,a):Object(i.e)("%s Selected (%s Physical, %s Virtual)",e.length,a,t):Object(i.e)("0 Selected")}})}),Object(M.h)($.a,{resourceName:"dataset",resourceLabel:Object(i.e)("dataset"),passwordsNeededMessage:P,confirmOverwriteMessage:F,addDangerToast:e,addSuccessToast:t,onModelImport:()=>{W(!1),R()},show:B,onHide:()=>{W(!1)},passwordFields:Q,setPasswordFields:K}))})},738:function(e,t,a){"use strict";var n=a(26),s=a.n(n),o=a(13),c=a.n(o),l=a(0),r=a.n(l),i=a(2),d=a.n(i),b=a(58),u=a(14),h=a(91),p=a(73),m=a(1);const j={dataEndpoint:d.a.string.isRequired,onChange:d.a.func.isRequired,mutator:d.a.func.isRequired,onAsyncError:d.a.func,value:d.a.oneOfType([d.a.number,d.a.arrayOf(d.a.number)]),valueRenderer:d.a.func,placeholder:d.a.string,autoSelect:d.a.bool},O={placeholder:Object(u.e)("Select ..."),onAsyncError:()=>{}};class g extends r.a.PureComponent{constructor(e){var t;super(e),this.state={isLoading:!1,options:[]},this.onChange=c()(t=this.onChange).call(t,this)}componentDidMount(){this.fetchOptions()}onChange(e){this.props.onChange(e)}fetchOptions(){this.setState({isLoading:!0});const{mutator:e,dataEndpoint:t}=this.props;return h.a.get({endpoint:t}).then(({json:t})=>{const a=e?e(t):t;this.setState({options:a,isLoading:!1}),!this.props.value&&this.props.autoSelect&&a.length>0&&this.onChange(a[0])}).catch(e=>Object(p.a)(e).then(e=>{this.props.onAsyncError(e.error||e.statusText||e),this.setState({isLoading:!1})}))}render(){return Object(m.h)(b.h,s()({placeholder:this.props.placeholder,options:this.state.options,value:this.props.value,isLoading:this.state.isLoading,onChange:this.onChange,valueRenderer:this.props.valueRenderer},this.props))}}g.propTypes=j,g.defaultProps=O,t.a=g}}]);