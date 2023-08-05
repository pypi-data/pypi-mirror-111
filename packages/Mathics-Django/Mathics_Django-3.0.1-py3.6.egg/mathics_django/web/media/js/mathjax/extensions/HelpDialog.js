/*
 *  /MathJax-v2/extensions/HelpDialog.js
 *
 *  Copyright (c) 2009-2018 The MathJax Consortium
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 */

(function(d,f,i,c,j){var e=MathJax.Extension.Help={version:"2.7.9"};var b="http://www.stixfonts.org/";var a=MathJax.Menu;var h,g;d.Register.StartupHook("MathEvents Ready",function(){h=MathJax.Extension.MathEvents.Event.False;g=MathJax.Extension.MathEvents.Event.KEY});var k=d.CombineConfig("HelpDialog",{styles:{"#MathJax_Help":{position:"fixed",left:"50%",width:"auto","max-width":"90%","text-align":"center",border:"3px outset",padding:"1em 2em","background-color":"#DDDDDD",color:"black",cursor:"default","font-family":"message-box","font-size":"120%","font-style":"normal","text-indent":0,"text-transform":"none","line-height":"normal","letter-spacing":"normal","word-spacing":"normal","word-wrap":"normal","white-space":"wrap","float":"none","z-index":201,"border-radius":"15px","-webkit-border-radius":"15px","-moz-border-radius":"15px","-khtml-border-radius":"15px","box-shadow":"0px 10px 20px #808080","-webkit-box-shadow":"0px 10px 20px #808080","-moz-box-shadow":"0px 10px 20px #808080","-khtml-box-shadow":"0px 10px 20px #808080",filter:"progid:DXImageTransform.Microsoft.dropshadow(OffX=2, OffY=2, Color='gray', Positive='true')"},"#MathJax_Help.MathJax_MousePost":{outline:"none"},"#MathJax_HelpContent":{overflow:"auto","text-align":"left","font-size":"80%",padding:".4em .6em",border:"1px inset",margin:"1em 0px","max-height":"20em","max-width":"30em","background-color":"#EEEEEE"},"#MathJax_HelpClose":{position:"absolute",top:".2em",right:".2em",cursor:"pointer",display:"inline-block",border:"2px solid #AAA","border-radius":"18px","-webkit-border-radius":"18px","-moz-border-radius":"18px","-khtml-border-radius":"18px","font-family":"'Courier New',Courier","font-size":"24px",color:"#F0F0F0"},"#MathJax_HelpClose span":{display:"block","background-color":"#AAA",border:"1.5px solid","border-radius":"18px","-webkit-border-radius":"18px","-moz-border-radius":"18px","-khtml-border-radius":"18px","line-height":0,padding:"8px 0 6px"},"#MathJax_HelpClose:hover":{color:"white!important",border:"2px solid #CCC!important"},"#MathJax_HelpClose:hover span":{"background-color":"#CCC!important"},"#MathJax_HelpClose:hover:focus":{outline:"none"}}});e.Dialog=function(l){j.loadDomain("HelpDialog",["Post",e,l])};e.Post=function(n){this.div=a.Background(this);var l=f.addElement(this.div,"div",{id:"MathJax_Help",tabIndex:0,onkeydown:e.Keydown},j._("HelpDialog",[["b",{style:{fontSize:"120%"}},[["Help","MathJax Help"]]],["div",{id:"MathJax_HelpContent",tabIndex:0},[["p",{},[["MathJax","*MathJax* is a JavaScript library that allows page authors to include mathematics within their web pages.  As a reader, you don't need to do anything to make that happen."]]],["p",{},[["Browsers","*Browsers*: MathJax works with all modern browsers including IE6+, Firefox 3+, Chrome 0.2+, Safari 2+, Opera 9.6+ and most mobile browsers."]]],["p",{},[["Menu","*Math Menu*: MathJax adds a contextual menu to equations.  Right-click or CTRL-click on any mathematics to access the menu."]]],["div",{style:{"margin-left":"1em"}},[["p",{},[["ShowMath","*Show Math As* allows you to view the formula's source markup for copy & paste (as MathML or in its original format)."]]],["p",{},[["Settings","*Settings* gives you control over features of MathJax, such as the size of the mathematics, and the mechanism used to display equations."]]],["p",{},[["Language","*Language* lets you select the language used by MathJax for its menus and warning messages."]]],]],["p",{},[["Zoom","*Math Zoom*: If you are having difficulty reading an equation, MathJax can enlarge it to help you see it better."]]],["p",{},[["Accessibilty","*Accessibility*: MathJax will automatically work with screen readers to make mathematics accessible to the visually impaired."]]],["p",{},[["Fonts","*Fonts*: MathJax will use certain math fonts if they are installed on your computer; otherwise, it will use web-based fonts.  Although not required, locally installed fonts will speed up typesetting.  We suggest installing the [STIX fonts](%1).",b]]]]],["a",{href:"http://www.mathjax.org/"},["www.mathjax.org"]],["span",{id:"MathJax_HelpClose",onclick:e.Remove,onkeydown:e.Keydown,tabIndex:0,role:"button","aria-label":j._(["HelpDialog","CloseDialog"],"Close help dialog")},[["span",{},["\u00D7"]]]]]));if(n.type==="mouseup"){l.className+=" MathJax_MousePost"}l.focus();j.setCSS(l);var o=(document.documentElement||{});var m=window.innerHeight||o.clientHeight||o.scrollHeight||0;if(a.prototype.msieAboutBug){l.style.width="20em";l.style.position="absolute";l.style.left=Math.floor((document.documentElement.scrollWidth-l.offsetWidth)/2)+"px";l.style.top=(Math.floor((m-l.offsetHeight)/3)+document.body.scrollTop)+"px"}else{l.style.marginLeft=Math.floor(-l.offsetWidth/2)+"px";l.style.top=Math.floor((m-l.offsetHeight)/3)+"px"}};e.Remove=function(l){if(e.div){document.body.removeChild(e.div);delete e.div}};e.Keydown=function(l){if(l.keyCode===g.ESCAPE||(this.id==="MathJax_HelpClose"&&(l.keyCode===g.SPACE||l.keyCode===g.RETURN))){e.Remove(l);a.CurrentNode().focus();h(l)}},MathJax.Callback.Queue(d.Register.StartupHook("End Config",{}),["Styles",i,k.styles],["Post",d.Startup.signal,"HelpDialog Ready"],["loadComplete",i,"[MathJax]/extensions/HelpDialog.js"])})(MathJax.Hub,MathJax.HTML,MathJax.Ajax,MathJax.OutputJax,MathJax.Localization);
