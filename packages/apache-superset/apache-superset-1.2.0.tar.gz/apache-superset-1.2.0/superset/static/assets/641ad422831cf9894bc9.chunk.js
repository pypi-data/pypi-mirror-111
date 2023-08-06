(window.webpackJsonp=window.webpackJsonp||[]).push([[27],{134:function(e,t,a){"use strict";a.d(t,"a",(function(){return g})),a.d(t,"b",(function(){return f})),a.d(t,"c",(function(){return y}));var l=a(71),n=a.n(l),o=a(32),i=a.n(o),s=(a(0),a(47)),c=a(9),r=a(707),d=a.n(r),b=a(48),h=a(1);const u=["fullWidth","allowOverflow"],m=Object(s.j)(d.a,{shouldForwardProp:e=>!i()(u).call(u,e)})`
  overflow: ${({allowOverflow:e})=>e?"visible":"hidden"};

  .ant-tabs-content-holder {
    overflow: ${({allowOverflow:e})=>e?"visible":"auto"};
  }

  .ant-tabs-tab {
    flex: 1 1 auto;

    &.ant-tabs-tab-active .ant-tabs-tab-btn {
      color: inherit;
    }

    &:hover {
      .anchor-link-container {
        cursor: pointer;

        .fa.fa-link {
          visibility: visible;
        }
      }
    }

    .short-link-trigger.btn {
      padding: 0 ${({theme:e})=>e.gridUnit}px;

      & > .fa.fa-link {
        top: 0;
      }
    }
  }

  ${({fullWidth:e})=>e&&c.a`
      .ant-tabs-nav-list {
        width: 100%;
      }

      .ant-tabs-tab {
        width: 0;
      }
    `};

  .ant-tabs-tab-btn {
    display: flex;
    flex: 1 1 auto;
    align-items: center;
    justify-content: center;
    font-size: ${({theme:e})=>e.typography.sizes.s}px;
    text-align: center;
    text-transform: uppercase;
    user-select: none;

    .required {
      margin-left: ${({theme:e})=>e.gridUnit/2}px;
      color: ${({theme:e})=>e.colors.error.base};
    }
  }

  .ant-tabs-ink-bar {
    background: ${({theme:e})=>e.colors.secondary.base};
  }
`,p=Object(s.j)(d.a.TabPane)``,j=n()(m,{TabPane:p});j.defaultProps={fullWidth:!0,animated:!0};const O=Object(s.j)(m)`
  .ant-tabs-content-holder {
    background: white;
  }

  & > .ant-tabs-nav {
    margin-bottom: 0;
  }

  .ant-tabs-tab-remove {
    padding-top: 0;
    padding-bottom: 0;
    height: ${({theme:e})=>6*e.gridUnit}px;
  }

  ${({fullWidth:e})=>e&&c.a`
      .ant-tabs-nav-list {
        width: 100%;
      }
    `}
`,g=n()(O,{TabPane:p});g.defaultProps={type:"editable-card",fullWidth:!1},g.TabPane.defaultProps={closeIcon:Object(h.h)(b.a,{role:"button",tabIndex:0,cursor:"pointer",name:"cancel-x"})};const v=Object(s.j)(g)`
  &.ant-tabs-card > .ant-tabs-nav .ant-tabs-tab {
    margin: 0 ${({theme:e})=>4*e.gridUnit}px;
    padding: ${({theme:e})=>`${3*e.gridUnit}px ${e.gridUnit}px`};
    background: transparent;
    border: none;
  }

  &.ant-tabs-card > .ant-tabs-nav .ant-tabs-ink-bar {
    visibility: visible;
  }

  .ant-tabs-tab-btn {
    font-size: ${({theme:e})=>e.typography.sizes.m}px;
  }

  .ant-tabs-tab-remove {
    margin-left: 0;
    padding-right: 0;
  }

  .ant-tabs-nav-add {
    min-width: unset !important;
    background: transparent !important;
    border: none !important;
  }
`,f=n()(v,{TabPane:p});var y=j},4532:function(e,t,a){"use strict";a(40);var l=a(11),n=a.n(l),o=a(0),i=a.n(o),s=a(47),c=a(14),r=a(48),d=a(101),b=a(445),h=a(1);Object(s.j)(r.a)`
  margin: auto ${({theme:e})=>2*e.gridUnit}px auto 0;
`;const u=s.j.div`
  display: block;
  color: ${({theme:e})=>e.colors.grayscale.base};
  font-size: ${({theme:e})=>e.typography.sizes.s-1}px;
`,m=s.j.div`
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
`;t.a=({resourceName:e,resourceLabel:t,passwordsNeededMessage:a,confirmOverwriteMessage:l,addDangerToast:s,addSuccessToast:r,onModelImport:p,show:j,onHide:O,passwordFields:g=[],setPasswordFields:v=(()=>{})})=>{const[f,y]=Object(o.useState)(!0),[x,_]=Object(o.useState)(null),[w,$]=Object(o.useState)({}),[N,S]=Object(o.useState)(!1),[C,k]=Object(o.useState)(!1),T=Object(o.useRef)(null),A=()=>{_(null),v([]),$({}),S(!1),k(!1),T&&T.current&&(T.current.value="")},{state:{alreadyExists:q,passwordsNeeded:U},importResource:E}=Object(b.e)(e,t,e=>{A(),s(e)});Object(o.useEffect)(()=>{v(U)},[U,v]),Object(o.useEffect)(()=>{S(q.length>0)},[q,S]);const L=e=>{var t,a;const l=null!=(t=null==(a=e.currentTarget)?void 0:a.value)?t:"";k(l.toUpperCase()===Object(c.e)("OVERWRITE"))};return f&&j&&y(!1),Object(h.h)(d.b,{name:"model",className:"import-model-modal",disablePrimaryButton:null===x||N&&!C,onHandledPrimaryAction:()=>{null!==x&&E(x,w,C).then(e=>{e&&(r(Object(c.e)("The import was successful")),A(),p())})},onHide:()=>{y(!0),O(),A()},primaryButtonName:N?Object(c.e)("Overwrite"):Object(c.e)("Import"),primaryButtonType:N?"danger":"primary",width:"750px",show:j,title:Object(h.h)("h4",null,Object(c.e)("Import %s",t))},Object(h.h)(m,null,Object(h.h)("div",{className:"control-label"},Object(h.h)("label",{htmlFor:"modelFile"},Object(c.e)("File"),Object(h.h)("span",{className:"required"},"*"))),Object(h.h)("input",{ref:T,name:"modelFile",id:"modelFile",type:"file",accept:".yaml,.json,.yml,.zip",onChange:e=>{const{files:t}=e.target;_(t&&t[0]||null)}})),0===g.length?null:Object(h.h)(i.a.Fragment,null,Object(h.h)("h5",null,"Database passwords"),Object(h.h)(u,null,a),n()(g).call(g,e=>Object(h.h)(m,{key:`password-for-${e}`},Object(h.h)("div",{className:"control-label"},e,Object(h.h)("span",{className:"required"},"*")),Object(h.h)("input",{name:`password-${e}`,autoComplete:`password-${e}`,type:"password",value:w[e],onChange:t=>$({...w,[e]:t.target.value})})))),N?Object(h.h)(i.a.Fragment,null,Object(h.h)(m,null,Object(h.h)("div",{className:"confirm-overwrite"},l),Object(h.h)("div",{className:"control-label"},Object(c.e)('Type "%s" to confirm',Object(c.e)("OVERWRITE"))),Object(h.h)("input",{id:"overwrite",type:"text",onChange:L}))):null)}},4541:function(e,t,a){"use strict";a.d(t,"a",(function(){return n}));var l=a(14);const n={name:Object(l.e)("Data"),tabs:[{name:"Databases",label:Object(l.e)("Databases"),url:"/databaseview/list/",usesRouter:!0},{name:"Datasets",label:Object(l.e)("Datasets"),url:"/tablemodelview/list/",usesRouter:!0},{name:"Saved queries",label:Object(l.e)("Saved queries"),url:"/savedqueryview/list/",usesRouter:!0},{name:"Query history",label:Object(l.e)("Query history"),url:"/superset/sqllab/history/",usesRouter:!0}]}},4912:function(e,t,a){"use strict";a.r(t);a(40);var l=a(14),n=a(47),o=a(91),i=a(0),s=a.n(i),c=a(96),r=a.n(c),d=a(42),b=a(445),h=a(125),u=a(129),m=a(1e3),p=a(1368),j=a(50),O=a(174),g=a(4526),v=a(4541),f=a(4532),y=a(309),x=a.n(y),_=a(5),w=a.n(_),$=a(48),N=a(1);const S=Object(n.j)(j.a)`
  cursor: pointer;

  path:first-of-type {
    fill: #999999;
  }
`,C={fontSize:"12px",lineHeight:"16px"};function k({tooltip:e,placement:t="right",trigger:a="hover",overlayStyle:l=C,bgColor:n="rgba(0,0,0,0.9)"}){return Object(N.h)(S,{title:e,placement:t,trigger:a,overlayStyle:l,color:n},Object(N.h)($.a,{name:"info-solid-small"}))}var T=a(134),A=a(44),q=a(4688),U=a(146),E=a(60);var L=a(101),D=a(233);const P=Object(n.j)(L.b)`
  .ant-collapse {
    .ant-collapse-header {
      padding-top: ${({theme:e})=>3.5*e.gridUnit}px;
      padding-bottom: ${({theme:e})=>2.5*e.gridUnit}px;

      .anticon.ant-collapse-arrow {
        top: calc(50% - ${6}px);
      }
      .helper {
        color: ${({theme:e})=>e.colors.grayscale.base};
      }
    }
    h4 {
      font-size: 16px;
      font-weight: bold;
      margin-top: 0;
      margin-bottom: ${({theme:e})=>e.gridUnit}px;
    }
    p.helper {
      margin-bottom: 0;
      padding: 0;
    }
  }
  .ant-modal-header {
    padding: 18px 16px 16px;
  }
  .ant-modal-body {
    padding-left: 0;
    padding-right: 0;
  }
  .ant-tabs-top > .ant-tabs-nav {
    margin-bottom: 0;
  }
  .ant-modal-close-x .close {
    color: ${({theme:e})=>e.colors.grayscale.dark1};
    opacity: 1;
  }

  .required {
    margin-left: ${({theme:e})=>e.gridUnit/2}px;
    color: ${({theme:e})=>e.colors.error.base};
  }

  .helper {
    display: block;
    padding: ${({theme:e})=>e.gridUnit}px 0;
    color: ${({theme:e})=>e.colors.grayscale.light1};
    font-size: ${({theme:e})=>e.typography.sizes.s-1}px;
    text-align: left;
  }
  .ant-modal-title > h4 {
    font-weight: bold;
  }
`,R=n.j.div`
  margin-bottom: ${({theme:e})=>6*e.gridUnit}px;
  &.mb-0 {
    margin-bottom: 0;
  }
  &.mb-8 {
    margin-bottom: ${({theme:e})=>2*e.gridUnit}px;
  }

  .control-label {
    color: ${({theme:e})=>e.colors.grayscale.dark1};
    font-size: ${({theme:e})=>e.typography.sizes.s-1}px;
    margin-bottom: ${({theme:e})=>2*e.gridUnit}px;
  }

  &.extra-container {
    padding-top: 8px;
  }

  .input-container {
    display: flex;
    align-items: top;

    label {
      display: flex;
      margin-left: ${({theme:e})=>2*e.gridUnit}px;
      margin-top: ${({theme:e})=>.75*e.gridUnit}px;
      font-family: ${({theme:e})=>e.typography.families.sansSerif};
      font-size: ${({theme:e})=>e.typography.sizes.m}px;
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
  &.expandable {
    height: 0;
    overflow: hidden;
    transition: height 0.25s;
    margin-left: ${({theme:e})=>8*e.gridUnit}px;
    margin-bottom: 0;
    padding: 0;
    .control-label {
      margin-bottom: 0;
    }
    &.open {
      height: ${102}px;
      padding-right: ${({theme:e})=>5*e.gridUnit}px;
    }
  }
`,H=Object(n.j)(D.d)`
  flex: 1 1 auto;
  border: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
  border-radius: ${({theme:e})=>e.gridUnit}px;
`,z=n.j.div`
  padding-top: ${({theme:e})=>e.gridUnit}px;
  .input-container {
    padding-top: ${({theme:e})=>e.gridUnit}px;
    padding-bottom: ${({theme:e})=>e.gridUnit}px;
  }
  &.expandable {
    height: 0;
    overflow: hidden;
    transition: height 0.25s;
    margin-left: ${({theme:e})=>7*e.gridUnit}px;
    &.open {
      height: ${154}px;
      &.ctas-open {
        height: ${256}px;
      }
    }
  }
`,I=Object(n.j)(T.c.TabPane)`
  padding-left: ${({theme:e})=>4*e.gridUnit}px;
  padding-right: ${({theme:e})=>4*e.gridUnit}px;
  margin-top: ${({theme:e})=>4*e.gridUnit}px;
`;var Q=Object(u.a)(({addDangerToast:e,addSuccessToast:t,onDatabaseAdd:a,onHide:o,show:s,database:c=null})=>{var r,d,h;const[u,m]=Object(i.useState)(!0),[p,j]=Object(i.useState)(null),[O,g]=Object(i.useState)(!0),[v,f]=Object(i.useState)("1"),y=Object(E.d)(e=>e.common.conf),_=null!==c,{state:{loading:$,resource:S},fetchResource:C,createResource:L,updateResource:D}=Object(b.g)("database",Object(l.e)("database"),e),Q=()=>{g(!0),o()},B=e=>{const{target:t}=e,{checked:a,name:l,value:n,type:o}=t,i={database_name:(null==p?void 0:p.database_name)||"",sqlalchemy_uri:(null==p?void 0:p.sqlalchemy_uri)||"",...p};i[l]="checkbox"===o?a:n,j(i)},F=(e,t)=>{const a={database_name:(null==p?void 0:p.database_name)||"",sqlalchemy_uri:(null==p?void 0:p.sqlalchemy_uri)||"",...p};a[t]=e,j(a)};if(_&&(!p||!p.id||(null==c?void 0:c.id)!==p.id||O&&s)){if(null!=c&&c.id&&!$){const t=c.id||0;f("1"),C(t).then(()=>{j(S)}).catch(t=>e(Object(l.e)("Sorry there was an error fetching database information: %s",t.message)))}}else!_&&(!p||p.id||O&&s)&&(f("1"),j({database_name:"",sqlalchemy_uri:""}));Object(i.useEffect)(()=>{var e;null!=p&&null!=(e=p.database_name)&&x()(e).call(e)&&null!=p&&p.sqlalchemy_uri?m(!1):m(!0)},[(null==p?void 0:p.database_name)||null,(null==p?void 0:p.sqlalchemy_uri)||null]),O&&s&&g(!1);const M=!(null==p||!p.expose_in_sqllab),W=!!(null!=p&&p.allow_ctas||null!=p&&p.allow_cvas);return Object(N.h)(P,{name:"database",className:"database-modal",disablePrimaryButton:u,height:"600px",onHandledPrimaryAction:()=>{if(_){var e;const t={database_name:(null==p?void 0:x()(e=p.database_name).call(e))||"",sqlalchemy_uri:(null==p?void 0:p.sqlalchemy_uri)||"",...p};t.id&&delete t.id,null!=p&&p.id&&D(p.id,t).then(e=>{e&&(a&&a(),Q())})}else if(p){var t;p.database_name=x()(t=p.database_name).call(t),L(p).then(e=>{e&&(a&&a(),Q())})}},onHide:Q,primaryButtonName:_?Object(l.e)("Save"):Object(l.e)("Add"),width:"500px",show:s,title:Object(N.h)("h4",null,_?Object(l.e)("Edit database"):Object(l.e)("Add database"))},Object(N.h)(T.c,{defaultActiveKey:"1",activeKey:v,onTabClick:e=>{f(e)}},Object(N.h)(I,{tab:Object(N.h)("span",null,Object(l.e)("Basic")),key:"1"},Object(N.h)(R,null,Object(N.h)("div",{className:"control-label"},Object(l.e)("Display Name"),Object(N.h)("span",{className:"required"},"*")),Object(N.h)("div",{className:"input-container"},Object(N.h)("input",{type:"text",name:"database_name",value:(null==p?void 0:p.database_name)||"",placeholder:Object(l.e)("Name your dataset"),onChange:B})),Object(N.h)("div",{className:"helper"},Object(l.e)("Pick a name to help you identify this database."))),Object(N.h)(R,null,Object(N.h)("div",{className:"control-label"},Object(l.e)("SQLAlchemy URI"),Object(N.h)("span",{className:"required"},"*")),Object(N.h)("div",{className:"input-container"},Object(N.h)("input",{type:"text",name:"sqlalchemy_uri",value:(null==p?void 0:p.sqlalchemy_uri)||"",autoComplete:"off",placeholder:Object(l.e)("dialect+driver://username:password@host:port/database"),onChange:B})),Object(N.h)("div",{className:"helper"},Object(l.e)("Refer to the "),Object(N.h)("a",{href:null!=(r=null==y?void 0:y.SQLALCHEMY_DOCS_URL)?r:"",target:"_blank",rel:"noopener noreferrer"},null!=(d=null==y?void 0:y.SQLALCHEMY_DISPLAY_TEXT)?d:""),Object(l.e)(" for more information on how to structure your URI."))),Object(N.h)(A.a,{onClick:()=>{var a;if(!p||!p.sqlalchemy_uri||!p.sqlalchemy_uri.length)return void e(Object(l.e)("Please enter a SQLAlchemy URI to test"));const n={sqlalchemy_uri:(null==p?void 0:p.sqlalchemy_uri)||"",database_name:(null==p?void 0:null==(a=p.database_name)?void 0:x()(a).call(a))||void 0,impersonate_user:(null==p?void 0:p.impersonate_user)||void 0,extra:(null==p?void 0:p.extra)||void 0,encrypted_extra:(null==p?void 0:p.encrypted_extra)||void 0,server_cert:(null==p?void 0:p.server_cert)||void 0};Object(b.b)(n,e,t)},cta:!0,buttonStyle:"link",style:{width:"100%",border:`1px solid ${n.k.colors.primary.base}`}},Object(l.e)("Test connection"))),Object(N.h)(T.c.TabPane,{tab:Object(N.h)("span",null,Object(l.e)("Advanced")),key:"2"},Object(N.h)(U.a,{expandIconPosition:"right",accordion:!0},Object(N.h)(U.a.Panel,{header:Object(N.h)("div",null,Object(N.h)("h4",null,"SQL Lab"),Object(N.h)("p",{className:"helper"},"Configure how this database will function in SQL Lab.")),key:"1"},Object(N.h)(R,{className:"mb-0"},Object(N.h)("div",{className:"input-container"},Object(N.h)(q.a,{id:"expose_in_sqllab",indeterminate:!1,checked:!(null==p||!p.expose_in_sqllab),onChange:B,labelText:Object(l.e)("Expose in SQL Lab")}),Object(N.h)(k,{tooltip:Object(l.e)("Allow this database to be queried in SQL Lab")})),Object(N.h)(z,{className:w()("expandable",{open:M,"ctas-open":W})},Object(N.h)(R,{className:"mb-0"},Object(N.h)("div",{className:"input-container"},Object(N.h)(q.a,{id:"allow_ctas",indeterminate:!1,checked:!(null==p||!p.allow_ctas),onChange:B,labelText:Object(l.e)("Allow CREATE TABLE AS")}),Object(N.h)(k,{tooltip:Object(l.e)("Allow creation of new tables based on queries")}))),Object(N.h)(R,{className:"mb-0"},Object(N.h)("div",{className:"input-container"},Object(N.h)(q.a,{id:"allow_cvas",indeterminate:!1,checked:!(null==p||!p.allow_cvas),onChange:B,labelText:Object(l.e)("Allow CREATE VIEW AS")}),Object(N.h)(k,{tooltip:Object(l.e)("Allow creation of new views based on queries")})),Object(N.h)(R,{className:w()("expandable",{open:W})},Object(N.h)("div",{className:"control-label"},Object(l.e)("CTAS & CVAS SCHEMA")),Object(N.h)("div",{className:"input-container"},Object(N.h)("input",{type:"text",name:"force_ctas_schema",value:(null==p?void 0:p.force_ctas_schema)||"",placeholder:Object(l.e)("Search or select schema"),onChange:B})),Object(N.h)("div",{className:"helper"},Object(l.e)("When allowing CREATE TABLE AS option in SQL Lab, this option forces the table to be created in this schema.")))),Object(N.h)(R,{className:"mb-0"},Object(N.h)("div",{className:"input-container"},Object(N.h)(q.a,{id:"allow_dml",indeterminate:!1,checked:!(null==p||!p.allow_dml),onChange:B,labelText:Object(l.e)("Allow DML")}),Object(N.h)(k,{tooltip:Object(l.e)("Allow manipulation of the database using non-SELECT statements such as UPDATE, DELETE, CREATE, etc.")}))),Object(N.h)(R,null,Object(N.h)("div",{className:"input-container"},Object(N.h)(q.a,{id:"allow_multi_schema_metadata_fetch",indeterminate:!1,checked:!(null==p||!p.allow_multi_schema_metadata_fetch),onChange:B,labelText:Object(l.e)("Allow multi schema metadata fetch")}),Object(N.h)(k,{tooltip:Object(l.e)("Allow SQL Lab to fetch a list of all tables and all views across all database schemas. For large data warehouse with thousands of tables, this can be expensive and put strain on the system.")})))))),Object(N.h)(U.a.Panel,{header:Object(N.h)("div",null,Object(N.h)("h4",null,"Performance"),Object(N.h)("p",{className:"helper"},"Adjust settings that will impact the performance of this database.")),key:"2"},Object(N.h)(R,{className:"mb-8"},Object(N.h)("div",{className:"control-label"},Object(l.e)("Chart cache timeout")),Object(N.h)("div",{className:"input-container"},Object(N.h)("input",{type:"number",name:"cache_timeout",value:(null==p?void 0:p.cache_timeout)||"",placeholder:Object(l.e)("Chart cache timeout"),onChange:B})),Object(N.h)("div",{className:"helper"},Object(l.e)("Duration (in seconds) of the caching timeout for charts of this database. A timeout of 0 indicates that the cache never expires. Note this defaults to the global timeout if undefined."))),Object(N.h)(R,{className:"mb-0"},Object(N.h)("div",{className:"input-container"},Object(N.h)(q.a,{id:"allow_run_async",indeterminate:!1,checked:!(null==p||!p.allow_run_async),onChange:B,labelText:Object(l.e)("Asynchronous query execution")}),Object(N.h)(k,{tooltip:Object(l.e)("Operate the database in asynchronous mode, meaning that the queries are executed on remote workers as opposed to on the web server itself. This assumes that you have a Celery worker setup as well as a results backend. Refer to the installation docs for more information.")})))),Object(N.h)(U.a.Panel,{header:Object(N.h)("div",null,Object(N.h)("h4",null,"Security"),Object(N.h)("p",{className:"helper"},"Add connection information for other systems.")),key:"3"},Object(N.h)(R,null,Object(N.h)("div",{className:"control-label"},Object(l.e)("Secure extra")),Object(N.h)("div",{className:"input-container"},Object(N.h)(H,{name:"encrypted_extra",value:(null==p?void 0:p.encrypted_extra)||"",placeholder:Object(l.e)("Secure extra"),onChange:e=>F(e,"encrypted_extra"),width:"100%",height:"160px"})),Object(N.h)("div",{className:"helper"},Object(N.h)("div",null,Object(l.e)("JSON string containing additional connection configuration.")),Object(N.h)("div",null,Object(l.e)("This is used to provide connection information for systems like Hive, Presto, and BigQuery, which do not conform to the username:password syntax normally used by SQLAlchemy.")))),Object(N.h)(R,null,Object(N.h)("div",{className:"control-label"},Object(l.e)("Root certificate")),Object(N.h)("div",{className:"input-container"},Object(N.h)("textarea",{name:"server_cert",value:(null==p?void 0:p.server_cert)||"",placeholder:Object(l.e)("Root certificate"),onChange:e=>{const{target:t}=e,{name:a,value:l}=t,n={database_name:(null==p?void 0:p.database_name)||"",sqlalchemy_uri:(null==p?void 0:p.sqlalchemy_uri)||"",...p};n[a]=l,j(n)}})),Object(N.h)("div",{className:"helper"},Object(l.e)("Optional CA_BUNDLE contents to validate HTTPS requests. Only available on certain database engines.")))),Object(N.h)(U.a.Panel,{header:Object(N.h)("div",null,Object(N.h)("h4",null,"Other"),Object(N.h)("p",{className:"helper"},"Additional settings.")),key:"4"},Object(N.h)(R,{className:"mb-0"},Object(N.h)("div",{className:"input-container"},Object(N.h)(q.a,{id:"impersonate_user",indeterminate:!1,checked:!(null==p||!p.impersonate_user),onChange:B,labelText:Object(l.e)("Impersonate Logged In User (Presto & Hive)")}),Object(N.h)(k,{tooltip:Object(l.e)("If Presto, all the queries in SQL Lab are going to be executed as the currently logged on user who must have permission to run them. If Hive and hive.server2.enable.doAs is enabled, will run the queries as service account, but impersonate the currently logged on user via hive.server2.proxy.user property.")}))),Object(N.h)(R,{className:"mb-0"},Object(N.h)("div",{className:"input-container"},Object(N.h)(q.a,{id:"allow_csv_upload",indeterminate:!1,checked:!(null==p||!p.allow_csv_upload),onChange:B,labelText:Object(l.e)("Allow data upload")}),Object(N.h)(k,{tooltip:Object(l.e)("If selected, please set the schemas allowed for data upload in Extra.")}))),Object(N.h)(R,{className:"extra-container"},Object(N.h)("div",{className:"control-label"},Object(l.e)("Extra")),Object(N.h)("div",{className:"input-container"},Object(N.h)(H,{name:"extra",value:null!=(h=null==p?void 0:p.extra)?h:'{\n  "metadata_params": {},\n  "engine_params": {},\n  "metadata_cache_timeout": {},\n  "schemas_allowed_for_csv_upload": [] \n}',placeholder:Object(l.e)("Secure extra"),onChange:e=>F(e,"extra"),width:"100%",height:"160px"})),Object(N.h)("div",{className:"helper"},Object(N.h)("div",null,Object(l.e)("JSON string containing extra configuration elements.")),Object(N.h)("div",null,Object(l.e)("1. The engine_params object gets unpacked into the sqlalchemy.create_engine call, while the metadata_params gets unpacked into the sqlalchemy.MetaData call.")),Object(N.h)("div",null,Object(l.e)('2. The metadata_cache_timeout is a cache timeout setting in seconds for metadata fetch of this database. Specify it as "metadata_cache_timeout": {"schema_cache_timeout": 600, "table_cache_timeout": 600}. If unset, cache will not be enabled for the functionality. A timeout of 0 indicates that the cache never expires.')),Object(N.h)("div",null,Object(l.e)('3. The schemas_allowed_for_csv_upload is a comma separated list of schemas that CSVs are allowed to upload to. Specify it as "schemas_allowed_for_csv_upload": ["public", "csv_upload"]. If database flavor does not support schema or any schema is allowed to be accessed, just leave the list empty.')),Object(N.h)("div",null,Object(l.e)("4. The version field is a string specifying this db's version. This should be used with Presto DBs so that the syntax is correct.")),Object(N.h)("div",null,Object(l.e)("5. The allows_virtual_table_explore field is a boolean specifying whether or not the Explore button in SQL Lab results is shown.")))))))))});const B=Object(l.e)('The passwords for the databases below are needed in order to import them. Please note that the "Secure Extra" and "Certificate" sections of the database configuration are not present in export files, and should be added manually after the import if they are needed.'),F=Object(l.e)("You are importing one or more databases that already exist. Overwriting might cause you to lose some of your work. Are you sure you want to overwrite?"),M=Object(n.j)(O.a.Check)`
  color: ${({theme:e})=>e.colors.grayscale.dark1};
`,W=Object(n.j)(O.a.CancelX)`
  color: ${({theme:e})=>e.colors.grayscale.dark1};
`,V=n.j.div`
  color: ${({theme:e})=>e.colors.grayscale.base};
`;function Y({value:e}){return e?Object(N.h)(M,null):Object(N.h)(W,null)}t.default=Object(u.a)((function({addDangerToast:e,addSuccessToast:t}){const{state:{loading:a,resourceCount:n,resourceCollection:c},hasPerm:u,fetchData:y,refreshData:x}=Object(b.f)("database",Object(l.e)("database"),e),[_,w]=Object(i.useState)(!1),[$,S]=Object(i.useState)(null),[C,k]=Object(i.useState)(null),[T,A]=Object(i.useState)(!1),[q,U]=Object(i.useState)([]),E=()=>{A(!0)},L=u("can_write"),D=u("can_write"),P=u("can_write"),R=u("can_read")&&Object(d.c)(d.a.VERSIONED_EXPORT),H={activeChild:"Databases",...v.a};L&&(H.buttons=[{"data-test":"btn-create-database",name:Object(N.h)(s.a.Fragment,null,Object(N.h)("i",{className:"fa fa-plus"})," ",Object(l.e)("Database")," "),buttonStyle:"primary",onClick:()=>{k(null),w(!0)}}],Object(d.c)(d.a.VERSIONED_EXPORT)&&H.buttons.push({name:Object(N.h)(j.a,{id:"import-tooltip",title:Object(l.e)("Import databases"),placement:"bottomRight"},Object(N.h)(O.a.Import,null)),buttonStyle:"link",onClick:E}));const z=Object(i.useMemo)(()=>[{accessor:"database_name",Header:Object(l.e)("Database")},{accessor:"backend",Header:Object(l.e)("Backend"),size:"lg",disableSortBy:!0},{accessor:"allow_run_async",Header:Object(N.h)(j.a,{id:"allow-run-async-header-tooltip",title:Object(l.e)("Asynchronous query execution"),placement:"top"},Object(N.h)("span",null,Object(l.e)("AQE"))),Cell:({row:{original:{allow_run_async:e}}})=>Object(N.h)(Y,{value:e}),size:"sm"},{accessor:"allow_dml",Header:Object(N.h)(j.a,{id:"allow-dml-header-tooltip",title:Object(l.e)("Allow data manipulation language"),placement:"top"},Object(N.h)("span",null,Object(l.e)("DML"))),Cell:({row:{original:{allow_dml:e}}})=>Object(N.h)(Y,{value:e}),size:"sm"},{accessor:"allow_csv_upload",Header:Object(l.e)("CSV upload"),Cell:({row:{original:{allow_csv_upload:e}}})=>Object(N.h)(Y,{value:e}),size:"md"},{accessor:"expose_in_sqllab",Header:Object(l.e)("Expose in SQL Lab"),Cell:({row:{original:{expose_in_sqllab:e}}})=>Object(N.h)(Y,{value:e}),size:"md"},{accessor:"created_by",disableSortBy:!0,Header:Object(l.e)("Created by"),Cell:({row:{original:{created_by:e}}})=>e?`${e.first_name} ${e.last_name}`:"",size:"xl"},{Cell:({row:{original:{changed_on_delta_humanized:e}}})=>e,Header:Object(l.e)("Last modified"),accessor:"changed_on_delta_humanized",size:"xl"},{Cell:({row:{original:e}})=>D||P||R?Object(N.h)(V,{className:"actions"},P&&Object(N.h)("span",{role:"button",tabIndex:0,className:"action-button",onClick:()=>{return t=e,o.a.get({endpoint:`/api/v1/database/${t.id}/related_objects/`}).then(({json:e={}})=>{S({...t,chart_count:e.charts.count,dashboard_count:e.dashboards.count})}).catch(Object(h.c)(e=>Object(l.e)("An error occurred while fetching database related data: %s",e)));var t}},Object(N.h)(j.a,{id:"delete-action-tooltip",title:Object(l.e)("Delete database"),placement:"bottom"},Object(N.h)(O.a.Trash,null))),R&&Object(N.h)(j.a,{id:"export-action-tooltip",title:Object(l.e)("Export"),placement:"bottom"},Object(N.h)("span",{role:"button",tabIndex:0,className:"action-button",onClick:()=>{return t=e,window.location.assign(`/api/v1/database/export/?q=${r.a.encode([t.id])}`);var t}},Object(N.h)(O.a.Share,null))),D&&Object(N.h)(j.a,{id:"edit-action-tooltip",title:Object(l.e)("Edit"),placement:"bottom"},Object(N.h)("span",{role:"button",tabIndex:0,className:"action-button",onClick:()=>(k(e),void w(!0))},Object(N.h)(O.a.EditAlt,null)))):null,Header:Object(l.e)("Actions"),id:"actions",hidden:!D&&!P,disableSortBy:!0}],[P,D,R]),I=Object(i.useMemo)(()=>[{Header:Object(l.e)("Expose in SQL Lab"),id:"expose_in_sqllab",input:"select",operator:g.a.equals,unfilteredLabel:"All",selects:[{label:"Yes",value:!0},{label:"No",value:!1}]},{Header:Object(N.h)(j.a,{id:"allow-run-async-filter-header-tooltip",title:Object(l.e)("Asynchronous query execution"),placement:"top"},Object(N.h)("span",null,Object(l.e)("AQE"))),id:"allow_run_async",input:"select",operator:g.a.equals,unfilteredLabel:"All",selects:[{label:"Yes",value:!0},{label:"No",value:!1}]},{Header:Object(l.e)("Search"),id:"database_name",input:"search",operator:g.a.contains}],[]);return Object(N.h)(s.a.Fragment,null,Object(N.h)(m.a,H),Object(N.h)(Q,{database:C,show:_,onHide:()=>w(!1),onDatabaseAdd:()=>{x()}}),$&&Object(N.h)(p.a,{description:Object(l.e)("The database %s is linked to %s charts that appear on %s dashboards. Are you sure you want to continue? Deleting the database will break those objects.",$.database_name,$.chart_count,$.dashboard_count),onConfirm:()=>{$&&function({id:a,database_name:n}){o.a.delete({endpoint:`/api/v1/database/${a}`}).then(()=>{x(),t(Object(l.e)("Deleted: %s",n)),S(null)},Object(h.c)(t=>e(Object(l.e)("There was an issue deleting %s: %s",n,t))))}($)},onHide:()=>S(null),open:!0,title:Object(l.e)("Delete Database?")}),Object(N.h)(g.b,{className:"database-list-view",columns:z,count:n,data:c,fetchData:y,filters:I,initialSort:[{id:"changed_on_delta_humanized",desc:!0}],loading:a,pageSize:25}),Object(N.h)(f.a,{resourceName:"database",resourceLabel:Object(l.e)("database"),passwordsNeededMessage:B,confirmOverwriteMessage:F,addDangerToast:e,addSuccessToast:t,onModelImport:()=>{A(!1),x()},show:T,onHide:()=>{A(!1)},passwordFields:q,setPasswordFields:U}))}))}}]);