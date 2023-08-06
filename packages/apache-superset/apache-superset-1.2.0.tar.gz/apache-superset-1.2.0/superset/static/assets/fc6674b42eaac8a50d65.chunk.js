(window.webpackJsonp=window.webpackJsonp||[]).push([[22],{4531:function(e,t,a){"use strict";a.d(t,"a",(function(){return b}));var n=a(11),o=a.n(n),c=(a(0),a(47)),l=a(50),i=a(174),r=a(1);const s=c.j.span`
  white-space: nowrap;
  min-width: 100px;
  svg,
  i {
    margin-right: 8px;

    &:hover {
      path {
        fill: ${({theme:e})=>e.colors.primary.base};
      }
    }
  }
`,d=c.j.span`
  color: ${({theme:e})=>e.colors.grayscale.base};
`;function b({actions:e}){return Object(r.h)(s,{className:"actions"},o()(e).call(e,(e,t)=>{const a=i.a[e.icon];return e.tooltip?Object(r.h)(l.a,{id:`${e.label}-tooltip`,title:e.tooltip,placement:e.placement,key:t},Object(r.h)(d,{role:"button",tabIndex:0,className:"action-button",onClick:e.onClick},Object(r.h)(a,null))):Object(r.h)(d,{role:"button",tabIndex:0,className:"action-button",onClick:e.onClick,key:t},Object(r.h)(a,null))}))}},4927:function(e,t,a){"use strict";a.r(t);a(40);var n=a(33),o=a.n(n),c=a(11),l=a.n(c),i=a(0),r=a.n(i),s=a(96),d=a.n(s),b=a(14),u=a(91),h=a(422),j=a(430),m=a(38),O=a.n(m),p=a(445),g=a(125),y=a(129),f=a(1e3),w=a(4531),x=a(4526),C=a(44),S=a(1368),D=a(1367),v=a(47),$=a(48),k=a(101),_=a(1);const A=v.j.div`
  margin: ${({theme:e})=>2*e.gridUnit}px auto
    ${({theme:e})=>4*e.gridUnit}px auto;
`,H=Object(v.j)($.a)`
  margin: auto ${({theme:e})=>2*e.gridUnit}px auto 0;
`,M=v.j.div`
  margin-bottom: ${({theme:e})=>10*e.gridUnit}px;

  .control-label {
    margin-bottom: ${({theme:e})=>2*e.gridUnit}px;
  }

  .required {
    margin-left: ${({theme:e})=>e.gridUnit/2}px;
    color: ${({theme:e})=>e.colors.error.base};
  }

  textarea,
  input[type='text'] {
    padding: ${({theme:e})=>1.5*e.gridUnit}px
      ${({theme:e})=>2*e.gridUnit}px;
    border: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
    border-radius: ${({theme:e})=>e.gridUnit}px;
    width: 50%;
  }

  input,
  textarea {
    flex: 1 1 auto;
  }

  textarea {
    width: 100%;
    height: 160px;
    resize: none;
  }

  input::placeholder,
  textarea::placeholder {
    color: ${({theme:e})=>e.colors.grayscale.light1};
  }
`;var N=Object(y.a)(({addDangerToast:e,onLayerAdd:t,onHide:a,show:n,layer:o=null})=>{const[c,l]=Object(i.useState)(!0),[r,s]=Object(i.useState)(),[d,u]=Object(i.useState)(!0),h=null!==o,{state:{loading:j,resource:m},fetchResource:O,createResource:g,updateResource:y}=Object(p.g)("annotation_layer",Object(b.e)("annotation_layer"),e),f=()=>{s({name:"",descr:""})},w=()=>{u(!0),f(),a()},x=e=>{const{target:t}=e,a={...r,name:r?r.name:"",descr:r?r.descr:""};a[t.name]=t.value,s(a)};return Object(i.useEffect)(()=>{if(h&&(!r||!r.id||o&&o.id!==r.id||d&&n)){if(n&&o&&null!==o.id&&!j){const e=o.id||0;O(e)}}else!h&&(!r||r.id||d&&n)&&f()},[o,n]),Object(i.useEffect)(()=>{m&&s(m)},[m]),Object(i.useEffect)(()=>{r&&r.name.length?l(!1):l(!0)},[r?r.name:"",r?r.descr:""]),d&&n&&u(!1),Object(_.h)(k.b,{disablePrimaryButton:c,onHandledPrimaryAction:()=>{if(h){if(r&&r.id){const e=r.id;delete r.id,delete r.created_by,y(e,r).then(e=>{e&&w()})}}else r&&g(r).then(e=>{e&&(t&&t(e),w())})},onHide:w,primaryButtonName:h?Object(b.e)("Save"):Object(b.e)("Add"),show:n,width:"55%",title:Object(_.h)("h4",null,h?Object(_.h)(H,{name:"edit-alt"}):Object(_.h)(H,{name:"plus-large"}),h?Object(b.e)("Edit annotation layer properties"):Object(b.e)("Add annotation layer"))},Object(_.h)(A,null,Object(_.h)("h4",null,Object(b.e)("Basic information"))),Object(_.h)(M,null,Object(_.h)("div",{className:"control-label"},Object(b.e)("Annotation layer name"),Object(_.h)("span",{className:"required"},"*")),Object(_.h)("input",{name:"name",onChange:x,type:"text",value:null==r?void 0:r.name})),Object(_.h)(M,null,Object(_.h)("div",{className:"control-label"},Object(b.e)("description")),Object(_.h)("textarea",{name:"descr",value:null==r?void 0:r.descr,placeholder:Object(b.e)("Description (this can be seen in the list)"),onChange:x})))});t.default=Object(y.a)((function({addDangerToast:e,addSuccessToast:t,user:a}){const{state:{loading:n,resourceCount:c,resourceCollection:s,bulkSelectEnabled:m},hasPerm:y,fetchData:v,refreshData:$,toggleBulkSelect:k}=Object(p.f)("annotation_layer",Object(b.e)("Annotation layers"),e),[A,H]=Object(i.useState)(!1),[M,U]=Object(i.useState)(null),[T,Y]=Object(i.useState)(null),B=y("can_write"),E=y("can_write"),z=y("can_write");function F(e){U(e),H(!0)}const L=[{id:"name",desc:!0}],P=Object(i.useMemo)(()=>[{accessor:"name",Header:Object(b.e)("Name"),Cell:({row:{original:{id:e,name:t}}})=>{let a=!0;try{Object(h.f)()}catch(e){a=!1}return a?Object(_.h)(j.b,{to:`/annotationmodelview/${e}/annotation`},t):Object(_.h)("a",{href:`/annotationmodelview/${e}/annotation`},t)}},{accessor:"descr",Header:Object(b.e)("Description")},{Cell:({row:{original:{changed_on:e}}})=>{const t=new Date(e),a=new Date(Date.UTC(t.getFullYear(),t.getMonth(),t.getDate(),t.getHours(),t.getMinutes(),t.getSeconds(),t.getMilliseconds()));return O()(a).format("MMM DD, YYYY")},Header:Object(b.e)("Last modified"),accessor:"changed_on",size:"xl"},{Cell:({row:{original:{created_on:e}}})=>{const t=new Date(e),a=new Date(Date.UTC(t.getFullYear(),t.getMonth(),t.getDate(),t.getHours(),t.getMinutes(),t.getSeconds(),t.getMilliseconds()));return O()(a).format("MMM DD, YYYY")},Header:Object(b.e)("Created on"),accessor:"created_on",size:"xl"},{accessor:"created_by",disableSortBy:!0,Header:Object(b.e)("Created by"),Cell:({row:{original:{created_by:e}}})=>e?`${e.first_name} ${e.last_name}`:"",size:"xl"},{Cell:({row:{original:e}})=>{var t;const a=o()(t=[E?{label:"edit-action",tooltip:Object(b.e)("Edit template"),placement:"bottom",icon:"Edit",onClick:()=>F(e)}:null,z?{label:"delete-action",tooltip:Object(b.e)("Delete template"),placement:"bottom",icon:"Trash",onClick:()=>Y(e)}:null]).call(t,e=>!!e);return Object(_.h)(w.a,{actions:a})},Header:Object(b.e)("Actions"),id:"actions",disableSortBy:!0,hidden:!E&&!z,size:"xl"}],[z,B]),q=[];B&&q.push({name:Object(_.h)(r.a.Fragment,null,Object(_.h)("i",{className:"fa fa-plus"})," ",Object(b.e)("Annotation layer")),buttonStyle:"primary",onClick:()=>{F(null)}}),z&&q.push({name:Object(b.e)("Bulk select"),onClick:k,buttonStyle:"secondary"});const I=Object(i.useMemo)(()=>[{Header:Object(b.e)("Created by"),id:"created_by",input:"select",operator:x.a.relationOneMany,unfilteredLabel:"All",fetchSelects:Object(g.e)("annotation_layer","created_by",Object(g.c)(e=>Object(b.e)("An error occurred while fetching dataset datasource values: %s",e)),a.userId),paginate:!0},{Header:Object(b.e)("Search"),id:"name",input:"search",operator:x.a.contains}],[]),R=Object(_.h)(C.a,{buttonStyle:"primary",onClick:()=>{F(null)}},Object(_.h)(r.a.Fragment,null,Object(_.h)("i",{className:"fa fa-plus"})," ",Object(b.e)("Annotation layer"))),J={message:Object(b.e)("No annotation layers yet"),slot:R};return Object(_.h)(r.a.Fragment,null,Object(_.h)(f.a,{name:Object(b.e)("Annotation layers"),buttons:q}),Object(_.h)(N,{addDangerToast:e,layer:M,onLayerAdd:e=>{window.location.href=`/annotationmodelview/${e}/annotation`},onHide:()=>{$(),H(!1)},show:A}),T&&Object(_.h)(S.a,{description:Object(b.e)("This action will permanently delete the layer."),onConfirm:()=>{T&&(({id:a,name:n})=>{u.a.delete({endpoint:`/api/v1/annotation_layer/${a}`}).then(()=>{$(),Y(null),t(Object(b.e)("Deleted: %s",n))},Object(g.c)(t=>e(Object(b.e)("There was an issue deleting %s: %s",n,t))))})(T)},onHide:()=>Y(null),open:!0,title:Object(b.e)("Delete Layer?")}),Object(_.h)(D.a,{title:Object(b.e)("Please confirm"),description:Object(b.e)("Are you sure you want to delete the selected layers?"),onConfirm:a=>{u.a.delete({endpoint:`/api/v1/annotation_layer/?q=${d.a.encode(l()(a).call(a,({id:e})=>e))}`}).then(({json:e={}})=>{$(),t(e.message)},Object(g.c)(t=>e(Object(b.e)("There was an issue deleting the selected layers: %s",t))))}},e=>{const t=z?[{key:"delete",name:Object(b.e)("Delete"),onSelect:e,type:"danger"}]:[];return Object(_.h)(x.b,{className:"annotation-layers-list-view",columns:P,count:c,data:s,fetchData:v,filters:I,initialSort:L,loading:n,pageSize:25,bulkActions:t,bulkSelectEnabled:m,disableBulkSelect:k,emptyState:J})}))}))}}]);