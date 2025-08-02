document.addEventListener('DOMContentLoaded', () => {
    const pagination = document.getElementById('pagination');

    pagination.addEventListener('click', async (e) => {
        const issueContainer = document.getElementById('issue-list');
        issueContainer.innerHTML = ''; // Clear existing
        const loading = document.createElement('div');
                    loading.className = "bg-gray-100 dark:bg-gray-800 rounded-xl shadow-md p-5 col-span-3 text-center";
                    loading.innerHTML = `
            <h3 class="text-xl lg:text-2xl font-semibold text-gray-800 dark:text-gray-100 mb-2">Loading</h3>
            <p class="text-sm lg:text-xl text-gray-600 dark:text-gray-100 mb-3">Please wait while we are loading data.</p>
          `;
          issueContainer.appendChild(loading);
        if (e.target.matches('button[data-page]')) {
            const page = e.target.getAttribute('data-page');
            const response = await fetch(`/api/issues?page=${page}`);
            const data = await response.json();
            // console.log(data)
            // Now dynamically update your issue list section
            console.log(page, "for", data)
            setTimeout(() => {
                issueContainer.innerHTML = ''; // Clear existing
                data.issues.forEach(issue => {
                    const card = document.createElement('div');
                    card.className = "bg-gray-100 dark:bg-gray-800 rounded-xl shadow-md p-5";
                    card.innerHTML = `
            <img src="${issue.image_url}" alt="Issue Image" class="rounded-md h-40 w-full object-cover mb-4">
            <h3 class="text-xl font-semibold text-gray-800 dark:text-gray-100 mb-2">${issue.title}</h3>
            <p class="text-sm text-gray-600 dark:text-gray-100 mb-3">${issue.description}</p>
            <div class="flex justify-between text-sm text-gray-500">
              <span>Status: <span class="text-yellow-600">${issue.status}</span></span>
              <span>${issue.distance}</span>
            </div>
          `;

                    issueContainer.appendChild(card);
                });
            }, 2000);
        }
    });
});
