
RGraph=window.RGraph||{isRGraph:true,isRGraphSVG:true};RGraph.SVG=RGraph.SVG||{};(function(win,doc,undefined)
{RGraph.SVG.tooltips={};RGraph.SVG.tooltips.style={display:'inline-block',position:'absolute',padding:'6px',lineHeight:'initial',fontFamily:'Arial',fontSize:'12pt',fontWeight:'normal',textAlign:'center',left:0,top:0,backgroundColor:'rgb(255,255,239)',color:'black',visibility:'visible',zIndex:3,borderRadius:'5px',boxShadow:'rgba(96,96,96,0.5) 0 0 5px',transition:'left ease-out .25s, top ease-out .25s'};RGraph.SVG.tooltip=function(opt)
{var obj=opt.object;RGraph.SVG.fireCustomEvent(obj,'onbeforetooltip');if(!opt.text||typeof opt.text==='undefined'||RGraph.SVG.trim(opt.text).length===0){return;}
var prop=obj.properties;if(typeof prop.tooltipsOverride==='function'){document.body.addEventListener('mouseup',function(e)
{obj.removeHighlight();},false);return(prop.tooltipsOverride)(obj,opt);}
if(!RGraph.SVG.REG.get('tooltip')){var tooltipObj=document.createElement('DIV');tooltipObj.className=prop.tooltipsCssClass;for(var i in RGraph.SVG.tooltips.style){if(typeof i==='string'){tooltipObj.style[i]=RGraph.SVG.tooltips.style[i];}}}else{var tooltipObj=RGraph.SVG.REG.get('tooltip');tooltipObj.__object__.removeHighlight();tooltipObj.style.width='';}
if(RGraph.SVG.REG.get('tooltip-lasty')){tooltipObj.style.left=RGraph.SVG.REG.get('tooltip-lastx')+'px';tooltipObj.style.top=RGraph.SVG.REG.get('tooltip-lasty')+'px';}
tooltipObj.innerHTML=opt.text;tooltipObj.__text__=opt.text;tooltipObj.id='__rgraph_tooltip_'+obj.id+'_'+obj.uid+'_'+opt.index;tooltipObj.__event__=prop.tooltipsEvent||'click';tooltipObj.__object__=obj;if(typeof opt.index==='number'){tooltipObj.__index__=opt.index;}
if(typeof opt.dataset==='number'){tooltipObj.__dataset__=opt.dataset;}
if(typeof opt.group==='number'||RGraph.SVG.isNull(opt.group)){tooltipObj.__group__=opt.group;}
if(typeof opt.sequentialIndex==='number'){tooltipObj.__sequentialIndex__=opt.sequentialIndex;}
document.body.appendChild(tooltipObj);var width=tooltipObj.offsetWidth,height=tooltipObj.offsetHeight;tooltipObj.style.left=opt.event.pageX-(width/2)+'px';tooltipObj.style.top=opt.event.pageY-height-15+'px';tooltipObj.style.width=width+'px';if(!RGraph.SVG.REG.get('tooltip-lastx')){for(var i=0;i<=30;++i){(function(idx)
{setTimeout(function()
{tooltipObj.style.opacity=(idx/30)*1;},(idx/30)*200);})(i);}}
if(parseFloat(tooltipObj.style.left)<=5){tooltipObj.style.left='5px';}
if(parseFloat(tooltipObj.style.left)+parseFloat(tooltipObj.style.width)>window.innerWidth){tooltipObj.style.left=''
tooltipObj.style.right='5px'}
if(RGraph.SVG.isFixed(obj.svg)){var scrollTop=window.scrollY||document.documentElement.scrollTop;tooltipObj.style.position='fixed';tooltipObj.style.top=opt.event.pageY-scrollTop-height-10+'px';}
tooltipObj.onmousedown=function(e)
{e.stopPropagation();};tooltipObj.onmouseup=function(e)
{e.stopPropagation();};tooltipObj.onclick=function(e)
{if(e.button==0){e.stopPropagation();}};document.body.addEventListener('mouseup',function(e)
{RGraph.SVG.hideTooltip();},false);RGraph.SVG.REG.set('tooltip',tooltipObj);RGraph.SVG.REG.set('tooltip-lastx',parseFloat(tooltipObj.style.left));RGraph.SVG.REG.set('tooltip-lasty',parseFloat(tooltipObj.style.top));RGraph.SVG.fireCustomEvent(obj,'ontooltip');};})(window,document);