function closeEditForm(form_id) {
    document.querySelector(`#form-${form_id}`).style.display = "none";
    document.querySelector(`#editbtn-${form_id}`).innerHTML = "Edit";

    document.querySelector(`#editbtn-${form_id}`).addEventListener(
        'click', () => showEditForm(form_id)
    );
}

function showEditForm(form_id) {
    document.querySelector(`#form-${form_id}`).style.display = "block";
    document.querySelector(`#editbtn-${form_id}`).innerHTML = "Undo";

    document.querySelector(`#editbtn-${form_id}`).addEventListener(
        'click', () => closeEditForm(form_id)
    );

    document.querySelector(`#form-${form_id}`).onsubmit = () => {
        const updated_content = document.querySelector(`#new-content-${form_id}`).value;
        document.querySelector(`#indiv-content-${form_id}`).innerHTML = updated_content;

        fetch(`/post/${form_id}`, {
            method: 'PUT',
            body: JSON.stringify({
                content: updated_content
            })
        });

        closeEditForm(form_id);

        return false;
    };
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('button').forEach(function(button) {
        if (button.innerHTML === "Edit") {

            button.onclick = function() {
                showEditForm(this.dataset.editbtnid);
            }

        }
    });
});
