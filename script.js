/**
 * Interactive Script for Resume Website
 * Author: Akshay Shridhar
 */

document.addEventListener('DOMContentLoaded', () => {
  const navToggle = document.getElementById('nav-toggle');
  const navMenu = document.getElementById('nav-menu');
  const navLinks = document.querySelectorAll('.nav-link');

  // Mobile menu toggle
  if (navToggle && navMenu) {
    navToggle.addEventListener('click', () => {
      navMenu.classList.toggle('active');
    });

    // Close menu when clicking a link
    navLinks.forEach(link => {
      link.addEventListener('click', () => {
        navMenu.classList.remove('active');
      });
    });
  }

  // Active navigation link highlighting on scroll
  const sections = document.querySelectorAll('section[id]');

  function highlightNavOnScroll() {
    const scrollY = window.pageYOffset;

    sections.forEach(current => {
      const sectionHeight = current.offsetHeight;
      const sectionTop = current.offsetTop - 120;
      const sectionId = current.getAttribute('id');
      const targetNavLink = document.querySelector(`.nav-menu a[href*="${sectionId}"]`);

      if (targetNavLink) {
        if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
          targetNavLink.classList.add('active-nav');
        } else {
          targetNavLink.classList.remove('active-nav');
        }
      }
    });
  }

  window.addEventListener('scroll', highlightNavOnScroll);
});

