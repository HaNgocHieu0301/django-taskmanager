const draggables = document.querySelectorAll(".task")
const droppables = document.querySelectorAll(".swim-lane")
draggables.forEach(draggable => {
    draggable.addEventListener('dragstart', () => {
        draggable.children[0].classList.add('is-dragging')
    })
    draggable.addEventListener('dragend', () => {
        draggable.children[0].classList.remove('is-dragging');
    })
})
droppables.forEach((zone) => {
    zone.addEventListener('dragover', (e) =>{
        e.preventDefault()
        const bottomTask = insertAboveTask(zone, e.clientY)
        // curTask = li tag
        const curTask = document.querySelector(".is-dragging").parentElement
        // document.querySelector(".is-dragging").style.background = '#000000'
        // document.querySelector(".is-dragging .deadline").style.background = '#000000'
        // document.querySelector(".is-dragging .deadline").style.color = '#000000'
        // document.querySelector(".is-dragging span").style.color = '#000000'
        // document.querySelector(".is-dragging").style.opacity = '0.5'
        if(!bottomTask){
            zone.children[0].appendChild(curTask)
        }else{
            zone.children[0].insertBefore(curTask, bottomTask)
        }
    })
    zone.addEventListener('drop', (e) =>{
        e.preventDefault()
        const curTask = document.querySelector(".is-dragging").parentElement
        const taskId = curTask.dataset.taskId;
        const task = tasksData.find(task => task.pk == taskId)
        const stateId = zone.parentElement.dataset.stateId
        // document.querySelector(".is-dragging").style.removeProperty('background')
        // document.querySelector(".is-dragging").style.removeProperty('opacity')
        // document.querySelector(".is-dragging span").style.removeProperty('color')
        // document.querySelector(".is-dragging .deadline").style.removeProperty('background')
        // document.querySelector(".is-dragging .deadline").style.removeProperty('color')
        UpdateTask(task, taskId, stateId, task.fields.description, task.fields.title, task.fields.deadline);
    })
    // let curTask = null; // Tạo biến tạm thời để lưu trữ curTask
    // let bottomTask = null
    // zone.addEventListener('dragover', (e) => {
    //     e.preventDefault();
    //     bottomTask = insertAboveTask(zone, e.clientY);
    //     if(!curTask){
    //         let emptyElement = document.querySelector(".is-dragging").parentElement.cloneNode(true);
    //         emptyElement.classList.add('empty-placeholder');
    //         emptyElement.children[0].style.backgroundColor = '#000000'
    //         emptyElement.children[0].style.color = '#000000'
    //         // emptyElement.style.opacity = '0.5'
    //         const removeElement = zone.querySelector('.empty-placeholder');
    //         if (removeElement) {
    //             zone.children[0].removeChild(removeElement);
    //         }
    //         if (!bottomTask) {
    //             zone.children[0].appendChild(emptyElement)
    //         } else {
    //             zone.children[0].insertBefore(emptyElement, bottomTask)
    //         }
    //     }
    //     curTask = document.querySelector(".is-dragging").parentElement
    // });
    //
    // zone.addEventListener('drop', (e) => {
    //     e.preventDefault();
    //     if (curTask) {
    //         const taskId = curTask.dataset.taskId;
    //         const task = tasksData.find(task => task.pk == taskId);
    //         const stateId = zone.parentElement.dataset.stateId;
    //         // UpdateTask(task, taskId, stateId, task.fields.description, task.fields.title, task.fields.deadline);
    //
    //         const emptyElement = zone.querySelector('.empty-placeholder');
    //         if (emptyElement) {
    //             zone.children[0].removeChild(emptyElement);
    //         }
    //         if (!bottomTask) {
    //             zone.children[0].appendChild(curTask)
    //         } else {
    //             zone.children[0].insertBefore(curTask, bottomTask)
    //         }
    //         curTask = null; // Đặt curTask về null sau khi thả
    //     }
    // });
})
const insertAboveTask = (zone, mouseY) => {
    const elsParent = zone.querySelectorAll(".task")
    const els = [...elsParent].filter(e => !e.classList.contains("is-dragging"))
    let closestTask = null;
    let closestOffset = Number.NEGATIVE_INFINITY

    els.forEach((task) => {
        const {top} = task.getBoundingClientRect()

        const offset = mouseY - top

        if (offset < 0 && offset > closestOffset) {
            closestOffset = offset
            closestTask = task
        }
    })
    return closestTask
}

function UpdateTask(task, taskId, state, description, title, deadline) {
    const taskData = {
        'new_task_id': taskId,
        'new_task_state': state,
        'new_task_description': description,
        'new_task_title': title,
        'new_task_deadline': deadline,
        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
    }
    $.ajax({
        type: 'POST',
        url: '', // URL của view, để trống nếu cùng URL với trang hiện tại
        data: taskData,
        success: function (response) {
            let countInt = parseInt($(`#state-${task.fields.state}`).html())
            $(`#state-${task.fields.state}`).html(countInt - 1)
            task.fields.state = state
            countInt = parseInt($(`#state-${task.fields.state}`).html())
            $(`#state-${task.fields.state}`).html(countInt + 1)
            console.log('Task updated successfully!');
        },
        error: function (error) {
            console.log('Error updating task:', error);
        }
    });
}