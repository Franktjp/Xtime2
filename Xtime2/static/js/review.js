$(function () {
    var $backToTop = $('.back-to-top');
    // 当用户点击按钮时，通过动画效果返回头部
    $backToTop.click(function () {
        $('html, body').animate({
            scrollTop: 0
        }, 400);
    });
});

// 点赞checked = True / 取消点赞checked = False
function PariseReview(review_id, checked) {
    // review_id类型应该可以为int
    // 注：用POST请求会报400BAD REQUEST的错误，原因未知，具体见开发文档
    var csrftoken = $('meta[name=csrf-token]').attr('content')
    $.ajax({
        url: '/review/' + review_id + '/praise',
        data: {
            review_id: review_id,
            checked: checked
        },
        type: 'POST',
        // dataType: "json",
        // contentType: "application/json",
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        },
        success: function (res) {
            var result = JSON.parse(res);
            if (result.status == 'OK') {
                if (checked === true) {
                    toastr['success']('点赞成功~');
                } else {
                    toastr['success']('取消点赞成功~');
                }
                // 更新icon图标下的点赞数
                var $p_praise = $('.praise').find('p').first();
                $p_praise.text(result.fav_nums);
            } else {
                alert(result.status);
            }
        },
        error: function (error) {
            console.log(error);
        }
    })
};

$(function () {
    // 注：给变量前面加$仅仅是为了区分jQuery变量和js变量
    var $praise = $('#praise');
    $praise.click(function (e) {
        // var review_id = $praise.parent().data('value');
        var review_id = $praise.data('value');
        // console.log('review_id = ' + review_id);
        if ($praise.hasClass('checked')) {
            // 取消点赞
            PariseReview(review_id, false)
            $praise.removeClass('checked')
        } else {
            // 点赞
            PariseReview(review_id, true)
            $praise.addClass('checked')
        }
    });
});
