const okTemplate = document.getElementById("card-instance-ok").content;
const downTemplate = document.getElementById("card-instance-down").content;
const columns = [
  document.getElementById("column-1"),
  document.getElementById("column-2"),
];

let addedInfos = 0;
function addInstanceInfo(instance, status) {
  let card;
  if (status == 1) {
    card = okTemplate.cloneNode(true);
  } else {
    card = downTemplate.cloneNode(true);
  }

  card.querySelector("h2").textContent = `Instance ${instance}`;
  columns[addedInfos % columns.length].appendChild(card);
  addedInfos++;
}

function fetchInstance(instance) {
  return fetch(`/api/uptime?instance=${instance}`);
}

async function fetchAllInstances() {
  let instances = [];
  for (let i = 1; ; i++) {
    const response = await fetchInstance(i).then((r) => r.json());
    if (!(response.data || {}).result.length > 0) {
      break;
    }

    instances.push([i, response.data.result[0].value[1]]);
  }
  return instances;
}

function updateInstances() {
  columns.forEach((column) => column.replaceChildren());
  fetchAllInstances().then((instances) =>
    instances.map(([instance, status]) => addInstanceInfo(instance, status))
  );
  setTimeout(updateInstances, 10 * 1000);
}

updateInstances();
