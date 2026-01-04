// GSAP Animations for Smiles We Created Page

// Register ScrollTrigger plugin
gsap.registerPlugin(ScrollTrigger);

// Hero Section Animations - Simplified
function initHeroAnimations() {
  const heroText = document.querySelector('.hero-text');
  const heroTitle = document.querySelector('.hero-title');
  const heroSubtitle = document.querySelector('.hero-subtitle');
  const heroDescription = document.querySelector('.hero-description');

  // Simple fade-in animation for hero text
  if (heroText) {
    gsap.from(heroText.children, {
      duration: 1,
      y: 30,
      opacity: 0,
      stagger: 0.2,
      ease: "power3.out",
      delay: 0.3
    });
  }
}

// Mission Section Animations
function initMissionAnimations() {
  const missionText = document.querySelector('.mission-text');
  const missionImage = document.querySelector('.mission-image');
  const statItems = document.querySelectorAll('.stat-item');

  // Mission text scroll animation
  gsap.from(missionText, {
    scrollTrigger: {
      trigger: missionText,
      start: "top 80%",
      end: "top 50%",
      toggleActions: "play none none reverse"
    },
    duration: 1,
    x: -50,
    opacity: 0,
    ease: "power3.out"
  });

  // Mission image scroll animation
  if (missionImage) {
    // Set image visible immediately
    gsap.set(missionImage, { opacity: 1, visibility: 'visible' });
    
    gsap.fromTo(missionImage, 
      {
        x: 50,
        opacity: 1
      },
      {
        scrollTrigger: {
          trigger: missionImage,
          start: "top 80%",
          end: "top 50%",
          toggleActions: "play none none reverse"
        },
        duration: 1,
        x: 0,
        opacity: 1,
        ease: "power3.out"
      }
    );
  }

  // Stat items stagger animation
  gsap.from(statItems, {
    scrollTrigger: {
      trigger: '.mission-stats',
      start: "top 80%"
    },
    duration: 0.8,
    y: 30,
    opacity: 0,
    stagger: 0.2,
    ease: "power2.out"
  });
}

// Counter Animations
function initCounterAnimations() {
  const counters = document.querySelectorAll('.counter-number');
  
  counters.forEach(counter => {
    const target = parseInt(counter.getAttribute('data-target'));
    const duration = 2;
    const increment = target / (duration * 60); // 60 FPS
    
    const counterAnimation = gsap.to({ value: 0 }, {
      value: target,
      duration: duration,
      ease: "power2.out",
      scrollTrigger: {
        trigger: counter,
        start: "top 80%",
        once: true
      },
      onUpdate: function() {
        const currentValue = Math.ceil(this.targets()[0].value);
        counter.textContent = currentValue;
      }
    });
  });
}

// Features Section Animations
function initFeaturesAnimations() {
  const featureCards = document.querySelectorAll('.feature-card');
  
  // Set all feature cards and images visible immediately
  gsap.set(featureCards, { opacity: 1, visibility: 'visible' });
  gsap.set('.feature-image img', { opacity: 1, visibility: 'visible', display: 'block' });

  gsap.fromTo(featureCards,
    {
      y: 50,
      opacity: 1
    },
    {
      scrollTrigger: {
        trigger: '.features-grid',
        start: "top 80%"
      },
      duration: 0.8,
      y: 0,
      opacity: 1,
      stagger: 0.15,
      ease: "power3.out"
    }
  );

  // Hover animation enhancement
  featureCards.forEach(card => {
    card.addEventListener('mouseenter', function() {
      gsap.to(this, {
        scale: 1.05,
        duration: 0.3,
        ease: "power2.out"
      });
    });

    card.addEventListener('mouseleave', function() {
      gsap.to(this, {
        scale: 1,
        duration: 0.3,
        ease: "power2.out"
      });
    });
  });
}

// Moments of Joy Section Animations
function initMomentsOfJoyAnimations() {
  const momentsSection = document.querySelector('.moments-of-joy-section');
  const momentItems = document.querySelectorAll('.moment-item');
  
  if (!momentsSection || momentItems.length === 0) return;
  
  // Set all items visible immediately
  gsap.set(momentItems, { opacity: 1, visibility: 'visible' });
  gsap.set('.moment-image', { opacity: 1, visibility: 'visible', display: 'block' });
  
  // Create a master timeline for the section
  const masterTimeline = gsap.timeline({
    scrollTrigger: {
      trigger: momentsSection,
      start: "top 80%",
      toggleActions: "play none none reverse"
    }
  });
  
  // Animate each moment item with unique effects
  momentItems.forEach((item, index) => {
    const image = item.querySelector('.moment-image');
    const overlay = item.querySelector('.moment-overlay');
    const content = item.querySelector('.moment-content');
    const icon = item.querySelector('.moment-content i');
    
    // Set initial states
    const isEven = index % 2 === 0;
    const rotationY = isEven ? -25 : 25;
    const rotationX = isEven ? 10 : -10;
    
    gsap.set(item, {
      rotationY: rotationY,
      rotationX: rotationX,
      scale: 0.7,
      opacity: 1,
      z: -200,
      transformOrigin: "center center"
    });
    
    gsap.set(image, {
      scale: 1.3,
      rotation: isEven ? -5 : 5,
      opacity: 1
    });
    
    gsap.set(overlay, {
      opacity: 0
    });
    
    gsap.set(content, {
      y: 50,
      opacity: 0
    });
    
    gsap.set(icon, {
      scale: 0,
      rotation: -180
    });
    
    // Add to master timeline with stagger
    masterTimeline.to(item, {
      rotationY: 0,
      rotationX: 0,
      scale: 1,
      z: 0,
      opacity: 1,
      duration: 1,
      ease: "power3.out"
    }, index * 0.15)
    .to(image, {
      scale: 1,
      rotation: 0,
      opacity: 1,
      duration: 1.2,
      ease: "power2.out"
    }, index * 0.15 + 0.2)
    .to(content, {
      y: 0,
      opacity: 1,
      duration: 0.8,
      ease: "back.out(1.4)"
    }, index * 0.15 + 0.5);
  });
  
  // Continuous floating animation for all items
  momentItems.forEach((item, index) => {
    gsap.to(item, {
      y: -15,
      duration: 2 + (index % 3) * 0.5,
      repeat: -1,
      yoyo: true,
      ease: "sine.inOut",
      delay: index * 0.3
    });
  });
  
  // Enhanced hover effects
  momentItems.forEach(item => {
    const image = item.querySelector('.moment-image');
    const overlay = item.querySelector('.moment-overlay');
    const content = item.querySelector('.moment-content');
    const icon = item.querySelector('.moment-content i');
    const shine = item.querySelector('.moment-shine');
    
    item.addEventListener('mouseenter', function() {
      // Stop floating animation
      gsap.killTweensOf(this);
      
      // Animate item
      gsap.to(this, {
        scale: 1.08,
        rotationY: 0,
        rotationX: 0,
        z: 100,
        duration: 0.6,
        ease: "power3.out"
      });
      
      // Animate image
      if (image) {
        gsap.to(image, {
          scale: 1.2,
          rotation: 3,
          duration: 0.6,
          ease: "power2.out"
        });
      }
      
      // Animate overlay
      if (overlay) {
        gsap.to(overlay, {
          opacity: 1,
          duration: 0.5,
          ease: "power2.out"
        });
      }
      
      // Animate content
      if (content) {
        gsap.to(content, {
          y: 0,
          opacity: 1,
          duration: 0.5,
          ease: "back.out(1.4)"
        });
      }
      
      // Animate icon
      if (icon) {
        gsap.to(icon, {
          scale: 1.2,
          rotation: 360,
          duration: 0.6,
          ease: "back.out(1.7)"
        });
      }
      
      // Animate shine effect
      if (shine) {
        gsap.to(shine, {
          x: "200%",
          duration: 0.8,
          ease: "power2.inOut"
        });
      }
    });
    
    item.addEventListener('mouseleave', function() {
      // Resume floating animation
      const index = Array.from(momentItems).indexOf(this);
      gsap.to(this, {
        y: -15,
        duration: 2 + (index % 3) * 0.5,
        repeat: -1,
        yoyo: true,
        ease: "sine.inOut"
      });
      
      // Reset item
      gsap.to(this, {
        scale: 1,
        rotationY: 0,
        rotationX: 0,
        z: 0,
        duration: 0.5,
        ease: "power2.out"
      });
      
      // Reset image
      if (image) {
        gsap.to(image, {
          scale: 1,
          rotation: 0,
          duration: 0.5,
          ease: "power2.out"
        });
      }
      
      // Reset overlay
      if (overlay) {
        gsap.to(overlay, {
          opacity: 0,
          duration: 0.4,
          ease: "power2.out"
        });
      }
      
      // Reset content
      if (content) {
        gsap.to(content, {
          y: 30,
          opacity: 0,
          duration: 0.4,
          ease: "power2.out"
        });
      }
      
      // Reset icon
      if (icon) {
        gsap.to(icon, {
          scale: 0,
          rotation: -180,
          duration: 0.4,
          ease: "power2.out"
        });
      }
      
      // Reset shine
      if (shine) {
        gsap.set(shine, { x: "-100%" });
      }
    });
  });
  
  // Parallax effect on scroll
  momentItems.forEach((item, index) => {
    const image = item.querySelector('.moment-image');
    if (image) {
      gsap.to(image, {
        scrollTrigger: {
          trigger: item,
          start: "top bottom",
          end: "bottom top",
          scrub: 1
        },
        y: index % 2 === 0 ? -40 : 40,
        scale: 1.1,
        rotation: index % 2 === 0 ? -2 : 2,
        ease: "none"
      });
    }
  });
}

// New Impact Section Animations
function initImpactSectionAnimations() {
  const impactSection = document.querySelector('.impact-section-new');
  const impactCards = document.querySelectorAll('.impact-card-new');
  const impactCategories = document.querySelectorAll('.impact-category-new');
  
  if (!impactSection || impactCards.length === 0) return;
  
  // Set all cards visible immediately
  gsap.set(impactCards, { opacity: 1, visibility: 'visible' });
  gsap.set('.impact-image-new', { opacity: 1, visibility: 'visible', display: 'block' });
  
  // Animate category headers
  impactCategories.forEach((category, catIndex) => {
    const title = category.querySelector('.impact-category-title');
    if (title) {
      gsap.fromTo(title,
        {
          y: 30,
          opacity: 0
        },
        {
          scrollTrigger: {
            trigger: category,
            start: "top 85%",
            toggleActions: "play none none reverse"
          },
          y: 0,
          opacity: 1,
          duration: 0.8,
          delay: catIndex * 0.2,
          ease: "power3.out"
        }
      );
    }
    
    // Animate cards in each category
    const cards = category.querySelectorAll('.impact-card-new');
    cards.forEach((card, index) => {
      const image = card.querySelector('.impact-image-new');
      const overlay = card.querySelector('.impact-overlay-new');
      const content = card.querySelector('.impact-content-new');
      const icon = card.querySelector('.impact-content-new i');
      const badge = card.querySelector('.impact-badge-new');
      
      // Set initial states
      const isEven = index % 2 === 0;
      const rotationY = isEven ? -20 : 20;
      const rotationX = isEven ? 10 : -10;
      
      gsap.set(card, {
        rotationY: rotationY,
        rotationX: rotationX,
        scale: 0.8,
        opacity: 1,
        z: -150,
        transformOrigin: "center center"
      });
      
      gsap.set(image, {
        scale: 1.2,
        rotation: isEven ? -3 : 3,
        opacity: 1
      });
      
      gsap.set(overlay, {
        opacity: 0
      });
      
      gsap.set(content, {
        y: 40,
        opacity: 0
      });
      
      gsap.set(icon, {
        scale: 0,
        rotation: -180
      });
      
      gsap.set(badge, {
        scale: 0,
        rotation: -180
      });
      
      // Animate entrance
      gsap.to(card, {
        scrollTrigger: {
          trigger: card,
          start: "top 85%",
          toggleActions: "play none none reverse"
        },
        rotationY: 0,
        rotationX: 0,
        scale: 1,
        z: 0,
        opacity: 1,
        duration: 0.9,
        delay: (catIndex * 0.3) + (index * 0.15),
        ease: "power3.out"
      });
      
      gsap.to(image, {
        scrollTrigger: {
          trigger: card,
          start: "top 85%",
          toggleActions: "play none none reverse"
        },
        scale: 1,
        rotation: 0,
        opacity: 1,
        duration: 1.1,
        delay: (catIndex * 0.3) + (index * 0.15) + 0.2,
        ease: "power2.out"
      });
      
      gsap.to(content, {
        scrollTrigger: {
          trigger: card,
          start: "top 85%",
          toggleActions: "play none none reverse"
        },
        y: 0,
        opacity: 1,
        duration: 0.8,
        delay: (catIndex * 0.3) + (index * 0.15) + 0.5,
        ease: "back.out(1.4)"
      });
      
      gsap.to(icon, {
        scrollTrigger: {
          trigger: card,
          start: "top 85%",
          toggleActions: "play none none reverse"
        },
        scale: 1,
        rotation: 0,
        duration: 0.8,
        delay: (catIndex * 0.3) + (index * 0.15) + 0.6,
        ease: "back.out(1.7)"
      });
      
      gsap.to(badge, {
        scrollTrigger: {
          trigger: card,
          start: "top 85%",
          toggleActions: "play none none reverse"
        },
        scale: 1,
        rotation: 360,
        duration: 0.8,
        delay: (catIndex * 0.3) + (index * 0.15) + 0.7,
        ease: "back.out(1.7)"
      });
    });
  });
  
  // Enhanced hover effects
  impactCards.forEach(card => {
    const image = card.querySelector('.impact-image-new');
    const overlay = card.querySelector('.impact-overlay-new');
    const content = card.querySelector('.impact-content-new');
    const icon = card.querySelector('.impact-content-new i');
    const badge = card.querySelector('.impact-badge-new');
    
    card.addEventListener('mouseenter', function() {
      // Animate card
      gsap.to(this, {
        scale: 1.05,
        rotationY: 0,
        rotationX: 0,
        z: 80,
        duration: 0.5,
        ease: "power3.out"
      });
      
      // Animate image
      if (image) {
        gsap.to(image, {
          scale: 1.2,
          rotation: 2,
          duration: 0.5,
          ease: "power2.out"
        });
      }
      
      // Animate overlay
      if (overlay) {
        gsap.to(overlay, {
          opacity: 1,
          duration: 0.4,
          ease: "power2.out"
        });
      }
      
      // Animate content
      if (content) {
        gsap.to(content, {
          y: 0,
          opacity: 1,
          duration: 0.4,
          ease: "back.out(1.4)"
        });
      }
      
      // Animate icon
      if (icon) {
        gsap.to(icon, {
          scale: 1.3,
          rotation: 360,
          duration: 0.5,
          ease: "back.out(1.7)"
        });
      }
      
      // Animate badge
      if (badge) {
        gsap.to(badge, {
          scale: 1.1,
          rotation: 360,
          duration: 0.5,
          ease: "back.out(1.7)"
        });
      }
    });
    
    card.addEventListener('mouseleave', function() {
      // Reset card
      gsap.to(this, {
        scale: 1,
        rotationY: 0,
        rotationX: 0,
        z: 0,
        duration: 0.4,
        ease: "power2.out"
      });
      
      // Reset image
      if (image) {
        gsap.to(image, {
          scale: 1,
          rotation: 0,
          duration: 0.4,
          ease: "power2.out"
        });
      }
      
      // Reset overlay
      if (overlay) {
        gsap.to(overlay, {
          opacity: 0,
          duration: 0.3,
          ease: "power2.out"
        });
      }
      
      // Reset content
      if (content) {
        gsap.to(content, {
          y: 30,
          opacity: 0,
          duration: 0.3,
          ease: "power2.out"
        });
      }
      
      // Reset icon
      if (icon) {
        gsap.to(icon, {
          scale: 0,
          rotation: -180,
          duration: 0.3,
          ease: "power2.out"
        });
      }
      
      // Reset badge
      if (badge) {
        gsap.to(badge, {
          scale: 1,
          rotation: 0,
          duration: 0.3,
          ease: "power2.out"
        });
      }
    });
  });
  
  // Parallax effect on scroll
  impactCards.forEach((card, index) => {
    const image = card.querySelector('.impact-image-new');
    if (image) {
      gsap.to(image, {
        scrollTrigger: {
          trigger: card,
          start: "top bottom",
          end: "bottom top",
          scrub: 1
        },
        y: index % 2 === 0 ? -30 : 30,
        scale: 1.05,
        rotation: index % 2 === 0 ? -1 : 1,
        ease: "none"
      });
    }
  });
}

// Gallery Section Animations
function initGalleryAnimations() {
  const galleryItems = document.querySelectorAll('.gallery-item');
  const galleryImages = document.querySelectorAll('.gallery-image img');
  
  // Set all gallery images visible immediately
  gsap.set(galleryItems, { opacity: 1, visibility: 'visible' });
  gsap.set(galleryImages, { opacity: 1, visibility: 'visible', display: 'block' });

  // Enhanced entrance animation with rotation and scale
  galleryItems.forEach((item, index) => {
    const image = item.querySelector('.gallery-image img');
    const overlay = item.querySelector('.gallery-overlay');
    
    // Set initial states
    gsap.set(item, {
      rotationY: index % 2 === 0 ? -15 : 15,
      scale: 0.8,
      opacity: 1,
      transformOrigin: "center center"
    });
    
    gsap.set(image, {
      scale: 1.2,
      opacity: 1
    });
    
    if (overlay) {
      gsap.set(overlay, {
        opacity: 0
      });
    }
    
    // Create scroll-triggered animation
    gsap.to(item, {
      scrollTrigger: {
        trigger: item,
        start: "top 85%",
        toggleActions: "play none none reverse"
      },
      rotationY: 0,
      scale: 1,
      opacity: 1,
      duration: 0.8,
      delay: index * 0.1,
      ease: "power3.out"
    });
    
    // Animate image zoom effect
    gsap.to(image, {
      scrollTrigger: {
        trigger: item,
        start: "top 85%",
        toggleActions: "play none none reverse"
      },
      scale: 1,
      opacity: 1,
      duration: 1,
      delay: index * 0.1 + 0.2,
      ease: "power2.out"
    });
    
    // Animate overlay content
    if (overlay) {
      const content = overlay.querySelector('.gallery-content');
      if (content) {
        gsap.set(content.children, {
          y: 20,
          opacity: 0
        });
      }
    }
  });

  // Enhanced hover effects with 3D transforms
  galleryItems.forEach(item => {
    const image = item.querySelector('.gallery-image img');
    const overlay = item.querySelector('.gallery-overlay');
    const content = overlay ? overlay.querySelector('.gallery-content') : null;
    
    item.addEventListener('mouseenter', function() {
      // Animate item
      gsap.to(this, {
        scale: 1.08,
        rotationY: 0,
        z: 50,
        duration: 0.5,
        ease: "power2.out"
      });
      
      // Animate image zoom
      if (image) {
        gsap.to(image, {
          scale: 1.15,
          duration: 0.5,
          ease: "power2.out"
        });
      }
      
      // Animate overlay
      if (overlay) {
        gsap.to(overlay, {
          opacity: 1,
          duration: 0.4,
          ease: "power2.out"
        });
      }
      
      // Animate content
      if (content) {
        gsap.to(content.children, {
          y: 0,
          opacity: 1,
          duration: 0.4,
          stagger: 0.1,
          ease: "power2.out"
        });
      }
    });

    item.addEventListener('mouseleave', function() {
      // Reset item
      gsap.to(this, {
        scale: 1,
        rotationY: 0,
        z: 0,
        duration: 0.4,
        ease: "power2.out"
      });
      
      // Reset image
      if (image) {
        gsap.to(image, {
          scale: 1,
          duration: 0.4,
          ease: "power2.out"
        });
      }
      
      // Reset overlay
      if (overlay) {
        gsap.to(overlay, {
          opacity: 0,
          duration: 0.3,
          ease: "power2.out"
        });
      }
      
      // Reset content
      if (content) {
        gsap.to(content.children, {
          y: 20,
          opacity: 0,
          duration: 0.3,
          ease: "power2.out"
        });
      }
    });
  });
  
  // Add parallax effect to gallery images on scroll
  galleryItems.forEach((item, index) => {
    const image = item.querySelector('.gallery-image img');
    if (image) {
      gsap.to(image, {
        scrollTrigger: {
          trigger: item,
          start: "top bottom",
          end: "bottom top",
          scrub: 1
        },
        y: index % 2 === 0 ? -30 : 30,
        scale: 1.05,
        ease: "none"
      });
    }
  });
}

// CTA Section Animations
function initCTAAnimations() {
  const ctaContent = document.querySelector('.cta-content');
  const ctaButtons = document.querySelectorAll('.cta-button');

  gsap.from(ctaContent, {
    scrollTrigger: {
      trigger: ctaContent,
      start: "top 80%"
    },
    duration: 1,
    y: 50,
    opacity: 0,
    ease: "power3.out"
  });

  gsap.from(ctaButtons, {
    scrollTrigger: {
      trigger: '.cta-buttons',
      start: "top 80%"
    },
    duration: 0.8,
    y: 30,
    opacity: 0,
    stagger: 0.2,
    ease: "power2.out"
  });
}

// Section Header Animations
function initSectionHeaderAnimations() {
  const sectionHeaders = document.querySelectorAll('.section-header');

  sectionHeaders.forEach(header => {
    // Animate each child element separately for better effect
    const children = Array.from(header.children);
    children.forEach((child, index) => {
      gsap.fromTo(child,
        {
          y: 40,
          opacity: 0,
          scale: 0.95
        },
        {
          scrollTrigger: {
            trigger: header,
            start: "top 85%",
            toggleActions: "play none none reverse"
          },
          duration: 0.8,
          y: 0,
          opacity: 1,
          scale: 1,
          delay: index * 0.1,
          ease: "power3.out"
        }
      );
    });
  });
}

// Image Loading Animation
function initImageLoadingAnimations() {
  const allImages = document.querySelectorAll('.gallery-image img, .feature-image img, .mission-image img');
  
  allImages.forEach((img, index) => {
    // Set image visible immediately
    img.style.opacity = '1';
    img.style.visibility = 'visible';
    img.style.display = 'block';
    
    // Add loading animation
    if (img.complete) {
      // Image already loaded
      gsap.set(img, { opacity: 1, scale: 1 });
    } else {
      // Image still loading
      gsap.set(img, { opacity: 0.3, scale: 1.1 });
      
      img.addEventListener('load', function() {
        gsap.to(img, {
          opacity: 1,
          scale: 1,
          duration: 0.6,
          delay: index * 0.05,
          ease: "power2.out"
        });
      });
      
      // Fallback: if image doesn't load, still show it
      setTimeout(() => {
        gsap.to(img, {
          opacity: 1,
          scale: 1,
          duration: 0.6,
          ease: "power2.out"
        });
      }, 2000);
    }
  });
}

// Smooth Scroll for Anchor Links
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      
      if (target) {
        // Use native smooth scroll if ScrollToPlugin is not available
        if (typeof ScrollToPlugin !== 'undefined') {
          gsap.to(window, {
            duration: 1,
            scrollTo: {
              y: target,
              offsetY: 100
            },
            ease: "power2.inOut"
          });
        } else {
          // Fallback to native smooth scroll
          target.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          });
        }
      }
    });
  });
}

// Parallax Effect for Hero Background
function initParallaxEffect() {
  const heroSection = document.querySelector('.hero-section');
  
  if (heroSection) {
    gsap.to(heroSection, {
      scrollTrigger: {
        trigger: heroSection,
        start: "top top",
        end: "bottom top",
        scrub: 1
      },
      y: 100,
      ease: "none"
    });
  }
}

// Initialize all animations when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
  // First, ensure all images are visible immediately before any animations
  const allImages = document.querySelectorAll('img');
  allImages.forEach(img => {
    img.style.opacity = '1';
    img.style.visibility = 'visible';
    img.style.display = 'block';
  });
  
  // Ensure mission image is visible
  const missionImage = document.querySelector('.mission-image');
  if (missionImage) {
    missionImage.style.opacity = '1';
    missionImage.style.visibility = 'visible';
    const missionImg = missionImage.querySelector('img');
    if (missionImg) {
      missionImg.style.opacity = '1';
      missionImg.style.visibility = 'visible';
      missionImg.style.display = 'block';
    }
  }
  
  // Ensure feature cards are visible
  const featureCards = document.querySelectorAll('.feature-card');
  featureCards.forEach(card => {
    card.style.opacity = '1';
    card.style.visibility = 'visible';
    const cardImages = card.querySelectorAll('img');
    cardImages.forEach(img => {
      img.style.opacity = '1';
      img.style.visibility = 'visible';
      img.style.display = 'block';
    });
  });
  
  // Ensure gallery items are visible
  const galleryItems = document.querySelectorAll('.gallery-item');
  galleryItems.forEach(item => {
    item.style.opacity = '1';
    item.style.visibility = 'visible';
    const galleryImages = item.querySelectorAll('img');
    galleryImages.forEach(img => {
      img.style.opacity = '1';
      img.style.visibility = 'visible';
      img.style.display = 'block';
    });
  });
  
  // Check if GSAP ScrollToPlugin is available
  if (typeof gsap.registerPlugin !== 'undefined') {
    // Try to load ScrollToPlugin if available
    if (typeof ScrollToPlugin !== 'undefined') {
      gsap.registerPlugin(ScrollToPlugin);
    }
  }

  // Initialize all animation functions
  initHeroAnimations();
  initMissionAnimations();
  initCounterAnimations();
  initFeaturesAnimations();
  initImageLoadingAnimations();
  initMomentsOfJoyAnimations();
  initImpactSectionAnimations();
  initGalleryAnimations();
  initCTAAnimations();
  initSectionHeaderAnimations();
  initSmoothScroll();
  initParallaxEffect();

  // Add scroll-triggered header effect
  const header = document.querySelector('.header');
  if (header) {
    window.addEventListener('scroll', function() {
      if (window.scrollY > 50) {
        header.style.boxShadow = '0 4px 30px rgba(0, 0, 0, 0.1)';
      } else {
        header.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.05)';
      }
    });
  }
});

// Handle window resize
let resizeTimer;
window.addEventListener('resize', function() {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(function() {
    ScrollTrigger.refresh();
  }, 250);
});

