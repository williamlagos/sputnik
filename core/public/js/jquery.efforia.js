$.fn.doNothing = function(event){
	event.preventDefault();
}

$.fn.Mosaic = function(data){
	if($('.masonry').length > 0) 
		$(this).masonry('destroy').infinitescroll('destroy').data('infinitescroll',null);
	$(this).empty().html(data).imagesLoaded(function(){
		$(this).masonry({
			itemSelector: '.block',
			position: 'relative',
			isAnimated: true,
			isFitWidth: true,
			gutterWidth: 5,
			columnWidth: function(containerWidth){
				return $('.span3').width();
			}
		}).infinitescroll({
		    navSelector  : '.pagination',            
		    nextSelector : '.next',
		    itemSelector : '.block',
		    path:function(number) { return ($('.navigation').attr('href') + '?page=' + number); },
		    loading:{
		    	img:'',
		    	msg:null,
		    	msgText:'',
		    	finishedMsg:'',
		    	},
			},function(elements){
				var $elems = $(elements).css({'opacity':0});
				$elems.imagesLoaded(function(){
	                $elems.animate({'opacity': 1});
	                $('#Grade').masonry('appended',$elems,true);
	                $.fn.eventLoop();
	            });
			}
		);
	});
	$('#Progresso').modal('hide');
}

$.fn.Window = function(data){
	$(this).empty().html(data);
	$(this).modal();
}

$.fn.changeOption = function(event){
	event.preventDefault();
	var next = $(this).attr('next');
	$.get($(this).attr('href'),{},function(data){
		$('.form').html(data);
		$('.send')
		.removeClass('uploadspread postspread eventspread videospread imagespread pagespread '+ 
					 'procfg imgcfg controlcfg placecfg socialcfg '+
					 'projectcreate movementcreate grabcreate')
		.addClass(next);
		$.e.uploadOpt['url'] = $('#image').attr('action');
		$('.datepicker').datepicker($.e.datepickerOpt);
		$('.upload,.file').fileUpload($.e.uploadOpt);
		if($('.wysiwygtxt').length > 0) $.fn.activateEditor();
		$.fn.eventLoop();
	});
}

$.fn.showContext = function(event){
	event.preventDefault();
	$.ajax({
		url:$(this).attr('href'),
		success:function(data){
			$('#Espaco').html(data).modal();
			$.get($('.active').attr('href'),{},function(data){
				$('.form').html(data);
				$('.datepicker').datepicker($.e.datepickerOpt);
				$('.upload,.file').fileUpload($.e.uploadOpt);
				if($('.wysiwygtxt').length > 0) $.fn.activateEditor();
				$.fn.eventLoop();
			});
		}
	});
}

$.fn.submitSearch = function(event){
	event.preventDefault();
	$.ajax({
		url:'explore',
		data:$('.explore').serialize(),
		beforeSend:function(){ $.fn.Progress('Realizando a busca'); },
		success:function(data){
			$('#Grade').Mosaic(data);
			$.fn.eventLoop();
		}
	});
}

$.fn.activateInterface = function(){
	$.get('options',{'interface':'interface'},function(data){
		if(data == 1) $('#Canvas').hide();
		else spin.createHelix();
	});
}

$.fn.activateEditor = function(){
	$.get('options',{'typeditor':'typeditor'},function(data){
		if(data == 1) $.e.editorOpt = $.f.simpleEditor;
		else $.e.editorOpt = $.f.advancedEditor;
		$('.wysiwygtxt').wysihtml5($.e.editorOpt);
	});
}

$.fn.activateMonetize = function(){
	$.get('options',{'monetize':'monetize'},function(data){
		if(data == 1) console.log('Deactivated');
		else console.log('Activated');
	});
}

$.fn.submitPlace = function(event){
	event.preventDefault();
	$.ajax({
		url:'place',
		type:'POST',
		data:$('#place').serialize(),
		beforeSend:function(){ $('.send').button('loading'); },
		success:function(data){
			$('#Espaco').modal('hide');
		}
	});
}

$.fn.submitControl = function(event){
	event.preventDefault();
	$.ajax({
		url:'appearance',
		type:'POST',
		data:{
			'interface':$('.interface .active').val(),
			'typeditor':$('.typeditor .active').val(),
			'language':$('.language .active').val(),
			'monetize':$('.monetize .active').val(),
		},
		beforeSend:function(){ $('.send').button('loading'); },
		success:function(data){
			window.location = '/';
		}
	});
}

$.fn.newSelection = function(event){ 
	$.e.selection = true; 
	$(this).showMosaic(event); 
}

$.fn.logout = function(event){
	event.preventDefault();
	$.get('leave',{},function(data){
		console.log(data);
		window.location = '/';
	});
}

$.fn.authenticate = function(event){
	event.preventDefault();
	$.get('enter', $('.navbar-form').serialize(), function(data) {
		return window.location = '/';
	});
}

$.fn.submitChanges = function(event){
	event.preventDefault();
	$.ajax({
		url:'profile',
		type:'POST',
		data:$('#profile').serialize(),
		beforeSend:function(){ $('.send').button('loading'); },
		success:function(data){
			$('#Espaco').modal('hide');
			return window.location = '/';
		}
	});
}

$.fn.submitPasswordChange = function(event){
	$.ajax({
		url:'password',
		success:function(data){
			$('#passwordchange').html(data);
			$('#password').attr('value','Alterar senha');
			$('#password').click(function(event){
				event.preventDefault();
				$.ajax({
					url:'password',
					type:'POST',
					data:$('#passwordform').serialize(),
					beforeSend:function(){
						$('.send').button('loading');
					},
					success:function(data){
						$('#Espaco').modal('hide');
						return window.location = '/';
					}
				});
			});
		}
	});
}

$.fn.deleteObject = function(event){
	event.preventDefault();
	var object_id = $('#Espaco .id').text().trim();
	var object_token = $('#Espaco .token').text().trim();
	$.get('delete',{'id':object_id,'token':object_token},function(data){ $.fn.showMosaic(); });
}

$.fn.verifyProjects = function(){
	$.ajax('deadlines',{},function(data){});
}

$.fn.reloadMosaic = function(event){
	event.preventDefault();
	$.fn.showMosaic();
}

$.fn.showMosaic = function(){
	$('#Espaco').modal('hide');
	$.ajax({
		url:'mosaic',
		beforeSend:function(){ $.fn.Progress('Carregando seu mosaico inicial');	},
		success:function(data){
			$('#Grade').Mosaic(data);
			$.fn.eventLoop();
		}
	}); 	
}

$.fn.showFollowing = function(event){
	event.preventDefault();
	var profile_id = $('.id','.profilehead').text().trim();
	$.ajax({
		url:'following',
		data:{'profile_id':profile_id},
		beforeSend:function(){ $.fn.Progress('Vendo quem está seguindo'); },
		success:function(data){
			$('#Grade').Mosaic(data);
			$.fn.eventLoop();
		}
	});
}

$.fn.unfollow = function(event){
	event.preventDefault();
	var profile_id = $('.id','.profilehead').text().trim();
	$.ajax({
		url:'unfollow',
		data:{'profile_id':profile_id},
		beforeSend:function(){ $('.send').button('loading'); },
		success:function(data){
			window.location = '/';
		}
	});
}

$.fn.brandHover = function(event){
	event.preventDefault();
	if($.e.brand == false){
		$.e.brand = true;
		$('.trade').addClass('btn');
	} else {
		$.e.brand = false;
		$('.trade').removeClass('btn');
	}
}

$.fn.unfollowHover = function(event){
	event.preventDefault();
	if($.e.unfollow == false){
		$.e.unfollow = true;
		$('.unfollow')
		.removeClass('btn-success')
		.addClass('btn-danger')
		.html('Deixar de seguir');
	} else {
		$.e.unfollow = false;
		$('.unfollow')
		.removeClass('btn-danger')
		.addClass('btn-success')
		.html('Seguindo');
	}
}

$.fn.follow = function(event){
	event.preventDefault();
	var profile_id = $('.id','.profilehead').text().trim();
	$.ajax({
		url:'follow',
		data:{'profile_id':profile_id},
		beforeSend:function(){ $('.follow').button('loading'); },
		success:function(data){
			window.location = '/';
		}
	});
}

$.fn.showProfile = function(event){
	event.preventDefault();
	var profile_id = $('.id',this).text().trim();
	var profile_name = $('.name',this).text().trim();
	$.get('known',{'profile_id':profile_id},function(data){
		$('.profilename').html(profile_name);
		$('.profilehead').html(data);
		$('.profilebutton').click();
		$.fn.eventLoop();
	});
	$.get('activity',{'profile_id':profile_id},function(data){
		$('#Grade').Mosaic(data); 
		$.fn.eventLoop(); 
	});
}

$.fn.showRegisterView = function(event){
	event.preventDefault();
	birthday = '<div><label>Aniversário</label><input id="birthday" type="text" class="date"></input></div>'
	$.ajax({url:'register',beforeSend:$.fn.animateProgress,success:function(data){
		$('#Espaco').Dialog(data);
		//$('#Espaco').find('#etiquetas').append(birthday);
		$('#id_birthday').datepicker($.e.birthdayOpt);
		$('#id_birthday').datepicker('option',$.datepicker.regional['pt-BR']);
		$('.submit').css({'width':50});
		$.fn.eventLoop();
	}});		
}

$.fn.hideMenus = function(){
	$('#Canvas').css({'opacity':0,'display':'none'});
	$('.back').parent().show('fade');
}

$.fn.showMenus = function(){
	$('.back').parent().hide('fade');
    $('#Canvas').css({'opacity':1,'display':''});
}

$.fn.showPage = function(event){
	event.preventDefault();
	$.get('pageview',{'title':$(this).text()},function(data){
		$('.main').html(data);
	});
}

$.fn.Progress = function(message){
	$('#Progresso').modal();
	$('#Progresso .message').html(message);
}

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
	query = 'search?explore='+$('.search-query').val();
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
		url:query,//+filters,
		beforeSend:function(){ /*$('#Espaco').Progress();*/ },
		success:function(data){
			$.fn.hideMenus();
			$('#Grade').loadMosaic(data);
		}
	});
}

}
