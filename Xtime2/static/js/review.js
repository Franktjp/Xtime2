$(function () {
    // 返回顶部
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
    // 注：用POST请求会报400BAD REQUEST的错误，原因是csrf_token，具体见开发文档
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
                // 更新icon图标下的点赞数(这里可以不更改，放入单独的页面进行)
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

// 点踩checked = True / 取消点踩checked = False
function StepReview(review_id, checked) {
    var csrftoken = $('meta[name=csrf-token]').attr('content')
    $.ajax({
        url: '/review/' + review_id + '/step',
        data: {
            review_id: review_id,
            checked: checked
        },
        type: 'POST',
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        },
        success: function (res) {
            var result = JSON.parse(res);
            if (result.status == 'OK') {
                if (checked === true) {
                    toastr['success']('点踩成功~');
                } else {
                    toastr['success']('取消点踩成功~');
                }
                // 更新icon图标下的点赞数
                var $step = $('.step').find('p').first();
                $step.text(result.dislike_nums);
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
    var $step = $('#step');
    var review_id = $('.newXtimebar').data('review_id');
    // 点赞
    $praise.click(function (e) {
        if ($praise.hasClass('checked')) {
            // 取消点赞
            PariseReview(review_id, false);
            $praise.removeClass('checked');
        } else {
            // 点赞
            PariseReview(review_id, true);
            $praise.addClass('checked');
        }
    });
    // 点踩
    $step.click(function (e) {
        if ($step.hasClass('checked')) {
            // 取消点踩
            StepReview(review_id, false);
            $step.removeClass('checked');
        } else {
            // 点踩
            StepReview(review_id, true);
            $step.addClass('checked');
        }
    });

});
