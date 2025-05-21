/**
 * File Upload
 */

'use strict';

(function () {
  Dropzone.autoDiscover = false;

  // Dropzone preview template
  const previewTemplate = `<div class="dz-preview dz-file-preview">
    <div class="dz-details">
      <div class="dz-thumbnail">
        <img data-dz-thumbnail>
        <span class="dz-nopreview">No preview</span>
        <div class="dz-success-mark"></div>
        <div class="dz-error-mark"></div>
        <div class="dz-error-message"><span data-dz-errormessage></span></div>
        <div class="progress m-4">
          <div class="progress-bar progress-bar-primary m-2" role="progressbar" aria-valuemin="0" aria-valuemax="100" data-dz-uploadprogress></div>
        </div>
      </div>
      <div class="dz-filename" data-dz-name></div>
      <div class="dz-size" data-dz-size></div>
    </div>
  </div>`;

  const dropzoneMulti = document.querySelector('#dropzone-multi');
  if (dropzoneMulti) {
    const myDropzoneMulti = new Dropzone(dropzoneMulti, {
      previewTemplate: previewTemplate,
      uploadMultiple: true,
      parallelUploads: 25,
      maxFilesize: 100, // 100MB max file size
      addRemoveLinks: true,
      autoProcessQueue: false, // Disable auto upload
      acceptedFiles: ".pdf,.csv,.txt,.xlsx,.docx" // Only allow PDF, CSV, and TXT files
    });

    // Success event listener: reloads page when all files are uploaded
    myDropzoneMulti.on("success", function (file, response) {
      console.log("[INFO] File uploaded successfully.");
      if (myDropzoneMulti.getQueuedFiles().length === 0 && myDropzoneMulti.getUploadingFiles().length === 0) {
        location.reload(); // Refresh the page
      }
    });

    // Error event listener: shows an alert and reloads page
    myDropzoneMulti.on("error", function (file, errorMessage, xhr) {
      console.error("[ERROR] Upload failed:", errorMessage);
      location.reload(); // Refresh the page
    });

    // Upload button click event
    const submitUploadButton = document.querySelector('#submit-upload');
    if (submitUploadButton) {
      submitUploadButton.addEventListener('click', function () {
        const files = myDropzoneMulti.getQueuedFiles();
        const oversizedFiles = files.filter(file => file.size > 100 * 1024 * 1024); // Files > 100MB

        var show_alert = document.getElementById("show_alert");
        show_alert.classList.add("d-none");

        if (oversizedFiles.length > 0) {
          show_alert.classList.remove("d-none");
          show_alert.innerHTML = 'File is over-sized, please select another file.';
        } else if (files.length > 0) {
          myDropzoneMulti.processQueue();
        } else {
          show_alert.classList.remove("d-none");
          show_alert.innerHTML = 'Please select a file.';
        }
      });
    }
  }
})();
