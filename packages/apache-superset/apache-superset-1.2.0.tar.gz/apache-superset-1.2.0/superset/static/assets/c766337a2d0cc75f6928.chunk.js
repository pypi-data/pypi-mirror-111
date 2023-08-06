(window.webpackJsonp=window.webpackJsonp||[]).push([[24],{4532:function(e,t,a){"use strict";a(40);var r=a(11),l=a.n(r),c=a(0),n=a.n(c),o=a(47),i=a(14),s=a(48),d=a(101),b=a(445),u=a(1);Object(o.j)(s.a)`
  margin: auto ${({theme:e})=>2*e.gridUnit}px auto 0;
`;const h=o.j.div`
  display: block;
  color: ${({theme:e})=>e.colors.grayscale.base};
  font-size: ${({theme:e})=>e.typography.sizes.s-1}px;
`,m=o.j.div`
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
`;t.a=({resourceName:e,resourceLabel:t,passwordsNeededMessage:a,confirmOverwriteMessage:r,addDangerToast:o,addSuccessToast:s,onModelImport:p,show:O,onHide:j,passwordFields:g=[],setPasswordFields:y=(()=>{})})=>{const[f,w]=Object(c.useState)(!0),[v,_]=Object(c.useState)(null),[x,S]=Object(c.useState)({}),[C,E]=Object(c.useState)(!1),[N,T]=Object(c.useState)(!1),k=Object(c.useRef)(null),$=()=>{_(null),y([]),S({}),E(!1),T(!1),k&&k.current&&(k.current.value="")},{state:{alreadyExists:z,passwordsNeeded:I},importResource:A}=Object(b.e)(e,t,e=>{$(),o(e)});Object(c.useEffect)(()=>{y(I)},[I,y]),Object(c.useEffect)(()=>{E(z.length>0)},[z,E]);const H=e=>{var t,a;const r=null!=(t=null==(a=e.currentTarget)?void 0:a.value)?t:"";T(r.toUpperCase()===Object(i.e)("OVERWRITE"))};return f&&O&&w(!1),Object(u.h)(d.b,{name:"model",className:"import-model-modal",disablePrimaryButton:null===v||C&&!N,onHandledPrimaryAction:()=>{null!==v&&A(v,x,N).then(e=>{e&&(s(Object(i.e)("The import was successful")),$(),p())})},onHide:()=>{w(!0),j(),$()},primaryButtonName:C?Object(i.e)("Overwrite"):Object(i.e)("Import"),primaryButtonType:C?"danger":"primary",width:"750px",show:O,title:Object(u.h)("h4",null,Object(i.e)("Import %s",t))},Object(u.h)(m,null,Object(u.h)("div",{className:"control-label"},Object(u.h)("label",{htmlFor:"modelFile"},Object(i.e)("File"),Object(u.h)("span",{className:"required"},"*"))),Object(u.h)("input",{ref:k,name:"modelFile",id:"modelFile",type:"file",accept:".yaml,.json,.yml,.zip",onChange:e=>{const{files:t}=e.target;_(t&&t[0]||null)}})),0===g.length?null:Object(u.h)(n.a.Fragment,null,Object(u.h)("h5",null,"Database passwords"),Object(u.h)(h,null,a),l()(g).call(g,e=>Object(u.h)(m,{key:`password-for-${e}`},Object(u.h)("div",{className:"control-label"},e,Object(u.h)("span",{className:"required"},"*")),Object(u.h)("input",{name:`password-${e}`,autoComplete:`password-${e}`,type:"password",value:x[e],onChange:t=>S({...x,[e]:t.target.value})})))),C?Object(u.h)(n.a.Fragment,null,Object(u.h)(m,null,Object(u.h)("div",{className:"confirm-overwrite"},r),Object(u.h)("div",{className:"control-label"},Object(i.e)('Type "%s" to confirm',Object(i.e)("OVERWRITE"))),Object(u.h)("input",{id:"overwrite",type:"text",onChange:H}))):null)}},4840:function(e,t,a){var r=a(844),l=a(1872);e.exports=function(e,t){return e&&e.length?l(e,r(t,2)):[]}},4899:function(e,t,a){"use strict";a.r(t);a(40);var r=a(267),l=a.n(r),c=a(204),n=a.n(c),o=a(11),i=a.n(o),s=a(4840),d=a.n(s),b=a(14),u=a(178),h=a(91),m=a(47),p=a(0),O=a.n(p),j=a(96),g=a.n(j),y=a(42),f=a(125),w=a(445),v=a(1367),_=a(1e3),x=a(826),S=a(4526),C=a(710),E=a(129),N=a(1339),T=a(4532),k=a(50),$=a(174),z=a(2091),I=a(1);const A=Object(b.e)('The passwords for the databases below are needed in order to import them together with the charts. Please note that the "Secure Extra" and "Certificate" sections of the database configuration are not present in export files, and should be added manually after the import if they are needed.'),H=Object(b.e)("You are importing one or more charts that already exist. Overwriting might cause you to lose some of your work. Are you sure you want to overwrite?"),F=Object(u.a)(),D=m.j.div`
  color: ${({theme:e})=>e.colors.grayscale.base};
`;t.default=Object(E.a)((function(e){var t,a;const{addDangerToast:r,addSuccessToast:c}=e,{state:{loading:o,resourceCount:s,resourceCollection:u,bulkSelectEnabled:m},setResourceCollection:j,hasPerm:E,fetchData:M,toggleBulkSelect:U,refreshData:R}=Object(w.f)("chart",Object(b.e)("chart"),r),B=Object(p.useMemo)(()=>i()(u).call(u,e=>e.id),[u]),[L,P]=Object(w.d)("chart",B,r),{sliceCurrentlyEditing:V,handleChartUpdated:q,openChartEditModal:W,closeChartEditModal:J}=Object(w.c)(j,u),[X,Y]=Object(p.useState)(!1),[G,K]=Object(p.useState)([]),Q=()=>{Y(!0)},Z=E("can_write"),ee=E("can_write"),te=E("can_write"),ae=E("can_read")&&Object(y.c)(y.a.VERSIONED_EXPORT),re=[{id:"changed_on_delta_humanized",desc:!0}],le=Object(p.useMemo)(()=>[{Cell:({row:{original:{id:e}}})=>Object(I.h)(x.a,{itemId:e,saveFaveStar:L,isStarred:P[e]}),Header:"",id:"id",disableSortBy:!0,size:"xs"},{Cell:({row:{original:{url:e,slice_name:t}}})=>Object(I.h)("a",{href:e},t),Header:Object(b.e)("Chart"),accessor:"slice_name"},{Cell:({row:{original:{viz_type:e}}})=>{var t;return(null==(t=F.get(e))?void 0:t.name)||e},Header:Object(b.e)("Visualization type"),accessor:"viz_type",size:"xxl"},{Cell:({row:{original:{datasource_name_text:e,datasource_url:t}}})=>Object(I.h)("a",{href:t},e),Header:Object(b.e)("Dataset"),accessor:"datasource_id",disableSortBy:!0,size:"xl"},{Cell:({row:{original:{changed_by_name:e,changed_by_url:t}}})=>Object(I.h)("a",{href:t},e),Header:Object(b.e)("Modified by"),accessor:"changed_by.first_name",size:"xl"},{Cell:({row:{original:{changed_on_delta_humanized:e}}})=>Object(I.h)("span",{className:"no-wrap"},e),Header:Object(b.e)("Last modified"),accessor:"changed_on_delta_humanized",size:"xl"},{accessor:"owners",hidden:!0,disableSortBy:!0},{Cell:({row:{original:{created_by:e}}})=>e?`${e.first_name} ${e.last_name}`:"",Header:Object(b.e)("Created by"),accessor:"created_by",disableSortBy:!0,size:"xl"},{Cell:({row:{original:e}})=>ee||te||ae?Object(I.h)(D,{className:"actions"},te&&Object(I.h)(v.a,{title:Object(b.e)("Please confirm"),description:Object(I.h)(O.a.Fragment,null,Object(b.e)("Are you sure you want to delete")," ",Object(I.h)("b",null,e.slice_name),"?"),onConfirm:()=>Object(f.l)(e,c,r,R)},e=>Object(I.h)(k.a,{id:"delete-action-tooltip",title:Object(b.e)("Delete"),placement:"bottom"},Object(I.h)("span",{role:"button",tabIndex:0,className:"action-button",onClick:e},Object(I.h)($.a.Trash,null)))),ae&&Object(I.h)(k.a,{id:"export-action-tooltip",title:Object(b.e)("Export"),placement:"bottom"},Object(I.h)("span",{role:"button",tabIndex:0,className:"action-button",onClick:()=>Object(f.i)([e])},Object(I.h)($.a.Share,null))),ee&&Object(I.h)(k.a,{id:"edit-action-tooltip",title:Object(b.e)("Edit"),placement:"bottom"},Object(I.h)("span",{role:"button",tabIndex:0,className:"action-button",onClick:()=>W(e)},Object(I.h)($.a.EditAlt,null)))):null,Header:Object(b.e)("Actions"),id:"actions",disableSortBy:!0,hidden:!ee&&!te}],[ee,te,ae,P]),ce=[{Header:Object(b.e)("Owner"),id:"owners",input:"select",operator:S.a.relationManyMany,unfilteredLabel:Object(b.e)("All"),fetchSelects:Object(f.e)("chart","owners",Object(f.c)(e=>r(Object(b.e)("An error occurred while fetching chart owners values: %s",e))),e.user.userId),paginate:!0},{Header:Object(b.e)("Created by"),id:"created_by",input:"select",operator:S.a.relationOneMany,unfilteredLabel:Object(b.e)("All"),fetchSelects:Object(f.e)("chart","created_by",Object(f.c)(e=>r(Object(b.e)("An error occurred while fetching chart created by values: %s",e))),e.user.userId),paginate:!0},{Header:Object(b.e)("Viz type"),id:"viz_type",input:"select",operator:S.a.equals,unfilteredLabel:Object(b.e)("All"),selects:n()(t=i()(a=l()(F).call(F)).call(a,e=>{var t;return{label:(null==(t=F.get(e))?void 0:t.name)||e,value:e}})).call(t,(e,t)=>e.label&&t.label?e.label>t.label?1:e.label<t.label?-1:0:0)},{Header:Object(b.e)("Dataset"),id:"datasource_id",input:"select",operator:S.a.equals,unfilteredLabel:Object(b.e)("All"),fetchSelects:(ne=Object(f.c)(e=>r(Object(b.e)("An error occurred while fetching chart dataset values: %s",e))),async(e="",t,a)=>{const r=e?{filters:[{col:"table_name",opr:"sw",value:e}]}:{};try{var l;const e=g.a.encode({columns:["datasource_name","datasource_id"],keys:["none"],order_column:"table_name",order_direction:"asc",...t?{page:t}:{},...a?{page_size:a}:{},...r}),{json:c={}}=await h.a.get({endpoint:`/api/v1/dataset/?q=${e}`}),n=null==c?void 0:null==(l=c.result)?void 0:i()(l).call(l,({table_name:e,id:t})=>({label:e,value:t}));return d()(n,"value")}catch(e){ne(e)}return[]}),paginate:!1},{Header:Object(b.e)("Favorite"),id:"id",urlDisplay:"favorite",input:"select",operator:S.a.chartIsFav,unfilteredLabel:Object(b.e)("Any"),selects:[{label:Object(b.e)("Yes"),value:!0},{label:Object(b.e)("No"),value:!1}]},{Header:Object(b.e)("Search"),id:"slice_name",input:"search",operator:S.a.chartAllText}];var ne;const oe=[{desc:!1,id:"slice_name",label:Object(b.e)("Alphabetical"),value:"alphabetical"},{desc:!0,id:"changed_on_delta_humanized",label:Object(b.e)("Recently modified"),value:"recently_modified"},{desc:!1,id:"changed_on_delta_humanized",label:Object(b.e)("Least recently modified"),value:"least_recently_modified"}];function ie(t){const{userId:a}=e.user,l=Object(C.a)(a.toString(),null);return Object(I.h)(z.a,{chart:t,showThumbnails:l?l.thumbnails:Object(y.c)(y.a.THUMBNAILS),hasPerm:E,openChartEditModal:W,bulkSelectEnabled:m,addDangerToast:r,addSuccessToast:c,refreshData:R,loading:o,favoriteStatus:P[t.id],saveFavoriteStatus:L})}const se=[];return(te||ae)&&se.push({name:Object(b.e)("Bulk select"),buttonStyle:"secondary","data-test":"bulk-select",onClick:U}),Z&&se.push({name:Object(I.h)(O.a.Fragment,null,Object(I.h)("i",{className:"fa fa-plus"})," ",Object(b.e)("Chart")),buttonStyle:"primary",onClick:()=>{window.location.assign("/chart/add")}}),Object(y.c)(y.a.VERSIONED_EXPORT)&&se.push({name:Object(I.h)(k.a,{id:"import-tooltip",title:Object(b.e)("Import charts"),placement:"bottomRight"},Object(I.h)($.a.Import,null)),buttonStyle:"link",onClick:Q}),Object(I.h)(O.a.Fragment,null,Object(I.h)(_.a,{name:Object(b.e)("Charts"),buttons:se}),V&&Object(I.h)(N.a,{onHide:J,onSave:q,show:!0,slice:V}),Object(I.h)(v.a,{title:Object(b.e)("Please confirm"),description:Object(b.e)("Are you sure you want to delete the selected charts?"),onConfirm:function(e){h.a.delete({endpoint:`/api/v1/chart/?q=${g.a.encode(i()(e).call(e,({id:e})=>e))}`}).then(({json:e={}})=>{R(),c(e.message)},Object(f.c)(e=>r(Object(b.e)("There was an issue deleting the selected charts: %s",e))))}},e=>{const t=[];return te&&t.push({key:"delete",name:Object(b.e)("Delete"),type:"danger",onSelect:e}),ae&&t.push({key:"export",name:Object(b.e)("Export"),type:"primary",onSelect:f.i}),Object(I.h)(S.b,{bulkActions:t,bulkSelectEnabled:m,cardSortSelectOptions:oe,className:"chart-list-view",columns:le,count:s,data:u,disableBulkSelect:U,fetchData:M,filters:ce,initialSort:re,loading:o,pageSize:25,renderCard:ie,defaultViewMode:Object(y.c)(y.a.LISTVIEWS_DEFAULT_CARD_VIEW)?"card":"table"})}),Object(I.h)(T.a,{resourceName:"chart",resourceLabel:Object(b.e)("chart"),passwordsNeededMessage:A,confirmOverwriteMessage:H,addDangerToast:r,addSuccessToast:c,onModelImport:()=>{Y(!1),R()},show:X,onHide:()=>{Y(!1)},passwordFields:G,setPasswordFields:K}))}))}}]);