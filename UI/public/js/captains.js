//Retrieve captains 
document.addEventListener('DOMContentLoaded', function() {
  const getCaptainsBtn = document.getElementById('getCaptainsBtn');
  if (getCaptainsBtn) {
    getCaptainsBtn.addEventListener('click', getCaptains);
  }
});

function getCaptains() {
  fetch('/api/captains/all')
    .then(response => response.json())
    .then(captains => {
      console.log(captains); // Debugging line
      let result = '<table><tr><th>Captain Badge</th><th>First Name</th><th>Last Name</th><th>Home Planet</th><th>Ranking</th></tr>';
      captains.forEach(captain => {
          result += `<tr><td>${captain['Captain Badge ']}</td><td>${captain['First_Name']}</td><td>${captain['Last_Name ']}</td><td>${captain['Home PLanet ']}</td><td>${captain['Ranking ']}</td></tr>`;
      });
      result += '</table>';
      document.getElementById('captainResult').innerHTML = result;
    })
    .catch(error => {
      console.error(error);
      alert('Error retrieving captains');
    });
}


//Create Captains in form
document.addEventListener('DOMContentLoaded', () => {

  document.getElementById('createCaptainBtn').addEventListener('click', () => {
    const createForm = document.getElementById('createCaptainForm');
    createForm.style.display = createForm.style.display === 'none' ? 'block' : 'none';
  });

  document.getElementById('addCaptainForm').addEventListener('submit', (event) => {
    event.preventDefault();

    const capt_badge = document.getElementById('capt_badge').value;
    const fname = document.getElementById('fname').value;
    const lname = document.getElementById('lname').value;
    const ranking = document.getElementById('ranking').value;
    const homeplanet = document.getElementById('homeplanet').value;

    const captainData = {
      capt_badge,
      fname,
      lname,
      ranking,
      homeplanet
    };

    fetch('/api/captains', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(captainData)
    })
      .then(response => response.text())
      .then(result => {
        alert(result);
        document.getElementById('addCaptainForm').reset();
      })
      .catch(error => {
        console.error(error);
        alert('Error creating captain');
      });
  });
});
//delete captain
app.delete('/api/captains/delete/:capt_badge', function(req, res) {
  const capt_badge = req.params.capt_badge;
  const confirmation = confirm(`Are you sure you want to delete captain badge ${capt_badge}?`);
  if (confirmation) {
    fetch(`/api/captains/delete/${badge}`, { method: 'DELETE' })
    .then(response => {
      console.log(response);
      alert(`Captain badge ${capt_badge} has been deleted.`);
      location.reload(); 
    })
    .catch(error => console.error(error));
  }
});