function editPost(postId) {
    const contentP = document.getElementById(`content-${postId}`);
    const original = contentP.innerText;
    contentP.innerHTML = `
        <textarea id="edit-textarea-${postId}" class="form-control" rows="3">${original}</textarea>
        <button class="btn btn-primary btn-sm mt-2" onclick="saveEdit(${postId})">Save</button>
        <button class="btn btn-secondary btn-sm mt-2" onclick="cancelEdit(${postId}, \`${original.replace(/`/g, '\\`')}\`)">Cancel</button>
    `;
}

function cancelEdit(postId, original) {
    document.getElementById(`content-${postId}`).innerHTML = original;
}

function saveEdit(postId) {
    const textarea = document.getElementById(`edit-textarea-${postId}`);
    const newContent = textarea.value;
    fetch(`/edit_post/${postId}/`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie('csrftoken')
        },
        body: JSON.stringify({ content: newContent })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            document.getElementById(`content-${postId}`).innerHTML = newContent;
        } else if (data.error) {
            alert(data.error);
        }
    });
}

function toggleLike(postId) {
    fetch(`/toggle_like/${postId}/`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.like_count !== undefined) {
            document.getElementById(`like-count-${postId}`).innerText = `Likes: ${data.like_count}`;
            document.getElementById(`like-btn-${postId}`).innerText = data.liked ? "Unlike" : "Like";
        }
    });
}

// Helper to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}