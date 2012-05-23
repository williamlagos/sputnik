var view = true;
var known = false;
var favor = true;
var w = window.innerWidth*0.85;
var h = window.innerHeight-40;
var marginFactor = 8;
document.documentElement.style.overflowX = 'hidden';
document.documentElement.style.overflowY = 'hidden';

$(document).ready(function(){
	
/*document.onselectstart = function () { return false; } // ie
document.onmousedown = function () { return false; } // mozilla*/

document.getElementById('efforia').width = w;
document.getElementById('efforia').height = h;

$('a').click(function(){ this.blur(); });
$.get('/',{'feed':'feed'},function(data){ 
	$('#Grade').loadMosaic(data);
	$('#Grade').css({'height':h});
	$('.mosaic-block').mosaic();
	$('.mosaic-block').bind("click",function(){ view = false; });
	if($('.blank').text() != '') marginFactor = 0;
	$('.causable,.playable,.spreadable,.event').click(function(event){
		event.preventDefault();
		$('#Espaco').html($(this).html());
		$('#Espaco').dialog({
			title:'Objeto',height:'auto',width:'auto',modal:true,
			position:'center',resizable:false,draggable:false
		});
	});	
	$('.movement,.schedule').click(function(event){
		event.preventDefault();
		title = $(this).find('h2').html();
		refer = $(this).attr('href');
		$.ajax({
			url:refer,
			data:{'view':refer,'title':title},
			success:function(data){ $('#Grade').loadMosaic(data); }
		});
	});
	$('.loadable').click(function(event){
		event.preventDefault();
		number = $(this).attr('name');
		$.post($(this).attr('href'),{'number':number},function(data){
			$('#Grade').css({marginTop:'0px'});
			$('#Grade').loadMosaic(data);
			if($('.blank').text() != '') marginFactor = 0;
		});
	}); 
});

$("input:submit, button", "#botoes" ).button();

var widthNow = $('html').width();
var heightNow = $('html').height();
var helix = null;
var canvas = new fabric.Canvas('efforia');
var radians = 180/Math.PI; 
var cX = canvas.width/2;
var cY = canvas.height/2;
var last = 0;
var velocity = 0.001;
var acceleration = 0.1;
var holding = clicked = false;

if(widthNow < 1280) $('body').css({'font-size':'0.8em'});

if (!window.requestAnimationFrame) {
	window.requestAnimationFrame = (function() 
	{
		return window.webkitRequestAnimationFrame 	|| 	
			   window.mozRequestAnimationFrame 		|| 	
		       window.oRequestAnimationFrame 		|| 	
			   window.msRequestAnimationFrame	 	||
			   function(callback,element)
			   { 
			   		window.setTimeout(callback,1000/60); 
			   };
  	})();
}

$(window).resize(function() {
	w = window.innerWidth*0.85;
	h = window.innerHeight-40;
	$('#conteudoCanvas,.canvas-container,.lower-canvas,#efforia').css({'height':h,'width':w});
	cX = canvas.width/2;
	cY = canvas.height/2;
	canvas.clear();
	scaleFactor = h/1200;
	helix.scale(scaleFactor);
	scaleFactor = w/1200;
	helix.scale(scaleFactor);
	widthNow = $('body').width();
	if(widthNow < 1280) $('body').css({'font-size':'0.8em'});
	else if(widthNow > 1280) $('body').css({'font-size':'1.0em'});
	canvas.add(helix);
	canvas.centerObjectH(helix).centerObjectV(helix);
});

drawElements();
function drawElements() 
{
	fabric.loadSVGFromURL('interface.svg', function(objects,options) 
	{
		canvas.forEachObject(function(obj) {
			obj.hasBorders = obj.hasControls = false;
			obj.lockScalingX = obj.lockScalingY = true;
			obj.lockMovementX = obj.lockMovementY = true;	
		});
		canvas.selection = false;
		helix = new fabric.PathGroup(objects);
		w = window.innerWidth*0.85;
		h = window.innerHeight-40;
		$('#conteudoCanvas,.canvas-container,.lower-canvas,#efforia').css({'height':h,'width':w});
		cX = canvas.width/2;
		cY = canvas.height/2;
		canvas.clear();
		scaleFactor = h/1200;
		helix.scale(scaleFactor);
		scaleFactor = w/1200;
		helix.scale(scaleFactor);
		widthNow = $('body').width();
		if(widthNow < 1280) $('body').css({'font-size':'0.8em'});
		else if(widthNow > 1280) $('body').css({'font-size':'1.0em'});
		canvas.add(helix);
		canvas.centerObjectH(helix).centerObjectV(helix);
		scaleFactor = h/1200;
		listenEvents();
	});
}

function listenEvents()
{
	canvas.observe('mouse:down',function(e) { holding = true; clicked = true; });
	canvas.observe('mouse:up'  ,function(e) { 
		holding = false;
		view = true; 
		if(!clicked){
			$('#Grade').animate({"marginTop":"-="+margin+"px"},1000);
			var marginTop = $('#Grade').css('marginTop').replace(/[^-\d\.]/g, '');
			var marginMax = -$('.mosaic-block').height()*marginFactor; 
			if(marginTop == 0 && margin < 0){
				$('#Grade').animate({"marginTop":"+="+margin+"px"},1000); 
			}else if(marginMax-marginTop == 0){
				$('#Grade').animate({"marginTop":"+="+margin+"px"},1000);
			}
		}
	});
	canvas.observe('mouse:move',function(e) 
	{
		if (holding) {
			clicked = false;
			pos = canvas.getPointer(e.memo.e);
			x = (cX)-pos.x; y = (cY)-pos.y;
			if (velocity < 0) velocity = -velocity;
			// Sentido antihorario
			if (velocity >= last) {
				margin = -$('.mosaic-block').height();
				last = velocity;
				velocity = -(Math.atan(y/x)/radians);
				velocity -= acceleration;
			// Sentido horario
			} else if (velocity < last) {
				margin = $('.mosaic-block').height();
				last = velocity;
				velocity = Math.atan(y/x)/radians;
				velocity += acceleration;
			}
			if (x <= cX && y <= cY)	velocity = -velocity;	
			helix.theta += velocity;
		}
	});
	date = new Date();
	time = date.getTime();  
	animateElements(time);	
}

function animateElements(lastTime)
{
	date = new Date();
    	time = date.getTime();
    	timeDiff = time - lastTime;
   	if (!holding && !clicked) {
    		angularFriction = 0.1;
    		angularVelocity = velocity*timeDiff*(1-angularFriction)/1000;
    		velocity -= angularVelocity;
        	helix.theta += velocity;
    	} else if (!holding && clicked && view) {
		$.fn.hideMenus();
    	}
    	helix.angle = helix.theta*radians;
	canvas.renderAll();
	window.requestAnimationFrame(function() { animateElements(time); });
}

});
