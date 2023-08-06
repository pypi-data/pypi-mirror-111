(window.webpackJsonp=window.webpackJsonp||[]).push([[23],{4531:function(t,e,n){"use strict";n.d(e,"a",(function(){return b}));var a=n(11),o=n.n(a),l=(n(0),n(47)),c=n(50),i=n(174),r=n(1);const s=l.j.span`
  white-space: nowrap;
  min-width: 100px;
  svg,
  i {
    margin-right: 8px;

    &:hover {
      path {
        fill: ${({theme:t})=>t.colors.primary.base};
      }
    }
  }
`,d=l.j.span`
  color: ${({theme:t})=>t.colors.grayscale.base};
`;function b({actions:t}){return Object(r.h)(s,{className:"actions"},o()(t).call(t,(t,e)=>{const n=i.a[t.icon];return t.tooltip?Object(r.h)(c.a,{id:`${t.label}-tooltip`,title:t.tooltip,placement:t.placement,key:e},Object(r.h)(d,{role:"button",tabIndex:0,className:"action-button",onClick:t.onClick},Object(r.h)(n,null))):Object(r.h)(d,{role:"button",tabIndex:0,className:"action-button",onClick:t.onClick,key:e},Object(r.h)(n,null))}))}},4928:function(t,e,n){"use strict";n.r(e);n(40);var a=n(11),o=n.n(a),l=n(0),c=n.n(l),i=n(422),r=n(430),s=n(14),d=n(91),b=n(47),h=n(38),u=n.n(h),m=n(96),j=n.n(m),O=n(4531),p=n(44),g=n(1367),_=n(1368),f=n(4526),y=n(1e3),w=n(73),x=n(129),v=n(445),$=n(125),k=n(989),S=n(48),C=n(101),D=n(233),A=n(1);const H=b.j.div`
  margin: ${({theme:t})=>2*t.gridUnit}px auto
    ${({theme:t})=>4*t.gridUnit}px auto;
`,N=Object(b.j)(D.d)`
  border-radius: ${({theme:t})=>t.borderRadius}px;
  border: 1px solid ${({theme:t})=>t.colors.secondary.light2};
`,Y=Object(b.j)(S.a)`
  margin: auto ${({theme:t})=>2*t.gridUnit}px auto 0;
`,E=b.j.div`
  margin-bottom: ${({theme:t})=>5*t.gridUnit}px;

  .control-label {
    margin-bottom: ${({theme:t})=>2*t.gridUnit}px;
  }

  .required {
    margin-left: ${({theme:t})=>t.gridUnit/2}px;
    color: ${({theme:t})=>t.colors.error.base};
  }

  textarea {
    flex: 1 1 auto;
    height: ${({theme:t})=>17*t.gridUnit}px;
    resize: none;
    width: 100%;
  }

  textarea,
  input[type='text'] {
    padding: ${({theme:t})=>1.5*t.gridUnit}px
      ${({theme:t})=>2*t.gridUnit}px;
    border: 1px solid ${({theme:t})=>t.colors.grayscale.light2};
    border-radius: ${({theme:t})=>t.gridUnit}px;
  }

  input[type='text'] {
    width: 65%;
  }
`;var U=Object(x.a)(({addDangerToast:t,annnotationLayerId:e,annotation:n=null,onAnnotationAdd:a,onHide:o,show:c})=>{var i,r;const[d,b]=Object(l.useState)(!0),[h,m]=Object(l.useState)(null),[j,O]=Object(l.useState)(!0),p=null!==n,{state:{loading:g,resource:_},fetchResource:f,createResource:y,updateResource:w}=Object(v.g)(`annotation_layer/${e}/annotation`,Object(s.e)("annotation"),t),x=()=>{m({short_descr:"",start_dttm:"",end_dttm:"",json_metadata:"",long_descr:""})},$=()=>{O(!0),x(),o()},S=t=>{const{target:e}=t,n={...h,end_dttm:h?h.end_dttm:"",short_descr:h?h.short_descr:"",start_dttm:h?h.start_dttm:""};n[e.name]=e.value,m(n)};return Object(l.useEffect)(()=>{if(p&&(!h||!h.id||n&&n.id!==h.id||j&&c)){if(n&&null!==n.id&&!g){const t=n.id||0;f(t)}}else!p&&(!h||h.id||j&&c)&&x()},[n]),Object(l.useEffect)(()=>{_&&m(_)},[_]),Object(l.useEffect)(()=>{h&&h.short_descr.length&&h.start_dttm.length&&h.end_dttm.length?b(!1):b(!0)},[h?h.short_descr:"",h?h.start_dttm:"",h?h.end_dttm:""]),j&&c&&O(!1),Object(A.h)(C.b,{disablePrimaryButton:d,onHandledPrimaryAction:()=>{if(p){if(h&&h.id){const t=h.id;delete h.id,delete h.created_by,delete h.changed_by,delete h.changed_on_delta_humanized,delete h.layer,w(t,h).then(t=>{t&&(a&&a(),$())})}}else h&&y(h).then(t=>{t&&(a&&a(),$())})},onHide:$,primaryButtonName:p?Object(s.e)("Save"):Object(s.e)("Add"),show:c,width:"55%",title:Object(A.h)("h4",null,p?Object(A.h)(Y,{name:"edit-alt"}):Object(A.h)(Y,{name:"plus-large"}),p?Object(s.e)("Edit annotation"):Object(s.e)("Add annotation"))},Object(A.h)(H,null,Object(A.h)("h4",null,Object(s.e)("Basic information"))),Object(A.h)(E,null,Object(A.h)("div",{className:"control-label"},Object(s.e)("Annotation name"),Object(A.h)("span",{className:"required"},"*")),Object(A.h)("input",{name:"short_descr",onChange:S,type:"text",value:null==h?void 0:h.short_descr})),Object(A.h)(E,null,Object(A.h)("div",{className:"control-label"},Object(s.e)("date"),Object(A.h)("span",{className:"required"},"*")),Object(A.h)(k.b,{format:"YYYY-MM-DD HH:mm",onChange:(t,e)=>{const n={...h,end_dttm:h&&e[1].length?u()(e[1]).format("YYYY-MM-DD HH:mm"):"",short_descr:h?h.short_descr:"",start_dttm:h&&e[0].length?u()(e[0]).format("YYYY-MM-DD HH:mm"):""};m(n)},showTime:{format:"hh:mm a"},use12Hours:!0,value:null!=h&&null!=(i=h.start_dttm)&&i.length||null!=h&&null!=(r=h.end_dttm)&&r.length?[u()(h.start_dttm),u()(h.end_dttm)]:null})),Object(A.h)(H,null,Object(A.h)("h4",null,Object(s.e)("Additional information"))),Object(A.h)(E,null,Object(A.h)("div",{className:"control-label"},Object(s.e)("description")),Object(A.h)("textarea",{name:"long_descr",value:h?h.long_descr:"",placeholder:Object(s.e)("Description (this can be seen in the list)"),onChange:S})),Object(A.h)(E,null,Object(A.h)("div",{className:"control-label"},Object(s.e)("JSON metadata")),Object(A.h)(N,{onChange:t=>{const e={...h,end_dttm:h?h.end_dttm:"",json_metadata:t,short_descr:h?h.short_descr:"",start_dttm:h?h.start_dttm:""};m(e)},value:h&&h.json_metadata?h.json_metadata:"",width:"100%",height:"120px"})))});e.default=Object(x.a)((function({addDangerToast:t,addSuccessToast:e}){const{annotationLayerId:n}=Object(i.g)(),{state:{loading:a,resourceCount:h,resourceCollection:m,bulkSelectEnabled:x},fetchData:k,refreshData:S,toggleBulkSelect:C}=Object(v.f)(`annotation_layer/${n}/annotation`,Object(s.e)("annotation"),t,!1),[D,H]=Object(l.useState)(!1),[N,Y]=Object(l.useState)(""),[E,B]=Object(l.useState)(null),[T,M]=Object(l.useState)(null),L=t=>{B(t),H(!0)},I=Object(l.useCallback)((async function(){try{const t=await d.a.get({endpoint:`/api/v1/annotation_layer/${n}`});Y(t.json.result.name)}catch(e){await Object(w.a)(e).then(({error:e})=>{t(e.error||e.statusText||e)})}}),[n]);Object(l.useEffect)(()=>{I()},[I]);const q=[{id:"short_descr",desc:!0}],z=Object(l.useMemo)(()=>[{accessor:"short_descr",Header:Object(s.e)("Label")},{accessor:"long_descr",Header:Object(s.e)("Description")},{Cell:({row:{original:{start_dttm:t}}})=>u()(new Date(t)).format("ll"),Header:Object(s.e)("Start"),accessor:"start_dttm"},{Cell:({row:{original:{end_dttm:t}}})=>u()(new Date(t)).format("ll"),Header:Object(s.e)("End"),accessor:"end_dttm"},{Cell:({row:{original:t}})=>{const e=[{label:"edit-action",tooltip:Object(s.e)("Edit annotation"),placement:"bottom",icon:"Edit",onClick:()=>L(t)},{label:"delete-action",tooltip:Object(s.e)("Delete annotation"),placement:"bottom",icon:"Trash",onClick:()=>M(t)}];return Object(A.h)(O.a,{actions:e})},Header:Object(s.e)("Actions"),id:"actions",disableSortBy:!0}],[!0,!0]),R=[];R.push({name:Object(A.h)(c.a.Fragment,null,Object(A.h)("i",{className:"fa fa-plus"})," ",Object(s.e)("Annotation")),buttonStyle:"primary",onClick:()=>{L(null)}}),R.push({name:Object(s.e)("Bulk select"),onClick:C,buttonStyle:"secondary","data-test":"annotation-bulk-select"});const F=b.j.div`
    display: flex;
    flex-direction: row;

    a,
    Link {
      margin-left: 16px;
      font-size: 12px;
      font-weight: normal;
      text-decoration: underline;
    }
  `;let J=!0;try{Object(i.f)()}catch(t){J=!1}const P=Object(A.h)(p.a,{buttonStyle:"primary",onClick:()=>{L(null)}},Object(A.h)(c.a.Fragment,null,Object(A.h)("i",{className:"fa fa-plus"})," ",Object(s.e)("Annotation"))),G={message:Object(s.e)("No annotation yet"),slot:P};return Object(A.h)(c.a.Fragment,null,Object(A.h)(y.a,{name:Object(A.h)(F,null,Object(A.h)("span",null,Object(s.e)(`Annotation Layer ${N}`)),Object(A.h)("span",null,J?Object(A.h)(r.b,{to:"/annotationlayermodelview/list/"},"Back to all"):Object(A.h)("a",{href:"/annotationlayermodelview/list/"},"Back to all"))),buttons:R}),Object(A.h)(U,{addDangerToast:t,annotation:E,show:D,onAnnotationAdd:()=>S(),annnotationLayerId:n,onHide:()=>H(!1)}),T&&Object(A.h)(_.a,{description:Object(s.e)(`Are you sure you want to delete ${null==T?void 0:T.short_descr}?`),onConfirm:()=>{T&&(({id:a,short_descr:o})=>{d.a.delete({endpoint:`/api/v1/annotation_layer/${n}/annotation/${a}`}).then(()=>{S(),M(null),e(Object(s.e)("Deleted: %s",o))},Object($.c)(e=>t(Object(s.e)("There was an issue deleting %s: %s",o,e))))})(T)},onHide:()=>M(null),open:!0,title:Object(s.e)("Delete Annotation?")}),Object(A.h)(g.a,{title:Object(s.e)("Please confirm"),description:Object(s.e)("Are you sure you want to delete the selected annotations?"),onConfirm:a=>{d.a.delete({endpoint:`/api/v1/annotation_layer/${n}/annotation/?q=${j.a.encode(o()(a).call(a,({id:t})=>t))}`}).then(({json:t={}})=>{S(),e(t.message)},Object($.c)(e=>t(Object(s.e)("There was an issue deleting the selected annotations: %s",e))))}},t=>{const e=[{key:"delete",name:Object(s.e)("Delete"),onSelect:t,type:"danger"}];return Object(A.h)(f.b,{className:"annotations-list-view",bulkActions:e,bulkSelectEnabled:x,columns:z,count:h,data:m,disableBulkSelect:C,emptyState:G,fetchData:k,initialSort:q,loading:a,pageSize:25})}))}))}}]);