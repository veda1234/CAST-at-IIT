$(document).ready(() => {
  $('#formAdd').on('submit', (event) => {
    event.preventDefault();
    const file = document.getElementById('fileInput').files[0];
    let formData = new FormData();
    formData.append('file', file);
    console.log(formData);
  });
});