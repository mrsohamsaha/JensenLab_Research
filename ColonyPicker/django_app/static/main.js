var hiddenClass = 'hidden';
var shownClass = 'toggled-from-hidden';

function petSectionHover() {
    var children = this.children;
    for(var i = 0; i < children.length; i++) {
        var child = children[i];
        if (child.className === hiddenClass) {
            child.className = shownClass;
        }
    }
}

function petSectionEndHover() {
    var children = this.children;
    for(var i = 0; i < children.length; i++) {
        var child = children[i];
        if (child.className === shownClass) {
            child.className = hiddenClass;
        }
    }
}

(function() {
    var petSections = document.getElementsByClassName('petname');
    for(var i = 0; i < petSections.length; i++) {
        petSections[i].addEventListener('mouseover', petSectionHover);
        petSections[i].addEventListener('mouseout', petSectionEndHover);
    }
}());

$( document ).ready(function() {
console.log( "ready!" );
// if(document.getElementsByClassName("zoomWindow")[0].style.display == "none"){
//   console.log('hi');
// }
var elements = document.getElementsByClassName("zoomWindow");
console.log(elements.length);
});
