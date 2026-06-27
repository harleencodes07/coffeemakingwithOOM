const drinks = [
  {
    name: "latte",
    water: 200,
    milk: 150,
    coffee: 24,
    cost: 2.5,
    image: "assets/latte.png",
  },
  {
    name: "espresso",
    water: 50,
    milk: 0,
    coffee: 18,
    cost: 1.5,
    image: "assets/espresso.png",
  },
  {
    name: "cappuccino",
    water: 250,
    milk: 50,
    coffee: 24,
    cost: 3,
    image: "assets/cappuccino.png",
  },
];

const resources = {
  water: 300,
  milk: 200,
  coffee: 100,
};

const maximums = {
  water: 1000,
  milk: 1000,
  coffee: 500,
};

let selectedDrink = null;
let profit = 0;
let brewTimer = null;

const drinkGrid = document.querySelector("#drinkGrid");
const selectedTitle = document.querySelector("#selectedTitle");
const selectedDetails = document.querySelector("#selectedDetails");
const buyButton = document.querySelector("#buyButton");
const brewStatus = document.querySelector("#brewStatus");
const brewStage = document.querySelector("#brewStage");
const coffeeFill = document.querySelector("#coffeeFill");
const progressFill = document.querySelector("#progressFill");
const resourceList = document.querySelector("#resourceList");
const profitValue = document.querySelector("#profitValue");

const paymentDialog = document.querySelector("#paymentDialog");
const paymentForm = document.querySelector("#paymentForm");
const paymentTitle = document.querySelector("#paymentTitle");
const paymentPrice = document.querySelector("#paymentPrice");
const amountInput = document.querySelector("#amountInput");
const paymentError = document.querySelector("#paymentError");

const refillDialog = document.querySelector("#refillDialog");
const refillForm = document.querySelector("#refillForm");
const refillError = document.querySelector("#refillError");

function formatCurrency(value) {
  return `$${value.toFixed(2)}`;
}

function titleCase(text) {
  return text.charAt(0).toUpperCase() + text.slice(1);
}

function renderMenu() {
  drinkGrid.innerHTML = "";

  drinks.forEach((drink) => {
    const card = document.createElement("article");
    card.className = "drink-card";
    card.dataset.drink = drink.name;
    card.innerHTML = `
      <img src="${drink.image}" alt="${titleCase(drink.name)}" />
      <h2>${titleCase(drink.name)}</h2>
      <strong>${formatCurrency(drink.cost)}</strong>
      <button class="secondary-button" type="button">Select</button>
    `;
    card.addEventListener("click", () => selectDrink(drink));
    drinkGrid.append(card);
  });
}

function selectDrink(drink) {
  selectedDrink = drink;
  document.querySelectorAll(".drink-card").forEach((card) => {
    card.classList.toggle("selected", card.dataset.drink === drink.name);
  });

  selectedTitle.textContent = titleCase(drink.name);
  selectedDetails.textContent =
    `Price: ${formatCurrency(drink.cost)} | Water: ${drink.water} ml | ` +
    `Milk: ${drink.milk} ml | Coffee: ${drink.coffee} g`;
  buyButton.disabled = false;
  brewStatus.textContent = `${titleCase(drink.name)} selected`;
  resetAnimation();
}

function renderResources() {
  resourceList.innerHTML = "";

  Object.entries(resources).forEach(([name, value]) => {
    const percent = Math.min(100, (value / maximums[name]) * 100);
    const unit = name === "coffee" ? "g" : "ml";
    const row = document.createElement("div");
    row.className = "resource-row";
    row.innerHTML = `
      <span>
        <strong>${titleCase(name)}</strong>
        <em>${value} ${unit}</em>
      </span>
      <div class="meter"><div style="width: ${percent}%"></div></div>
    `;
    resourceList.append(row);
  });

  profitValue.textContent = formatCurrency(profit);
}

function getResourceError(drink) {
  if (drink.water > resources.water) return "Not enough water.";
  if (drink.milk > resources.milk) return "Not enough milk.";
  if (drink.coffee > resources.coffee) return "Not enough coffee.";
  return "";
}

function openPayment() {
  if (!selectedDrink) return;

  const resourceError = getResourceError(selectedDrink);
  if (resourceError) {
    brewStatus.textContent = resourceError;
    return;
  }

  paymentTitle.textContent = `${titleCase(selectedDrink.name)} Payment`;
  paymentPrice.textContent = `Price: ${formatCurrency(selectedDrink.cost)}`;
  paymentError.textContent = "";
  amountInput.value = "";
  paymentDialog.showModal();
  amountInput.focus();
}

function processPayment(event) {
  event.preventDefault();
  const amount = Number(amountInput.value);

  if (!Number.isFinite(amount) || amount < 0) {
    paymentError.textContent = "Enter a valid amount.";
    return;
  }

  if (amount < selectedDrink.cost) {
    const shortage = selectedDrink.cost - amount;
    paymentError.textContent = `You need ${formatCurrency(shortage)} more.`;
    return;
  }

  const change = amount - selectedDrink.cost;
  profit += selectedDrink.cost;
  resources.water -= selectedDrink.water;
  resources.milk -= selectedDrink.milk;
  resources.coffee -= selectedDrink.coffee;

  renderResources();
  paymentDialog.close();
  animateBrew(`Payment successful! Change: ${formatCurrency(change)}`);
}

function animateBrew(paymentMessage) {
  clearInterval(brewTimer);
  buyButton.disabled = true;
  brewStage.classList.add("brewing");
  selectedDetails.textContent = "Grinding beans";
  brewStatus.textContent = "Brewing in progress";

  const steps = ["Grinding beans", "Heating water", "Brewing", "Pouring", "Ready"];
  let progress = 0;

  brewTimer = setInterval(() => {
    progress = Math.min(100, progress + 2);
    progressFill.style.width = `${progress}%`;
    coffeeFill.style.height = `${Math.min(86, progress * 0.86)}%`;
    selectedDetails.textContent = steps[Math.min(steps.length - 1, Math.floor(progress / 25))];

    if (progress === 100) {
      clearInterval(brewTimer);
      brewStage.classList.remove("brewing");
      selectedDetails.textContent = `${paymentMessage} Enjoy your ${selectedDrink.name}!`;
      brewStatus.textContent = "Ready for the next order";
      buyButton.disabled = false;
    }
  }, 55);
}

function resetAnimation() {
  clearInterval(brewTimer);
  brewStage.classList.remove("brewing");
  coffeeFill.style.height = "0";
  progressFill.style.width = "0";
}

function openRefill() {
  refillError.textContent = "";
  refillDialog.showModal();
}

function refillMachine(event) {
  event.preventDefault();
  const water = Number(document.querySelector("#waterInput").value);
  const milk = Number(document.querySelector("#milkInput").value);
  const coffee = Number(document.querySelector("#coffeeInput").value);

  const values = [water, milk, coffee];
  if (values.some((value) => !Number.isInteger(value) || value < 0)) {
    refillError.textContent = "Enter whole numbers zero or higher.";
    return;
  }

  if (values.every((value) => value === 0)) {
    refillError.textContent = "Enter at least one amount.";
    return;
  }

  resources.water += water;
  resources.milk += milk;
  resources.coffee += coffee;
  renderResources();
  refillDialog.close();
  brewStatus.textContent = "Machine refilled successfully";
}

function showReport() {
  alert(
    `Water: ${resources.water} ml\n` +
      `Milk: ${resources.milk} ml\n` +
      `Coffee: ${resources.coffee} g\n` +
      `Profit: ${formatCurrency(profit)}`,
  );
}

buyButton.addEventListener("click", openPayment);
paymentForm.addEventListener("submit", processPayment);
refillForm.addEventListener("submit", refillMachine);
document.querySelector("#refillButton").addEventListener("click", openRefill);
document.querySelector("#reportButton").addEventListener("click", showReport);
document.querySelector("#cancelPayment").addEventListener("click", () => paymentDialog.close());
document.querySelector("#cancelRefill").addEventListener("click", () => refillDialog.close());

renderMenu();
renderResources();
