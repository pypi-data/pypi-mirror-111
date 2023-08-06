(window.webpackJsonp=window.webpackJsonp||[]).push([[26],{4532:function(e,t,a){"use strict";a(40);var r=a(11),o=a.n(r),l=a(0),s=a.n(l),c=a(47),n=a(14),i=a(48),d=a(101),b=a(445),u=a(1);Object(c.j)(i.a)`
  margin: auto ${({theme:e})=>2*e.gridUnit}px auto 0;
`;const h=c.j.div`
  display: block;
  color: ${({theme:e})=>e.colors.grayscale.base};
  font-size: ${({theme:e})=>e.typography.sizes.s-1}px;
`,O=c.j.div`
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
`;t.a=({resourceName:e,resourceLabel:t,passwordsNeededMessage:a,confirmOverwriteMessage:r,addDangerToast:c,addSuccessToast:i,onModelImport:j,show:p,onHide:m,passwordFields:g=[],setPasswordFields:f=(()=>{})})=>{const[y,w]=Object(l.useState)(!0),[S,v]=Object(l.useState)(null),[x,_]=Object(l.useState)({}),[C,E]=Object(l.useState)(!1),[I,T]=Object(l.useState)(!1),D=Object(l.useRef)(null),N=()=>{v(null),f([]),_({}),E(!1),T(!1),D&&D.current&&(D.current.value="")},{state:{alreadyExists:$,passwordsNeeded:k},importResource:F}=Object(b.e)(e,t,e=>{N(),c(e)});Object(l.useEffect)(()=>{f(k)},[k,f]),Object(l.useEffect)(()=>{E($.length>0)},[$,E]);const H=e=>{var t,a;const r=null!=(t=null==(a=e.currentTarget)?void 0:a.value)?t:"";T(r.toUpperCase()===Object(n.e)("OVERWRITE"))};return y&&p&&w(!1),Object(u.h)(d.b,{name:"model",className:"import-model-modal",disablePrimaryButton:null===S||C&&!I,onHandledPrimaryAction:()=>{null!==S&&F(S,x,I).then(e=>{e&&(i(Object(n.e)("The import was successful")),N(),j())})},onHide:()=>{w(!0),m(),N()},primaryButtonName:C?Object(n.e)("Overwrite"):Object(n.e)("Import"),primaryButtonType:C?"danger":"primary",width:"750px",show:p,title:Object(u.h)("h4",null,Object(n.e)("Import %s",t))},Object(u.h)(O,null,Object(u.h)("div",{className:"control-label"},Object(u.h)("label",{htmlFor:"modelFile"},Object(n.e)("File"),Object(u.h)("span",{className:"required"},"*"))),Object(u.h)("input",{ref:D,name:"modelFile",id:"modelFile",type:"file",accept:".yaml,.json,.yml,.zip",onChange:e=>{const{files:t}=e.target;v(t&&t[0]||null)}})),0===g.length?null:Object(u.h)(s.a.Fragment,null,Object(u.h)("h5",null,"Database passwords"),Object(u.h)(h,null,a),o()(g).call(g,e=>Object(u.h)(O,{key:`password-for-${e}`},Object(u.h)("div",{className:"control-label"},e,Object(u.h)("span",{className:"required"},"*")),Object(u.h)("input",{name:`password-${e}`,autoComplete:`password-${e}`,type:"password",value:x[e],onChange:t=>_({...x,[e]:t.target.value})})))),C?Object(u.h)(s.a.Fragment,null,Object(u.h)(O,null,Object(u.h)("div",{className:"confirm-overwrite"},r),Object(u.h)("div",{className:"control-label"},Object(n.e)('Type "%s" to confirm',Object(n.e)("OVERWRITE"))),Object(u.h)("input",{id:"overwrite",type:"text",onChange:H}))):null)}},4930:function(e,t,a){"use strict";a.r(t);a(40);var r,o=a(11),l=a.n(o),s=a(14),c=a(47),n=a(91),i=a(0),d=a.n(i),b=a(96),u=a.n(b),h=a(42),O=a(125),j=a(445),p=a(1367),m=a(1e3),g=a(4526),f=a(710),y=a(129),w=a(1372),S=a(174),v=a(826),x=a(1341),_=a(50),C=a(4532),E=a(2092);!function(e){e.PUBLISHED="published",e.DRAFT="draft"}(r||(r={}));var I=a(1);const T=Object(s.e)('The passwords for the databases below are needed in order to import them together with the dashboards. Please note that the "Secure Extra" and "Certificate" sections of the database configuration are not present in export files, and should be added manually after the import if they are needed.'),D=Object(s.e)("You are importing one or more dashboards that already exist. Overwriting might cause you to lose some of your work. Are you sure you want to overwrite?"),N=c.j.div`
  color: ${({theme:e})=>e.colors.grayscale.base};
`;t.default=Object(y.a)((function(e){const{addDangerToast:t,addSuccessToast:a}=e,{state:{loading:o,resourceCount:c,resourceCollection:b,bulkSelectEnabled:y},setResourceCollection:$,hasPerm:k,fetchData:F,toggleBulkSelect:H,refreshData:A}=Object(j.f)("dashboard",Object(s.e)("dashboard"),t),z=Object(i.useMemo)(()=>l()(b).call(b,e=>e.id),[b]),[M,U]=Object(j.d)("dashboard",z,t),[P,B]=Object(i.useState)(null),[R,L]=Object(i.useState)(!1),[V,q]=Object(i.useState)([]),W=()=>{L(!0)},J=k("can_write"),Y=k("can_write"),X=k("can_write"),G=k("can_read"),K=[{id:"changed_on_delta_humanized",desc:!0}];function Q(e){B(e)}function Z(e){return n.a.get({endpoint:`/api/v1/dashboard/${e.id}`}).then(({json:e={}})=>{$(l()(b).call(b,t=>t.id===e.id?e.result:t))},Object(O.c)(e=>t(Object(s.e)("An error occurred while fetching dashboards: %s",e))))}const ee=Object(i.useMemo)(()=>[{Cell:({row:{original:{id:e}}})=>Object(I.h)(v.a,{itemId:e,saveFaveStar:M,isStarred:U[e]}),Header:"",id:"id",disableSortBy:!0,size:"xs"},{Cell:({row:{original:{url:e,dashboard_title:t}}})=>Object(I.h)("a",{href:e},t),Header:Object(s.e)("Title"),accessor:"dashboard_title"},{Cell:({row:{original:{changed_by_name:e,changed_by_url:t}}})=>Object(I.h)("a",{href:t},e),Header:Object(s.e)("Modified by"),accessor:"changed_by.first_name",size:"xl"},{Cell:({row:{original:{status:e}}})=>e===r.PUBLISHED?Object(s.e)("Published"):Object(s.e)("Draft"),Header:Object(s.e)("Status"),accessor:"published",size:"xl"},{Cell:({row:{original:{changed_on_delta_humanized:e}}})=>Object(I.h)("span",{className:"no-wrap"},e),Header:Object(s.e)("Modified"),accessor:"changed_on_delta_humanized",size:"xl"},{Cell:({row:{original:{created_by:e}}})=>e?`${e.first_name} ${e.last_name}`:"",Header:Object(s.e)("Created by"),accessor:"created_by",disableSortBy:!0,size:"xl"},{Cell:({row:{original:{owners:e=[]}}})=>Object(I.h)(w.a,{users:e}),Header:Object(s.e)("Owners"),accessor:"owners",disableSortBy:!0,size:"xl"},{Cell:({row:{original:e}})=>Object(I.h)(N,{className:"actions"},X&&Object(I.h)(p.a,{title:Object(s.e)("Please confirm"),description:Object(I.h)(d.a.Fragment,null,Object(s.e)("Are you sure you want to delete")," ",Object(I.h)("b",null,e.dashboard_title),"?"),onConfirm:()=>Object(O.m)(e,A,a,t)},e=>Object(I.h)(_.a,{id:"delete-action-tooltip",title:Object(s.e)("Delete"),placement:"bottom"},Object(I.h)("span",{role:"button",tabIndex:0,className:"action-button",onClick:e},Object(I.h)(S.a.Trash,null)))),G&&Object(I.h)(_.a,{id:"export-action-tooltip",title:Object(s.e)("Export"),placement:"bottom"},Object(I.h)("span",{role:"button",tabIndex:0,className:"action-button",onClick:()=>Object(O.j)([e])},Object(I.h)(S.a.Share,null))),Y&&Object(I.h)(_.a,{id:"edit-action-tooltip",title:Object(s.e)("Edit"),placement:"bottom"},Object(I.h)("span",{role:"button",tabIndex:0,className:"action-button",onClick:()=>Q(e)},Object(I.h)(S.a.EditAlt,null)))),Header:Object(s.e)("Actions"),id:"actions",hidden:!Y&&!X&&!G,disableSortBy:!0}],[Y,X,G,U]),te=[{Header:Object(s.e)("Owner"),id:"owners",input:"select",operator:g.a.relationManyMany,unfilteredLabel:Object(s.e)("All"),fetchSelects:Object(O.e)("dashboard","owners",Object(O.c)(e=>t(Object(s.e)("An error occurred while fetching dashboard owner values: %s",e))),e.user.userId),paginate:!0},{Header:Object(s.e)("Created by"),id:"created_by",input:"select",operator:g.a.relationOneMany,unfilteredLabel:Object(s.e)("All"),fetchSelects:Object(O.e)("dashboard","created_by",Object(O.c)(e=>t(Object(s.e)("An error occurred while fetching dashboard created by values: %s",e))),e.user.userId),paginate:!0},{Header:Object(s.e)("Status"),id:"published",input:"select",operator:g.a.equals,unfilteredLabel:Object(s.e)("Any"),selects:[{label:Object(s.e)("Published"),value:!0},{label:Object(s.e)("Draft"),value:!1}]},{Header:Object(s.e)("Favorite"),id:"id",urlDisplay:"favorite",input:"select",operator:g.a.dashboardIsFav,unfilteredLabel:Object(s.e)("Any"),selects:[{label:Object(s.e)("Yes"),value:!0},{label:Object(s.e)("No"),value:!1}]},{Header:Object(s.e)("Search"),id:"dashboard_title",input:"search",operator:g.a.titleOrSlug}],ae=[{desc:!1,id:"dashboard_title",label:Object(s.e)("Alphabetical"),value:"alphabetical"},{desc:!0,id:"changed_on_delta_humanized",label:Object(s.e)("Recently modified"),value:"recently_modified"},{desc:!1,id:"changed_on_delta_humanized",label:Object(s.e)("Least recently modified"),value:"least_recently_modified"}];function re(r){const{userId:l}=e.user,s=Object(f.a)(l.toString(),null);return Object(I.h)(E.a,{dashboard:r,hasPerm:k,bulkSelectEnabled:y,refreshData:A,showThumbnails:s?s.thumbnails:Object(h.c)(h.a.THUMBNAILS),loading:o,addDangerToast:t,addSuccessToast:a,openDashboardEditModal:Q,saveFavoriteStatus:M,favoriteStatus:U[r.id]})}const oe=[];return(X||G)&&oe.push({name:Object(s.e)("Bulk select"),buttonStyle:"secondary","data-test":"bulk-select",onClick:H}),J&&oe.push({name:Object(I.h)(d.a.Fragment,null,Object(I.h)("i",{className:"fa fa-plus"})," ",Object(s.e)("Dashboard")),buttonStyle:"primary",onClick:()=>{window.location.assign("/dashboard/new")}}),Object(h.c)(h.a.VERSIONED_EXPORT)&&oe.push({name:Object(I.h)(_.a,{id:"import-tooltip",title:Object(s.e)("Import dashboards"),placement:"bottomRight"},Object(I.h)(S.a.Import,null)),buttonStyle:"link",onClick:W}),Object(I.h)(d.a.Fragment,null,Object(I.h)(m.a,{name:Object(s.e)("Dashboards"),buttons:oe}),Object(I.h)(p.a,{title:Object(s.e)("Please confirm"),description:Object(s.e)("Are you sure you want to delete the selected dashboards?"),onConfirm:function(e){return n.a.delete({endpoint:`/api/v1/dashboard/?q=${u.a.encode(l()(e).call(e,({id:e})=>e))}`}).then(({json:e={}})=>{A(),a(e.message)},Object(O.c)(e=>t(Object(s.e)("There was an issue deleting the selected dashboards: ",e))))}},e=>{const t=[];return X&&t.push({key:"delete",name:Object(s.e)("Delete"),type:"danger",onSelect:e}),G&&t.push({key:"export",name:Object(s.e)("Export"),type:"primary",onSelect:O.j}),Object(I.h)(d.a.Fragment,null,P&&Object(I.h)(x.a,{dashboardId:P.id,show:!0,onHide:()=>B(null),onSubmit:Z}),Object(I.h)(g.b,{bulkActions:t,bulkSelectEnabled:y,cardSortSelectOptions:ae,className:"dashboard-list-view",columns:ee,count:c,data:b,disableBulkSelect:H,fetchData:F,filters:te,initialSort:K,loading:o,pageSize:25,renderCard:re,defaultViewMode:Object(h.c)(h.a.LISTVIEWS_DEFAULT_CARD_VIEW)?"card":"table"}))}),Object(I.h)(C.a,{resourceName:"dashboard",resourceLabel:Object(s.e)("dashboard"),passwordsNeededMessage:T,confirmOverwriteMessage:D,addDangerToast:t,addSuccessToast:a,onModelImport:()=>{L(!1),A()},show:R,onHide:()=>{L(!1)},passwordFields:V,setPasswordFields:q}))}))}}]);