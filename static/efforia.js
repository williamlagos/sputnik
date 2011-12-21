function init() {
	(function()
	{
		if (!window.requestAnimationFrame )
		{
			window.requestAnimationFrame = (function() 
			{
				return window.webkitRequestAnimationFrame 	|| 	
					   window.mozRequestAnimationFrame 		|| 	
				       window.oRequestAnimationFrame 		|| 	
					   window.msRequestAnimationFrame	 	||
					   function(callback,element)
					   {	window.setTimeout(callback,1000/60); };
      		})();	
    	}
		var canvas = new fabric.Canvas('efforia');
		canvas.width  = window.innerWidth;
  		canvas.height = window.innerHeight;
		drawShape();
		function drawShape() {
			fabric.loadSVGFromURL('static/interface.svg', function(objects,options) {
				var helix = new fabric.PathGroup(objects,options);
				helix.set({
              		//left: coords[i].x,
              		//top: coords[i].y,
              		//angle: 30,
            	});
            	var rect = new fabric.Rect({
            		top: 100,
            		left: 100,
            		fill: 'blue',
            		width: 20,
            		height: 20
            	});
				canvas.add(helix);
				canvas.add(rect);
				
  				canvas.centerObjectH(helix).centerObjectV(helix);
  				canvas.item(0).hasBorders = false;
  				canvas.item(0).hasControls = false;
  				canvas.item(0).lockScalingX = canvas.item(0).lockScalingY = true;
  				canvas.item(0).lockMovementY = canvas.item(0).lockMovementX = true;
				
  				canvas.observe({
    				/*'mouse:down': function(e) {
      					if (e.memo.target) {
        					e.memo.target.opacity = 0.5;
        					canvas.renderAll();
      					}
    				},
    				'mouse:up': function(e) {
      					if (e.memo.target) {
        					e.memo.target.opacity = 1;
        					canvas.renderAll();
      					}
    				},*/
    				'mouse:move':function(e) {
    					var mousePos = canvas.getPointer(e.memo.e);
    					if(e.memo.target) {
                    		var x = (canvas.width / 2) - mousePos.x;
                    		var y = (canvas.height / 2) - mousePos.y;
                    		/*e.memo.target.theta = (1.5 * Math.PI + Math.atan(y / x))/180*Math.PI;
                    		e.memo.target.angle = 1.5 * Math.PI + Math.atan(y / x);
                    		if (mousePos.x <= canvas.width / 2) {*/
                    			e.memo.target.theta += Math.PI/180*Math.PI;
                    			e.memo.target.angle += Math.PI;
                    		//}	
                    		canvas.renderAll();
    					}
    				}
  				});
				//canvas.item(0).selectable = false;// helice nao pode ser selecionada
  				//canvas.selection = false;//group selection desabilitado*/
  				animate();
			});
		}
		var angle = 0;
		//var time = new Date().getTime() * 0.002;
    	//var x = Math.sin( time ) * 96 + 128;
    	//var y = Math.cos( time ) * 96 + 128;
		function animate() {
			/*angle += 1;
      		if (angle === 360) {
        		angle = 0;
      		}
      		var x = Math.sin( time ) * 96 + 128;
    		var y = Math.cos( time ) * 96 + 128;
      		canvas.item(0).setAngle(angle);
      		var time = new Date().getTime() * 0.002;
      		
      		canvas.item(1).setOptions({
      			top: x,
            	left: y
      		});*/
      		
      		canvas.renderAll();
        	window.requestAnimationFrame(animate);
      	} 
	})();
}