/* Namespace Explore */ explore = {

selectFilter:function(event){
	event.preventDefault();
	if(!$.e.openedMenu){
		$('#Menu').slideDown("slow");
		$.e.openedMenu = true;	
	}else{
		$('#Menu').slideUp("slow");
		$('.lupa').focus();
		$.e.openedMenu = false;
	}
},

submitSearch:function(event){
	event.preventDefault(); 
	all = '';
	query = this.action+'?'+$(this).serialize();
	filters = '&filters='
	leastone = false;
	$('.checkbox').each(function(){
		if($(this).css('background-position') == '0px -55px'){
			filters += $(this).parent().text().toLowerCase().replace(/^\s+|\s+$/g,'')+',';
			leastone = true;
		}
		all += $(this).parent().text().toLowerCase().replace(/^\s+|\s+$/g,'')+',';
	});
	if(!leastone) filters += all;
	$.ajax({
		url:query+filters,
		beforeSend:function(){ $('#Espaco').Progress(); },
		success:function(data){
			$.fn.hideMenus();
			$('#Grade').loadMosaic(data);
		}
	});
}

}