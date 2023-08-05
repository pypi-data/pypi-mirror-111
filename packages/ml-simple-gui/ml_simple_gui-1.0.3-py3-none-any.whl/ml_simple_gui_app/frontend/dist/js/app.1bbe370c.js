(function(e){function t(t){for(var r,s,c=t[0],o=t[1],l=t[2],p=0,f=[];p<c.length;p++)s=c[p],Object.prototype.hasOwnProperty.call(a,s)&&a[s]&&f.push(a[s][0]),a[s]=0;for(r in o)Object.prototype.hasOwnProperty.call(o,r)&&(e[r]=o[r]);u&&u(t);while(f.length)f.shift()();return i.push.apply(i,l||[]),n()}function n(){for(var e,t=0;t<i.length;t++){for(var n=i[t],r=!0,c=1;c<n.length;c++){var o=n[c];0!==a[o]&&(r=!1)}r&&(i.splice(t--,1),e=s(s.s=n[0]))}return e}var r={},a={app:0},i=[];function s(t){if(r[t])return r[t].exports;var n=r[t]={i:t,l:!1,exports:{}};return e[t].call(n.exports,n,n.exports,s),n.l=!0,n.exports}s.m=e,s.c=r,s.d=function(e,t,n){s.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:n})},s.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},s.t=function(e,t){if(1&t&&(e=s(e)),8&t)return e;if(4&t&&"object"===typeof e&&e&&e.__esModule)return e;var n=Object.create(null);if(s.r(n),Object.defineProperty(n,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var r in e)s.d(n,r,function(t){return e[t]}.bind(null,r));return n},s.n=function(e){var t=e&&e.__esModule?function(){return e["default"]}:function(){return e};return s.d(t,"a",t),t},s.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},s.p="/";var c=window["webpackJsonp"]=window["webpackJsonp"]||[],o=c.push.bind(c);c.push=t,c=c.slice();for(var l=0;l<c.length;l++)t(c[l]);var u=o;i.push([0,"chunk-vendors"]),n()})({0:function(e,t,n){e.exports=n("56d7")},"479b":function(e,t,n){"use strict";n.r(t),n.d(t,"state",(function(){return u})),n.d(t,"mutations",(function(){return g})),n.d(t,"actions",(function(){return O})),n.d(t,"getters",(function(){return S}));var r,a=n("1da1"),i=n("ade3"),s=(n("96cf"),n("b0c0"),n("a9e3"),n("bc3a")),c=n.n(s),o="http://127.0.0.1:5000",l=n("2b0e"),u={trainTestDataFile:null,testPercent:25,learningRate:.01,learningEpochs:1e3,resultLoading:!1,result:{sensitivity:0,specificity:0,accuracy:0}},p="SET_TRAIN_TEST_FILE",f="TEST_PERCENT",d="LEARNING_RATE",m="LEARNING_EPOCHS",v="FETCH_RESULTS_START",b="FETCH_RESULTS_END",h="SET_RESULTS",g=(r={},Object(i["a"])(r,p,(function(e,t){e.trainTestDataFile=t})),Object(i["a"])(r,f,(function(e,t){e.testPercent=t})),Object(i["a"])(r,d,(function(e,t){e.learningRate=t})),Object(i["a"])(r,m,(function(e,t){e.learningEpochs=t})),Object(i["a"])(r,v,(function(e){e.resultLoading=!0})),Object(i["a"])(r,b,(function(e){e.resultLoading=!1})),Object(i["a"])(r,h,(function(e,t){l["a"].set(e,"result",t)})),r),O={uploadFile:function(e,t){return Object(a["a"])(regeneratorRuntime.mark((function n(){var r,a,i;return regeneratorRuntime.wrap((function(n){while(1)switch(n.prev=n.next){case 0:if(r=e.commit,n.prev=1,"undefined"!==typeof t.name){n.next=4;break}throw new Error("Empty file");case 4:return a=new FormData,a.append("file",t),n.next=8,c.a.post("".concat(o,"/upload_data/"),a,{headers:{"Content-Type":"multipart/form-data"}}).then((function(e){return e.data||{}})).catch((function(){console.log("FAILURE!!")}));case 8:if(i=n.sent,"success"!==i.status){n.next=14;break}return n.next=12,r(p,i.result);case 12:n.next=15;break;case 14:console.log(i.result.message||"error");case 15:n.next=20;break;case 17:n.prev=17,n.t0=n["catch"](1),console.log(n.t0.message);case 20:case"end":return n.stop()}}),n,null,[[1,17]])})))()},setTestPercent:function(e,t){var n=e.commit;n(f,Number(t))},setLearningRate:function(e,t){var n=e.commit;n(d,Number(t))},setLearningEpochs:function(e,t){var n=e.commit;n(m,Number(t))},fetchResults:function(e,t){return Object(a["a"])(regeneratorRuntime.mark((function n(){var r,a;return regeneratorRuntime.wrap((function(n){while(1)switch(n.prev=n.next){case 0:return r=e.commit,n.prev=1,n.next=4,r(v);case 4:return n.next=6,c.a.post("".concat(o,"/fit_predict/"),t).then((function(e){return e.data||{}})).catch((function(){console.log("FAILURE!!")}));case 6:if(a=n.sent,"success"!==a.status){n.next=14;break}return n.next=10,r(h,a.result);case 10:return n.next=12,r(b);case 12:n.next=17;break;case 14:return n.next=16,r(b);case 16:console.log(a.result.message||"error");case 17:n.next=24;break;case 19:return n.prev=19,n.t0=n["catch"](1),n.next=23,r(b);case 23:console.log(n.t0.message);case 24:case"end":return n.stop()}}),n,null,[[1,19]])})))()}},S={trainTestDataFile:function(e){return e.trainTestDataFile},isTrainTestDataFileValid:function(e){return!!e.trainTestDataFile},testPercent:function(e){return e.testPercent},learningRate:function(e){return e.learningRate},learningEpochs:function(e){return e.learningEpochs},result:function(e){return e.result},resultLoading:function(e){return e.resultLoading}}},"56d7":function(e,t,n){"use strict";n.r(t);n("e260"),n("e6cf"),n("cca6"),n("a79d");var r=n("2b0e"),a=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("v-app",[n("v-app-bar",{attrs:{app:""}},[n("v-toolbar-title",[e._v(e._s(e.applicationTitle))])],1),n("v-main",[n("router-view")],1)],1)},i=[],s={name:"App",data:function(){return{applicationTitle:"Simple Machine Learning GUI"}}},c=s,o=n("2877"),l=n("6544"),u=n.n(l),p=n("7496"),f=n("40dc"),d=n("f6c4"),m=n("2a7f"),v=Object(o["a"])(c,a,i,!1,null,null,null),b=v.exports;u()(v,{VApp:p["a"],VAppBar:f["a"],VMain:d["a"],VToolbarTitle:m["a"]});var h=n("f309");r["a"].use(h["a"]);var g=new h["a"]({}),O=n("8c4f"),S=n("2106"),j=n.n(S),_=n("bc3a"),x=n.n(_),T=n("ade3"),E=n("5530"),R=n("3835"),y=(n("d81d"),n("d3b7"),n("ddb0"),n("ac1f"),n("5319"),n("2f62"));r["a"].use(y["a"]);var P=n("6c17"),w=P.keys().map((function(e){return[e.replace(/(^.\/)|(\.js$)/g,""),P(e)]})).reduce((function(e,t){var n=Object(R["a"])(t,2),r=n[0],a=n[1];return void 0===a.namespaced&&(a.namespaced=!0),Object(E["a"])(Object(E["a"])({},e),{},Object(T["a"])({},r,a))}),{}),F=new y["a"].Store({modules:w}),V=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("v-stepper",{model:{value:e.mainStepperProgress,callback:function(t){e.mainStepperProgress=t},expression:"mainStepperProgress"}},[n("v-stepper-header",[e._l(e.steps,(function(t,r){return[n("v-stepper-step",{key:t.id+"-step",attrs:{complete:e.mainStepperProgress>r,step:r}},[e._v(" "+e._s(t.name)+" "),n("v-divider")],1),n("v-divider",{key:t.id+"-divider"})]}))],2),n("v-stepper-items",e._l(e.steps,(function(t,r){return n("v-stepper-content",{key:t.id,attrs:{step:r}},[n("v-card",{staticClass:"mb-12"},[n(t.component,{tag:"component",attrs:{"is-opened":e.mainStepperProgress===Number(r)}})],1),n("v-row",{attrs:{justify:"space-between"}},[n("v-col",{staticClass:"my-1"},[r>e.minStepNumber?n("v-btn",{on:{click:e.previousStep}},[e._v(" Назад ")]):e._e()],1),n("v-col",{staticClass:"text-end my-1"},[r<e.maxStepNumber?n("v-btn",{attrs:{color:"primary",disabled:e.isNextButtonDisabled},on:{click:e.nextStep}},[e._v(" Вперед ")]):e._e()],1)],1)],1)})),1)],1)},L=[],k=(n("b64b"),n("2ef0")),D=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",[n("v-file-input",{ref:"dataFile",attrs:{rules:e.rules,accept:".csv",placeholder:"Файл с обучающей выборкой",label:"Файл с обучающей выборкой"},on:{change:e.onFileChange}})],1)},C=[],N=n("1da1"),I=(n("96cf"),{name:"UploadFilesStep",props:["isOpened"],data:function(){return{rules:[function(e){return!e||e.size<2e8||"Файл должен быть меньше 200 МБ!"}]}},computed:Object(E["a"])({},Object(y["c"])({trainTestDataFile:"main/trainTestDataFile"})),methods:Object(E["a"])(Object(E["a"])({},Object(y["b"])({uploadFile:"main/uploadFile"})),{},{onFileChange:function(){var e=Object(N["a"])(regeneratorRuntime.mark((function e(t){return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return e.next=2,this.uploadFile(t||{});case 2:case"end":return e.stop()}}),e,this)})));function t(t){return e.apply(this,arguments)}return t}()})}),A=I,U=n("23a7"),M=Object(o["a"])(A,D,C,!1,null,"d0e6fbb6",null),$=M.exports;u()(M,{VFileInput:U["a"]});var B=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("v-row",[n("v-col",[n("v-text-field",{attrs:{label:"Процент тестовой выборки",required:""},model:{value:e.testPercent,callback:function(t){e.testPercent=t},expression:"testPercent"}})],1),n("v-col",[n("v-text-field",{attrs:{label:"Скорость обучения",required:""},model:{value:e.learningRate,callback:function(t){e.learningRate=t},expression:"learningRate"}})],1),n("v-col",[n("v-text-field",{attrs:{label:"Количество эпох",required:""},model:{value:e.learningEpochs,callback:function(t){e.learningEpochs=t},expression:"learningEpochs"}})],1)],1)},H=[],q={name:"SelectParamsStep",props:["isOpened"],data:function(){return{testPercent:25,learningRate:.01,learningEpochs:1e3}},methods:Object(E["a"])({},Object(y["b"])({setTestPercent:"main/setTestPercent",setLearningRate:"main/setLearningRate",setLearningEpochs:"main/setLearningEpochs"})),watch:{testPercent:function(e){this.setTestPercent(e)},learningRate:function(e){this.setLearningRate(e)},learningEpochs:function(e){this.setLearningEpochs(e)}}},G=q,J=n("62ad"),z=n("0fd9"),K=n("8654"),Q=Object(o["a"])(G,B,H,!1,null,"0a76dfec",null),W=Q.exports;u()(Q,{VCol:J["a"],VRow:z["a"],VTextField:K["a"]});var X=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("v-row",[n("v-col",{attrs:{cols:"6"}},[e.resultLoading?n("v-skeleton-loader",{attrs:{type:"list-item-three-line, list-item-three-line, image, actions"}}):[n("v-list",{staticClass:"transparent"},[n("v-list-item",[n("v-list-item-title",[e._v("Точность")]),n("v-list-item-subtitle",{staticClass:"text-right"},[e._v(" "+e._s(e.result.accuracy)+"% ")])],1),n("v-list-item",[n("v-list-item-title",[e._v("Чувствительность")]),n("v-list-item-subtitle",{staticClass:"text-right"},[e._v(" "+e._s(e.result.sensitivity)+"% ")])],1),n("v-list-item",[n("v-list-item-title",[e._v("Специфичность")]),n("v-list-item-subtitle",{staticClass:"text-right"},[e._v(" "+e._s(e.result.specificity)+"% ")])],1)],1)]],2)],1)},Y=[],Z={name:"ResultStep",props:["isOpened"],methods:Object(E["a"])({},Object(y["b"])({fetchResults:"main/fetchResults"})),computed:Object(E["a"])({},Object(y["c"])({trainTestDataFile:"main/trainTestDataFile",testPercent:"main/testPercent",learningRate:"main/learningRate",learningEpochs:"main/learningEpochs",resultLoading:"main/resultLoading",result:"main/result"})),watch:{isOpened:function(e){e&&this.fetchResults({file:this.trainTestDataFile,testPercent:this.testPercent,learningRate:this.learningRate,learningEpochs:this.learningEpochs})}}},ee=Z,te=n("8860"),ne=n("da13"),re=n("5d23"),ae=n("3129"),ie=Object(o["a"])(ee,X,Y,!1,null,"73715f51",null),se=ie.exports;u()(ie,{VCol:J["a"],VList:te["a"],VListItem:ne["a"],VListItemSubtitle:re["a"],VListItemTitle:re["b"],VRow:z["a"],VSkeletonLoader:ae["a"]});var ce={name:"MainSteps",components:{UploadFilesStep:$,SelectParamsStep:W,ResultStep:se},data:function(){return{mainStepperProgress:1,steps:{1:{id:"loadFile",name:"Загрузка данных",component:"upload-files-step"},2:{id:"selectParams",name:"Настройка параметров модели",component:"select-params-step"},3:{id:"results",name:"Результаты",component:"result-step"}}}},computed:Object(E["a"])(Object(E["a"])({},Object(y["c"])({isTrainTestDataFileValid:"main/isTrainTestDataFileValid"})),{},{maxStepNumber:function(){return Object(k["last"])(Object.keys(this.steps))},minStepNumber:function(){return Object(k["first"])(Object.keys(this.steps))},isNextButtonDisabled:function(){return!this["".concat(this.steps[this.mainStepperProgress].id,"Valid")]},selectParamsValid:function(){return!0},loadFileValid:function(){return this.isTrainTestDataFileValid},resultsValid:function(){return!0}}),methods:{nextStep:function(){this.mainStepperProgress++},previousStep:function(){this.mainStepperProgress--}}},oe=ce,le=n("8336"),ue=n("b0af"),pe=n("ce7e"),fe=n("7e85"),de=n("e516"),me=n("9c54"),ve=n("56a4"),be=Object(o["a"])(oe,V,L,!1,null,"4a2a8838",null),he=be.exports;u()(be,{VBtn:le["a"],VCard:ue["a"],VCol:J["a"],VDivider:pe["a"],VRow:z["a"],VStepper:fe["a"],VStepperContent:de["a"],VStepperHeader:me["a"],VStepperItems:me["b"],VStepperStep:ve["a"]});var ge=[{path:"/",component:he}],Oe=new O["a"]({mode:"history",routes:ge});r["a"].use(O["a"]),r["a"].use(j.a,x.a),r["a"].config.productionTip=!1,new r["a"]({vuetify:g,store:F,router:Oe,render:function(e){return e(b)}}).$mount("#app")},"6c17":function(e,t,n){var r={"./main.js":"479b"};function a(e){var t=i(e);return n(t)}function i(e){if(!n.o(r,e)){var t=new Error("Cannot find module '"+e+"'");throw t.code="MODULE_NOT_FOUND",t}return r[e]}a.keys=function(){return Object.keys(r)},a.resolve=i,e.exports=a,a.id="6c17"}});
//# sourceMappingURL=app.1bbe370c.js.map