/*var rect = new fabric.Rect({
            		top: 100,
            		left: 100,
            		fill: 'blue',
            		width: 20,
            		height: 20
            	});*/
//var time = new Date().getTime() * 0.002;

function init(){(function() 
{
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
	c = new fabric.Canvas('efforia');
	angle = 0; drawShape();
	function drawShape() 
	{
		fabric.loadSVGFromURL('static/interface.svg', function(objects,options) 
		{
			helix = new fabric.PathGroup(objects,options);
			c.add(helix);
  			c.centerObjectH(helix).centerObjectV(helix);
  			c.selection = false;//group selection desabilitado
  			c.item(0).hasBorders = false;
  			//c.item(0).selectable = false;
  			c.item(0).lockScalingX = c.item(0).lockScalingY = true;
  			c.item(0).lockMovementX = c.item(0).lockMovementY = true;
  			
  			listenEvents();
		});
	}
	function listenEvents()
	{
		c.observe({'mouse:move' : function(e) 
		{
	    	var mousePos = canvas.getPointer(e.memo.target);
            var x = (c.width / 2) - mousePos.x;
            var y = (c.height / 2) - mousePos.y;
            c.item(0).setAngle(1.5 * Math.PI + Math.atan(y / x));
            if (mousePos.x <= c.width / 2) {
             	angle += Math.PI
                c.item(0).setAngle(angle);
            }
	    	c.renderAll();
	    }});
	    animate();
	    
	}
	function animate()
	{
    	angle += 0.5;
    	c.item(0).setAngle(angle);
    	c.renderAll();
       	window.requestAnimationFrame(animate);
    } 
})();}