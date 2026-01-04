// Hero Section JavaScript with GSAP Animations

// Image array - Replace with your actual image paths
const heroImages = [
    "images/mainimage.jpg",
    "images/bgimg.jpg",
    "images/scroll2.jpg",
    "images/scroll3.jpg",
    "images/scroll4.jpg",
    "images/training.jpg",
    "images/Soundhealing.jpg",
    "images/therapy.jpg",
    "images/IMG-20251111-WA0011.jpg"
];

const mainBoxes = document.querySelector(".mainBoxes");
const mainClose = document.querySelector(".mainClose");
const lightbox = document.getElementById("lightbox");
const lightboxImg = document.getElementById("lightbox-img");
const lightboxClose = document.getElementById("lightbox-close");

let currentImg = null;
let currentImgProps = { x: 0, y: 0 };
let isZooming = false;
let column = -1;
let mouse = { x: 0, y: 0 };
let delayedPlay;

// Check if mobile
const isMobile = window.innerWidth <= 768;
const isSmallMobile = window.innerWidth <= 480;

// Build floating image boxes
heroImages.forEach((src, i) => {
    if (i % 3 === 0) column++;
    const b = document.createElement("div");
    mainBoxes.appendChild(b);
    
    // Responsive positioning and sizing
    let colX, startY, endY, duration, boxWidth, boxHeight, boxScale;
    
    if (isSmallMobile) {
        // Small mobile: single column, smaller boxes
        colX = 0;
        startY = -400;
        endY = 400;
        duration = 30;
        boxWidth = 240;
        boxHeight = 350;
        boxScale = 1;
    } else if (isMobile) {
        // Mobile: single column, medium boxes
        colX = 0;
        startY = -450;
        endY = 450;
        duration = 35;
        boxWidth = 280;
        boxHeight = 400;
        boxScale = 1;
    } else {
        // Desktop: multi-column layout
        colX = [60, 280, 500][column];
        startY = [-575, 800, 800][column];
        endY = [800, -575, -575][column];
        duration = [40, 35, 26][column];
        boxWidth = 400;
        boxHeight = 640;
        boxScale = 0.5;
    }

    gsap.set(b, {
        id: `b${i}`,
        className: `photoBox pb-col${column}`,
        backgroundImage: `url(${src})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
        overflow: "hidden",
        x: colX,
        width: boxWidth,
        height: boxHeight,
        borderRadius: isMobile ? 24 : 20,
        scale: boxScale,
        zIndex: isMobile ? (3 - (i % 3)) : 1,
        opacity: isMobile ? 0 : 1
    });

    // Only create floating animation for desktop
    if (!isMobile) {
        b.tl = gsap.timeline({ paused: true, repeat: -1 })
            .fromTo(b, { y: startY, rotation: -0.05 }, { duration, y: endY, rotation: 0.05, ease: "none" })
            .progress((i % 3) / 3);
    } else {
        // Mobile: static stack with entrance animation
        b.tl = null;
    }
});

function pauseBoxes(box) {
    if (window.innerWidth <= 768) return; // Skip on mobile
    const classStr = box.classList.contains("pb-col1") ? "pb-col1" : box.classList.contains("pb-col2") ? "pb-col2" : "pb-col0";
    Array.from(mainBoxes.children).forEach((child) => {
        if (child.classList.contains(classStr) && child.tl) gsap.to(child.tl, { timeScale: 0, ease: "sine" });
    });
}

function playBoxes() {
    if (window.innerWidth <= 768) return; // Skip on mobile
    Array.from(mainBoxes.children).forEach((child) => {
        if (child.tl) {
            const tl = child.tl;
            tl.play();
            gsap.to(tl, { duration: 0.4, timeScale: 1, ease: "sine.in", overwrite: true });
        }
    });
}

function lightboxOpen(src) {
    lightboxImg.src = src;
    lightbox.classList.add("show");
}

function lightboxCloseFn() {
    lightbox.classList.remove("show");
}

// Booking modal function (placeholder)
function openBookingModal() {
    alert("Booking modal would open here");
    // Replace with your actual booking modal code
}

window.onload = function () {
    const isMobile = window.innerWidth <= 768;
    const isTablet = window.innerWidth > 768 && window.innerWidth <= 1024;
    
    // Text entrance animations
    if (isMobile) {
        // Mobile: Staggered fade-in animations
        gsap.from(".hero-content h1", {
            y: 30,
            opacity: 0,
            duration: 0.8,
            delay: 0.1,
            ease: "power2.out"
        });
        gsap.from(".hero-content .lead", {
            y: 30,
            opacity: 0,
            duration: 0.8,
            delay: 0.4,
            ease: "power2.out"
        });
        gsap.from(".hero-content .book-btn", {
            y: 30,
            opacity: 0,
            duration: 0.8,
            delay: 0.6,
            ease: "power2.out"
        });
        
        // Mobile: Show all images in horizontal scrollable carousel
        const photoBoxes = document.querySelectorAll(".photoBox");
        photoBoxes.forEach((box, index) => {
            // Show all images on mobile in a scrollable carousel
            gsap.set(box, { 
                opacity: 1, 
                display: "block",
                x: 0,
                y: 0,
                scale: 1
            });
            
            // Animate entrance
            gsap.from(box, {
                opacity: 0,
                x: 50,
                duration: 0.6,
                delay: 0.8 + (index * 0.1),
                ease: "power2.out"
            });
        });
    } else {
        // Desktop: Original animations
        gsap.from(".hero-anim", { 
            y: 30, 
            opacity: 0, 
            duration: 0.6, 
            stagger: 0.12, 
            ease: "power2.out" 
        });
    }

    // Responsive sizing for mainBoxes
    let mainBoxesWidth = 1200;
    let mainBoxesLeft = "72%";
    let rotationX = 14;
    let rotationY = -15;
    let rotationZ = 10;
    
    if (isMobile) {
        mainBoxesWidth = Math.min(window.innerWidth - 40, 600);
        mainBoxesLeft = "50%";
        rotationX = 0;
        rotationY = 0;
        rotationZ = 0;
    } else if (isTablet) {
        mainBoxesWidth = 800;
        mainBoxesLeft = "60%";
        rotationX = 8;
        rotationY = -8;
        rotationZ = 5;
    }

    const _tl = gsap.timeline({ onStart: !isMobile ? playBoxes : null })
        .set(".main", { perspective: isMobile ? 0 : 800 })
        .set(".photoBox", { 
            opacity: isMobile ? 0 : 1, 
            cursor: "pointer" 
        })
        .set(".mainBoxes", { 
            left: mainBoxesLeft, 
            xPercent: -50, 
            width: mainBoxesWidth, 
            rotationX: rotationX, 
            rotationY: rotationY, 
            rotationZ: rotationZ 
        })
        .set(".mainClose", { 
            autoAlpha: 0, 
            width: 60, 
            height: 60, 
            left: -30, 
            top: -31, 
            pointerEvents: "none",
            display: isMobile ? "none" : "block"
        })
        .fromTo(".main", { autoAlpha: 0 }, { duration: 0.6, ease: "power2.inOut", autoAlpha: 1 }, 0.2);

    mainBoxes.addEventListener("mousemove", (e) => {
        mouse.x = e.x;
        mouse.y = e.layerY;
        if (currentImg) gsap.to(".mainClose", { duration: 0.1, x: mouse.x, y: mouse.y, overwrite: "auto" });
    });

    // Only add hover effects on desktop
    if (!isMobile) {
        mainBoxes.addEventListener("mouseenter", (e) => {
            const target = e.target.closest(".photoBox");
            if (!target || currentImg) return;
            if (delayedPlay) delayedPlay.kill();
            pauseBoxes(target);
            gsap.to(".photoBox", { duration: 0.2, overwrite: "auto", opacity: (i, t) => (t === target ? 1 : 0.33) });
            gsap.fromTo(target, { zIndex: 100 }, { duration: 0.2, scale: 0.62, overwrite: "auto", ease: "power3" });
        }, true);

        mainBoxes.addEventListener("mouseleave", (e) => {
            const target = e.target.closest(".photoBox");
            if (!target || currentImg) return;
            if (gsap.getProperty(target, "scale") > 0.62) delayedPlay = gsap.delayedCall(0.3, playBoxes);
            else playBoxes();
            gsap.timeline()
                .set(target, { zIndex: 1 })
                .to(target, { duration: 0.3, scale: 0.5, overwrite: "auto", ease: "expo" }, 0)
                .to(".photoBox", { duration: 0.5, opacity: 1, ease: "power2.inOut" }, 0);
        }, true);
    }

    // Handle both click and touch events for mobile
    const handleImageInteraction = (e) => {
        const target = e.target.closest(".photoBox");
        if (!target || isZooming) return;
        isZooming = true;
        gsap.delayedCall(0.8, () => { isZooming = false; });

        if (currentImg) {
            // Get responsive values
            const isMobile = window.innerWidth <= 768;
            const isTablet = window.innerWidth > 768 && window.innerWidth <= 1024;
            let resetWidth = 1200;
            let resetLeft = "72%";
            let resetRotationX = 14;
            let resetRotationY = -15;
            let resetRotationZ = 10;
            
            if (isMobile) {
                resetWidth = Math.min(window.innerWidth - 40, 600);
                resetLeft = "50%";
                resetRotationX = 0;
                resetRotationY = 0;
                resetRotationZ = 0;
            } else if (isTablet) {
                resetWidth = 800;
                resetLeft = "60%";
                resetRotationX = 8;
                resetRotationY = -8;
                resetRotationZ = 5;
            }
            
            gsap.timeline({ defaults: { ease: "expo.inOut" } })
                .to(".mainClose", { duration: 0.1, autoAlpha: 0, overwrite: true }, 0)
                .to(".mainBoxes", { duration: 0.5, scale: 1, left: resetLeft, width: resetWidth, rotationX: resetRotationX, rotationY: resetRotationY, rotationZ: resetRotationZ, overwrite: true }, 0)
                .to(".photoBox", { duration: 0.6, opacity: 1, ease: "power4.inOut" }, 0)
                .to(currentImg, { duration: 0.6, width: isMobile ? Math.min(window.innerWidth - 40, 280) : 400, height: isMobile ? 400 : 640, borderRadius: 20, x: currentImgProps.x, y: currentImgProps.y, scale: 0.5, rotation: 0, zIndex: 1 }, 0);
            currentImg = null;
        } else {
            pauseBoxes(target);
            currentImg = target;
            currentImgProps.x = gsap.getProperty(currentImg, "x");
            currentImgProps.y = gsap.getProperty(currentImg, "y");

            gsap.timeline({ defaults: { duration: 0.6, ease: "expo.inOut" } })
                .set(currentImg, { zIndex: 100 })
                .fromTo(".mainClose", { x: mouse.x, y: mouse.y, background: "rgba(0,0,0,0)" }, { autoAlpha: 1, duration: 0.3, ease: "power3.inOut" }, 0)
                .to(".photoBox", { opacity: 0 }, 0)
                .to(currentImg, { width: "100%", height: "100%", borderRadius: 0, x: 0, top: 0, y: 0, scale: 1, opacity: 1 }, 0)
                .to(".mainBoxes", { duration: 0.5, left: "50%", width: "100%", rotationX: 0, rotationY: 0, rotationZ: 0 }, 0.15)
                .to(".mainBoxes", { duration: 5, scale: 1.06, rotation: 0.05, ease: "none" }, 0.65);

            lightboxOpen(getComputedStyle(currentImg).backgroundImage.slice(5, -2));
        }
    };

    // Add event listeners for both click and touch
    mainBoxes.addEventListener("click", handleImageInteraction);
    if (isMobile) {
        mainBoxes.addEventListener("touchend", (e) => {
            e.preventDefault();
            handleImageInteraction(e);
        });
    }
};

// Lightbox event listeners
lightboxClose?.addEventListener("click", lightboxCloseFn);
lightbox?.addEventListener("click", (e) => {
    if (e.target.classList.contains("lightbox-backdrop")) lightboxCloseFn();
});



