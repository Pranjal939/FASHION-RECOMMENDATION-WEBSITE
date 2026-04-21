// Product Data
const products = {
    trending: [
        {
            id: 1,
            name: "Denim Jacket",
            price: 550,
            image: "images/denim_jecket.jpeg",
            description: "Stylish casual denim wear",
            colors: [
                { name: "Black", image: "images/denim_jecket.jpeg" },
                { name: "Wine", image: "images/denim_wine.jpg" },
                { name: "Blue", image: "images/denim_blue.jpg" }
            ],
            sizes: ["S", "M", "L", "XL"]
        },
        {
            id: 2,
            name: "Leather Watch",
            price: 450,
            image: "images/brown_watch.jpg",
            description: "Elegant minimalist analog watch",
            colors: [
                { name: "Brown", image: "images/brown_watch.jpg" },
                { name: "Navy", image: "images/neavy_blue_watch.png" },
                { name: "Green", image: "images/forest_green_watch.png" }
            ],
            sizes: ["One Size"]
        },
        {
            id: 3,
            name: "Printed Shirt",
            price: 400,
            image: "images/styalish.jpg",
            description: "Light weight printed short sleeve shirt",
            colors: [
                { name: "White", image: "images/styalish.jpg", color: "#FFFFFF" },
                { name: "Maroon", image: "images/maroon_shirt.png", color: "#800000" }
            ],
            sizes: ["S", "M", "L", "XL"]
        },
        {
            id: 4,
            name: "Streetwear Hoodie",
            price: 800,
            image: "images/comfort.jpg",
            description: "Comfort meets fashion hoodie set",
            colors: [
                { name: "White", image: "images/comfort.jpg", color: "#FFFFFF" },
                { name: "Brown", image: "images/brown_hoodie.png", color: "#8B4513" },
                { name: "Black", image: "images/black_hoodie.png", color: "#000000" }
            ],
            sizes: ["S", "M", "L", "XL", "XXL"]
        }
    ],
    occasion: [
        {
            id: 5,
            name: "Diwali Kurta Set",
            price: 1150,
            image: "images/kurta set.png",
            description: "Stylish embroidered kurta set perfect for festive occasions",
            colors: [
                { name: "Pink", image: "images/kurta set.png", color: "#FFC0CB" },
                { name: "Blue", image: "images/blue_kurta.png", color: "#4169E1" },
                { name: "Green", image: "images/green_kurta.png", color: "#228B22" }
            ],
            sizes: ["S", "M", "L", "XL"]
        },
        {
            id: 6,
            name: "Cocktail Party Saree",
            price: 2499,
            image: "images/sarii.jpg",
            description: "Designer saree perfect for cocktail parties",
            colors: [
                { name: "Red", image: "images/red.png", color: "#FF0000" },
                { name: "Black", image: "images/sarii.jpg", color: "#000000" }
            ],
            sizes: ["Free Size"]
        },
        {
            id: 7,
            name: "Wedding Outfit",
            price: 5000,
            image: "images/cocktail.png",
            description: "Elegant party outfit with modern festive style",
            colors: [
                { name: "Gold", image: "images/cocktail.png", color: "#FFD700" }
            ],
            sizes: ["S", "M", "L", "XL"]
        }
    ],
    bestsellers: [
        {
            id: 8,
            name: "Low-Top Sneakers",
            price: 2199,
            image: "images/sneakers.jpg",
            description: "Classic white & grey street sneakers",
            colors: [
                { name: "White", image: "images/sneakers.jpg", color: "#FFFFFF" }
            ],
            sizes: ["7", "8", "9", "10", "11"]
        },
        {
            id: 9,
            name: "Half-Zip Sweatshirt",
            price: 550,
            image: "images/sweatshirt.jpg",
            description: "Premium half-zip sweatshirt modern design",
            colors: [
                { name: "Green", image: "images/sweatshirt.jpg", color: "#228B22" },
                { name: "Maroon", image: "images/maroon_sweat.png", color: "#800000" },
                { name: "Brown", image: "images/brown_sweat.png", color: "#8B4513" }
            ],
            sizes: ["S", "M", "L", "XL", "XXL"]
        }
    ]
};

// Shopping cart
let cart = JSON.parse(localStorage.getItem('cart')) || [];

// DOM elements
const hamburger = document.getElementById('hamburger');
const navMenu = document.getElementById('nav-menu');
const cartSidebar = document.getElementById('cart-sidebar');
const cartOverlay = document.getElementById('cart-overlay');
const cartCount = document.getElementById('cart-count');
const cartItems = document.getElementById('cart-items');
const cartTotal = document.getElementById('cart-total');

// Initialize the website
document.addEventListener('DOMContentLoaded', function() {
    loadProducts();
    updateCartUI();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    // Mobile menu toggle
    hamburger.addEventListener('click', () => {
        hamburger.classList.toggle('active');
        navMenu.classList.toggle('active');
    });

    // Contact form
    document.getElementById('contact-form').addEventListener('submit', function(e) {
        e.preventDefault();
        alert('Thank you for your message! We will get back to you soon.');
        this.reset();
    });

    // Smooth scrolling for navigation links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            scrollToSection(targetId);
            
            // Close mobile menu
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
        });
    });
}