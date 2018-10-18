
function noCover() {
    var img = event.srcElement;
    img.src = "/static/images/default.png";
    img.onerror = null;
};


var cloudstore = 'https://jdiandian-1257713877.cos.ap-hongkong.myqcloud.com/'
//get the author info
var postId = $('#post_info').data('id')
var authorId = $('#post_info').data('uid').toString()
var authorName = $('#post_info').data('author')
var avatar =  cloudstore + authorId + '/avatar.jpg'
var donate = cloudstore + authorId + '/donate.jpg'

$('#author_name').text(authorName)
$('#avatar').attr('src', avatar)



$(document).ready(function () {
    $(document).mousemove(function(e){
        if(e.pageY < 120){
            $('header').show()
        }else{
            $('header').hide()
        }
    })

    $('#flow-body')
        .find('img')
        .each(function () {
            $(this).addClass('responsive-img z-depth-2')
        })

    $('#flow-body')
        .find('vedio')
        .each(function () {
            $(this).addClass('responsive-video')
        })

    var toggleFlowTextButton = $('#flow-toggle');
    toggleFlowTextButton.click(function () {
        $('#flow-body')
            .children('p')
            .each(function () {
                $(this).toggleClass('flow-text');
            });
    })

    $('#author').one('mouseenter',function () {
        $('#author_info').load('/author/'+authorId)
    })

    $('#donate').magnificPopup({
        items: {
            src:donate
        },
        type:'image',
    })

    $('#subscribe').click(function(e){
        e.stopPropagation()
        $.ajax({
            type:"POST",
            url:'/subscribe',
            data:JSON.stringify({"id":authorId,"name":authorName}),
            contentType:"application/json;chaerset=UTF-8",
            success:function(result){
                M.toast({html:result, classes:'rounded skr-pink'})
            }
        })
    })

    $('#comment_submit').click(function(e){
        e.preventDefault()
        var praise =$("input[name='praise']:checked").val()
        var comment =$('#comment_area').val()
        if(comment==''){
            M.toast({html:'请填写评论！',classes:'rounded skr-pink'})
            return false;
        }
        var nhtml= `
        <li class="collection-item avatar">
            <i class="material-icons circle green">android</i>
            <p id=comment_body>${comment}</p>
            <a href="#!" class="secondary-content"><i class="material-icons skr-pink-color">thumb_${praise}</i></a>
        </li>`
        $('#comments').prepend(nhtml)

        $.ajax({
            type:"POST",
            url:'/post/'+postId+'/comment/add',
            data:JSON.stringify({"praise":praise,"body":comment}),
            contentType:"application/json;chaerset=UTF-8",
            success:function(result){
                M.toast({html:result,classes:'rounded skr-pink'})
            }
        });
    })

   $.getJSON('/post/'+postId+'/comment',function(result){
       var chtml = ''
       for(var i in result){
          chtml= chtml + `
            <li class="collection-item avatar">
                <a href="/user/${result[i].id}">
                <img class="comment-avatar circle" src="${cloudstore+result[i].id}/avatar.jpg" onerror="this.onerror='';src='/static/images/default-avatar.jpg'"/>
                </a>
                <p id=comment_body>${result[i].body}</p>
                <a href="#!" class="secondary-content"><i class="material-icons skr-pink-color">thumb_${result[i].praise}</i>
            </li>`
       }
       $('#comments').html(chtml)
   })

})
