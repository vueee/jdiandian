$(document).ready(function(){
    $('.collapsible').collapsible();
    $('.sidenav').sidenav();
    $('.tooltipped').tooltip();
    //$('.scrollspy').scrollSpy();
    //$('.fixed-action-btn').floatingActionButton();
    // $('.dropdown-trigger').dropdown();
    //$('.tap-target').tapTarget();
    //$('.materialboxed').materialbox();
    //$('.tabs').tabs();
    
    $.getJSON('/static/rss.json',function(result){
        max = result.length
        num = Math.round(Math.random()*max)-1
        $('#rss').text(result[num].body)
    })
})