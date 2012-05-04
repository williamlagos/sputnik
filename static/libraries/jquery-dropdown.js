/**
 * DropDown plugin - v1.0.5
 * Author: Eli Van Zoeren
 * Copyright (c) 2009 New Media Campaigns
 * http://www.newmediacampaigns.com 
 **/
(function(b){b.fn.DropDown=function(e){var a=b.extend({},b.fn.DropDown.defaults,e);return this.each(function(){var d=b(this);submenus=d.children("li:has("+a.submenu_selector+")");if(a.fix_IE){d.css("z-index",51).parents().each(function(c){b(this).css("position")=="relative"&&b(this).css("z-index",c+52)});submenus.children(a.submenu_selector).css("z-index",50)}over=function(c){b(c||this).addClass(a.active_class).children(a.submenu_selector).animate(a.show,a.show_speed);return false};out=function(c){b(c||
this).removeClass(a.active_class).children(a.submenu_selector).animate(a.hide,a.hide_speed);return false};if(a.trigger=="click")submenus.click(function(c){if(b(c.target).parent().get(0)==this){c.preventDefault();b(this).hasClass(a.active_class)?out(this):over(this)}}).children(a.submenu_selector).hide();else b().hoverIntent?submenus.hoverIntent({interval:a.show_delay,over:over,timeout:a.hide_delay,out:out}).children(a.submenu_selector).hide():submenus.hover(over,out).children(a.submenu_selector).hide()})};
b.fn.DropDown.defaults={trigger:"hover",active_class:"open",submenu_selector:"ul",show:{opacity:"show"},show_speed:300,show_delay:50,hide:{opacity:"hide"},hide_speed:200,hide_delay:100,fix_IE:true}})(jQuery);