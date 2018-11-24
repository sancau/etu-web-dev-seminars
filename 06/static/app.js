(function () {
	'use strict';

	const recordHTML = (title, message) => `
  <div class="record">
    <div class="title">
      ${title}
    </div>
    <div class="message">
      ${message}
    </div>
  </div>
  `;

	const renderRecord = (title, message) => {
    const container = document.getElementById('records-container');
    const record = document.createElement('div');
    record.innerHTML = recordHTML(title, message);
    container.appendChild(record);
  };

	const clearList = () => {
	  const container = document.getElementById('records-container');
	  container.innerHTML = '';
  };

	const requestRecords = (searchTerm, callback) => {
	  const xhr = new XMLHttpRequest();
    xhr.open('GET', `api/records/?search=${searchTerm}`);
    xhr.onload = function() {
        if (xhr.status === 200) {
          const records = JSON.parse(xhr.responseText);
          callback(records);
        }
        else {
            console.error(`Request failed. Returned status of ${xhr.status}`);
        }
    };
    xhr.send();
  };

	const fetchAndRender = (searchTerm) => {
	  requestRecords(searchTerm, (records) => {
      clearList();
	    records.forEach((item, i, arr) => {
        renderRecord(item.title, item.message);
      })
    });
  };

	// event listeners
	document.getElementById('search-input').addEventListener('input', (e) => {
	  fetchAndRender(e.target.value);
  });

	fetchAndRender('');

}());