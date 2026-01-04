// Modal Elements
const modal = document.getElementById('product-modal');
const modalOverlay = document.getElementById('modal-overlay');
const modalClose = document.getElementById('modal-close');
const demoBtn = document.getElementById('demo-btn');

// Tab Elements
const tabButtons = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');

// Content Elements
const modalImage = document.getElementById('modal-image');
const modalTitle = document.getElementById('modal-title');
const detailMaterial = document.getElementById('detail-material');
const detailSize = document.getElementById('detail-size');
const detailWeight = document.getElementById('detail-weight');
const detailNote = document.getElementById('detail-note');
const descriptionText = document.getElementById('description-text');
const whatsappBtn = document.getElementById('whatsapp-btn');
const emailBtn = document.getElementById('email-btn');

// Sample Product Data
const sampleProduct = {
  name: "Old Buddha/Cham Bowl",
  image: "https://via.placeholder.com/500x600/8B7355/FFFFFF?text=Singing+Bowl",
  material: "Seven metals (copper, tin, lead, mercury, iron, gold, silver)",
  size: "Medium (15cm diameter)",
  weight: "1.2 kg",
  note: "Over 100 years old, traditional handcrafted",
  description: "This Buddha Cham bowl is over 100 years old and holds significant traditional and spiritual value. It is thick in structure, which allows it to produce a higher and more resonant frequency compared to other singing bowls. The bowl is traditionally handcrafted using seven different metals—copper, tin, lead, mercury, iron, gold, and silver—each believed to represent celestial elements and contribute to its powerful sound, durability, and healing vibrations. Perfect for meditation, sound therapy, and creating a calm, healing environment."
};

// Open Modal Function
function openModal(product = sampleProduct) {
  // Set modal content
  modalImage.src = product.image;
  modalImage.alt = product.name;
  modalTitle.textContent = product.name;
  detailMaterial.textContent = product.material || "-";
  detailSize.textContent = product.size || "-";
  detailWeight.textContent = product.weight || "-";
  detailNote.textContent = product.note || "-";
  descriptionText.textContent = product.description || "No description available.";

  // Set WhatsApp link
  const whatsappMessage = encodeURIComponent("Hello, I want to know more about your instruments.");
  whatsappBtn.href = `https://wa.me/9779843213802?text=${whatsappMessage}`;

  // Set Email link
  const emailSubject = encodeURIComponent("Inquiry from website");
  emailBtn.href = `mailto:singingbowlandgonghouse@gmail.com?subject=${emailSubject}`;

  // Show modal
  modal.setAttribute('aria-hidden', 'false');
  document.body.style.overflow = 'hidden';

  // Reset to Details tab
  switchTab('details');
}

// Close Modal Function
function closeModal() {
  modal.setAttribute('aria-hidden', 'true');
  document.body.style.overflow = '';
}

// Tab Switching Function
function switchTab(tabName) {
  // Remove active class from all tabs and contents
  tabButtons.forEach(btn => btn.classList.remove('active'));
  tabContents.forEach(content => content.classList.remove('active'));

  // Add active class to selected tab and content
  const activeTabBtn = document.querySelector(`[data-tab="${tabName}"]`);
  const activeTabContent = document.getElementById(`${tabName}-content`);

  if (activeTabBtn && activeTabContent) {
    activeTabBtn.classList.add('active');
    activeTabContent.classList.add('active');
  }
}

// Event Listeners
// Demo button to open modal
if (demoBtn) {
  demoBtn.addEventListener('click', () => openModal());
}

// Close modal
if (modalClose) {
  modalClose.addEventListener('click', closeModal);
}

if (modalOverlay) {
  modalOverlay.addEventListener('click', closeModal);
}

// Tab button clicks
tabButtons.forEach(btn => {
  btn.addEventListener('click', () => {
    const tabName = btn.getAttribute('data-tab');
    switchTab(tabName);
  });
});

// Close on Escape key
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && modal.getAttribute('aria-hidden') === 'false') {
    closeModal();
  }
});

// Prevent modal content clicks from closing modal
const modalContainer = document.querySelector('.modal-container');
if (modalContainer) {
  modalContainer.addEventListener('click', (e) => {
    e.stopPropagation();
  });
}

// Initialize - Open modal on page load for demo (optional)
// Uncomment the line below if you want the modal to open automatically
// window.addEventListener('load', () => openModal());
