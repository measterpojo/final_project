


document.addEventListener('DOMContentLoaded', () => {
    'use strict';

    var csrf_token = $('[name="csrfmiddlewaretoken"]').attr('value');

    console.log('Jquery')

    // SET FLAG
    $('#flagmodal').on("show.bs.modal", function(event) {
        var button = $(event.relatedTarget);
        var pk = button.data("comment-id")
        var modal = $(this);
        console.log(modal.find('form'))
        modal.find('.form').removeAttr('action')
        modal.find('form').attr('action', "http://localhost:8000/flag/" + pk + "/comment/")

    })

    // POST CRUD
    $('#staticedit').on("show.bs.modal", function(event) {
        var button = $(event.relatedTarget);
        var pk = button.data("article-id")
        console.log(pk)
        var modal = $(this);
        modal.find('form').attr('action', "update/article/" + pk + "/")
        console.log(pk)

    })


    $('#staticdelete').on("show.bs.modal", function(event) {

        var button = $(event.relatedTarget);
        var pk = button.data("article-id")
        console.log(pk)
        var modal = $(this);
        modal.find('form').attr('action', "delete/" + pk + "/")
        console.log(pk)

    })

    // COMMENT CRUD
    $('#ModalComment').on("show.bs.modal", function(event) {

        var button = $(event.relatedTarget);
        console.log(button)
        var pk = button.data("comment-id")
        var modal = $(this);
        console.log(modal)
        modal.find('.updateComment').removeAttr('action')
        modal.find('.updateComment').attr('action','http://localhost:8000/comment/edit/'+ pk + '/')
        console.log(pk)
        

    })

    $('#exampleModalCommentDelete').on("show.bs.modal", function(event) {

        var button = $(event.relatedTarget);
        console.log('assssssssss')
        console.log(button)
        var pk = button.data("comment-id")
        var modal = $(this);
        console.log(modal)
        modal.find('.deletecomment').removeAttr('action')
        modal.find('.deletecomment').attr('action','http://localhost:8000/comment/delete/'+ pk + '/')
        console.log(pk)


    })


    // REACTION LIKE DISLIKES
    $('.reaction-key').click(function() {
        console.log('reaction-key')

        var btn = $(this);

        console.log(btn)

        let targetReaction = btn.find('.comment-reaction-icon');


        $.ajaxSetup({
                headers: { "X-CSRFToken": csrf_token }
              });

        $.ajax({
            type: 'POST',
            url: btn.attr("data-url"),

             
            // on success
            success: function (response){
                console.log('success',response);
                console.log('-----------')  

                fillReaction(targetReaction);


                },

            // on error
            error: function(response){
                    // alert the error if any error occured


                console.log('error',response)
                }

        })

    })

    // FLAG 
    $('.js-comment-flag').click(function() {
        console.log('flagkey')

        var btn = $(this);



        $.ajaxSetup({
            headers: { "X-CSRFToken": csrf_token }
          });
        $.ajax({
            type: 'POST',
            url: btn.attr("data-url"),

             
            // on success
            success: function (response){
                console.log('success',response)

                },

            // on error
            error: function(response){
                    // alert the error if any error occured

                console.log('error',response)
                }


    })

    })


})




let fillReaction = (targetReaction) =>{
    let likeIcon = $('.reaction-like');
    let dislikeIcon = $('.reaction-dislike');

    


    // let isLikeEmpty = hasClass(likeIcon.classList);
    // let isDislikeEmpty = hasClass(dislikeIcon.classList);
    // let addClass = "user-has-reacted";
    // let removeClass = "user-has-not-reacted";
    // if (isLikeEmpty && isDislikeEmpty) {
    //     toggleClass(targetReaction, addClass, removeClass, 'add');
    // } else {
    //     let currentReaction = (isLikeEmpty) ? dislikeIcon : likeIcon;
    //     toggleClass(currentReaction, addClass, removeClass, 'remove');
    //     if (targetReaction !== currentReaction) {
    //         toggleClass(targetReaction, addClass, removeClass, 'add');
    //     }
    // }
};

