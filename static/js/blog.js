var log = function() {
  console.log(arguments)
}



var blogCommentTemplate = function(comment) {
    var c = comment
    var t = `
        <div class="cell-inner item">
            <span class="comment">${ c.comment }</span>
            <span class="right span-margin">${ c.created_time }</span>
            <span class="right span-margin">by:${ c.name }</span>
        </div>
    `
    return t
}

var bindEventCommentToggle = function(){
            log('点到了博客评论按钮，哈哈')

//     展开评论事件
    $('a.blog-com').on('click', function(){
        $(this).parent().next().slideToggle()
        return false;
        // 因为展开评论是一个超链接 a 标签
        // 所以需要 return false 来阻止它的默认行为
        // a 的默认行为是跳转链接，没有指定 href 的时候就跳转到当前页面
        // 所以需要阻止

    })
}


var bindEventComment = function(){
    $('.blog-comment').on('click', '.blog-comment-add', function(){
        log('点到了博客评论按钮')
        var button = $(this)
        var parent = button.parent()
        var blog_id = parent.find('.comment-blog_id').val()
        log('blog_id', blog_id)
        var comment = parent.find('.comment-content').val()
        log('comment', comment)
        var form = {
            blog_id: blog_id,
            comment: comment,
        }
        var response = function(r){
            if (r.success){
                var c = r.data
                log('c', c)
                var commentList = $(parent).parent().find('.comment-list')
                log('commentList', commentList)
                commentList.append(blogCommentTemplate(c))
                alert("评论博客成功")

//                var b = r.data

            }else{
                alert(r.message)
            }
        }
        api.blogComment(form, response)
    })

}


var bindEvents = function() {
    // 不同的事件用不同的函数去绑定处理
    // 这样逻辑就非常清晰了
    bindEventCommentToggle()
    bindEventComment()
}


// 页面载入完成后会调用这个函数，所以可以当做入口
$(document).ready(function(){
    // 用 bindEvents 函数给不同的功能绑定事件处理
    // 这样逻辑就非常清晰了
    bindEvents()
})

//window.onload = main;
//
//function main(){
//  $('a.com').on('click', function(){
//    $(this).parent().next().slideToggle()
//    return false;
//  })
//
//  $('a.blog-com').on('click', function(){
//    $(this).parent().next().slideToggle()
//    return false;
//  })
//
//  $('.blog-comment-add').on('click', function(){
//      console.log('add button')
//      var button = $(this)
//      var parent = button.parent()
//      var blog_id = parent.find('.comment-blog_id').val()
//      console.log('weibo', blog_id)
//      var comment = parent.find('.comment-content').val()
//      console.log('comment', comment)
//
//      var commentList = parent.parent().find('.comment-list')
//      console.log('commentList', commentList)
//
//      var weibo = {
//          'blog_id': blog_id,
//          'comment': comment
//      }
//      var request = {
//          url: '/blog/comment',
//          type: 'post',
//          data: weibo,
//          success: function() {
//              console.log('成功', arguments)
//              var response = arguments[0]
//              var comment = JSON.parse(response)
//              var content = comment.comment
//              var avatar = comment.avatar
//              var created_time = comment.created_time
//              var name = comment.name
//              var cell = `
//                  <div class="cell-inner item">
//                    <span class="comment">${content}</span>
//                    <span class="right span-margin">${created_time}</span>
//                    <span class="right span-margin">by:${name}</span>
//                  </div>
//              `;
//              commentList.append(cell)
//              parent.find('.comment-content').val("")
//
//          },
//          error: function() {
//              console.log('错误', arguments)
//          }
//      }
//      $.ajax(request)
//  })
//
//
//}
