// on document load, add dragstart event listener to .draggable-item elements
document.addEventListener('DOMContentLoaded', function() {
    const draggableItems = document.querySelectorAll('.draggable-item');

    draggableItems.forEach(item => {
        item.addEventListener('dragstart', dragStart);
    });

    const equationBuilder = document.getElementById('equation-builder');

    equationBuilder.addEventListener('drop', drop);
    equationBuilder.addEventListener('dragover', allowDrop);
    equationBuilder.addEventListener('dragstart', dragStart);
});

// capture outerhtml of target to later copy it to the target location
function dragStart(event) {
    event.dataTransfer.setData('text/plain', event.target.outerHTML);
}

// prevents normal (???) functionality of dropping into a box
function allowDrop(event) {
    // prevent default to allow drop
    event.preventDefault();
}

function drop(event) {
    // prevent default action (open as link for some elements)
    event.preventDefault();
    const data = event.dataTransfer.getData('text/plain');
    const term = document.createElement('div');
    term.innerHTML = data;
    
    try {
        isDraggableElement = term.firstChild.classList.contains('draggable-item');
    } 
    catch (error) {
        console.log (error);
        return
    }
    
    if (event.target.id == 'equation-builder') {
        term.classList.add('playlist-equation-term');
        term.classList.add('draggable-item');
        term.draggable = true;
        event.target.appendChild(term);
    }
    
    // LATER: if target is in equation builder, swap positions

    // LATER: if target is the space between elements, fill that space and add two new spaces to the side
    // standard: e.g. PLAYLIST space OPERATOR space PLAYLIST
    
    else {
        console.log('debug: please drag into the equation builder')
    }
}

document.addEventListener('dragstart', function(event) {
    if (event.target.closest('#equation-builder')) {
        event.target.addEventListener('dragend', function() {
            event.target.parentNode.removeChild(event.target);
        });
    }
});