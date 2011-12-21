function init(){(function(){

var radians = 180/Math.PI; 
var canvas = new fabric.Canvas('efforia');
var cX = canvas.width/2;
var cY = canvas.height/2;
var last = 0;
var velocity = 0.001;
var acceleration = 0.05;
var clicked = false;

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
	fabric.loadSVGFromURL('static/interface.svg', function(objects,options) 
	{
		helix = new fabric.PathGroup(objects);
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
	canvas.observe('mouse:down',function(e) { clicked = true; });
	canvas.observe('mouse:up'  ,function(e) { clicked = false; });
	canvas.observe('mouse:move',function(e) 
	{
		if (clicked) {
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
   	if (!clicked) {
    	angularFriction = 0.2;
    	angularVelocity = velocity*timeDiff*(1-angularFriction)/1000;
    	velocity -= angularVelocity;
        helix.theta += velocity;
    }
	helix.angle = helix.theta*radians;
	canvas.renderAll();
	window.requestAnimationFrame(function() { animateElements(time); });
}

})();}