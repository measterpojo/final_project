
document.addEventListener('DOMContentLoaded', () => {
    'use strict';
    console.log('plan js')

    let openThreeDostMenu = threeDotBtn => {
        threeDotBtn.nextElementSibling.classList.toggle('d-none')
    }

    // show and hide child comments
    let replyLink = replyLinkElement => {
        getNthParent(replyLinkElement, 3).nextElementSibling.classList.toggle('d-none');
    };

    
    document.addEventListener('click', (event) => {
        if (event.target.closest('.js-three-dots')){
            event.preventDefault();
            openThreeDostMenu(event.target.closest('.js-three-dots'));
        } else if (event.target.closest('.js-reply-link')){
            event.preventDefault();
            replyLink(event.target);
        };
    })

    let getParents = element => {
        let parent = element.parentElement;
        let parents = [];
        let commentRootElement = document.getElementById('comments');
        console.log(commentRootElement)
        while (parent !== commentRootElement) {
            let child = parent;
            parents.push(child);
            parent = child.parentElement;
        }
        return parents;
    };


    let getNthParent = (element, nth) => {
        let parents = getParents(element);
        if (parents.length >= nth) {
            return parents[nth - 1];
        }
    };
    

})


