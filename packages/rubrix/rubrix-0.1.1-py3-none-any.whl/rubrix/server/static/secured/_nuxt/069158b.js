(window.webpackJsonp=window.webpackJsonp||[]).push([[3,8,9,24,35,43,44],{448:function(t,e,n){"use strict";var o=n(3),r=n(70),l=n(451),c=n(368),d=n(6),f=1..toFixed,h=Math.floor,m=function(t,e,n){return 0===e?n:e%2==1?m(t,e-1,n*t):m(t*t,e/2,n)},v=function(data,t,e){for(var n=-1,o=e;++n<6;)o+=t*data[n],data[n]=o%1e7,o=h(o/1e7)},x=function(data,t){for(var e=6,n=0;--e>=0;)n+=data[e],data[e]=h(n/t),n=n%t*1e7},_=function(data){for(var t=6,s="";--t>=0;)if(""!==s||0===t||0!==data[t]){var e=String(data[t]);s=""===s?e:s+c.call("0",7-e.length)+e}return s};o({target:"Number",proto:!0,forced:f&&("0.000"!==8e-5.toFixed(3)||"1"!==.9.toFixed(0)||"1.25"!==1.255.toFixed(2)||"1000000000000000128"!==(0xde0b6b3a7640080).toFixed(0))||!d((function(){f.call({})}))},{toFixed:function(t){var e,n,o,d,f=l(this),h=r(t),data=[0,0,0,0,0,0],w="",y="0";if(h<0||h>20)throw RangeError("Incorrect fraction digits");if(f!=f)return"NaN";if(f<=-1e21||f>=1e21)return String(f);if(f<0&&(w="-",f=-f),f>1e-21)if(n=(e=function(t){for(var e=0,n=t;n>=4096;)e+=12,n/=4096;for(;n>=2;)e+=1,n/=2;return e}(f*m(2,69,1))-69)<0?f*m(2,-e,1):f/m(2,e,1),n*=4503599627370496,(e=52-e)>0){for(v(data,0,n),o=h;o>=7;)v(data,1e7,0),o-=7;for(v(data,m(10,o,1),0),o=e-1;o>=23;)x(data,1<<23),o-=23;x(data,1<<o),v(data,1,1),x(data,2),y=_(data)}else v(data,0,n),v(data,1<<-e,0),y=_(data)+c.call("0",h);return y=h>0?w+((d=y.length)<=h?"0."+c.call("0",h-d)+y:y.slice(0,d-h)+"."+y.slice(d-h)):w+y}})},451:function(t,e,n){var o=n(65);t.exports=function(t){if("number"!=typeof t&&"Number"!=o(t))throw TypeError("Incorrect invocation");return+t}},462:function(t,e,n){n(154).register({ignore:{width:17,height:18,viewBox:"0 0 17 18",data:'<defs><path pid="0" id="svgicon_ignore_a" d="M0 0h16.914v17.826H0z"/></defs><g _fill="none" fill-rule="evenodd"><path pid="1" d="M14.81 3.525l2.018-2.161L15.365 0l-2.076 2.224A7.937 7.937 0 008.914.913c-4.411 0-8 3.589-8 8a7.94 7.94 0 001.632 4.822L0 16.462l1.463 1.364 2.479-2.657a7.953 7.953 0 004.972 1.744c4.411 0 8-3.59 8-8a7.961 7.961 0 00-2.104-5.388M2.914 8.913c0-3.31 2.691-6 6-6 1.087 0 2.104.295 2.984.802L3.931 12.25a5.963 5.963 0 01-1.017-3.338m6 6A5.962 5.962 0 015.313 13.7l8.13-8.711a5.966 5.966 0 011.471 3.923c0 3.309-2.691 6-6 6" _fill="#000"/></g>'}})},464:function(t,e,n){"use strict";n.r(e);n(155),n(448);var o={props:{value:{type:Number,default:void 0},type:{type:String,default:void 0},decimals:{type:Number,default:2},percent:{type:Boolean,default:!1}},data:function(){return{}},computed:{numericValue:function(){if(!0===this.percent){var t=100*this.value;return t%1==0?t:t.toFixed(this.decimals)}return this.value.toFixed(this.decimals)}}},r=n(43),component=Object(r.a)(o,(function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("span",[t._v("\n  "+t._s(t.numericValue)),n("span",[t._v(t._s(t.type))]),t._v(" "),t._t("default"),t._v(" "),t.percent?n("span",[t._v("%")]):t._e()],2)}),[],!1,null,null,null);e.default=component.exports},487:function(t,e,n){var content=n(540);content.__esModule&&(content=content.default),"string"==typeof content&&(content=[[t.i,content,""]]),content.locals&&(t.exports=content.locals);(0,n(100).default)("4ed68fcc",content,!0,{sourceMap:!1})},488:function(t,e,n){var content=n(544);content.__esModule&&(content=content.default),"string"==typeof content&&(content=[[t.i,content,""]]),content.locals&&(t.exports=content.locals);(0,n(100).default)("a9038ea2",content,!0,{sourceMap:!1})},489:function(t,e,n){var content=n(549);content.__esModule&&(content=content.default),"string"==typeof content&&(content=[[t.i,content,""]]),content.locals&&(t.exports=content.locals);(0,n(100).default)("975687ca",content,!0,{sourceMap:!1})},504:function(t,e,n){"use strict";n.r(e);var o=n(13),r=(n(370),n(36),n(32),n(28),n(31),n(44),n(25),n(45),n(62));function l(object,t){var e=Object.keys(object);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(object);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(object,t).enumerable}))),e.push.apply(e,n)}return e}function c(t){for(var i=1;i<arguments.length;i++){var source=null!=arguments[i]?arguments[i]:{};i%2?l(Object(source),!0).forEach((function(e){Object(o.a)(t,e,source[e])})):Object.getOwnPropertyDescriptors?Object.defineProperties(t,Object.getOwnPropertyDescriptors(source)):l(Object(source)).forEach((function(e){Object.defineProperty(t,e,Object.getOwnPropertyDescriptor(source,e))}))}return t}var d={props:{annotationMode:{type:Boolean,default:!1},record:{type:r.a,required:!0}},data:function(){return{statusActions:[{name:"Discard",key:"Discarded",class:"discard"}]}},computed:{hasMetadata:function(){var t=this.record.metadata;return t&&Object.values(t).length},recordStatus:function(){return this.record.status},allowedStatusActions:function(){var t=this;return this.annotationMode?this.statusActions.map((function(e){return c(c({},e),{},{isActive:t.recordStatus===e.key})})):[]}},methods:{onChangeRecordStatus:function(t){this.record.status!==t?this.$emit("onChangeRecordStatus",t):this.$emit("onChangeRecordStatus","Edited")}}},f=(n(539),n(43)),component=Object(f.a)(d,(function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{staticClass:"record__extra-actions"},[t.hasMetadata?n("div",{on:{click:function(e){return t.$emit("onShowMetadata")}}},[n("span",[t._v("View metadata")])]):t._e(),t._v(" "),t._l(t.allowedStatusActions,(function(e){return n("div",{key:e.key,on:{click:function(n){return t.onChangeRecordStatus(e.key)}}},[n("span",[t._v(t._s(e.name))])])}))],2)}),[],!1,null,"3349dbc7",null);e.default=component.exports},539:function(t,e,n){"use strict";n(487)},540:function(t,e,n){var o=n(99)(!1);o.push([t.i,'.record__extra-actions[data-v-3349dbc7]{line-height:1;text-align:left;color:#4c4ea3;margin-top:1em;margin-bottom:1em;font-size:13px;font-size:.8125rem}.record__extra-actions .annotate[data-v-3349dbc7]{color:#60a018}.record__extra-actions .discard[data-v-3349dbc7]{color:#ff1e5e}.record__extra-actions>div[data-v-3349dbc7]{margin-top:0}.record__extra-actions>*[data-v-3349dbc7]+:before{content:"";margin:auto 1em;height:1em;width:1px;background:#686a6d;vertical-align:middle;display:inline-block}.record__extra-actions>*[data-v-3349dbc7]{display:inline-block;cursor:pointer}',""]),t.exports=o},541:function(t,e,n){var content=n(587);content.__esModule&&(content=content.default),"string"==typeof content&&(content=[[t.i,content,""]]),content.locals&&(t.exports=content.locals);(0,n(100).default)("85175b0e",content,!0,{sourceMap:!1})},542:function(t,e,n){var content=n(589);content.__esModule&&(content=content.default),"string"==typeof content&&(content=[[t.i,content,""]]),content.locals&&(t.exports=content.locals);(0,n(100).default)("568a272c",content,!0,{sourceMap:!1})},543:function(t,e,n){"use strict";n(488)},544:function(t,e,n){var o=n(99)(!1);o.push([t.i,".re-annotation-button[data-v-ce2c4b1a]{width:auto;margin:16px 8px 16px 0;display:inline-flex;position:relative}.re-annotation-button .annotation-button-container[data-v-ce2c4b1a]{display:none}.re-annotation-button.label-button[data-v-ce2c4b1a]{margin:auto auto 20px;color:#4a4a4a;padding:0;transition:all .3s ease;max-width:238px;width:100%;border-radius:7px}.re-annotation-button.label-button .button[data-v-ce2c4b1a]{outline:none;cursor:pointer;border-radius:5px;background:#fff;border:1px solid #e9eaed;height:40px;line-height:40px;padding-left:.5em;padding-right:.5em;width:100%;display:flex;font-weight:600;overflow:hidden;color:#4a4a4a}.re-annotation-button.label-button.active[data-v-ce2c4b1a]{transition:all .02s ease-in-out;box-shadow:none;-webkit-animation:pulse-data-v-ce2c4b1a .4s;animation:pulse-data-v-ce2c4b1a .4s;transform:scaleX(1);-webkit-font-smoothing:antialiased;transform:translate3d(1,1,1)}.re-annotation-button.label-button.active .button[data-v-ce2c4b1a]{background:#4c4ea3;border:1px solid #4c4ea3}.re-annotation-button.label-button.active[data-v-ce2c4b1a]:after{display:none!important}@-webkit-keyframes pulse-data-v-ce2c4b1a{0%{transform:scaleX(1)}70%{transform:scale3d(1.04,1.04,1.04)}to{transform:scaleX(1)}}@keyframes pulse-data-v-ce2c4b1a{0%{transform:scaleX(1)}70%{transform:scale3d(1.04,1.04,1.04)}to{transform:scaleX(1)}}@-webkit-keyframes pulse-font-data-v-ce2c4b1a{0%{transform:scaleX(1)}70%{transform:scale3d(1.06,1.06,1.06)}to{transform:scaleX(1)}}@keyframes pulse-font-data-v-ce2c4b1a{0%{transform:scaleX(1)}70%{transform:scale3d(1.06,1.06,1.06)}to{transform:scaleX(1)}}.re-annotation-button.label-button.active .annotation-button-data__confidence[data-v-ce2c4b1a],.re-annotation-button.label-button.active .annotation-button-data__text[data-v-ce2c4b1a]{color:#fff;-webkit-animation:pulse-font-data-v-ce2c4b1a .5s;animation:pulse-font-data-v-ce2c4b1a .5s}.re-annotation-button.label-button .annotation-button-data[data-v-ce2c4b1a]{overflow:hidden;transition:transform .3s ease}.re-annotation-button.label-button .annotation-button-data__text[data-v-ce2c4b1a]{max-width:calc(100% - 10px);overflow:hidden;text-overflow:ellipsis;display:inline-block;white-space:nowrap;vertical-align:top}.re-annotation-button.label-button .annotation-button-data__info[data-v-ce2c4b1a]{margin-right:0;margin-left:auto;transform:translateY(0);transition:all .3s ease}.re-annotation-button.label-button .annotation-button-data__confidence[data-v-ce2c4b1a]{width:40px;font-size:12px;font-size:.75rem;display:inline-block;text-align:center;line-height:1.5em;border-radius:2px}.re-annotation-button.label-button[data-v-ce2c4b1a]:not(.active):hover{box-shadow:0 3px 8px 3px hsla(0,0%,87.1%,.4)!important;border-color:#f2f3f7}.re-annotation-button.disabled[data-v-ce2c4b1a]{opacity:.5}.re-annotation-button[data-v-ce2c4b1a]:not(.disabled),.re-annotation-button:not(.disabled) .annotation-button[data-v-ce2c4b1a]{cursor:pointer}.re-annotation-button .annotation-button[data-v-ce2c4b1a]{height:20px;padding-left:8px;line-height:20px}",""]),t.exports=o},545:function(t,e,n){var content=n(591);content.__esModule&&(content=content.default),"string"==typeof content&&(content=[[t.i,content,""]]),content.locals&&(t.exports=content.locals);(0,n(100).default)("57626434",content,!0,{sourceMap:!1})},546:function(t,e,n){n(154).register({"predicted-ok":{width:15,height:18,viewBox:"0 0 15 18",data:'<path pid="0" d="M13.675 0C14.407 0 15 .62 15 1.383V18h-1.032a.438.438 0 01-.368-.254l-.61-1.456c-.352-.84-1.346-1.52-2.227-1.52H1.322C.592 14.77 0 14.152 0 13.385V1.383C0 .619.593 0 1.325 0h12.35zm-2.908 4.197a.655.655 0 00-.99.06L6.596 8.186 5.2 6.623a.655.655 0 00-.99-.007.832.832 0 00-.007 1.094l1.92 2.148a.67.67 0 00.498.23h.018a.673.673 0 00.504-.258l3.68-4.541a.83.83 0 00-.055-1.092z" fill-rule="evenodd"/>'}})},547:function(t,e,n){n(154).register({"predicted-ko":{width:15,height:18,viewBox:"0 0 15 18",data:'<path pid="0" d="M1.325 0h12.35C14.407 0 15 .592 15 1.322v11.474a1.32 1.32 0 01-1.322 1.322H4.237c-.881 0-1.875.65-2.227 1.453l-.61 1.393a.439.439 0 01-.368.242H0V1.322C0 .592.593 0 1.325 0zm7.01 7.115l1.483-1.482-.78-.78-1.482 1.482-1.482-1.482-.78.78 1.482 1.482-1.482 1.481.78.78 1.482-1.481 1.482 1.481.78-.78-1.482-1.481z" fill-rule="nonzero"/>'}})},548:function(t,e,n){"use strict";n(489)},549:function(t,e,n){var o=n(99)(!1);o.push([t.i,".pill[data-v-755c6a68]{display:inline-flex;width:auto;background:transparent;color:#fff;border-radius:3px;padding:.2em 1em;font-size:14px;font-size:.875rem;margin-top:0;margin-bottom:0;border:1px solid transparent;margin-right:.5em}.annotations[data-v-755c6a68]{position:absolute;right:0;top:0;display:block;height:100%;overflow:auto;text-align:right;padding:1em}.annotations .pill[data-v-755c6a68]{text-align:left;background:#f5f5f6;border:none;display:inline-block;border-radius:10px}.annotations .pill__text[data-v-755c6a68]{word-break:break-all;white-space:break-spaces}.predictions[data-v-755c6a68]{margin-top:1em;display:flex;flex-wrap:wrap;margin-right:-.8em;margin-left:-.8em}.predictions .pill[data-v-755c6a68]{height:40px;line-height:40px;display:flex;width:240px;align-items:center;margin-left:.8em;margin-right:.8em;margin-bottom:1.6em;font-weight:700;border:1px solid #e9eaed;border-radius:5px}.predictions .pill__confidence[data-v-755c6a68]{margin-right:0;margin-left:auto}.pill[data-v-755c6a68]{border:1px solid #686a6d;color:#686a6d;margin-bottom:.5em;line-height:1.4em}.pill__container[data-v-755c6a68]{display:flex;margin-bottom:1em}.pill__text[data-v-755c6a68]{display:inline-block;max-width:200px;text-overflow:ellipsis;white-space:nowrap;overflow:hidden}.pill__confidence[data-v-755c6a68]{font-weight:700;margin-left:1em}.pill.active[data-v-755c6a68]{border-color:#4c4ea3}.icon__predicted[data-v-755c6a68]{display:block;text-align:right;margin-right:0;margin-left:auto;margin-bottom:1em}.icon__predicted.ko[data-v-755c6a68]{fill:#ff1e5e}.icon__predicted.ok[data-v-755c6a68]{fill:#60a018}",""]),t.exports=o},555:function(t,e,n){"use strict";n.r(e);n(546),n(547);var o={props:{labels:{type:Array,required:!0},predicted:{type:String},showConfidence:{type:Boolean,default:!1},annotationLabels:{type:Array}},methods:{decorateConfidence:function(t){return 100*t},isAnnotated:function(label){return label.confidence>.5}}},r=(n(548),n(43)),component=Object(r.a)(o,(function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",[t.predicted?n("svgicon",{class:["icon__predicted",t.predicted],attrs:{width:"20",height:"20",name:t.predicted?"predicted-ko":"predicted-ok"}}):t._e(),t._v(" "),t._l(t.labels,(function(label){return n("p",{key:label.index,class:["pill",t.isAnnotated(label)?"active":""],attrs:{title:label.class}},[n("span",{staticClass:"pill__text"},[t._v(t._s(label.class)+" ")]),t._v(" "),t.showConfidence?n("span",{staticClass:"pill__confidence"},[n("ReNumeric",{staticClass:"radio-data__confidence",attrs:{value:t.decorateConfidence(label.confidence),type:"%",decimals:2}})],1):t._e()])}))],2)}),[],!1,null,"755c6a68",null);e.default=component.exports;installComponents(component,{ReNumeric:n(464).default})},569:function(t,e,n){"use strict";n.r(e);n(64),n(79),n(46),n(366);var o={model:{prop:"areChecked",event:"change"},props:["areChecked","value","id","disabled","label","allowMultiple"],data:function(){return{checked:this.value||!1}},computed:{classes:function(){return{active:Array.isArray(this.areChecked)?this.areChecked.includes(this.value):this.checked,disabled:this.disabled}}},watch:{value:function(){this.checked=!!this.value}},methods:{decorateConfidence:function(t){return 100*t},toggleCheck:function(){if(!this.disabled){var t=this.areChecked.slice(),e=t.indexOf(this.value);e>=0?t.splice(e,1):(t.length&&!this.allowMultiple&&(t=[]),t.push(this.value)),this.$emit("change",t)}}}},r=(n(543),n(43)),component=Object(r.a)(o,(function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{staticClass:"re-annotation-button",class:t.classes},[n("label",{staticClass:"button",attrs:{for:t.id},on:{click:function(e){return e.preventDefault(),t.toggleCheck.apply(null,arguments)}}},[n("span",{staticClass:"annotation-button-data__text",attrs:{title:t.label.class}},[t._v(t._s(t.label.class)+"\n    ")]),t._v(" "),n("div",{staticClass:"annotation-button-data__info"},[t.decorateConfidence(t.label.confidence)?n("ReNumeric",{staticClass:"annotation-button-data__confidence",attrs:{value:t.decorateConfidence(t.label.confidence),type:"%",decimals:0}}):t._e()],1)]),t._v(" "),n("div",{staticClass:"annotation-button-container",attrs:{tabindex:"0"},on:{click:function(e){return e.stopPropagation(),t.toggleCheck.apply(null,arguments)}}},[n("input",{attrs:{id:t.id,type:"checkbox",disabled:t.disabled},domProps:{value:t.value,checked:t.checked}})])])}),[],!1,null,"ce2c4b1a",null);e.default=component.exports;installComponents(component,{ReNumeric:n(464).default})},586:function(t,e,n){"use strict";n(541)},587:function(t,e,n){var o=n(99)(!1);o.push([t.i,".record[data-v-7289b17c]{white-space:pre-line;display:block}.record__key[data-v-7289b17c]{font-weight:600;margin-right:.5em;text-transform:uppercase}.record__item[data-v-7289b17c],.record__key[data-v-7289b17c]{font-size:16px;font-size:1rem}.record__item[data-v-7289b17c]{margin-right:1em;display:inline-block;line-height:1.6em}.record--email[data-v-7289b17c]{display:block}.record--email[data-v-7289b17c]  table{width:calc(100% - 3em)!important;max-width:700px!important;display:inline-block;overflow:scroll}.record--email[data-v-7289b17c]  table td{min-width:100px!important}@media (min-width:1901px){.record--email[data-v-7289b17c]  table{max-width:1140px!important}}.record--email[data-v-7289b17c]  img{display:none}.record--email[data-v-7289b17c]  pre{white-space:pre-wrap!important}.record--email[data-v-7289b17c]  .record__content{display:block;max-width:748px!important;margin-left:0!important;word-break:break-word!important}@media (min-width:1901px){.record--email[data-v-7289b17c]  .record__content{max-width:1140px!important}}.record--email[data-v-7289b17c]  div.WordSection1{word-break:break-all!important}.record--email[data-v-7289b17c]  div.WordSection1 p{font-family:serif!important;font-family:initial!important}",""]),t.exports=o},588:function(t,e,n){"use strict";n(542)},589:function(t,e,n){var o=n(99)(!1);o.push([t.i,".label-button[data-v-8233300e],.select--label[data-v-8233300e]{width:30%;min-width:225px;flex-grow:0;flex-shrink:0;margin-left:1%!important;margin-right:1%!important;max-width:238px}.feedback-interactions[data-v-8233300e]{margin:1.5em auto 0;padding-right:0}.feedback-interactions>div[data-v-8233300e]{width:100%}.feedback-interactions__items[data-v-8233300e]{display:flex;flex-flow:wrap;margin-left:-1%;margin-right:-1%}[data-v-8233300e] .dropdown__header{border:1px solid #e9eaed;margin:auto auto 20px;width:auto;height:42px;line-height:42px;padding-left:.5em;font-weight:600}[data-v-8233300e] .dropdown__content{max-height:280px;overflow:scroll}.select--label[data-v-8233300e]  .--checked{color:#fff;font-weight:600;text-transform:none;display:flex;width:calc(100% - 1em)}.select--label[data-v-8233300e]  .--checked span:first-child{width:112px;overflow:hidden;text-overflow:ellipsis}.select--label[data-v-8233300e]  .--checked span:last-child{margin-left:5px}.select--label.active[data-v-8233300e]  .dropdown__header{background:#4c4ea3;margin:auto auto 20px;border:1px solid #f2f3f7;border-radius:5px;transition:all .3s ease;max-width:238px}.select--label.active[data-v-8233300e]  .dropdown__header:after{border-color:#fff}.list-item[data-v-8233300e]{display:inline-block;margin-right:10px}.list-enter-active[data-v-8233300e],.list-leave-active[data-v-8233300e]{transition:all 1s}.list-enter[data-v-8233300e],.list-leave-to[data-v-8233300e]{opacity:0;transform:translateX(30px);display:flex;justify-content:space-around;align-items:center}",""]),t.exports=o},590:function(t,e,n){"use strict";n(545)},591:function(t,e,n){var o=n(99)(!1);o.push([t.i,"",""]),t.exports=o},605:function(t,e,n){var content=n(651);content.__esModule&&(content=content.default),"string"==typeof content&&(content=[[t.i,content,""]]),content.locals&&(t.exports=content.locals);(0,n(100).default)("9a401636",content,!0,{sourceMap:!1})},623:function(t,e,n){"use strict";n.r(e);n(28),n(31),n(44),n(45);var o=n(4),r=n(13),l=(n(59),n(25),n(36),n(50),n(32),n(64),n(49)),c=n(81);function d(object,t){var e=Object.keys(object);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(object);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(object,t).enumerable}))),e.push.apply(e,n)}return e}function f(t){for(var i=1;i<arguments.length;i++){var source=null!=arguments[i]?arguments[i]:{};i%2?d(Object(source),!0).forEach((function(e){Object(r.a)(t,e,source[e])})):Object.getOwnPropertyDescriptors?Object.defineProperties(t,Object.getOwnPropertyDescriptors(source)):d(Object(source)).forEach((function(e){Object.defineProperty(t,e,Object.getOwnPropertyDescriptor(source,e))}))}return t}var h={props:{dataset:{type:l.a,required:!0},record:{type:l.b,required:!0}},data:function(){return{}},computed:{labelsForAnnotation:function(){var t={};this.dataset.labels.forEach((function(label){t[label]={confidence:0,selected:!1}}));var e=this.annotationLabels.map((function(label){return f(f({},label),{},{selected:!0})}));return this.predictionLabels.concat(e).forEach((function(label){t[label.class]={confidence:label.confidence,selected:label.selected}})),Object.keys(t).map((function(label){return{class:label,confidence:t[label].confidence,selected:t[label].selected}}))},annotationEnabled:function(){return this.dataset.viewSettings.annotationEnabled},annotationLabels:function(){return this.record.annotation?this.record.annotation.labels:[]},predictionLabels:function(){return this.record.prediction?this.record.prediction.labels:[]}},methods:f(f({},Object(c.b)({editAnnotations:"entities/datasets/editAnnotations",discard:"entities/datasets/discardAnnotations",validate:"entities/datasets/validateAnnotations"})),{},{onChangeRecordStatus:function(t){var e=this;return Object(o.a)(regeneratorRuntime.mark((function n(){return regeneratorRuntime.wrap((function(n){for(;;)switch(n.prev=n.next){case 0:n.t0=t,n.next="Validated"===n.t0?3:"Discarded"===n.t0?6:"Edited"===n.t0?9:12;break;case 3:return n.next=5,e.validate({dataset:e.dataset,records:[e.record]});case 5:return n.abrupt("break",13);case 6:return n.next=8,e.discard({dataset:e.dataset,records:[e.record]});case 8:return n.abrupt("break",13);case 9:return n.next=11,e.editAnnotations({dataset:e.dataset,records:[f(f({},e.record),{},{status:"Edited",annotation:{agent:e.$auth.user,labels:[]}})]});case 11:return n.abrupt("break",13);case 12:console.warn("waT?",t);case 13:case"end":return n.stop()}}),n)})))()},onAnnotate:function(t){var e=this;return Object(o.a)(regeneratorRuntime.mark((function n(){var o;return regeneratorRuntime.wrap((function(n){for(;;)switch(n.prev=n.next){case 0:return o=t.labels,n.next=3,e.validate({dataset:e.dataset,records:[f(f({},e.record),{},{status:["Discarded","Validated"].includes(e.record.status)?"Edited":e.record.status,annotation:{agent:e.$auth.user,labels:o.map((function(label){return{class:label,confidence:1}}))}})]});case 3:case"end":return n.stop()}}),n)})))()}})},m=(n(650),n(43)),component=Object(m.a)(h,(function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{staticClass:"record"},[n("div",{staticClass:"record--left"},[n("RecordInputs",{attrs:{predicted:t.record.predicted,data:t.record.inputs,explanation:t.record.explanation,"query-text":t.dataset.query.text}}),t._v(" "),t.annotationEnabled?n("ClassifierAnnotationArea",{attrs:{labels:t.labelsForAnnotation,"multi-label":t.record.multi_label},on:{annotate:t.onAnnotate,updateStatus:t.onChangeRecordStatus}}):n("ClassifierExplorationArea",{attrs:{labels:t.predictionLabels}}),t._v(" "),n("RecordExtraActions",{attrs:{"allow-validate":!1,"annotation-mode":t.annotationEnabled,record:t.record},on:{onChangeRecordStatus:t.onChangeRecordStatus,onShowMetadata:function(e){return t.$emit("onShowMetadata")}}})],1),t._v(" "),t.annotationEnabled?t._e():n("div",{staticClass:"record__labels"},[t.record.annotation&&!t.annotationEnabled?n("LabelPill",{staticClass:"annotations",attrs:{labels:t.record.annotation.labels,predicted:t.record.predicted}}):t._e()],1)])}),[],!1,null,"e8d59686",null);e.default=component.exports;installComponents(component,{RecordInputs:n(624).default,ClassifierAnnotationArea:n(625).default,ClassifierExplorationArea:n(626).default,RecordExtraActions:n(504).default,LabelPill:n(555).default})},624:function(t,e,n){"use strict";n.r(e);n(64),n(79);var o={props:{data:{type:Object,required:!0},queryText:{type:String},predicted:{type:String,default:void 0},explanation:{type:Object,default:function(){}}},methods:{isHtml:function(t){return t.includes("<meta")}}},r=(n(586),n(43)),component=Object(r.a)(o,(function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",t._l(t.data,(function(text,e){return n("span",{key:e,staticClass:"record"},[n("span",{class:["record__item",t.isHtml(text)?"record--email":""]},[n("span",{staticClass:"record__key"},[t._v(t._s(e)+":")]),t._v(" "),t.explanation?n("LazyRecordExplain",{attrs:{predicted:t.predicted,"query-text":t.queryText,explain:t.explanation[e]}}):t._e(),t._v(" "),n("LazyRecordString",{attrs:{"query-text":t.queryText,text:text}})],1)])})),0)}),[],!1,null,"7289b17c",null);e.default=component.exports},625:function(t,e,n){"use strict";n.r(e);var o=n(80),r=(n(82),n(46),n(31),n(58),n(158),n(36),n(462),{props:{labels:{type:Array,required:!0},multiLabel:{type:Boolean,required:!0}},data:function(){return{searchText:void 0,componentLabels:void 0,maxLabelsShown:12,selectedLabel:void 0,dropdownLabels:void 0,visible:void 0,selectedLabels:[]}},computed:{sortedLabels:function(){return Object(o.a)(this.labels).sort((function(a,b){return a.confidence>b.confidence?-1:1}))},dropdownSortedLabels:function(){var t=this;return this.sortedLabels.slice(this.maxLabelsShown).filter((function(label){return label.class.toLowerCase().match(t.searchText)}))},appliedLabels:function(){return this.labels.filter((function(t){return t.selected})).map((function(label){return label.class}))}},updated:function(){this.selectedLabels=this.appliedLabels},mounted:function(){this.selectedLabels=this.appliedLabels},methods:{updateLabels:function(){this.selectedLabels.length>0?this.annotate():this.$emit("updateStatus","Edited")},annotate:function(){this.$emit("annotate",{labels:this.selectedLabels})},onVisibility:function(t){this.visible=t},decorateConfidence:function(t){return 100*t}}}),l=(n(588),n(43)),component=Object(l.a)(r,(function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{staticClass:"feedback-interactions__items",class:["feedback-interactions"]},[n("transition-group",{attrs:{name:"list",tag:"div"}},t._l(t.sortedLabels.slice(0,t.maxLabelsShown),(function(label){return n("ClassifierAnnotationButton",{key:label.class,class:["label-button",t.selectedLabels.includes(label)?"active":""],attrs:{id:label.class,"allow-multiple":t.multiLabel,label:label,"data-title":label.class,value:label.class},on:{change:t.updateLabels},model:{value:t.selectedLabels,callback:function(e){t.selectedLabels=e},expression:"selectedLabels"}})})),1),t._v(" "),t.sortedLabels.length>t.maxLabelsShown?n("FilterDropdown",{staticClass:"select--label",class:{checked:!1},attrs:{visible:t.visible},on:{visibility:t.onVisibility}},[n("template",{slot:"dropdown-header"},[n("span",{staticClass:"dropdown__text"},[t._v("More labels")])]),t._v(" "),n("template",{slot:"dropdown-content"},[n("input",{directives:[{name:"model",rawName:"v-model",value:t.searchText,expression:"searchText"}],attrs:{type:"text",autofocus:"",placeholder:"Search label..."},domProps:{value:t.searchText},on:{input:function(e){e.target.composing||(t.searchText=e.target.value)}}}),t._v(" "),null!=t.searchText?n("svgicon",{staticClass:"clean-search",attrs:{name:"cross",width:"10",height:"10",color:"#9b9b9b"},on:{click:function(e){t.searchText=""}}}):t._e(),t._v(" "),t._l(t.dropdownSortedLabels,(function(label){return n("ClassifierAnnotationButton",{key:label.class,class:["label-button"],attrs:{id:label.class,"allow-multiple":t.multiLabel,label:label,"data-title":label.class,value:label.class},on:{change:t.updateLabels},model:{value:t.selectedLabels,callback:function(e){t.selectedLabels=e},expression:"selectedLabels"}})}))],2)],2):t._e()],1)}),[],!1,null,"8233300e",null);e.default=component.exports;installComponents(component,{ClassifierAnnotationButton:n(569).default,FilterDropdown:n(454).default})},626:function(t,e,n){"use strict";n.r(e);n(46),n(462);var o={props:{labels:{type:Array,required:!0}},data:function(){return{maxLabels:16}},computed:{showLabels:function(){return this.labels.length>this.maxLabels?this.labels.slice(0,this.maxLabels):this.labels}}},r=(n(590),n(43)),component=Object(r.a)(o,(function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",[n("LabelPill",{staticClass:"predictions",attrs:{labels:t.showLabels,showConfidence:!0}})],1)}),[],!1,null,"ccc58390",null);e.default=component.exports;installComponents(component,{LabelPill:n(555).default})},650:function(t,e,n){"use strict";n(605)},651:function(t,e,n){var o=n(99)(!1);o.push([t.i,".record[data-v-e8d59686]{display:flex}.record--left[data-v-e8d59686]{width:100%;padding:2em 2em .5em}.list__item--annotation-mode .record--left[data-v-e8d59686]{padding-left:4em}.record__labels[data-v-e8d59686]{position:relative;border-left:1px solid #f5f5f6;margin-left:2em;width:170px;flex-shrink:0}",""]),t.exports=o}}]);