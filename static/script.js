document.getElementById("studentForm").addEventListener("submit", addStudent);

let editingStudentId = null;

// ----------------------
// Add / Update Student
// ----------------------
function addStudent(event) {

    event.preventDefault();

    const name = document.getElementById("name").value;
    const age = document.getElementById("age").value;
    const course = document.getElementById("course").value;

    const url = editingStudentId
        ? `/students/${editingStudentId}`
        : "/students";

    const method = editingStudentId
        ? "PUT"
        : "POST";

    fetch(url, {
        method: method,
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            name: name,
            age: age,
            course: course
        })
    })
    .then(response => response.json())
    .then(data => {

        alert(data.message);

        document.getElementById("studentForm").reset();

        editingStudentId = null;

        document.querySelector(".add-btn").textContent = "Add Student";

        loadStudents();

    })
    .catch(error => {

        console.log(error);
        alert("Something went wrong!");

    });

}

// ----------------------
// Load Students
// ----------------------
function loadStudents() {

    const statusMessage = document.getElementById("statusMessage");

    statusMessage.textContent = "⏳Loading students...";

    fetch("/students")
    .then(response => response.json())
    .then(data => {

        const studentList = document.getElementById("studentList");

        studentList.innerHTML = "";

        statusMessage.textContent = "✅ Students loaded successfully.";
        setTimeout(() => {
            statusMessage.textContent = "";
        }, 2000);

        data.forEach(student => {

            studentList.innerHTML += `
                <tr>
                    <td>${student.id}</td>
                    <td>${student.name}</td>
                    <td>${student.age}</td>
                    <td>${student.course}</td>
                    <td>
                        <button class="edit-btn" onclick="editStudent(${student.id})">
                            Edit
                        </button>

                        <button class="delete-btn" onclick="deleteStudent(${student.id})">
                            Delete
                        </button>
                    </td>
                </tr>
            `;

        });

    })
    .catch(error => {

        statusMessage.textContent = "❌ Unable to connect to the server";

        console.log(error);

    });

}

// ----------------------
// Delete Student
// ----------------------
function deleteStudent(id) {

    if (!confirm("Are you sure you want to delete this student?")) {
        return;
    }

    fetch(`/students/${id}`, {
        method: "DELETE"
    })
    .then(response => response.json())
    .then(data => {

        alert(data.message);

        loadStudents();

    })
    .catch(error => {

        console.log(error);

    });

}

// ----------------------
// Edit Student
// ----------------------
function editStudent(id) {

    fetch(`/students/${id}`)
    .then(response => response.json())
    .then(student => {

        document.getElementById("name").value = student.name;
        document.getElementById("age").value = student.age;
        document.getElementById("course").value = student.course;

        editingStudentId = student.id;

        document.querySelector(".add-btn").textContent = "Update Student";

    })
    .catch(error => {

        console.log(error);

    });

}

// ----------------------
// Load Students on Page Load
// ----------------------
loadStudents();