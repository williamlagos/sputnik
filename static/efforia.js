var view = true;
var known = false;
var favor = true;
var margin = 200;
var w = window.innerWidth*0.6775;
var h = window.innerHeight;
document.documentElement.style.overflowX = 'hidden';
document.documentElement.style.overflowY = 'hidden';

$(document).ready(function(){

document.getElementById('efforia').width = w;
document.getElementById('efforia').height = h;

$('#conhecidos').hide();
$('.fade').mosaic();
$('.mosaic-block').css({height:h*0.2});
$('.mosaic-small-block').css({height:h*0.05});
$('#conteudoCentral').masonry({itemSelector:'.mosaic-block'});
$('#dialogo').dialog({height:'auto',width:'auto',modal:true});
$("input:submit, button", "#botoes" ).button();
$('#radio').buttonsetv();

$('#radio').change(function(){
	if(!favor && known){
		$('#conhecidos:visible').hide('slide');
		$('#favoritos:hidden').show('slide');
	} else {
		$('#favoritos:visible').hide('slide');
		$('#conhecidos:hidden').show('slide');
	}
	known = !known;
	favor = !favor;
});

$('.mosaic-block').bind("click",function(){ view = false; });

var canvas = new fabric.Canvas('efforia');
var radians = 180/Math.PI; 
var cX = canvas.width/2;
var cY = canvas.height/2;
var last = 0;
var velocity = 0.001;
var acceleration = 0.1;
var holding = clicked = false;

if (!window.requestAnimationFrame) {
	window.requestAnimationFrame = (function() 
	{
		return window.webkitRequestAnimationFrame 	|| 	
			   window.mozRequestAnimationFrame 		|| 	
		       window.oRequestAnimationFrame 		|| 	
			   window.msRequestAnimationFrame	 	||
			   function(callback,element)
			   { window.setTimeout(callback,1000/60); };
  	})();
}

drawElements();
function drawElements() 
{
	fabric.loadSVGFromURL('interface.svg', function(objects,options) 
	{
		helix = new fabric.PathGroup(objects);
		scaleFactor = h/900;
		helix.scale(scaleFactor);
		canvas.add(helix);
		canvas.centerObjectH(helix).centerObjectV(helix);
		canvas.selection = false;
		canvas.forEachObject(function(obj) {
			obj.hasBorders = obj.hasControls = false;
			obj.lockScalingX = obj.lockScalingY = true;
			obj.lockMovementX = obj.lockMovementY = true;	
		});
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
			$('.mosaic-block').animate({"bottom":"-="+margin+"px"},1000); 
		}
	});
	canvas.observe('mouse:move',function(e) 
	{
		if (holding) {
			clicked = false;
			pos = canvas.getPointer(e.memo.e);
			x = (cX)-pos.x; y = (cY)-pos.y;
			if (velocity < 0) velocity = -velocity;
			if (velocity >= last) {
				last = velocity;
				velocity = -(Math.atan(y/x)/radians);
				velocity -= acceleration;
			} else if (velocity < last) {
				last = velocity;
				velocity = Math.atan(y/x)/radians;
				velocity += acceleration;
			}
			if (x <= cX && y <= cY)	velocity = -velocity;	
			margin = -margin;
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
    		$('#horizontal').tubeplayer('destroy');
    		$('#horizontal').empty();
    		$('#conteudoEsquerda:visible').hide('fade');
			$('#conteudoDireita:visible').hide('fade');
			$('#conteudoCanvas:visible').hide('fade');
			$('#ferramentas:visible').hide('fade');
    	}
    	helix.angle = helix.theta*radians;
	canvas.renderAll();
	window.requestAnimationFrame(function() { animateElements(time); });
}

});
