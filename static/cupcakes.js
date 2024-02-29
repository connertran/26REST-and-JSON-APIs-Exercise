const BASE_URL = "http://127.0.0.1:5000/api";

// initialize the page
function createNewHTMLCupcakes(cupcake) {
  return `
        <div data-cupcake-id= ${cupcake.id}>
        <img class= "Cupcake-img"
        src = "${cupcake.image}"
        alt = "(no image provided)">
            <li> ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
            <button class="delete-button">X</button>
            </li>
        </div>`;
}

async function getCupcakes() {
  try {
    let response = await axios.get(`${BASE_URL}/cupcakes`);
    console.log(response.data.cupcakes);
    return response.data.cupcakes;
  } catch (error) {
    console.error("Error fetching cupcakes:", error);
  }
}
async function displayCupcakesHTML() {
  let all_cupcakes = await getCupcakes();
  for (let i of all_cupcakes) {
    let newCupcake = $(createNewHTMLCupcakes(i));
    $("#cupcakes-list").append(newCupcake);
  }
}

displayCupcakesHTML();

// after the initialization
let $deleteBtn = $(".delete-button");
$("#cupcakes-list").on("click", $deleteBtn, deleteCupcake);
async function deleteCupcake(evt) {
  evt.preventDefault();
  let $cupcake = $(evt.target).closest("div");
  let cupcakeId = $cupcake.attr("data-cupcake-id");
  await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
  $cupcake.remove();
}

$("#add-cupcake-form").on("click", "#add-btn", async function (evt) {
  evt.preventDefault();

  let flavor = $("#form-flavor").val();
  let size = $("#form-size").val();
  let rating = $("#form-rating").val();
  let image = $("#form-image").val();
  postResponse = await axios.post(`${BASE_URL}/cupcakes`, {
    flavor: flavor,
    rating: rating,
    size: size,
    image: image,
  });
  // now append the new cupcake to the list
  let newCupcake = $(createNewHTMLCupcakes(postResponse.data.cupcake));
  $("#cupcakes-list").append(newCupcake);
  $("#add-cupcake-form").trigger("reset");
});
