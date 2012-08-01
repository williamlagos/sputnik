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
	$.get($.fn.getSearchFilters(this.action,$(this).serialize()),{},function(data){
		$.fn.hideMenus();
		$('#Grade').loadMosaic(data);
	});
}

}