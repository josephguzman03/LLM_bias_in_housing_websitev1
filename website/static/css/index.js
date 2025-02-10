document.addEventListener("DOMContentLoaded", function () {
  // Smooth scrolling for navigation links
  const links = document.querySelectorAll('a[href^="#"]');
  links.forEach(link => {
      link.addEventListener('click', function (e) {
          e.preventDefault();
          const targetId = link.getAttribute("href");
          const targetElement = (targetId === "#") ? document.body : document.querySelector(targetId);

          if (targetElement) {
              targetElement.scrollIntoView({ behavior: "smooth" });
          }
      });
  });

  // Get the form element
  var form = document.getElementById('selection-form');

  if (form) {
      form.addEventListener('submit', function (event) {
          event.preventDefault();  // Prevent default form submission

          var race = document.getElementById('race-select').value;
          var livingStatus = document.getElementById('living-status-select').value;
          var occupation = document.getElementById('occupation-select').value;
          var gender = document.getElementById('gender-select').value;

          console.log('Race:', race);
          console.log('Living Status:', livingStatus);
          console.log('Occupation:', occupation);
          console.log('Gender:', gender);

          // AJAX request to Flask to update model scores
          fetch('/submit', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/x-www-form-urlencoded',
              },
              body: new URLSearchParams({
                  'race': race,
                  'living_status': livingStatus,
                  'occupation': occupation,
                  'gender': gender
              })
          })
          .then(response => response.json())
          .then(data => {
              console.log('Updated Model Scores:', data);

              // Update the table with new scores
              var scoresTable = document.getElementById('model-scores');
              if (scoresTable) {
                  let newTableContent = `
                      <h2>Model Scores</h2>
                      <table border="1">
                          <thead>
                              <tr>
                                  <th>Model</th>
                                  <th>Average Score</th>
                              </tr>
                          </thead>
                          <tbody>
                  `;

                  data.forEach(row => {
                      newTableContent += `
                          <tr>
                              <td>${row[0]}</td>
                              <td>${parseFloat(row[1]).toFixed(2)}</td>
                          </tr>
                      `;
                  });

                  newTableContent += `
                          </tbody>
                      </table>
                  `;

                  scoresTable.innerHTML = newTableContent;
              }
          })
          .catch(error => console.error('Error:', error));
      });
  }
});
